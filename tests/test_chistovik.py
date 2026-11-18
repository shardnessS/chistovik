"""Тесты Чистовика: python -m unittest discover -s tests -v"""

import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "chistovik"
FIXTURES = ROOT / "tests" / "fixtures"
sys.path.insert(0, str(SKILL / "scripts"))

import chistovik as c  # noqa: E402


def ids(text, genre="article"):
    return {f["id"] for f in c.scan(text, genre)["findings"]}


def cats(text, genre="article"):
    return {f["category"] for f in c.scan(text, genre)["findings"]}


class EveryRuleCatchesItsExample(unittest.TestCase):
    def test_every_phrase_pattern_matches_its_example(self):
        for p in c.PHRASES:
            with self.subTest(rule=p["id"]):
                masked = c.mask_quotes(c.mask_code(c.norm(p["example"])))
                self.assertTrue(p["re"].search(masked), f"{p['id']} не ловит свой пример: {p['example']}")

    def test_every_phrase_example_survives_the_pipeline(self):
        for p in c.PHRASES:
            genre = next(g for g in ("chat", "article", "cv", "post", "docs") if c.severity(p, g) != "off")
            with self.subTest(rule=p["id"], genre=genre):
                found = {f["id"] for f in c.scan(p["example"], genre)["findings"]}
                self.assertIn(p["id"], found)

    def test_ids_are_unique_and_categories_known(self):
        all_ids = [p["id"] for p in c.PHRASES] + [s[0] for s in c.STRUCTURE_CHECKS]
        self.assertEqual(len(all_ids), len(set(all_ids)))
        for p in c.PHRASES:
            self.assertIn(p["cat"], c.CATEGORIES)
        for s in c.STRUCTURE_CHECKS:
            self.assertIn(s[1], c.CATEGORIES)

    def test_every_category_has_a_protection_example(self):
        rows = json.loads((FIXTURES / "ne_trogaet.json").read_text(encoding="utf-8"))
        covered = {r["cat"] for r in rows}
        used = {p["cat"] for p in c.PHRASES} | {s[1] for s in c.STRUCTURE_CHECKS}
        self.assertEqual(used - covered, set(), "у категории нет примера «не трогает»")


class LeavesNormalTextAlone(unittest.TestCase):
    def test_protection_examples(self):
        rows = json.loads((FIXTURES / "ne_trogaet.json").read_text(encoding="utf-8"))
        for row in rows:
            with self.subTest(text=row["text"][:50], genre=row["genre"]):
                found = [f for f in c.scan(row["text"], row["genre"])["findings"] if f["category"] == row["cat"]]
                self.assertEqual(found, [], f"лишняя находка: {found}")

    def test_quoted_examples_are_not_flagged(self):
        text = "Не пишите в отклике «буду рад обсудить возможности» и «обладаю навыками»."
        self.assertNotIn("rad_obsudit", ids(text, "chat"))
        self.assertIn("rad_obsudit", {f["id"] for f in c.scan(text, "chat", include_quoted=True)["findings"]})

    def test_code_is_not_flagged(self):
        text = "Пример:\n\n```\nДавайте разберёмся, это не просто код, а данные.\n```\n\nКонец примера."
        self.assertEqual(ids(text, "docs") & {"davayte", "ne_prosto"}, set())

    def test_clean_message_has_no_hard_findings(self):
        text = ("Здравствуйте, Анна. Я Java-разработчик, пишу на Java 6 лет. Увидел вакансию бэкенд-разработчика "
                "и откликаюсь, резюме прикладываю. Когда вам удобно созвониться на этой неделе?")
        self.assertEqual(c.scan(text, "chat")["hard"], 0)

    def test_yo_is_matched_like_e(self):
        self.assertIn("davayte", ids("Давайте разберёмся с этим.", "article"))
        self.assertIn("davayte", ids("Давайте разберемся с этим.", "article"))


class StructureChecks(unittest.TestCase):
    def test_usiliteli_only_when_many(self):
        self.assertIn("usiliteli", ids("Это действительно невероятно важная и крайне полезная функция."))
        self.assertNotIn("usiliteli", ids("Это действительно так."))

    def test_yavlyaetsya(self):
        text = "Сервис является платформой. Платформа является облачной. Облако является частным."
        self.assertIn("yavlyaetsya", ids(text))
        self.assertNotIn("yavlyaetsya", ids(text, "official"))

    def test_ne_tolko_twice(self):
        text = "Он не только пишет код, но и тестирует. Он не только тестирует, но и деплоит."
        self.assertIn("ne_tolko", ids(text))

    def test_connective_paragraphs(self):
        text = ("Кроме того, сервис быстрый.\n\nБолее того, он дешёвый.\n\nОднако есть минусы.\n\n"
                "Таким образом, выбор за вами.")
        self.assertIn("svyazki_abzacev", ids(text))

    def test_same_paragraph_openers(self):
        text = "Я разработал сервис.\n\nЯ внедрил Kafka.\n\nЯ настроил мониторинг.\n\nЯ обучил команду."
        found = [f for f in c.scan(text)["findings"] if f["id"] == "odinakovye_nachala"]
        self.assertTrue(found)
        self.assertEqual(found[0]["severity"], "hard")

    def test_flat_rhythm(self):
        text = " ".join(["Мы запустили новый сервис для курьеров в трёх городах страны."] * 3 +
                        ["Команда собрала обратную связь от водителей за первую неделю работы."] * 3)
        self.assertIn("rovny_ritm", ids(text))

    def test_long_sentences(self):
        sentence = ("Мы решили перенести всю обработку заказов из старого монолита в отдельный сервис, который "
                    "работает с очередью сообщений и пишет результаты в отдельную базу данных для аналитики. ")
        self.assertIn("dlinnye_predlozheniya", ids(sentence * 2))

    def test_long_chat_message(self):
        text = " ".join(f"Это предложение номер {i} в длинном сообщении." for i in range(8))
        self.assertIn("dlinny_chat", ids(text, "chat"))
        self.assertNotIn("dlinny_chat", ids(text, "article"))

    def test_staccato_paragraphs(self):
        text = "Мы начали.\n\nМы ошиблись.\n\nМы выросли."
        self.assertIn("rublenye_abzacy", ids(text))
        self.assertNotIn("rublenye_abzacy", ids(text, "post"))

    def test_staccato_phrases(self):
        self.assertIn("rublenye_frazy", ids("Быстро. Просто. Надёжно. Попробуйте сервис сегодня."))

    def test_triads(self):
        text = "Быстрый, удобный и надёжный сервис. Гибкость, надёжность и масштабируемость решения."
        self.assertIn("troyki", ids(text))

    def test_moral_last_paragraph(self):
        text = "Мы перевели сборку на Gradle.\n\nТаким образом, автоматизация помогает бизнесу."
        self.assertIn("moral_v_kontse", ids(text))

    def test_editor_fragments(self):
        self.assertIn("ne_fragment", ids("Проблема в людях. Не инструмент. Команда."))
        self.assertIn("bez_bez", ids("Сервис работает сразу. Без регистрации. Без смс."))


class Punctuation(unittest.TestCase):
    def test_dash_in_chat_is_hard(self):
        found = [f for f in c.scan("Я — Java-разработчик.", "chat")["findings"] if f["id"] == "tire"]
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0]["severity"], "hard")

    def test_dash_density_in_article(self):
        text = "Мы запустили сервис — и всё изменилось — клиенты пошли — продажи выросли."
        self.assertIn("tire", ids(text))
        self.assertNotIn("tire", ids(text, "docs"))

    def test_hyphen_with_spaces_counts_as_dash(self):
        self.assertIn("tire", ids("Я - Java-разработчик.", "chat"))

    def test_guillemets_only_in_chat(self):
        self.assertIn("elochki_v_chate", ids("Работал в «Ромашке» три года.", "chat"))
        self.assertNotIn("elochki_v_chate", ids("Работал в «Ромашке» три года.", "article"))

    def test_english_quotes(self):
        self.assertIn("angliyskie_kavychki", ids("Компания “Ромашка” открыла офис."))

    def test_exclamations(self):
        self.assertIn("vosklitsaniya", ids("Отличные новости! Мы запустились!", "chat"))
        self.assertNotIn("vosklitsaniya", ids("Отличные новости! Мы запустились!", "post"))


class Formatting(unittest.TestCase):
    def test_bold_and_lists_in_chat(self):
        text = "Добрый день.\n\n- опыт 6 лет\n- Java, Spring\n\n**Опыт:** 6 лет"
        found = ids(text, "chat")
        self.assertIn("spisok_v_chate", found)
        self.assertIn("zhirny", found)

    def test_resume_bold_is_fine(self):
        text = "**Java-разработчик**\n\n**Java и Spring:** Spring Boot\n**Данные:** PostgreSQL\n**Тесты:** JUnit"
        self.assertEqual(cats(text, "cv") & {"oformlenie", "ritm"}, set())

    def test_bold_labels(self):
        text = "**Скорость:** быстро\n**Надёжность:** высокая\n**Цена:** низкая"
        self.assertIn("zhirnye_podpisi", ids(text, "article"))
        self.assertNotIn("zhirnye_podpisi", ids(text, "docs"))

    def test_emoji_heading(self):
        self.assertIn("emodzi", ids("## 🚀 Быстрый старт\n\nСтавим пакет.", "docs"))

    def test_title_case_heading(self):
        self.assertIn("zaglavnye", ids("## Как Устроен Наш Сервис\n\nТекст раздела.", "docs"))
        self.assertNotIn("zaglavnye", ids("## Как устроен сервис\n\nТекст раздела.", "docs"))


class Facts(unittest.TestCase):
    def verdict(self, before, after, genre="article", new=False):
        return c.check(before, after, genre, new)

    def test_identical_text_passes(self):
        text = "Сервис обрабатывает 1200 заказов в день. Команда из 5 человек."
        self.assertEqual(self.verdict(text, text)["verdict"], "pass")

    def test_lost_number(self):
        r = self.verdict("Активация выросла с 31% до 44% за шесть недель.", "Активация выросла до 44%.")
        self.assertEqual(r["verdict"], "fail")
        self.assertTrue(any("31%" in e for e in r["errors"]))
        self.assertTrue(any("шесть недель" in e for e in r["errors"]))

    def test_invented_number(self):
        r = self.verdict("Активация выросла.", "Активация выросла на 13%.")
        self.assertTrue(any("Появилось число" in e for e in r["errors"]))

    def test_magnitude_change(self):
        r = self.verdict("Выручка 47 млн рублей.", "Выручка 47 млрд рублей.")
        self.assertTrue(any("Число изменилось" in e for e in r["errors"]))

    def test_approximation_dropped(self):
        r = self.verdict("Конверсия около 60%.", "Конверсия 60%.")
        self.assertTrue(any("Число изменилось" in e for e in r["errors"]))

    def test_unit_changed(self):
        r = self.verdict("До склада 150 км.", "До склада 150 миль.")
        self.assertEqual(r["verdict"], "fail")

    def test_equivalent_forms_pass(self):
        r = self.verdict("Опыт пять лет, зарплата от 175 000 ₽.", "Опыт 5 лет, зарплата от 175 тыс. ₽.")
        self.assertEqual(r["errors"], [])

    def test_name_inflection_is_fine(self):
        r = self.verdict("Я работаю в Яндексе и пишу на Kotlin.", "Пишу на Kotlin, работаю в компании Яндекс.")
        self.assertEqual(r["errors"], [])

    def test_lost_name_and_term(self):
        r = self.verdict("Сделал интеграцию с Kafka для Сбера.", "Сделал интеграцию.")
        joined = " ".join(r["errors"])
        self.assertIn("Kafka", joined)
        self.assertIn("Сбера", joined)

    def test_negation_and_scope_warnings(self):
        r = self.verdict("Пароль нельзя хранить в коде. Доступ только у админов.",
                         "Пароль храните в коде. Доступ у админов.")
        joined = " ".join(r["warnings"])
        self.assertIn("Отрицаний", joined)
        self.assertIn("только", joined)

    def test_new_slop_in_revision_fails(self):
        r = self.verdict("Сервис ускоряет сборку на 20%.", "Сервис ускоряет сборку на 20%. Без воды. Только суть.")
        self.assertEqual(r["verdict"], "fail")

    def test_new_mode_only_checks_invented(self):
        brief = "Python 4 года, в «Ромашке» с марта 2025, ищу удалёнку, от 200 000 на руки."
        draft = "Здравствуйте. Я Python-разработчик, 4 года опыта, ищу удалённую работу."
        self.assertEqual(self.verdict(brief, draft, "chat", new=True)["errors"], [])
        bad = draft + " Руководил командой из 12 человек."
        self.assertTrue(self.verdict(brief, bad, "chat", new=True)["errors"])

    def test_new_mode_does_not_pair_different_units(self):
        brief = "На дорогу уходит 6 часов. Работаю с ноября 2020."
        r = self.verdict(brief, "Шесть лет пишу бэкенд.", "chat", new=True)
        self.assertFalse(any("Число изменилось" in e for e in r["errors"]))
        self.assertTrue(any("Появилось число" in e and "Шесть лет" in e for e in r["errors"]))

    def test_new_mode_still_pairs_same_unit(self):
        r = self.verdict("Опыт около 6 лет.", "Опыт 6 лет.", "chat", new=True)
        self.assertTrue(any("Число изменилось" in e for e in r["errors"]))


class Voice(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        os.environ["CHISTOVIK_HOME"] = self.tmp.name
        self.samples = Path(self.tmp.name) / "in"
        self.samples.mkdir()
        texts = [
            "привет, глянул твой пр. норм, но в сервисе заказов есть гонка, поправь плиз) я бы вынес ретраи в отдельный класс",
            "короче, база опять легла ночью. я поднял, но причину пока не нашел. завтра посмотрю логи, напишу",
            "кстати, по кафке: сделал отдельный топик под уведомления. вроде работает, но надо прогнать нагрузку)",
            "смотри, тут два варианта. можно оставить как есть, можно переписать на корутины. я за первый, быстрее",
        ]
        for i, t in enumerate(texts):
            (self.samples / f"s{i}.txt").write_text(t, encoding="utf-8")

    def tearDown(self):
        os.environ.pop("CHISTOVIK_HOME", None)
        self.tmp.cleanup()

    def test_build_and_compare(self):
        profile = c.build_voice("ya", [str(self.samples)])
        self.assertEqual(profile["samples"], 4)
        card = (Path(self.tmp.name) / "golos" / "ya" / "card.md").read_text(encoding="utf-8")
        self.assertIn("ё не пишет", card)
        self.assertIn("маленькой буквы", card)
        own = c.compare_voice(profile, "глянул логи. база легла из-за пула, поправил конфиг, вроде норм)")
        alien = c.compare_voice(profile, "Уважаемые коллеги! В рамках проекта — и это важно — мы осуществили "
                                         "миграцию. Подводя итог, отмечу: всё прошло успешно!")
        self.assertGreater(own["score"], alien["score"])
        self.assertTrue(alien["differences"])

    def test_cli_list_and_show(self):
        c.build_voice("ya", [str(self.samples)])
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            c.main(["golos", "list"])
        self.assertIn("ya", out.getvalue())


class CatalogAndCli(unittest.TestCase):
    def test_catalog_file_is_up_to_date(self):
        path = SKILL / "references" / "shtampy.md"
        self.assertEqual(path.read_text(encoding="utf-8"), c.catalog_markdown(),
                         "перегенерируй: python skills/chistovik/scripts/chistovik.py catalog > "
                         "skills/chistovik/references/shtampy.md")

    def test_genre_aliases(self):
        self.assertEqual(c.resolve_genre("hr"), "chat")
        self.assertEqual(c.resolve_genre("Резюме"), "cv")
        self.assertEqual(c.resolve_genre(None), "article")

    def test_check_exit_code(self):
        with tempfile.TemporaryDirectory() as tmp:
            a, b = Path(tmp) / "a.txt", Path(tmp) / "b.txt"
            a.write_text("Выручка 47 млн рублей.", encoding="utf-8")
            b.write_text("Выручка 47 млрд рублей.", encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(c.main(["check", str(a), str(b)]), 1)
                self.assertEqual(c.main(["check", str(a), str(a)]), 0)

    def test_cp1251_file_is_read(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "win.txt"
            p.write_bytes("Давайте разберёмся.".encode("cp1251"))
            self.assertIn("davayte", {f["id"] for f in c.scan(c.read_text(str(p)))["findings"]})


if __name__ == "__main__":
    unittest.main()
