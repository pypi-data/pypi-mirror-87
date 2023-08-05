"""
数据生成的主要逻辑
"""

import numpy as np


def generate_matrix(
        board_grid: int, unit_grid: int, unit_n: int, positions: list
) -> np.ndarray:
    """生成指定布局矩阵

    Args:
        board_grid (int): 布局板分辨率，代表矩形区域的边长像素数
        unit_grid (int): 矩形组件分辨率
        unit_n (int): 组件数
        positions (list): 每个元素代表每个组件的位置
    Returns:
        np.ndarray: 布局矩阵
    """
    matrix = np.zeros([board_grid, board_grid], dtype=int)
    for i in range(unit_n):
        pos = positions[i] - 1
        num = board_grid / unit_grid
        pos_column = int((pos % num) * unit_grid)
        pos_row = int((pos // num) * unit_grid)
        pos_row_end = pos_row + unit_grid
        pos_column_end = pos_column + unit_grid
        matrix[pos_row:pos_row_end, pos_column:pos_column_end] = 1
    print(matrix)
    return matrix
