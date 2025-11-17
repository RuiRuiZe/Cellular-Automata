# 工具函数

def neighbors(x, y, grid, cell_type):
    rows, cols = grid.shape
    neigh = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                if grid[nx, ny] == cell_type:
                    neigh.append((nx, ny))
    return neigh