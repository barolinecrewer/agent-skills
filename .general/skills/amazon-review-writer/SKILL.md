---
name: amazon-review-writer
description: Draft or revise concise Amazon product reviews from the user's actual experience and notes. Use for review titles and bodies, not product advertising or invented testimonials.
---

# Amazon Review Writer

Turn the user's experience into a concise, natural Amazon-style review title and body. Help a prospective buyer understand how the product worked in a concrete situation. Preserve the user's opinion and level of certainty.

## Grounding rules

- Use only facts and experiences the user provides. Never invent firsthand experience, usage duration, measurements, tests, defects, results, product specifications, purchase details, or other claims.
- First-person statements must describe the user's supplied experience. Do not turn a product listing, another review, or an assumption into something the user supposedly observed.
- Keep subjective impressions subjective: “feels sturdy” does not establish durability; “seems faster” does not establish a measured improvement. Short use does not establish long-term reliability.
- Preserve qualifiers, conditions, and scope. One successful use is not “always reliable”; trouble with one setup is not universal incompatibility. Do not invent causes for a problem.
- Include comparisons only when the user supplies them. Do not imply they have used a competing product unless they say so.
- Include relevant reported downsides without softening or exaggerating them. Balanced means faithful to the evidence, not forcing equal praise and criticism. Never manufacture a drawback or say “no issues” just because dislikes are blank.
- Use an optional rating exactly as supplied. Never infer a rating or change it to match the prose. Clarify an invalid or ambiguous rating, or a material contradiction between the rating and notes.
- If the user has supplied no actual experience, ask for it before drafting. Do not write a first-person review from the product name or description alone. If asked to fabricate experience, offer to edit truthful notes instead.
- Do not add promotional language, seller talking points, calls to purchase, claims about review helpfulness, or promises of an Amazon Vine invitation. Preserve any user-provided disclosure of a free product or other relevant relationship.

## Input template

Accept this template or equivalent informal notes. Blank optional fields are unknown, not evidence that something did not happen.

```text
Product name:
Category:
How long I've used it / frequency of use:
Setup and context (where, with what, and what I use it for):
What I liked (specific observations):
What I disliked or limitations I noticed:
Comparisons with products I've actually used (optional):
Rating out of 5 (optional):
Other facts, uncertainty, or disclosure to preserve (optional):
Preferred length or tone (optional):
```

## Workflow

1. Identify the user's supplied facts, opinions, uncertainties, and rating. Treat pasted listings or other people's reviews as background only; they cannot supply firsthand evidence.
2. Check whether there is enough experience to write a useful review. If a crucial fact is missing or contradictory, ask one focused question or a short set of necessary questions. Otherwise draft from available information, omitting unknown details. Do not require every template field.
3. Choose the most useful concrete use case and observation. Add duration, setup, a comparison, or a downside when supplied and relevant. Fit the structure to the notes rather than filling a fixed praise–criticism formula.
4. Draft a short title and body. Aim for a 4–10-word title and roughly 60–140 words of body text when the notes support that length. Use fewer words for sparse notes; never pad to reach a target. Follow explicit user length preferences.
5. Audit every factual clause against the notes. Remove unsupported details, overstatements, invented comparisons, implied tests, and conclusions that extend beyond the user's experience. Check that the title is grounded too.
6. Run the human-sounding pass below. Make targeted edits, then check it once more for any pattern the first pass missed.
7. Return only the finished review in the format below, unless clarification is needed.

## Writing guidance

- Sound like a person explaining a purchase to another person: direct, specific, and non-promotional.
- Vary sentence lengths, openings, and structure naturally. Avoid a repeated template across reviews, forced slang, deliberate errors, or decorative anecdotes.
- Prefer concrete use cases and supplied observations to generic judgments. “I keep it beside my bed” is useful when supplied; “perfect for everyday life” is filler.
- Avoid generic openings and endings such as “I recently purchased,” “exceeded my expectations,” “game changer,” “highly recommend,” and “you won't regret it.” Preserve a phrase only if the user specifically requests it.
- Avoid excessive adjectives, superlatives, exclamation points, marketing copy, keyword repetition, and repeatedly spelling out the full product name.
- Keep the user's sentiment intact. A positive review may be wholly positive; a negative review need not invent praise. Mention who or what a limitation affects only when supported by the user's context.
- Use one or two short paragraphs by default. Do not force headings, pros-and-cons lists, or a final verdict into a brief review.

## Human-sounding pass

Adapt the relevant guidance from [conorbronsdon/avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing) to short consumer reviews. Treat these patterns as editing signals, not proof that a person or model wrote the text.

- Preserve the user's voice. If the notes include contractions, plain wording, a preference, or a mild uncertainty, keep that character when it reads naturally. Do not “upgrade” simple words or sand every sentence into the same polished register.
- Do not manufacture personality. Never add slang, typos, fake candor, dramatic fragments, rhetorical questions, or first-person anecdotes that are absent from the notes.
- Vary rhythm without turning the review into a performance. Mix sentence lengths and openings, but avoid a run of clipped sentences, repeated grammatical shapes, or several sentences beginning with the same word.
- Cut chatbot and review boilerplate. Examples include “I recently purchased,” “let's dive in,” “here's the thing,” “what surprised me most,” “it's worth noting,” “in conclusion,” “only time will tell,” and “I hope this helps.”
- Cut inflated or promotional wording such as “game changer,” “seamless,” “robust,” “cutting-edge,” “exceptional,” “must-have,” and “highly recommend.” Replace it with a supplied observation, or remove it if the notes do not support anything more specific.
- Prefer plain verbs. Write “is,” “has,” “uses,” or “fits” when accurate instead of “serves as,” “boasts,” “features,” “utilizes,” or “delivers” used as marketing language.
- Avoid staged contrast formulas such as “It's not just X; it's Y,” fake concessions, a forced set of three benefits, and teaser fragments such as “The catch?” State the useful point directly.
- Use transitions only when they express a real relationship. Remove mechanical openers such as “Moreover,” “Furthermore,” “Additionally,” and “That said” when the sentences connect without them.
- Avoid stacked adjectives, repeated superlatives, em dashes used for drama, title case, emoji, hashtags, and unnecessary formatting. An Amazon review should read like a brief account of use, not a social post or product page.
- Keep concrete details only when they came from the user. Never cure vague writing by adding a number, date, test, use case, comparison, reaction, or flaw.

On the second pass, compare every first-person claim and concrete detail with the input again. Subtract filler and sharpen supplied observations, but do not add experience, facts, stance, or personality. If the draft is already natural and grounded, leave it alone rather than rewriting for the sake of variation.

## Output format

```text
Title: [Concise title grounded in the user's notes]
Rating: [User-supplied rating]/5

[Review body]
```

Omit the entire rating line if none was supplied. Do not put placeholders, drafting commentary, fact-check notes, or requests for more details inside a finished review. This skill drafts text; it does not publish reviews.

## Examples

The inputs below are fictional demonstrations, not reusable facts. Never transfer their experiences or measurements into a real review.

### Example 1: Specific use and a supplied downside

**Input**

```text
Product name: Clip-on reading light
Category: Lighting
How long I've used it: Three weeks, most evenings
Setup and context: Clipped to a paperback while reading in bed
Liked: Lowest setting is comfortable for me; clip stays on my paperback
Disliked: Buttons are hard to tell apart in the dark
Rating: 4/5
```

**Output**

```text
Title: Comfortable light, hard-to-distinguish buttons
Rating: 4/5

I've used this most evenings for three weeks, clipped to a paperback while reading in bed. The lowest setting is comfortable for me, and the clip stays on the book. My main annoyance is the buttons: they're hard to tell apart in the dark.
```

### Example 2: Comparison without invented performance claims

**Input**

```text
Product name: Adjustable laptop stand
Category: Desk accessories
How long I've used it: Two months
Setup and context: Home desk, 14-inch laptop, separate keyboard
Liked: Raises the screen to a height I find comfortable; folds into my desk drawer
Disliked: Wobbles when I type directly on the laptop
Comparisons: My old fixed stand did not fold
Rating: Not supplied
```

**Output**

```text
Title: Useful with my separate keyboard

This raises my 14-inch laptop screen to a height I find comfortable at my home desk. I've used it for two months with a separate keyboard. It also folds into my desk drawer, which my old fixed stand couldn't do.

The downside is wobble when I type directly on the laptop. That's the main limitation I've noticed with this setup.
```

### Example 3: Limited experience and no supplied downsides

**Input**

```text
Product name: Silicone muffin tray
Category: Bakeware
How long I've used it: Once
Setup and context: Made blueberry muffins
Liked: Muffins came out without sticking
Disliked: Nothing to report yet
Rating: Not supplied
```

**Output**

```text
Title: Blueberry muffins released without sticking

I've used this tray once for blueberry muffins, and they came out without sticking. That's all I can speak to so far; I haven't used it enough to judge how it holds up over time.
```
