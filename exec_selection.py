import sublime
import sublime_plugin

from Default.exec import ExecCommand


class ExecSelectionCommand(ExecCommand):
    def run(self, **kwargs):
        # Extract from our arguments the potential replacement build options
        # that can contain the new $SELECTION variable.
        cmd_sel = kwargs.pop("cmd_sel", None)
        shell_cmd_sel = kwargs.pop("shell_cmd_sel", None)

        # Obtain the selection from the currently active view, which may be an
        # empty string.
        v = self.window.active_view()
        selection = "" if v is None else "\n".join([v.substr(s) for s in v.sel()])

        # Obtain the standard variables, then add in the selection if we found
        # one. If the selection is empty, it's not added to the list of
        # variables so that a default can be used.
        cVars = self.window.extract_variables()
        if selection:
            cVars["SELECTION"] = selection

        # If the build has an alternate "cmd" argument, expand it.
        if cmd_sel is not None:
            kwargs["cmd"] = sublime.expand_variables(cmd_sel, cVars)

        # If the build has an alternate "shell_cmd" argument, expand it.
        if shell_cmd_sel is not None:
            kwargs["shell_cmd"] = sublime.expand_variables(shell_cmd_sel, cVars)

        # Let our parent class (the standard exec command) perform the build
        # now.
        super().run(**kwargs)
