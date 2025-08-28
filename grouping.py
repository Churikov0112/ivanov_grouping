import numpy as np

def setup(matrix):
    global M, n
    M = np.array(matrix, dtype=int)
    n = M.shape[0]
    # Симметризация матрицы: берем максимум между M[i,j] и M[j,i]
    M_sym = np.maximum(M, M.T)
    M = M_sym  # Заменяем исходную матрицу симметричной (без принудительной рефлексивности)

def visualize_groups(M):
    groups = []
    visited = [False] * n
    # Начинаем только с рефлексивных элементов
    reflexive_indices = [i for i in range(n) if M[i, i] == 1]
    for i in reflexive_indices:
        if not visited[i]:
            group = []
            stack = [i]
            while stack:
                current = stack.pop()
                if not visited[current] and M[current, current] == 1:  # Только рефлексивные
                    visited[current] = True
                    group.append(current)
                    # Добавляем только прямо связанных рефлексивных соседей
                    for j in reflexive_indices:
                        if M[current, j] == 1 and not visited[j]:
                            stack.append(j)
            if group:  # Исключаем пустые группы
                groups.append(group)
    print("Подгруппы (нумерация с 1):", [f"{[k+1 for k in g]}" for g in groups])

# Пример ассиметричной матрицы для тестирования
if __name__ == "__main__":
    # Пример ассиметричной матрицы с направленными связями
    initial_matrix = [
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Группа 1
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Группа 2
        [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # Группа 3 (малая)
        [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],  # Одинокий человек
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1], # 14й член нерефлексивен
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1]
    ]
    setup(initial_matrix)
    visualize_groups(M)