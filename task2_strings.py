"""Задание 2. Строковые операции и поиск закономерностей."""

import re
from collections import Counter

VOWELS = set("аеёиоуыэюяaeiou")
QUOTE_REGEX = re.compile(r"«([^»]*)»|\"([^\"]*)\"")


# Разбивает текст на слова, сохраняя исходный регистр
def split_words(text: str) -> list[str]:
    """Извлекает последовательности букв и цифр как отдельные слова."""
    return re.findall(r"[A-Za-zА-Яа-яЁё0-9]+", text)


# Считает слова, начинающиеся с гласной и с согласной буквы
def count_words_by_first_letter(text: str) -> tuple[int, int]:
    """Возвращает количество слов, начинающихся с гласной и с согласной."""
    vowel_count = 0
    consonant_count = 0

    for word in split_words(text):
        first = word[0].lower()
        # Слова, начинающиеся с цифры, не относим ни к гласным, ни к согласным
        if not first.isalpha():
            continue
        if first in VOWELS:
            vowel_count += 1
        else:
            consonant_count += 1

    return vowel_count, consonant_count


# Находит самое частое слово (регистр не учитывается)
def most_frequent_word(text: str) -> tuple[str, int]:
    """Возвращает самое частое слово в нижнем регистре и его частоту."""
    words = [word.lower() for word in split_words(text)]
    if not words:
        return "", 0
    return Counter(words).most_common(1)[0]


# Удаляет повторяющиеся подряд символы: «аааббвв» -> «абв»
def compress_repeats(text: str) -> str:
    """Сжимает каждую серию одинаковых подряд идущих символов до одного."""
    if not text:
        return ""

    result = [text[0]]
    for char in text[1:]:
        if char != result[-1]:
            result.append(char)

    return "".join(result)


# Оставляет только буквы в нижнем регистре (пробелы и знаки не учитываются)
def normalize_letters(text: str) -> Counter[str]:
    """Возвращает счётчик букв строки без учёта регистра."""
    return Counter(char.lower() for char in text if char.isalpha())


# Проверяет, являются ли две строки анаграммами
def is_anagram(first: str, second: str) -> bool:
    """Сравнивает наборы букв двух строк без учёта регистра и пробелов."""
    return normalize_letters(first) == normalize_letters(second)


# Извлекает подстроки, заключённые в «...» или "..."
def extract_quoted(text: str) -> list[str]:
    """Возвращает список содержимого всех кавычек в тексте."""
    result: list[str] = []

    for match in QUOTE_REGEX.finditer(text):
        # Первая группа — для «», вторая — для ""
        value = match.group(1) if match.group(1) is not None else match.group(2)
        result.append(value.strip())

    return result


# Считает «быков» (символ на своём месте) и «коров» (символ есть, но не на месте)
def bulls_and_cows(secret: str, guess: str) -> tuple[int, int]:
    """Возвращает пару (быки, коровы) для строк одинаковой длины."""
    bulls = sum(1 for a, b in zip(secret, guess) if a == b)

    # Общие символы с учётом количества; всё, что не быки, — коровы
    common = Counter(secret) & Counter(guess)
    cows = sum(common.values()) - bulls

    return bulls, cows


def main() -> None:
    print("Введите текст (пустая строка завершает ввод):")
    lines: list[str] = []

    while True:
        try:
            line = input()
        except EOFError:
            break
        if line == "":
            break
        lines.append(line)

    text = "\n".join(lines)
    if not text.strip():
        print("Ошибка: пустой текст.")
        return

    vowel_count, consonant_count = count_words_by_first_letter(text)
    frequent_word, frequent_count = most_frequent_word(text)
    compressed = compress_repeats(text)
    quoted = extract_quoted(text)

    second_string = input("\nВведите вторую строку для проверки анаграммы: ")

    while True:
        secret = input("Введите первую строку для «быков и коров»: ").strip()
        guess = input("Введите вторую строку той же длины: ").strip()
        if len(secret) == len(guess):
            break
        print("Ошибка: строки должны быть одинаковой длины.")

    bulls, cows = bulls_and_cows(secret, guess)

    print("\n" + "=" * 60)
    print("СТРОКОВЫЕ ОПЕРАЦИИ (ВАРИАНТ 2, ЗАД. 2)")
    print("=" * 60)

    print(f"Слов с гласной: {vowel_count} | с согласной: {consonant_count}")

    if frequent_word:
        print(f"Самое частое слово: «{frequent_word}» (частота: {frequent_count})")
    else:
        print("В тексте нет слов.")

    print("Текст после сжатия повторов:")
    print(compressed)

    print(f"Анаграммы: {'да' if is_anagram(text, second_string) else 'нет'}")

    print("Подстроки в кавычках:", quoted if quoted else "нет")

    print(f"Быки и коровы для «{secret}» и «{guess}»: быки={bulls}, коровы={cows}")


if __name__ == "__main__":
    main()
