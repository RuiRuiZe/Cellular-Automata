import numpy as np
import random
from utils import neighbors

# 状态定义
ACTIVE, BORN, DEAD = 0, 1, 2
IDLE, ACT1, ACT2 = 0, 1, 2

# 马尔可夫矩阵-状态
M_cell_state = np.array([
    [0.55, 0.4, 0.05],  # ACTIVE -> (A, B, D)
    [0.75, 0.2, 0.05],  # BORN   -> (A, B, D)
    [0.0,  0.0,  1.0]   # DEAD   -> (A, B, D)
])

# 马尔可夫矩阵-行为
M_cell_act = np.array([
    [[0.8, 0.1, 0.1],  # IDLE
     [0.5, 0.3, 0.2],  # ACT1
     [0.6, 0.1, 0.3]], # ACT2

    [[0.8, 0.1, 0.1],  # IDLE
     [0.5, 0.3, 0.2],  # ACT1
     [0.6, 0.1, 0.3]], # ACT2

    [[1, 0, 0],        # IDLE
     [1, 0, 0],        # ACT1
     [1, 0, 0]],       # ACT2
])

def cell_act(stats_grid, act_grid, rows, cols):
    actions = []  # 缓冲所有行动（同步）
    for i in range(rows):
        for j in range(cols):
            cur_state = stats_grid[i, j]
            cur_act = act_grid[i, j]

            # ---------- 行动状态转移 ----------
            prob = M_cell_act[cur_state, cur_act].copy()
            next_act = np.random.choice([IDLE, ACT1, ACT2], p=prob)
            act_grid[i, j] = next_act
            born_neigh = neighbors(i, j, stats_grid, BORN)
            dead_neigh = neighbors(i, j, stats_grid, DEAD)

            # ---------- 根据行动执行行为 ----------
            if cur_state == ACTIVE:
                if next_act == ACT1:
                    # 杀死邻居 BORN
                    born_cells = [(nx, ny) for nx, ny in born_neigh if stats_grid[nx, ny] == BORN]
                    if born_cells:
                        nx, ny = random.choice(born_cells)
                        actions.append((nx, ny, DEAD))
                elif next_act == ACT2:
                    # DEAD -> ACTIVE
                    dead_cells = [(nx, ny) for nx, ny in dead_neigh if stats_grid[nx, ny] == DEAD]
                    if dead_cells:
                        nx, ny = random.choice(dead_cells)
                        actions.append((nx, ny, ACTIVE))

            elif cur_state == BORN:
                if next_act == ACT1:
                    # BORN 特定行为，比如感染 DEAD -> ACTIVE
                    dead_cells = [(nx, ny) for nx, ny in dead_neigh if stats_grid[nx, ny] == DEAD]
                    if dead_cells:
                        nx, ny = random.choice(dead_cells)
                        actions.append((nx, ny, ACTIVE))
                elif next_act == ACT2:
                    # BORN 另一种行为，比如强化自己 BORN -> ACTIVE
                    active_cells = [(nx, ny) for nx, ny in born_neigh if stats_grid[nx, ny] == ACTIVE]
                    if active_cells:
                        nx, ny = random.choice(active_cells)
                        actions.append((nx, ny, BORN))

            elif cur_state == DEAD:
                # DEAD 的行为也可以定义
                if next_act == ACT2:
                    dead_cells = [(nx, ny) for nx, ny in dead_neigh if stats_grid[nx, ny] == DEAD]
                    if dead_cells:
                        nx, ny = random.choice(dead_cells)
                        actions.append((nx, ny, BORN))

    # 执行同步行动
    for x, y, new_state in actions:
        stats_grid[x, y] = new_state

def next_state(stats_grid, rows, cols):
    for i in range(rows):
        for j in range(cols):
            cur = stats_grid[i, j]
            prob = M_cell_state[cur].copy()
            new_state = np.random.choice([ACTIVE, BORN, DEAD], p=prob)   
            stats_grid[i, j] = new_state
    return stats_grid