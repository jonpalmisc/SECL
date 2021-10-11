import sublime
import sublime_plugin


class SicilyMoveToExtremeCommand(sublime_plugin.TextCommand):
    def run(self, edit: sublime.Edit, location: str):
        self.view.sel().clear()

        destination = 0 if location == "start" else self.view.size()
        self.view.sel().add(sublime.Region(destination))
