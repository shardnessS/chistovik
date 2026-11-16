# Genres

The genre changes which findings count and how strict they are. `python scripts/chistovik.py genres` prints the same list with aliases.

| Genre | Text | What changes |
|---|---|---|
| `chat` | Message to HR, a recruiter, a colleague in Telegram or another messenger | No lists, bold, headings, long dashes. «Ёлочки» and `!` are suspicious. Resume and outreach cliches are hard. More than 6 sentences or 120 words is too long |
| `cv` | Resume, cover letter, hh or LinkedIn profile | Lists and bold labels are fine. Outreach cliches and listed personal qualities are hard |
| `letter` | Business e-mail | Lists are fine. Outreach cliches are hard, bureaucratic phrasing is soft |
| `post` | Telegram channel, social network | Short paragraphs, short lines and emoji in text are fine |
| `article` | Article, blog, Habr, vc.ru, any other text. Default | Standard rules |
| `docs` | README, documentation, landing page | Lists, bold labels, headings and dashes are fine. Marketing gloss is still hard |
| `official` | Statement, contract, coursework, report | Bureaucratic phrasing is normal and not flagged. Negations and requirements are checked strictly |

## How to write in each genre

**chat.** One message, greeting and content together: never a lone «Здравствуйте» waiting for an answer. Three to five sentences. Why you are writing to this person or company, one or two facts about yourself, one concrete question at the end («Когда удобно созвониться?»). Plain punctuation: commas and full stops, straight quotes or none. No «Надеюсь, у вас всё хорошо», «Буду рад обсудить возможности», «Уверен, что мой опыт будет полезен».

**cv.** Facts instead of adjectives: what you built, for whom, with what result, in numbers when the user gave numbers. Past tense verbs: «сделал», «перевёл», «ускорил». Personal qualities only through examples. No «стрессоустойчивый», «командный игрок», «нацелен на результат».

**letter.** Subject line says what is needed. First sentence says why you write. One request per letter, with a date if there is a deadline. Polite but not ceremonial.

**post.** One thought per post. Start with the event or the fact, not with «Друзья, сегодня хочу поделиться». Rhetorical questions and dramatic one-liners are still tells when they repeat.

**article.** Headings say what the section shows. No announcement of the article's contents, no closing recap. Each claim with a source or the author's own experience.

**docs.** Short sentences, concrete numbers, commands in code blocks. Evaluations («мощный», «бесшовный», «интуитивно понятный») go; what it does and in how many steps stays.

**official.** Keep the form the document requires. Fix only chatbot leftovers, inflated significance and calques. Never touch legal wording, references to articles and sections, or obligations.
