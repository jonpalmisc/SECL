import sublime
import sublime_plugin


class SeclComment(sublime_plugin.TextCommand):
    def comment_start(self) -> str:
        for v in self.view.meta_info("shellVariables", 0):
            if v["name"] == "TM_COMMENT_START":
                return v["value"]

        return "// "

    def start_comment_eol(self, edit: sublime.Edit, reg: sublime.Region) -> int:
        """Insert a comment at the line's end, return the new point position."""

        current_line = self.view.lines(reg)[0]
        self.view.insert(edit, current_line.end(), " " + self.comment_start())

        return current_line.end() + len(self.comment_start()) + 1

    def run(self, edit: sublime.Edit):
        # TODO: Support multiple regions.
        sel = self.view.sel()
        if len(sel) == 0:
            return
        reg = sel[0]

        # TOOD: Jump to comment if it already exists.
        if reg.begin() == reg.end():
            new_point = self.start_comment_eol(edit, reg)
            self.view.sel().clear()
            self.view.sel().add(new_point)
        else:
            self.view.run_command("toggle_comment", {})


class SeclMoveToExtremeCommand(sublime_plugin.TextCommand):
    def run(self, edit: sublime.Edit, forward: bool):
        self.view.sel().clear()
        dest = self.view.size() if forward else 0
        reg = sublime.Region(dest)

        self.view.sel().add(reg)
        self.view.show(reg)


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
        reg = sublime.Region(dest)

        self.view.sel().clear()
        self.view.sel().add(reg)
        self.view.show(reg, False)
