# Multi-Agent Decomposition Attack — Threat Model

A plain-language walkthrough of the multi-agent decomposition attack technique. This is a
**conceptual** explainer for understanding and defense — it describes *how the attack works
in principle*, not a recipe for executing it.



## The one-sentence version

A **decomposition attack** is when you stop asking one AI one big forbidden question, and instead use
**many small, innocent-looking moves** — sometimes across **several AI agents** — so that no
single step looks dangerous, then **stitch the harmless pieces back together** yourself.

The name is an animal metaphor: a single wolf can't take down large prey, but a
**coordinated pack** can. No one wolf does anything special — the *coordination* is the weapon.
In evalkit this is modelled as the **multi-agent orchestration** strategy.

---

## Why it even works (the core idea)

Most AI safety filters check **one message at a time**. They ask: *"Is THIS request
dangerous?"*

A decomposition attack is built to make the answer to that question **always "no"** — because every
individual request really is harmless on its own. The danger only appears when you **add up
all the answers**, and by then the filter has already let each piece through.

Think of it like a bank that checks every withdrawal but never notices that the same person
made 50 small withdrawals to avoid the "large transaction" alarm.

---

## The steps, in plain language

### Step 1 — Split the goal into harmless pieces
Instead of asking the one forbidden question, the attacker breaks it into **many small
sub-questions**, each of which is genuinely normal and answerable.

- *(This is called **decomposition**.)*
- Each piece looks like ordinary curiosity. None of them, alone, trips an alarm.
- The attacker keeps the "big picture" only in their **own head** — never on the screen.

### Step 2 — Disguise the words
The attacker hides trigger words so the filter's "bad word" radar doesn't catch them.

- Swap letters for **look-alikes** from other alphabets (a Latin `a` for a Cyrillic `а`).
  *(These are called **homoglyphs** — characters that look identical but are different to a
  computer.)*
- Use odd spellings, spacing, or invisible characters.
- To a human it reads normally; to a keyword filter it's an unfamiliar string.

### Step 3 — Wrap it in an innocent costume
The attacker frames the conversation as something legitimate so the *context* feels safe.

- "I'm writing a **novel**, my character explains…" *(fiction framing)*
- "Make a **study guide / glossary / table** about this academic topic…" *(document framing)*
- The harmful request rides along **inside** a believable, harmless-looking container.

### Step 4 — Bury it in a long conversation
Modern AIs can read very long chats. The attacker uses that against them.

- Spread the pieces across a **huge, rambling conversation** so the harmful thread is diluted.
  *(This is **long-context smuggling**.)*
- Establish "facts" early, then refer back to them later, so the dangerous part is assembled
  from things that were each introduced innocently, far apart.

### Step 5 — Bring in the pack (multiple agents)
This is the part that makes it a *pack* hunt rather than a lone trick.

- Use **more than one AI agent**, each doing a small, safe-looking job.
- One agent rephrases, another "translates," another "summarizes," another "fills in a
  table." Each agent only ever sees a **harmless slice**.
- Because no single agent ever holds the whole dangerous picture, no single agent refuses.
  The **coordination between them** does what no one agent would.

### Step 6 — Reassemble offline
The model never produces the dangerous thing in one place. **The attacker does the final
assembly themselves**, combining the innocent fragments into something usable.

- The AI did the easy, harmless parts.
- The human (or a controlling script) snaps the puzzle together at the end.

---

## The same idea as a picture

```
Forbidden goal
      │
      ▼
 ┌─────────────────────────────────────────────┐
 │  Step 1: chop into small harmless questions  │
 └─────────────────────────────────────────────┘
      │        │        │        │
   piece A  piece B  piece C  piece D     ← each looks innocent
      │        │        │        │
 [disguise words] [fiction frame] [long chat] [different agent]
      │        │        │        │
      ▼        ▼        ▼        ▼
   answer   answer   answer   answer        ← filter says "fine" every time
      └────────┴────┬───┴────────┘
                    ▼
        Step 6: human reassembles the pieces  ← danger appears only HERE,
                                                 after the AI is done
```

The whole trick is geometry: keep every visible step **below the alarm line**, and do the
illegal addition **off-screen**.

---

## Why the defenders say it failed here

Anthropic's argument is worth understanding, because it's the other half of the story:

1. **Refusals are not the real wall.** Getting a model to *keep talking* after it says "I'd
   rather not" is an old, well-known weakness of almost all chatbots. It's annoying, but it's
   not the same as defeating safety.
2. **The real guards stand outside the model.** Separate "classifier" systems watch inputs
   and outputs **independently**. Talking the model itself into cooperating doesn't switch
   those off.
3. **No real "uplift."** On review, they say the outputs were either **not from Fable 5** at
   all, or were just **public-knowledge information** that gives no real-world advantage to a
   bad actor.

So the lesson isn't "AI safety is fake." It's a genuine open research question: **safety
checks that only look at one message, or one model, at a time can miss a threat that only
exists when you add many harmless pieces together.**

---

## The takeaways (if you remember three things)

1. **No single step looks dangerous** — that's the entire design.
2. **The danger lives in the reassembly**, which happens *after* and *outside* the AI.
3. **One-message-at-a-time filtering is the blind spot** the attack aims at — which is why
   defenders are moving toward checks that look at the **whole conversation and the whole
   multi-agent system**, not just individual messages.

---


