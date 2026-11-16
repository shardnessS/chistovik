---
type: llm
---

PASS if the assistant saved the three messages as separate UTF-8 files outside the user's project, ran `chistovik.py golos build chat` with them, and showed the card in Russian. The answer says the profile is provisional because there are few words, and asks for more messages of the same kind. The card mentions lowercase sentence starts, no letter ё, no long dashes and smileys from brackets.
FAIL if the assistant described the style from its own impression without running the script, saved the samples into the user's project, or claimed the profile is reliable.
