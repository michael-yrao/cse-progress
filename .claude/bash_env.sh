# Sourced by every non-interactive `bash -c` the Claude Code / VS Code Bash tool
# runs, via BASH_ENV=".claude/bash_env.sh" in .claude/settings.json (CWD = repo root).
#
# Why this exists: on Windows the Bash tool starts bash NON-interactive, NON-login,
# with the *Windows* PATH (';'-separated, 'C:\' drive letters). bash splits PATH on
# ':', so every drive-letter colon shreds the list and NOTHING resolves -- not even
# ls / head / git / python. If PATH still contains a ';', it is a raw Windows list;
# convert it to a POSIX list with cygpath. No-op when PATH is already POSIX.
case "$PATH" in
  *\;*)
    export PATH="/usr/bin:/mingw64/bin:$(/usr/bin/cygpath -p "$PATH")"
    ;;
esac
