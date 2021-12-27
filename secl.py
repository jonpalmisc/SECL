import sublime
import sublime_plugin


class SeclMoveToExtremeCommand(sublime_plugin.TextCommand):
    def run(self, edit: sublime.Edit, location: str):
        self.view.sel().clear()

        destination = 0 if location == "start" else self.view.size()

        # Move the cursor to the destination, then ensure the cursor is visible
        # after moving.
        self.view.sel().add(sublime.Region(destination))
        self.view.show_at_center(self.view.sel()[0])


class SeclMoveRepeatCommand(sublime_plugin.TextCommand):
    def run(self, edit: sublime.Edit, count: int, by: str, forward: bool, extend: bool):
        args = {"by": by, "forward": forward, "extend": extend}

        for i in range(count):
            self.view.run_command("move", args)
