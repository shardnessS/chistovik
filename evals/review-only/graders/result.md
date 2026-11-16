---
type: llm
---

PASS if the assistant ran `chistovik.py scan`, did not return a rewritten version of the whole text, and gave a report in Russian that separates clear problems from judgment calls. The report names at least: «В современном мире», «играет ключевую роль», «Эксперты отмечают» (no source), the self-answered question «Почему это важно? Потому что», «не просто преимущество, это», «Цифры говорят сами за себя», and the closing moral («это напоминает нам», «будущее за»). Each hard finding has a short suggestion. The figure «в 3 раза» is mentioned as a fact that needs a source, not as a cliche.
FAIL if the assistant rewrote the text instead of reporting, missed more than two of the listed spans, or claimed the text was definitely written by AI or by a person.
