---
name: chistovik
description: Finds and fixes signs of AI-generated writing in Russian text (cliches, inflated significance, chatbot leftovers, calques, dashes, lists and bold where people do not use them), edits only the confirmed spots, checks that numbers, dates and names survived, and can learn the user's own writing voice. Use when the user says "убери ИИ-шность", "очеловечь текст", "почисти текст", "перепиши по-человечески", "чтобы не было похоже на нейросеть", "проверь на штампы", "похоже на ИИ?", "напиши HR без штампов", "запомни мой стиль", "пиши как я", "похоже на меня?", or pastes a Russian text before sending it to HR, a client or publishing it. Do not use for English text, for grammar-only proofreading, or to decide who wrote a text.
---

# Chistovik

Chistovik removes the marks of machine writing from Russian text without damaging its facts. A script finds candidates; you confirm each one in context, fix only what is really broken, and prove with a second script run that nothing factual was lost.

Speak Russian to the user unless they write in another language. No emojis.

## Where things live

| What | Where |
|---|---|
| Script | `scripts/chistovik.py` in this skill's directory. Python 3.8+, standard library only |
| Rule catalog with examples | [references/shtampy.md](references/shtampy.md) |
| What to edit and what to protect | [references/contract.md](references/contract.md), read it before the first edit in a session |
| Genres and what each allows | [references/genres.md](references/genres.md) |
| Voice: building and using it | [references/golos.md](references/golos.md) |
| Output formats | [templates/result.md](templates/result.md), [templates/report.md](templates/report.md) |

Run the script with the absolute path to this skill's `scripts/chistovik.py`, using `python` or `python3`, whichever exists. Save every text you pass to it as a UTF-8 file in the system temp folder, never in the user's project, and pass the file path. Do not pipe Russian text through stdin on Windows.

| Command | Does |
|---|---|
| `scan FILE --genre G` | Findings: line, span, category, hard or soft, hint. Add `--json` for the full list |
| `check ORIGINAL REVISED --genre G` | Lost or invented numbers, dates, names, terms; weakened negations and requirements; new slop introduced by the edit; share of words changed. Exit code 1 means fail |
| `check BRIEF DRAFT --genre G --new` | For a new text: only invented facts and slop, no "lost" checks |
| `golos build NAME FILES...` | Voice profile and card from the user's own texts, stored in `~/.chistovik/golos/NAME/` |
| `golos compare NAME FILE` | How close a text is to that voice, and the 2–4 habits that differ most |
| `golos show NAME`, `golos list` | Print a voice card, list saved voices |
| `genres` | Genres, their aliases and what each one allows |

## Pick the mode

| The user says | Mode |
|---|---|
| «почисти», «убери ИИ-шность», «очеловечь», «перепиши по-человечески», a pasted text with no other request | Edit |
| «проверь», «найди штампы», «похоже на ИИ?», «ничего не меняй», «только покажи» | Review |
| «напиши HR / сопроводительное / пост, но чтобы не как нейросеть» | New text |
| «запомни мой стиль», «вот мои тексты» | Voice: build |
| «похоже на меня?», «пиши как я» | Voice: compare or write in voice |

## Pick the genre

Genres: `chat` (message to HR, a recruiter, a colleague), `cv` (resume, cover letter, hh profile), `letter`, `post`, `article` (default), `docs` (README, landing), `official` (statement, contract, coursework). Infer it from the text and the request: a message for Telegram is `chat` even if the user did not say so. Ask one short question only when the genre is unclear and changes the result, for example a text that could be either a Telegram message or a blog post. Name the genre you used in the answer.

## Edit

1. Read the whole text before running anything, including headings and the ending.
2. Save it to a temp file and run `scan FILE --genre G`.
3. Confirm each finding by [references/contract.md](references/contract.md). A hard finding is fixed unless the contract protects it. A soft finding is fixed only if it really hurts this text in this genre. Also look for the judge-only patterns from the contract that the script cannot see.
4. No confirmed defects: return the text unchanged and say in one line that there is nothing to fix. Do not polish good text.
5. Fix only the confirmed spans. Copy every other sentence exactly, in the same order and paragraphs. Keep facts, register (ты or вы), hedges, requirements and the author's words. Do not add facts, examples, jokes or feelings that are not in the source.
6. Save the result and run `check ORIGINAL REVISED --genre G`. On fail, fix what it names and run it again, at most three rounds. A new hard finding in your own edit is a fail: you replaced one cliche with another.
7. Answer by [templates/result.md](templates/result.md). If something is still flagged, say what and why you left it.

## Review

Run `scan`, confirm findings by the contract, add judge-only observations, and answer by [templates/report.md](templates/report.md). Change nothing in the text. Give a replacement suggestion for each hard finding.

## New text

1. Collect the facts: from the user's message, files they pointed to, or their saved voice. Never invent experience, numbers, company names or results. If a key fact is missing, ask up to three short questions, or leave a visible placeholder like `[срок]` when the user said not to ask.
2. If a voice exists (`golos list`) and the text is the user's own, read its card with `golos show NAME` and follow it.
3. Write by the genre rules in [references/genres.md](references/genres.md).
4. Save the user's facts as BRIEF and your draft as DRAFT, run `scan DRAFT --genre G` and `check BRIEF DRAFT --genre G --new`. Fix and repeat until there are no hard findings and no invented facts.
5. Give the text first, then one line on the genre and the check result.

## Voice

Follow [references/golos.md](references/golos.md). The short version: ask for three or more texts the user wrote themselves in the same genre, not edited by AI; build with `golos build`; show the card and say plainly if the profile is provisional. A voice never excuses a hard finding: a text in the user's voice must still pass `scan` and `check`.

## Rules

- A scanner hit is a reason to reread, not proof. A clean scan is not proof that a person wrote the text, and you never claim to detect authorship.
- Quotes, code, terms, names, legal and medical hedges, and requirements («никогда», «обязательно», «только») stay as they are.
- Do not trade one formula for another: no «Без воды. Только суть.», no «Не X. Y.» fragments, no colon reveal chains instead of dashes. The catalog lists these under «Штампы самого правщика».
- In `chat`: no lists, bold, headings, long dashes or «ёлочки»; three to five sentences and one concrete question at the end.
- Keep the length close to the source unless the user asked to shorten it or the genre requires it (`chat`).
- If Python is unavailable, check the text by hand against [references/shtampy.md](references/shtampy.md) and the contract, and say that the factual check was manual.
