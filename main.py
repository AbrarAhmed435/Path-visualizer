import pygame
from queue import Queue, PriorityQueue

# Constants
WIDTH = 600
ROWS = 20
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("BFS and A* Pathfinding Visualizer")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Node Class
class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = row * WIDTH // ROWS
        self.y = col * WIDTH // ROWS
        self.color = WHITE
        self.neighbors = []

    def get_pos(self):
        return self.row, self.col

    def is_wall(self):
        return self.color == BLACK

    def make_wall(self):
        self.color = BLACK

    def make_start(self):
        self.color = GREEN

    def make_end(self):
        self.color = RED

    def make_visited(self):
        self.color = BLUE

    def make_path(self):
        self.color = YELLOW

    def make_open(self):
        self.color = PURPLE

    def reset(self):
        self.color = WHITE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, WIDTH // ROWS, WIDTH // ROWS))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < ROWS - 1 and not grid[self.row + 1][self.col].is_wall():
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_wall():
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < ROWS - 1 and not grid[self.row][self.col + 1].is_wall():
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_wall():
            self.neighbors.append(grid[self.row][self.col - 1])

# Grid Functions
def make_grid():
    return [[Node(i, j) for j in range(ROWS)] for i in range(ROWS)]

def draw_grid(win, grid):
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)
    for i in range(ROWS):
        pygame.draw.line(win, GREY, (0, i * WIDTH // ROWS), (WIDTH, i * WIDTH // ROWS))
        for j in range(ROWS):
            pygame.draw.line(win, GREY, (j * WIDTH // ROWS, 0), (j * WIDTH // ROWS, WIDTH))
    pygame.display.update()

def get_clicked_pos(pos):
    gap = WIDTH // ROWS
    x, y = pos
    return x // gap, y // gap

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw, start):
    while current in came_from:
        current = came_from[current]
        if current != start:
            current.make_path()
            draw()

def astar(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    f_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score[start] = h(start.get_pos(), end.get_pos())
    open_set_hash = {start}

    while not open_set.empty():
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw, start)
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    if neighbor != end:
                        neighbor.make_open()
        draw()
        if current != start:
            current.make_visited()
    return False

# BFS Algorithm
def bfs(draw, grid, start, end):
    queue = Queue()
    queue.put(start)
    visited = {start}
    came_from = {}

    while not queue.empty():
        current = queue.get()

        if current == end:
            reconstruct_path(came_from, end, draw, start)
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.put(neighbor)
                if neighbor != end:
                    neighbor.make_visited()
                draw()
    return False

# Main Function
def main():
    grid = make_grid()
    start = None
    end = None
    run = True
    algorithm = "bfs"

    while run:
        draw_grid(WIN, grid)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()
                elif not end and node != start:
                    end = node
                    end.make_end()
                elif node != end and node != start:
                    node.make_wall()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    if algorithm == "bfs":
                        bfs(lambda: draw_grid(WIN, grid), grid, start, end)
                    elif algorithm == "astar":
                        astar(lambda: draw_grid(WIN, grid), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid()

                if event.key == pygame.K_1:
                    algorithm = "bfs"
                    print("Switched to BFS")
                if event.key == pygame.K_2:
                    algorithm = "astar"
                    print("Switched to A*")

    pygame.quit()

main()
