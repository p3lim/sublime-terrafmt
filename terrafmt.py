import re
import subprocess

import sublime
import sublime_plugin

ANSI_ESCAPE = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

settings = None

def plugin_loaded():
	'''
	Called when the plugin is loaded, used to load the settings for the package.
	'''
	global settings
	settings = sublime.load_settings('Terrafmt.sublime-settings')

class Formatter(object):
	'''
	Wrapper for the process used to format the Terraform file.

	:param sublime.View view: The view of the file to be formatted.
	'''
	def __init__(self, view):
		self.view = view
		self.window = view.window()
		self.encoding = view.encoding()

		if self.encoding == 'Undefined':
			self.encoding = 'utf-8'

		self.cmd = settings.get('cmd', ['terraform', 'fmt', '-'])

	def format(self, region):
		'''
		Attempts to format the code, raising any errors in an output panel if they arise.

		:param sublime.Region region: The region for the file to format
		:returns: str. Returns the formatted content if no errors arose, else the original content.
		'''
		contents = self.view.substr(region)

		# run the formatting tool
		output, error = self._exec(contents)
		if error:
			# there was an error, display it
			self._show_errors(error)

			# return the original content
			return contents

		# hide any existing errors
		self._hide_errors()

		# return the formatted output
		return output

	def _exec(self, stdin):
		'''
		Execute the formatting tool.

		:param str stdin: Stdin for the process, the file content to format
		:returns: stdout, stderr: Returns the stdout if successful, an empty stdout and error if
		    unsuccessful.
		'''
		proc = subprocess.Popen(
			self.cmd,
			stdin=subprocess.PIPE,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE
		)

		stdout, stderr = proc.communicate(stdin.encode())
		if stderr or proc.returncode != 0:
			return "", stderr.decode('utf-8')
		else:
			return stdout.decode(self.encoding), None

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
	'''
	The `terrafmt` command, invoked by the command palette or before a file save.
	'''
	def is_enabled(self):
		'''
		Checks if the current file viewed is a Terraform file (.tf, .tfvars) or not.

		:returns: bool
		'''
		return self.view.score_selector(0, 'source.terraform') != 0

	def run(self, edit):
		'''
		Formats the current file viewed, replacing its contents.
		'''
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
		'''
		Called before a dirty view is stored to disk, running the `terrafmt` command.
		'''
		if settings.get('format_on_save', True):
			view.run_command('terrafmt')
