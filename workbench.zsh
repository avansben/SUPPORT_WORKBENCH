# Support Workbench helpers for zsh.
#   source ~/docs/SUPPORT_WORKBENCH/workbench.zsh
# Add that line to ~/.zshrc to have it in every terminal.
#
#   wb               cd to the workbench root
#   wb-new <slug>    scaffold a case and make it the current one
#   wb-use [case]    switch the current case (default: most recently modified); tab-completes
#   wb-cases         list cases, marking the current one
#   ev <command…>    run a command and log it as evidence for the current case
#   evp '<a | b>'    same, for a pipeline (quote the whole pipeline)
#
# Sets $WB (workbench root), $C (current case) and $P (practice scenario 01) as
# absolute paths, so the helpers work from any directory.

# Let pasted commands carry "# comments", as the README's code blocks do.
setopt interactivecomments

WB="${${(%):-%x}:A:h}"
P="$WB/practice/01-webhook-signatures"

wb() { cd "$WB" }

wb-new() {
  if (( $# != 1 )); then
    echo "usage: wb-new <slug>" >&2
    return 2
  fi
  local out
  out="$("$WB/bin/new-case" "$1")" || return
  C="$WB/$out"
  echo "current case: $C"
}

wb-use() {
  local -a all
  all=("$WB"/cases/*(N/om))
  if (( $# == 0 )); then
    if (( ${#all} == 0 )); then
      echo "no cases yet; create one with: wb-new <slug>" >&2
      return 1
    fi
    C="${all[1]}"
  elif [[ -d "$WB/cases/$1" ]]; then
    C="$WB/cases/${1%/}"
  elif [[ -f "$1/case.md" ]]; then
    C="${1:A}"
  else
    echo "no such case: $1" >&2
    return 1
  fi
  echo "current case: $C"
}

wb-cases() {
  local d
  for d in "$WB"/cases/*(N/); do
    if [[ "$d" == "$C" ]]; then echo "* ${d:t}"; else echo "  ${d:t}"; fi
  done
}

ev() {
  if [[ -z "$C" ]]; then
    echo "ev: no current case; run wb-use or wb-new <slug> first" >&2
    return 2
  fi
  if [[ "$1" == "--allow-write" ]]; then
    shift
    "$WB/bin/ev" --allow-write "$C" "$@"
  else
    "$WB/bin/ev" "$C" "$@"
  fi
}

evp() {
  if (( $# != 1 )); then
    echo "usage: evp '<command | command>'" >&2
    return 2
  fi
  ev sh -c "$1"
}

# Tab completion for wb-use, when the completion system is loaded.
if (( $+functions[compdef] )); then
  _wb_cases() { _path_files -W "$WB/cases" -/ }
  compdef _wb_cases wb-use
fi

# Start on the most recently modified case, if there is one.
() {
  local -a all
  all=("$WB"/cases/*(N/om))
  (( ${#all} )) && C="${all[1]}"
}
