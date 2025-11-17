import numpy as np
import random
from CA_anim import run_animation
from CA_rules import ACTIVE, BORN, DEAD, IDLE, ACT1, ACT2

# 状态定义
rows, cols = 100, 100

def initialize_clusters(grid, num_clusters=5, cluster_size=3):
    for _ in range(num_clusters):
        cx = rows // 2 + random.randint(-5, 5)
        cy = cols // 2 + random.randint(-5, 5)

        for dx in range(-cluster_size, cluster_size + 1):
            for dy in range(-cluster_size, cluster_size + 1):
                nx, ny = cx + dx, cy + dy

                if 0 <= nx < rows and 0 <= ny < cols:
                    # 随机转换为 A / B / D
                    grid[nx, ny] = np.random.choice([ACTIVE, BORN, DEAD],
                                                    p=[0.9, 0.05, 0.05]) 
                    # （可调）A：B：D = 6:3:1 的比例

    return grid

grid = np.full((rows, cols), DEAD)
grid = initialize_clusters(grid, num_clusters=5, cluster_size=2)

# 初始化行为网格
act_grid = np.full((rows, cols), IDLE)

# 运行动画
if __name__ == "__main__":
    run_animation(grid, act_grid, rows, cols)