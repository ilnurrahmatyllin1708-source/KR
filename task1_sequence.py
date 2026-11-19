"""Задание 1. Обработка числовой последовательности с условиями."""

import math


# Ищет пики (строго больше соседей) и впадины (строго меньше соседей)
def find_peaks_and_pits(nums: list[int]) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
    """Возвращает списки пиков и впадин в виде пар (индекс, значение)."""
    peaks: list[tuple[int, int]] = []
    pits: list[tuple[int, int]] = []

    # У крайних элементов нет двух соседей, поэтому идём от 1 до len(nums) - 2
    for i in range(1, len(nums) - 1):
        if nums[i] > nums[i - 1] and nums[i] > nums[i + 1]:
            peaks.append((i, nums[i]))
        elif nums[i] < nums[i - 1] and nums[i] < nums[i + 1]:
            pits.append((i, nums[i]))

    return peaks, pits


# Сумма элементов на чётных позициях (позиции считаются с 1)
def sum_even_positions(nums: list[int]) -> int:
    """Складывает элементы с позициями 2, 4, 6, ... (индексы 1, 3, 5, ...)."""
    return sum(nums[i] for i in range(1, len(nums), 2))


# Произведение элементов на нечётных позициях (позиции считаются с 1)
def product_odd_positions(nums: list[int]) -> int:
    """Перемножает элементы с позициями 1, 3, 5, ... (индексы 0, 2, 4, ...)."""
    return math.prod(nums[0::2])


# Проверяет, есть ли подряд идущая арифметическая прогрессия длины >= 3
def has_arithmetic_progression(nums: list[int], min_len: int = 3) -> bool:
    """Ищет хотя бы три подряд элемента с одинаковой разностью."""
    # Для коротких последовательностей прогрессии быть не может
    if len(nums) < min_len:
        return False

    diff = nums[1] - nums[0]
    run_len = 2

    for i in range(2, len(nums)):
        current_diff = nums[i] - nums[i - 1]
        if current_diff == diff:
            run_len += 1
        else:
            diff = current_diff
            run_len = 2

        if run_len >= min_len:
            return True

    return False


# Строит новый список: элемент + его соседи (у краёв — только один сосед)
def build_neighbor_sums(nums: list[int]) -> list[int]:
    """Заменяет каждый элемент суммой самого элемента и соседних элементов."""
    result: list[int] = []
    n = len(nums)

    for i in range(n):
        total = nums[i]
        if i > 0:
            total += nums[i - 1]
        if i + 1 < n:
            total += nums[i + 1]
        result.append(total)

    return result


# Вычисляет медиану последовательности
def calculate_median(nums: list[int]) -> float:
    """Возвращает средний элемент или среднее двух центральных элементов."""
    ordered = sorted(nums)
    n = len(ordered)
    middle = n // 2

    if n % 2 == 1:
        return float(ordered[middle])

    return (ordered[middle - 1] + ordered[middle]) / 2.0


# Считает элементы, отклоняющиеся от медианы больше чем на 10
def count_far_from_median(nums: list[int], median_value: float, threshold: float = 10.0) -> int:
    """Считает элементы, для которых |x - медиана| > threshold."""
    return sum(1 for value in nums if abs(value - median_value) > threshold)


# Читает целое число с проверкой диапазона
def read_int(prompt: str, min_val: int | None = None, max_val: int | None = None) -> int:
    while True:
        raw = input(prompt).strip()
        if not raw:
            print("Ошибка: пустой ввод.")
            continue
        try:
            value = int(raw)
        except ValueError:
            print("Ошибка: введите целое число.")
            continue
        if min_val is not None and value < min_val:
            print(f"Ошибка: значение должно быть >= {min_val}.")
            continue
        if max_val is not None and value > max_val:
            print(f"Ошибка: значение должно быть <= {max_val}.")
            continue
        return value


def main() -> None:
    n = read_int("Введите N (4 <= N <= 600): ", min_val=4, max_val=600)

    print(f"Введите {n} целых чисел (можно в несколько строк):")
    nums: list[int] = []
    while len(nums) < n:
        try:
            line = input().strip()
        except EOFError:
            break
        if not line:
            continue
        for token in line.split():
            if len(nums) >= n:
                break
            try:
                nums.append(int(token))
            except ValueError:
                print(f"Пропущено: '{token}' не является целым числом.")

    if len(nums) < n:
        print(f"Ошибка: введено только {len(nums)} из {n} чисел.")
        return

    peaks, pits = find_peaks_and_pits(nums)
    even_sum = sum_even_positions(nums)
    odd_product = product_odd_positions(nums)
    has_progression = has_arithmetic_progression(nums)
    neighbor_sums = build_neighbor_sums(nums)
    median_value = calculate_median(nums)
    deviations = count_far_from_median(nums, median_value)

    print("\n" + "=" * 60)
    print("ОБРАБОТКА ЧИСЛОВОЙ ПОСЛЕДОВАТЕЛЬНОСТИ (ВАРИАНТ 2, ЗАД. 1)")
    print("=" * 60)

    # Пики и впадины выводим с позициями, начиная с 1
    print("Пики (позиция, значение):", [(i + 1, v) for i, v in peaks] if peaks else "нет")
    print("Впадины (позиция, значение):", [(i + 1, v) for i, v in pits] if pits else "нет")

    print(f"Сумма элементов на чётных позициях: {even_sum}")
    print(f"Произведение элементов на нечётных позициях: {odd_product}")

    print(f"Арифметическая прогрессия длины >= 3: {'есть' if has_progression else 'нет'}")

    print(f"Новый список (элемент + соседи): {neighbor_sums}")
    print(f"Медиана исходной последовательности: {median_value:.2f}")
    print(f"Элементов, отклоняющихся от медианы более чем на 10: {deviations}")


if __name__ == "__main__":
    main()
