"""Задание 3. Матричные операции и анализ."""

import math
import random


# Читает целое число с проверкой диапазона
def read_int(prompt: str, min_val: int, max_val: int) -> int:
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
        if value < min_val or value > max_val:
            print(f"Ошибка: число должно быть в диапазоне [{min_val}; {max_val}].")
            continue
        return value


# Создаёт матрицу нужного размера выбранным способом
def generate_matrix(rows: int, cols: int, mode: int, seed: int = 42) -> list[list[int]]:
    """mode=1 — числа 1..R*C по строкам; mode=2 — случайные числа 1..50."""
    if mode == 1:
        return [[i * cols + j + 1 for j in range(cols)] for i in range(rows)]

    # Фиксированный seed делает случайное заполнение воспроизводимым
    rng = random.Random(seed)
    return [[rng.randint(1, 50) for _ in range(cols)] for _ in range(rows)]


# Печатает матрицу в виде выровненной таблицы
def print_matrix(matrix: list[list[int]], title: str) -> None:
    """Выводит матрицу с заголовком и одинаковой шириной столбцов."""
    print(f"\n--- {title} ---")

    if not matrix:
        print("Матрица пуста.")
        return

    width = max(len(str(value)) for row in matrix for value in row)
    width = max(width, 2)

    for row in matrix:
        print(" ".join(f"{value:>{width}}" for value in row))


# Считает суммы всех строк
def row_sums(matrix: list[list[int]]) -> list[int]:
    """Возвращает список сумм элементов каждой строки."""
    return [sum(row) for row in matrix]


# Считает произведения всех строк
def row_products(matrix: list[list[int]]) -> list[int]:
    """Возвращает список произведений элементов каждой строки."""
    return [math.prod(row) for row in matrix]


# Считает суммы всех столбцов
def column_sums(matrix: list[list[int]]) -> list[int]:
    """Возвращает список сумм элементов каждого столбца."""
    cols = len(matrix[0])
    return [sum(matrix[i][j] for i in range(len(matrix))) for j in range(cols)]


# Считает произведения всех столбцов
def column_products(matrix: list[list[int]]) -> list[int]:
    """Возвращает список произведений элементов каждого столбца."""
    cols = len(matrix[0])
    return [math.prod(matrix[i][j] for i in range(len(matrix))) for j in range(cols)]


# Меняет местами первую и последнюю строки
def swap_first_last_rows(matrix: list[list[int]]) -> list[list[int]]:
    """Возвращает копию матрицы с переставленными первой и последней строками."""
    result = [row[:] for row in matrix]
    result[0], result[-1] = result[-1], result[0]
    return result


# Меняет местами первый и последний столбцы
def swap_first_last_columns(matrix: list[list[int]]) -> list[list[int]]:
    """Возвращает копию матрицы с переставленными первым и последним столбцами."""
    result = [row[:] for row in matrix]
    for row in result:
        row[0], row[-1] = row[-1], row[0]
    return result


# Создаёт транспонированную матрицу
def transpose_matrix(matrix: list[list[int]]) -> list[list[int]]:
    """Строки исходной матрицы становятся столбцами новой."""
    return [list(column) for column in zip(*matrix)]


# Ищет седловые точки: минимум в строке и максимум в столбце или наоборот
def find_saddle_points(matrix: list[list[int]]) -> list[tuple[int, int, int, str]]:
    """Возвращает список (строка, столбец, значение, тип) для седловых точек."""
    rows = len(matrix)
    cols = len(matrix[0])

    row_min = [min(row) for row in matrix]
    row_max = [max(row) for row in matrix]
    col_min = [min(matrix[i][j] for i in range(rows)) for j in range(cols)]
    col_max = [max(matrix[i][j] for i in range(rows)) for j in range(cols)]

    result: list[tuple[int, int, int, str]] = []

    for i in range(rows):
        for j in range(cols):
            value = matrix[i][j]
            if value == row_min[i] and value == col_max[j]:
                result.append((i, j, value, "минимум в строке, максимум в столбце"))
            elif value == row_max[i] and value == col_min[j]:
                result.append((i, j, value, "максимум в строке, минимум в столбце"))

    return result


def main() -> None:
    rows = read_int("Введите количество строк R (2 <= R <= 12): ", 2, 12)
    cols = read_int("Введите количество столбцов C (2 <= C <= 12): ", 2, 12)

    print("Выберите способ заполнения:")
    print("  1 — последовательные числа от 1 по строкам")
    print("  2 — случайные числа от 1 до 50")
    mode = read_int("Ваш выбор (1 или 2): ", 1, 2)

    matrix = generate_matrix(rows, cols, mode)
    is_square = rows == cols

    print("\n" + "=" * 60)
    print("МАТРИЧНЫЕ ОПЕРАЦИИ (ВАРИАНТ 2, ЗАД. 3)")
    print("=" * 60)
    print_matrix(matrix, "Исходная матрица")

    sums_rows = row_sums(matrix)
    products_rows = row_products(matrix)
    sums_cols = column_sums(matrix)
    products_cols = column_products(matrix)

    print("\n--- Суммы и произведения строк ---")
    for i, (total, product) in enumerate(zip(sums_rows, products_rows), start=1):
        print(f"Строка {i}: сумма = {total}, произведение = {product}")

    print("\n--- Суммы и произведения столбцов ---")
    for j, (total, product) in enumerate(zip(sums_cols, products_cols), start=1):
        print(f"Столбец {j}: сумма = {total}, произведение = {product}")

    # Индексы строки и столбца с максимальной суммой (max хранит первый максимум)
    best_row = max(range(rows), key=lambda i: sums_rows[i])
    best_col = max(range(cols), key=lambda j: sums_cols[j])
    print(f"\nСтрока с максимальной суммой: {best_row + 1} (сумма = {sums_rows[best_row]})")
    print(f"Столбец с максимальной суммой: {best_col + 1} (сумма = {sums_cols[best_col]})")

    swapped = swap_first_last_rows(matrix)
    swapped = swap_first_last_columns(swapped)
    print_matrix(swapped, "После перестановки первой/последней строки и столбца")

    transposed = transpose_matrix(matrix)
    print_matrix(transposed, "Транспонированная матрица")

    if is_square:
        equal = transposed == matrix
        print(f"Транспонированная матрица равна исходной: {'да' if equal else 'нет'}")
    else:
        print("Матрица не квадратная: проверка равенства транспонированной матрицы пропущена.")

    saddles = find_saddle_points(matrix)
    print("\n--- Седловые точки ---")
    if saddles:
        # Позиции выводим с 1, как принято для строк и столбцов
        for i, j, value, kind in saddles:
            print(f"({i + 1}, {j + 1}) = {value} — {kind}")
    else:
        print("Седловых точек нет.")

    unique_values = sorted({value for row in matrix for value in row})
    print("\nУникальные элементы по возрастанию:", unique_values)

    if is_square:
        trace = sum(matrix[i][i] for i in range(rows))
        print(f"След матрицы (сумма главной диагонали): {trace}")
    else:
        print("След матрицы не определён: матрица не квадратная.")


if __name__ == "__main__":
    main()
