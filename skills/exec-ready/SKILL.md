Rewrite or audit the current document so an executive who pastes it into an LLM gets an accurate, useful summary on the first ask.

## Process

1. Read the document the user points you to (or the currently open file).
2. Audit it against the checklist below.
3. Rewrite or restructure in place, preserving all factual content.

## Checklist

Apply every applicable rule:

### Lead with the answer
- The first 2-3 sentences should state the conclusion, decision, or recommendation outright. An LLM asked "what does this mean?" will pull its answer from the opening.
- If there's a summary table, move it to the top, above any methodology or context.

### Label what's what
- Mark sections that are context/detail as "Detail" or place them below a horizontal rule. LLMs weight early content higher when summarizing.
- If there's one canonical number vs. many supporting numbers, say which is canonical explicitly ("The key metric is X").

### One sentence per claim
- Every major claim gets its own sentence. Compound sentences with multiple stats get split. LLMs extract claims at the sentence boundary.

### Disambiguate numbers
- When two numbers could be confused (e.g., two percentages from different analyses), label each with its source inline: "Sales analysis: 43.5%; v2 pipeline: 48.5%."
- Never let a number float without context about what it measures and which dataset it comes from.

### State the "so what" explicitly
- Don't let the reader's LLM infer the implication. Write it: "This means we should..." or "No action needed because..."
- If the document is informational (no action required), say that upfront: "This is for awareness, not decision."

### Remove ambiguity traps
- Eliminate vague pronouns ("it", "this", "that") when they could refer to more than one thing. Repeat the noun.
- Don't use "significant" without specifying statistical or practical significance.
- Don't use "directional" as a result label.

### Structure for chunking
- Use headings (##) for every distinct topic. LLMs chunk on headings.
- Prefer tables over paragraphs for comparisons.
- Keep paragraphs under 4 sentences.

### Metadata up front
- If the document has a date, author, or status, put it in the first few lines or frontmatter so the LLM can cite it.

## Constraints

- Never add opinions, recommendations, or implications the author didn't state. You are restructuring, not interpreting.
- Never strengthen or weaken a claim. If the doc says "results suggest," don't rewrite as "results prove" or "results show."
- Never invent a "so what" the author didn't provide. If the doc has no conclusion, flag it ("Note: this doc has no stated recommendation — consider adding one") rather than writing one yourself.
- Preserve the author's hedging, caveats, and qualifying language exactly. Moving a caveat is fine; dropping or softening it is not.
- If a number has no stated interpretation in the original, don't add one. Label and disambiguate it, but don't tell the reader what it means.

## Output

Return the rewritten document in place (edit the file). After the edit, add a brief note (3 lines max) stating what you changed and what you skipped.
