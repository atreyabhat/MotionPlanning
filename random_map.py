import random

# Create a random map based on the template, including start and goal
def generate_random_map(rows, cols, obstacle_density):
    # Initialize the map with zeros (free space)
    map_data = [[0] * cols for _ in range(rows)]

    # Set start and goal positions
    start_row, start_col = random.randint(0, rows - 1), random.randint(0, cols - 1)
    goal_row, goal_col = random.randint(0, rows - 1), random.randint(0, cols - 1)

    # Set obstacles based on density
    for row in range(rows):
        for col in range(cols):
            if random.random() < obstacle_density:
                map_data[row][col] = 1  # Set as an obstacle

    # Ensure start and goal positions are not obstacles
    map_data[start_row][start_col] = 0
    map_data[goal_row][goal_col] = 0

    return map_data, (start_row, start_col), (goal_row, goal_col)

