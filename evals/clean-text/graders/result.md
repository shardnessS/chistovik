---
type: llm
---

PASS if the assistant ran `chistovik.py scan`, found no hard findings, and said in Russian that there is nothing to fix, returning the text unchanged or not returning a new version at all. Any optional remark is limited to one or two lines.
FAIL if the assistant rewrote or "improved" the text, changed «3 ночи», «80%», «Postgres» or «debug», added new sentences, or invented problems to justify an edit.
