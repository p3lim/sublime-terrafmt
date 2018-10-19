import re
import subprocess

import sublime
import sublime_plugin

ANSI_ESCAPE = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

settings = None

def plugin_loaded():
	global settings
	settings = sublime.load_settings('Terrafmt.sublime-settings')

class Formatter(object):
	def __init__(self, view):
		self.view = view
		self.window = view.window()
		self.encoding = view.encoding()

		if self.encoding == 'Undefined':
			self.encoding = 'utf-8'

		self.cmd = settings.get('cmd', ['terraform', 'fmt', '-'])

	def format(self, region):
		# get the region contents
		contents = self.view.substr(region)

		# prepare the formatting tool process
		proc = subprocess.Popen(
			self.cmd,
			stdin=subprocess.PIPE,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE
		)

		# invoke the process with the contents as stdin, capturing stdout and stderr
		stdout, stderr = proc.communicate(contents.encode())
		if stderr or proc.returncode != 0:
			# there was an error, display it
			self._show_errors(stderr.decode('utf-8'))

			# return the original content
			return contents

		# hide any existing errors
		self._hide_errors()

		# return the formatted output
		return stdout.decode(self.encoding)

	def _show_errors(self, errors):
		'''
		Show the stderr of a failed process in an output panel.

		:param str stderr: Stderr output of a process.
		'''
		panel = self.window.create_output_panel('terrafmt')
		panel.set_scratch(True)
		panel.run_command('select_all')
		panel.run_command('right_delete')
		panel.run_command('insert', {'characters': ANSI_ESCAPE.sub('', errors)})
		self.window.run_command('show_panel', {'panel': 'output.terrafmt'})

	def _hide_errors(self):
		'''
		Hide any previously displayed error panel.
		'''
		self.window.run_command('hide_panel', {'panel': 'output.terrafmt'})

class TerrafmtCommand(sublime_plugin.TextCommand):
	def is_enabled(self):
		# checks if the file matches the terraform file types
		return self.view.score_selector(0, 'source.terraform') != 0

	def run(self, edit):
		formatter = Formatter(self.view)

		# get the entire view region
		region = sublime.Region(0, self.view.size())

		# run the formatter with the given region
		replacement = formatter.format(region)

		# replace the region if the content has changes
		if self.view.substr(region) != replacement:
			self.view.replace(edit, region, replacement)

class TerrafmtListener(sublime_plugin.EventListener):
	def on_pre_save(self, view):
		if settings.get('format_on_save', True):
			view.run_command('terrafmt')
