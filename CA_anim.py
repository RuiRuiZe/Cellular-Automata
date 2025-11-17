import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap
from CA_rules import cell_act, next_state

# 动画更新（同步）
def update(frame_num, img, grid, act_grid, rows, cols, ax):
    new_grid = grid.copy()  # 旧态作为参照
    cell_act(new_grid, act_grid, rows, cols)
    next_state(new_grid, rows, cols)
    img.set_data(new_grid)
    grid[:] = new_grid[:]  # 覆盖到 grid，实现同步更新
    ax.set_title(f"step = {frame_num}", color='white', loc='right')
    return img, ax.title

# 图像显示
cmap = ListedColormap(['green', 'orange', 'black'])

def run_animation(grid, act_grid, rows, cols):
    fig, ax = plt.subplots()
    ax.set_title("step = 0", color='white', loc='right')
    img = ax.imshow(grid, cmap=cmap, vmin=0, vmax=2)
    ax.axis('off')
    fig.set_facecolor('black')

    ani = animation.FuncAnimation(
        fig, update, fargs=(img, grid, act_grid, rows, cols, ax),
        interval=200, blit=False, repeat=True
    )

    plt.show()