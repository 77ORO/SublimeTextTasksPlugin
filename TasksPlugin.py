import sublime
import sublime_plugin

# Global Variables
# -------------------
# Modify them according to your environment

TASKSFolder="~/Documents/tasks/"
TASKSFilenames=("low.tasks","mid.tasks","high.tasks","crit.tasks")

# -------------------

def getTextOfCurrentLine(self):
	textonline = None

	self.view.window().active_view().run_command("expand_selection", {"to": "line"})

	for region in self.view.window().active_view().sel():
		if not region.empty():
			textonline = self.view.window().active_view().substr(region)
	return textonline


def insertTextAtEndOfFile(self, content):
	# Select end of file
	self.view.window().active_view().selection.clear()
	self.view.window().active_view().selection.add(1)
	self.view.window().active_view().run_command("move_to", {"to": "eof"})

	# Ensure that we are on a blank line. Otherwise add a new line at the end
	contentCurrentLine = getTextOfCurrentLine(self)
	if contentCurrentLine != None:
		self.view.window().active_view().run_command("move_to", {"to": "eof"})
		self.view.window().active_view().run_command("insert", {"characters": "\n"})
		self.view.window().active_view().run_command("move_to", {"to": "eof"})

	# Insert Data
	self.view.window().active_view().run_command("insert", {"characters": content})


def getNextSplitWindow(self):
	currentSplitWindow = selectedSplitWindow = self.view.window().active_sheet_in_group(self.view.window().active_group())
	nextSplitWindow = 0

	avaiablesplitwindows = self.view.window().sheets_in_group(self.view.window().active_group())
	isNext = False
	for splitwindow in avaiablesplitwindows:
		if isNext:
			nextSplitWindow = splitwindow
			break
		if splitwindow == currentSplitWindow:
			isNext = True

	return nextSplitWindow


def getPreviousSplitWindow(self):
	currentSplitWindow = selectedSplitWindow = self.view.window().active_sheet_in_group(self.view.window().active_group())
	previousSplitWindow = 0

	avaiablesplitwindows = self.view.window().sheets_in_group(self.view.window().active_group())
	isNext = False
	for splitwindow in avaiablesplitwindows:
		if splitwindow == currentSplitWindow:
			break
		previousSplitWindow = splitwindow

	return previousSplitWindow


class MoveToHigherPrioCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		textonline = getTextOfCurrentLine(self)

		# Change to next split window
		nextSplitWindow = getNextSplitWindow(self)
		if nextSplitWindow != 0:

			# remove old text
			self.view.run_command("left_delete")
			
			self.view.window().focus_sheet(nextSplitWindow)

			insertTextAtEndOfFile(self, textonline)


class MoveToLowerPrioCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		textonline = getTextOfCurrentLine(self)

		# Change to next split window
		previousSplitWindow = getPreviousSplitWindow(self)
		if previousSplitWindow != 0:

			# remove old text
			self.view.run_command("left_delete")

			self.view.window().focus_sheet(previousSplitWindow)

			insertTextAtEndOfFile(self, textonline)


class SelectHigherPrioSheetCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		nextSplitWindow = getNextSplitWindow(self)
		if nextSplitWindow != 0:
			self.view.window().focus_sheet(nextSplitWindow)


class SelectLowerPrioSheetCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		previousSplitWindow = getPreviousSplitWindow(self)
		if previousSplitWindow != 0:
			self.view.window().focus_sheet(previousSplitWindow)


class TaskpluginOpenSplitviewCommand(sublime_plugin.WindowCommand):
	def run(self):
		global TASKSFolder
		global TASKSFilenames

		sublime.run_command("new_window")
		newWindow = sublime.active_window()

		createdSheets = list()

		for filename in TASKSFilenames:
			newWindow.open_file(TASKSFolder + filename)
			createdSheets.append(newWindow.active_sheet())
			newWindow.active_view().run_command("toggle_setting", {"setting": "word_wrap"})
			newWindow.active_view().run_command("set_setting", {"setting": "scroll_past_end", "value": False})

		newWindow.select_sheets(createdSheets)

		# Change settings for newly created window
		newWindow.set_sidebar_visible(False)
		newWindow.set_minimap_visible(False)
		newWindow.set_tabs_visible(False)
		newWindow.set_status_bar_visible(False)

