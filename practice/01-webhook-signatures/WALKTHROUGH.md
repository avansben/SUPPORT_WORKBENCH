# Walkthrough: the webhook signatures case

This scenario is the hands-on one: the logs, code and replay tool are all local,
so you run commands yourself and log them with `bin/ev` (see the workbench
README, "When you can run commands yourself").

This walks the practice scenario step by step. It tells you which commands to
run and what to record, but not what the answer is. The commands are verified
to work as written.

### 0. Set up

```sh
cd ~/docs/SUPPORT_WORKBENCH
C=cases/2026-10-09-webhook-signatures
P=practice/01-webhook-signatures
```

`C` is the path that `bin/new-case webhook-signatures` printed. If you sourced
`workbench.zsh`, skip the two assignments: `$C` and `$P` are already set (check
with `wb-cases`).

Optional, but it lets you show your fix as a diff in step 6:

```sh
git init -q && git add -A && git commit -qm "baseline"
```

### 1. Intake (about 5 minutes)

1. Read `$P/README.md`, then `$P/ticket.md`.
2. Paste the ticket into section 1 of `$C/case.md`.
3. Write the restatement, impact and environment.
4. In section 2, list the customer's claims. Note that the ticket contains two
   theories of its own. Record them as *Reported* hypotheses, not as facts.

### 2. Scope the failure (about 10 minutes)

Answer four questions from the customer's log before theorising: how many, what
kind, where, and since when.

```sh
# How many deliveries, and how many failed?
bin/ev $C wc -l $P/logs/receiver.log
bin/ev $C sh -c "grep -o 'reason=[a-z_]*' $P/logs/receiver.log | sort | uniq -c"

# Is it one region or both?
bin/ev $C sh -c "grep status=401 $P/logs/receiver.log | grep -o 'region=[a-z-]*' | sort | uniq -c"

# When did it start? Look at the first failure and what passed before it.
bin/ev $C grep status=401 $P/logs/receiver.log

# What changed around then?
bin/ev $C cat $P/CHANGELOG.md
```

Add a row to section 3 of `case.md` for each, and fill in "What changed
recently?" with every candidate, including the customer's own change.

### 3. Hypotheses (about 5 minutes)

Write at least three rows in section 4: the customer's two theories plus at
least one of your own. For each, fill in the "if true" and "if false" columns
before running anything. A useful prompt for Claude here:

> Here is the ticket and my evidence so far. Give me four hypotheses. For each,
> one observation that would confirm it and one that would kill it. Then tell
> me which single read-only check separates the most of them.

### 4. Test the hypotheses (about 10 minutes)

The replay tool sends the exported events through the product's sender and the
customer's receiver locally. It writes nothing and exits 1 if any delivery
fails.

```sh
# Does it reproduce locally at all, with today's code and one secret on both sides?
bin/ev $C python3 $P/tools/replay.py

# Customer theory: clock drift. Give the receiver a 2-minute offset.
bin/ev $C python3 $P/tools/replay.py --skew 120

# Customer theory: the old secret. Replay with it on both sides.
bin/ev $C python3 $P/tools/replay.py --secret whsec_test_northwind_a71e

# What do the failing events have in common that the passing ones do not?
bin/ev $C sh -c "grep status=401 $P/logs/receiver.log | grep -o 'evt_[0-9]*' | grep -f - $P/data/events.jsonl"
bin/ev $C sh -c "grep status=401 $P/logs/receiver.log | grep -o 'evt_[0-9]*' | grep -v -f - $P/data/events.jsonl"
```

Compare the two event lists side by side. Also compare the set of failures in
the customer's log with the set of failures in your replay: if they differ,
the event that differs is your most informative data point.

Update the Status column for each hypothesis, and move the dead ones to
"Killed" with the evidence file that killed them.

### 5. Read the code and reproduce (about 5 minutes)

Only now read the code, with a specific question in mind.

```sh
bin/ev $C cat $P/app/webhooks.py $P/app/transport.py $P/app/signing.py
bin/ev $C cat $P/customer/receiver.py
bin/ev $C python3 -m unittest discover -s $P/tests
```

Then find the smallest repro: one event that fails and one similar event that
passes.

```sh
bin/ev $C python3 $P/tools/replay.py --event evt_NNNN
bin/ev $C python3 $P/tools/replay.py --event evt_MMMM
```

Replace `evt_NNNN` with a failing event id and `evt_MMMM` with a passing one.

Put both commands and their output in section 5 of `case.md`. Ask yourself why
the existing tests pass.

### 6. Fix or escalate (about 5 minutes)

1. Add a failing test to `$P/tests/test_webhooks.py` that captures the repro,
   and confirm it fails:

   ```sh
   python3 -m unittest discover -s $P/tests
   ```

2. Make the smallest change in `$P/app/` that fixes it.
3. Confirm the test passes and the full replay is clean:

   ```sh
   bin/ev $C python3 -m unittest discover -s $P/tests
   bin/ev $C python3 $P/tools/replay.py
   ```

   The replay should now report `0 failed` and exit 0.

4. If you ran `git init` in step 0, capture the patch for the escalation:

   ```sh
   git diff -- $P/app $P/tests
   ```

In a real support role you would usually not ship this fix yourself, so write
`escalation.md` as if engineering will apply it. Think about scope: is this
one customer's problem?

### 7. Write up (about 5 minutes)

1. `$C/case.md` section 6: root cause in one paragraph citing evidence files,
   your confidence, and what would change your mind.
2. `$C/customer-reply.md`: lead with what is happening and what they should
   do. Address both of their theories in a sentence each. Consider what they
   should *not* do.
3. `$C/escalation.md`: summary, repro commands, evidence, ruled-out table,
   proposed diff, and who else is affected.

### 8. Check your work

Compare against `$P/.solution/ANSWER.md`, or ask Claude: "Check my case against
the practice 01 answer key and tell me what I missed." To run the scenario
again from scratch, undo your changes to `$P/app` and `$P/tests`
(`git checkout -- $P` if you made the baseline commit) and create a new case
with a different slug.

