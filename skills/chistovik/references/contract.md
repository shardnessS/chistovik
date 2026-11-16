# Editing contract

This file decides what you change and what you leave alone. The script only proposes; this contract decides.

## Confirm a finding

For each finding ask: what does this span hide, repeat, inflate or fake? If you cannot name it, leave the span.

Fix when:
- the span carries no meaning and deleting it costs nothing («Важно отметить, что», «Надеюсь, это поможет!»);
- it replaces a fact with an evaluation («мощный инструмент», «широкий спектр услуг») and the source has the fact nearby, or the evaluation can simply go;
- it is a formula a reader recognises as generated («это не просто X, а Y», «Результат? …», «Цифры говорят сами за себя»);
- it breaks the genre: a list, bold or a long dash in a Telegram message to HR.

Protect when:
- it is a quotation, a name, code, a term or a literal use («уникальный идентификатор», «вызов функции», «играет роль Гамлета»);
- it is the author's deliberate example of bad writing, usually in quotes or a table of «не пишем»;
- it carries legal, medical, security or scientific meaning: «может вызвать», «не менее», «обязан», «в рамках договора»;
- it is natural for the genre: «данный» and «в рамках» in an official document, short punchy lines in a post, a dash between subject and predicate in an article (`Москва — столица`).

A scanner hit, an unusual rhythm or your own taste is never enough on its own. Use only the source as evidence.

## Patterns the script cannot see

Look for these yourself in every Edit and Review. Report them as judge-only findings.

- **Manufactured balance**: every claim gets a symmetrical «с одной стороны… с другой», pros and cons of equal length.
- **Lesson arc**: problem, struggle, lesson, uplifting moral. Real stories rarely end with a moral.
- **Recap ending**: the last paragraph repeats the first one in other words.
- **Uniform emotion**: every paragraph equally enthusiastic or equally neutral.
- **Invented detail**: a vivid example, quote or number that the author never gave. In a rewrite this is the worst defect: remove it.
- **Answer that repeats the question**: «Вы спрашиваете, как настроить X. Чтобы настроить X…».
- **Hedge stack**: «возможно, в некоторой степени, отчасти» in one sentence.
- **Over-explaining**: defining what the reader obviously knows («Резюме — это документ, который…»).
- **Synonym cycling**: the same thing called by four different names to avoid repetition.

## Rewrite

- Edit only confirmed spans. Copy everything else exactly, in the same order and paragraphs.
- With no confirmed defects return the source unchanged.
- Keep facts, numbers with their qualifiers («около», «не менее»), names, terms, quotes, code, links.
- Keep the register: ты stays ты, вы stays вы, a formal letter stays formal.
- Keep hedges and uncertainty that the author meant: «кажется», «пока не проверял».
- Keep requirements exactly: «никогда», «обязательно», «только», «должен», «все» where they define a rule.
- Do not add facts, examples, numbers, emotions, jokes or personality. If the fix needs a fact that is missing, ask or leave `[placeholder]`.
- Delete before you rewrite. Most cliches are removed, not replaced.
- Vary the fixes. Do not turn every dash into a colon or every cliche into the same plain phrase: a page full of colons is a new tell.
- Never use the editor's own formulas: «Без воды. Только суть.», «Ничего лишнего.», «Не X. Y.», «Коротко и по делу.», slogans like «Четыре режима, один вход.».
- Keep the length close to the source, except in `chat`, where 3–5 sentences is the target, or when the user asked to shorten.

## Check

After every edit run `check ORIGINAL REVISED --genre G`.

- **Fail** (exit 1): a number, date, name, term or link was lost, changed or invented, or your edit introduced a hard finding. Fix it and run again, up to three rounds.
- **Warnings**: fewer negations or requirement words, a lost quotation, more than half of the words changed, a hard finding left in place. Reread each one. Keep it only if you can explain why, and say so in the answer.

Report the final verdict honestly. Never claim a check passed if you did not run it.
