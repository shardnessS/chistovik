# Voice

A voice is a short description of how one person writes: sentence length, punctuation, ё, ты or вы, conversational words, typical openers, a few of their own sentences. Chistovik measures it from samples and keeps it in `~/.chistovik/golos/<name>/`: `profile.json` for the script, `card.md` for you, `samples/` with copies of the texts.

## Build

1. Ask for samples: three or more texts the user wrote themselves, of the same genre as the texts they want help with. Telegram messages for messages, cover letters for cover letters. 600 words in total is the minimum for a usable profile.
2. Warn once: texts written or edited by AI would teach the profile the very style Chistovik removes. Ask the user to give only their own writing.
3. If the user pastes texts, save each to its own UTF-8 file in the system temp folder. If they point to files or a folder, use those paths. Only `.txt` and `.md` are read.
4. Run `golos build NAME FILES...`. Use a short Latin name: `me`, `work`, `chat`.
5. Show the card from `golos show NAME`. If the script says the profile is provisional, say so and ask for more samples of the same genre.

Personal texts stay on the user's computer. Do not copy them into the project, into examples or into any public place.

## Compare

`golos compare NAME FILE` gives a score from 0 to 100 and the habits that differ most, for example «длинные тире: у автора 0, в тексте 14 на 1000 слов». Retell the differences in plain words and suggest one or two concrete changes. Under 60 words the numbers are noisy: say so. The score is a rough measure of 22 habits. It does not prove or disprove authorship, and you never present it that way.

## Write in a voice

1. Read the card with `golos show NAME`.
2. Follow the measured habits: sentence length, punctuation, ё, register, conversational words, openers. Use the quoted sentences only as a feel for the rhythm, never copy them into the new text.
3. Do not invent habits the card does not show.
4. Run `scan` and `check` as for any new text. A hard finding fails the draft even if it sounds like the user.
5. Optionally run `golos compare` and adjust the two habits that differ most.
