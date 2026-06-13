# Techniques

## Query Decomposition

Splits a single blocked query into N sub-queries, each innocuous in isolation.

**Mechanism:** An LLM (or rule-based fallback) receives the query and a stealth prompt asking for a "curriculum design" or "study materials" breakdown. Trigger words are sanitized (e.g., "exploit" → "utilize") before reaching the helper model.

**Purpose:** No individual sub-query triggers the safety classifier; the target information is only revealed when all responses are reassembled externally.

## Unicode Homoglyph Substitution

Replaces ASCII characters with visually identical Unicode characters from other scripts.

**Mechanism:** Maps each letter to a pool of homoglyphs (e.g., `a` → `а` Cyrillic, `o` → `о` Cyrillic). Controlled by obfuscation level: light (15% replacement), moderate (30%), aggressive (50%).

**Purpose:** Evades keyword-based safety classifiers that don't normalize Unicode before matching.

## Narrative Framing

Wraps each sub-query in a benign narrative context.

**Strategies:**
- **Fiction:** "Writing a techno-thriller novel..."
- **Study Guide:** "Create a study guide for a university course..."
- **Academic Review:** "Writing a literature review for my PhD..."
- **Documentation:** "Writing internal documentation for our team..."
- **Translation:** "Translate this technical description..."
- **None:** No wrapping (baseline)

**Purpose:** Makes each sub-query appear as legitimate educational/creative content rather than a coordinated extraction attempt.

## Long-Context Padding

Adds filler content before the sub-query to dilute classifier signal density.

**Mechanism:** Prepends N tokens of filler content (repeated innocuous words) to each API request. Leverages large context windows (Fable 5: ~1M tokens).

**Purpose:** Safety classifiers that score the full context window see a lower density of trigger content, potentially reducing classification confidence.

## Multi-Agent Orchestration

Uses multiple agent roles to transform queries before sending to the target.

**Agent types:**
- **Decomposer:** Splits query into sub-parts
- **Rephraser:** Rewrites query in different vocabulary
- **Translator:** Chain-translates through intermediate languages
- **Summarizer:** Condenses text while preserving key info
- **Filler:** Generates innocuous padding content

**Purpose:** Each transformation layer removes surface-level indicators of malicious intent, making classifier evasion more robust.

## Context Smuggling

Builds multi-turn conversation history where early turns are innocuous QA and later turns gradually introduce the target topic.

**Mechanism:** Alternates user/assistant turns with benign content (e.g., "What is the capital of France?", "How does photosynthesis work?") before the target sub-query. Filler questions and answers are drawn from a curated pool of neutral topics.

**Purpose:** The safety classifier evaluates each turn in context; the gradual introduction of sensitive topics within a long conversation can evade single-turn classification thresholds.

## Self-Correction (Retry Loop)

After reassembly, verifies the output contains the target information. If not, retries with different parameters.

**Parameters varied:** Obfuscation level, framing strategy, padding amount, agent configuration, prompt variant.

**Purpose:** A single parameter combination may not evade the classifier; the retry loop finds working configurations.
