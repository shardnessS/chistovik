---
type: llm
---

PASS if the assistant ran `chistovik.py scan` with genre `chat` and then `chistovik.py check` on the original and the revision, and gave a cleaned message in Russian. The message keeps «Анна», «Python», «4 года» (or «четыре года»), «Django», «PostgreSQL», «Ромашка», «сервис платежей» and «удалённую работу». It has none of: «Надеюсь, у вас всё хорошо», «Давайте разберёмся», «Обладаю навыками», «В рамках проекта», «не просто», «коммуникабельный», «целеустремлённый», «Уверен, что мой опыт», «Буду рад обсудить», long dashes, `**`, lists. It is 3–6 sentences and ends with one concrete question. After the text there is a short list of changes and the check verdict.
FAIL if any listed fact is lost or changed, the message invents a fact that is not in the source (new numbers, results, technologies, team size, reasons for leaving), keeps any listed cliche, replaces cliches with editor formulas like «Без воды» or «Коротко и по делу», or the assistant claims a check passed without running it.
