# [Terrafmt](//packagecontrol.io/packages/Terrafmt)

This plugin will automatically run `terraform fmt` on any [Terraform](https://www.terraform.io/) file before saving.

There's also a command palette entry called `Terrafmt: Format this file` to manually format.

## Options

Options are stores in `Packages/User/Terrafmt.sublime-settings`, you can also find it through the menu.

```json
{
	// the command and arguments to run, the file contents are sent as stdin
	"cmd": ["terraform", "fmt", "-"],
	// enable the package to run on file saves
	"format_on_save": true
}
```

## Installation

##### Using the package manager

1. Install the [Sublime Text Package Control](//packagecontrol.io/installation) plugin if you haven't already.
    - Menu entry _Preferences_ > _Package Control_
2. Open up the command palette (<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>) and enter `Package Control: Install Package`
3. Search for `Terrafmt` and hit <kbd>Enter</kbd> to install.
4. Follow the instructions that appears on the screen.

##### Manual installation with Git

1. Click the `Preferences > Browse Packages` menu.
2. Open up a terminal and execute the following:
    - `git clone https://github.com/p3lim/sublime-terrafmt Terrafmt`
3. Restart Sublime Text.
