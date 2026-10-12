# Support Workbench

A small environment for working any technical support problem with an AI
assistant. You describe the situation in plain language; Claude structures it,
proposes what to ask and check, keeps track of what is known, and drafts the
write-ups. You make the calls.

It works whether or not you can touch the affected system. In most support
work you can't, so the workbench is built around questions, checks for someone
else to run, and reading what comes back.

| Outcome | Where it happens |
|---|---|
| 1. Understand an unfamiliar problem quickly | `case.md` → Intake, Known / unknown |
| 2. Narrow it down without unsafe changes | `case.md` → Checks, Findings |
| 3. Use AI to generate and test hypotheses, not invent a diagnosis | `case.md` → Hypotheses; rules in `CLAUDE.md` |
| 4. Reach a verified fix or a useful escalation | `case.md` → Resolution; `escalation.md` |
| Know what to do next without rereading the case | `next-steps.md` |
| 5. Explain the result to a customer and an engineer | `customer-reply.md`, `escalation.md` |

## Layout

```
CLAUDE.md          rules the AI follows in this directory
.claude/commands/  shortcuts: /triage /update /reply /escalate /challenge
templates/         case.md, next-steps.md, customer-reply.md, escalation.md
cases/             one folder per problem (created for you)
bin/new-case       scaffold a case from templates/
bin/ev             optional: run a local command and save its output
workbench.zsh      optional zsh helpers for the terminal
practice/          a hands-on scenario with local logs and code
```

## How to use it

Open this folder in Claude Code (desktop app: choose the folder
`SUPPORT_WORKBENCH`; terminal: `cd` here and run `claude`). `CLAUDE.md` loads
automatically, so plain language is enough.

### 1. Describe the problem

Type the situation as it was given to you, details included:

> There is no connectivity to a client running Windows 11 23H2 with IP address
> 10.20.4.37.

or `/triage` followed by the same text. Claude creates
`cases/<date>-<slug>/` and replies with:

- **Restatement**: one sentence, including what isn't known yet
- **Known / not known**: each statement labelled Observed, Reported, Inferred or Assumed
- **Questions**: up to five, each with what the answer decides
- **Hypotheses**: two to four, ranked, each with what would confirm or kill it
- **First checks**: exact commands or steps for that platform, read-only first,
  each with how to read the result

### 2. Feed back what you learn

Answer a question or paste output, in plain language or with `/update`:

> /update Customer says other PCs on the same switch are fine. ipconfig shows
> 169.254.11.80, no default gateway.

Claude records the finding, kills or strengthens hypotheses, says what changed
in its thinking, and gives the next check. Repeat until there is a cause you
can verify or a clear dead end.

### 3. Push back

`/challenge`, or "what doesn't the leading hypothesis explain?" Use this before
you commit to a cause.

### 4. Write it up

- `/reply non-technical office manager` → `customer-reply.md`
- `/escalate network team` → `escalation.md`

Both are drafted from `case.md` only, and each stands on its own.

## Prompts worth having ready

- "List what here is observed versus merely reported."
- "Which single read-only check separates the most hypotheses?"
- "What is the riskiest step you've proposed, and how would we undo it?"
- "What evidence contradicts your leading hypothesis?"
- "Are you recalling that behaviour from memory or from a source? Look it up."
- "Give me those steps for a customer who has never opened a command prompt."
- "Same problem, but the client is macOS / Linux / a phone. What changes?"
- "We've run out of things to check remotely. Draft the escalation."

## Ways to narrow a problem

Four questions split almost any problem: **one or many? always or sometimes?
since when, and what changed? what still works?** Then pick a method to match:

| Problem type | Method | Typical first split |
|---|---|---|
| No connectivity | Work up the layers: link → address → gateway → name resolution → port → application | Is it this device, this network segment, or the destination? |
| Can't log in / access denied | Separate "who are you" from "what are you allowed" | Exact error text; one user or everyone; one resource or all |
| Slow | Find where the time goes | Slow compared with what; one user or all; constant or at certain times |
| "It worked yesterday" | Timeline of changes | What changed on either side: updates, config, credentials, hardware |
| Error or crash | Reproduce, then shrink | Exact message; the log at that moment; smallest steps that trigger it |
| API / integration | Follow one request end to end | Does the request leave, arrive, get rejected, or get a bad response? |
| Wrong or missing data | Trace one known-bad record | Where along the path it first goes wrong |
| Install / upgrade fails | Compare with a working install | Versions, prerequisites, installer log |

## Pacing a live scenario

| Phase | Do | Say out loud |
|---|---|---|
| Intake | Restate. Split reported from observed. | "Here's what I know, here's what I'm assuming." |
| Scope | One or many, since when, what changed, what works. | "Before I theorise I want to know how wide this is." |
| Hypotheses | Rank them; choose the check that splits them. | "If it's A I expect X; if not, Y." |
| Checks | Read-only first. Read each result against the hypotheses. | "That rules out A. Next I'd check…" |
| Resolve | Verified fix, workaround, or escalation. | "This check failed before and passes now." |
| Write up | Customer reply and escalation. | Lead with the answer, then the evidence. |

When the AI proposes something, say why you accept it or don't. Read its
commands before repeating them, question anything stated without a source, and
make the decisions yourself, especially before any step that changes state.

## When you can run commands yourself

If the fault is on your own machine, or you've been given logs, config or code,
ask Claude to inspect them directly. It stays read-only unless you approve a
specific change.

`bin/ev` is there when you want a record of what a command printed:

```sh
bin/ev cases/2026-10-11-lan-ping-ethernet ipconfig /all
bin/ev cases/2026-10-11-lan-ping-ethernet sh -c "grep ERROR app.log | wc -l"
```

It saves the output under the case's `evidence/` with the time and exit code,
and refuses commands that look like they change state unless you pass
`--allow-write`. Nothing else in the workbench depends on it.

`workbench.zsh` adds terminal shortcuts (`wb-new`, `wb-use`, `ev`, `evp`);
`source` it from `~/.zshrc` if you want them. Its header lists what each does.

## Practice

- **Open-ended:** make up a one-line problem from each row of the table above
  and run it through steps 1 to 4, playing the customer yourself.
- **Hands-on:** [practice/01-webhook-signatures/](practice/01-webhook-signatures/)
  has local logs, code and a replay tool. Follow its
  [WALKTHROUGH.md](practice/01-webhook-signatures/WALKTHROUGH.md).
