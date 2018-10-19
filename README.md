# [Terrafmt](//packagecontrol.io/packages/Terrafmt)

This plugin will automatically run `terraform fmt` on any [Terraform](https://www.terraform.io/) file before saving.

There's also a command palette entry called `Terrafmt: Format this file` to manually format.

## Options

Users can override the options in `Packages/User/Terrafmt.sublime-settings`.

This file can be opened either through the menus (_Preferences_ > _Package Settings_ > _Terrafmt_ > _Settings_) or through the command palette (<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>) and enter `Preferences: Terrafmt settings`.

## Installation

##### Using the package manager

1. Install the [Sublime Text Package Control](//packagecontrol.io/installation) plugin if you haven't already.
    - _Preferences_ > _Package Control_
2. Open up the command palette (<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>) and enter `Package Control: Install Package`
3. Search for `Terrafmt` and hit <kbd>Enter</kbd> to install.

##### Manual installation with Git

1. Click the `Preferences > Browse Packages` menu.
2. Open up a terminal and execute the following:
    - `git clone https://github.com/p3lim/sublime-terrafmt Terrafmt`
3. Restart Sublime Text.
