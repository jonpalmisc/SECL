import sublime
import sublime_plugin


class SicilyMoveToExtremeCommand(sublime_plugin.TextCommand):
    def run(self, edit: sublime.Edit, location: str):
        self.view.sel().clear()

        destination = 0 if location == "start" else self.view.size()

        # Move the cursor to the destination, then ensure the cursor is visible
        # after moving.
        self.view.sel().add(sublime.Region(destination))
        self.view.show_at_center(self.view.sel()[0])
