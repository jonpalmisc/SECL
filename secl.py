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


class SeclMoveByParagraphCommand(sublime_plugin.TextCommand):
    def prev_par_from(self, start: int) -> int:
        """Get the previous paragraph from the given start point."""

        pars = [p for p in self.view.find_all("\n\n", 0) if p.end() < start]
        return 0 if len(pars) == 0 else pars[-1].end()

    def next_par_from(self, start: int) -> int:
        """Get the next paragraph from the given start point."""

        next_par = self.view.find("\n\n", start).end()
        return next_par if next_par != -1 else self.view.size()

    def run(self, edit: sublime.Edit, forward: bool):
        pos = self.view.sel()[0].begin()
        dest = self.next_par_from(pos) if forward else self.prev_par_from(pos)

        self.view.sel().clear()
        self.view.sel().add(sublime.Region(dest))
