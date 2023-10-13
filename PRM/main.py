
from PIL import Image
import numpy as np
from RRT import RRT
from PRM import PRM
from PRM_Incremental import PRM_increment
import matplotlib.pyplot as plt
import time

#import pandas as pd
#import seaborn as sns

def load_map(file_path, resolution_scale):
    """Load map from an image and return a 2D binary numpy array
    where 0 represents obstacles and 1 represents free space
    """
    # Load the image with grayscale
    img = Image.open(file_path).convert("L")
    # Rescale the image
    size_x, size_y = img.size
    new_x, new_y = int(size_x * resolution_scale), int(
        size_y * resolution_scale
    )
    img = img.resize((new_x, new_y), Image.ANTIALIAS)

    map_array = np.asarray(img, dtype="uint8")

    # Get bianry image
    threshold = 127
    map_array = 1 * (map_array > threshold)

    # Result 2D numpy array
    return map_array


# if __name__ == "__main__":
#     # Load the map
#     start = (150, 150)
#     goal = (300,150)
#     map_array = load_map("maze.jpg", 0.5)

#     # Planning class
#     PRM_planner = PRM(map_array)
#     RRT_planner = RRT(map_array, start, goal)

#     # # Search with PRM
#     # PRM_planner.sample(n_pts=1000, sampling_method="uniform")
#     # PRM_planner.search(start, goal)
#     # PRM_planner.sample(n_pts=2000, sampling_method="gaussian")
#     # PRM_planner.search(start, goal)
#     # PRM_planner.sample(n_pts=20000, sampling_method="bridge")
#     # PRM_planner.search(start, goal)
#     PRM_planner.sample(n_pts=50, sampling_method="circle")
#     PRM_planner.search(start, goal)
#     #RRT_planner.RRT(n_pts=2000)


if __name__ == "__main__":

    # Load the map
    start = (50, 100)
    goal = (320,300)
    map_array = load_map("map_sample.png", 1.0)

    # Get the size of the map
    map_height, map_width = len(map_array), len(map_array[0])
    # Generate a random goal within the map's bounds
    

    # Initialize counters for success and total runs
    total_runs = 20
    success_rrt = 0
    success_circle = 0
    total_time_rrt = 0
    total_time_circle = 0
    length_rrt = 0
    length_circle = 0

    for _ in range(total_runs):
        # Search with PRM using uniform sampling
        # Planning class
        PRM_planner = PRM(map_array)
        # RRT_planner = RRT(map_array, start, goal)

        # start_time = time.time()
        # RRT_planner.RRT(n_pts=5000)
        # end_time = time.time()
        # total_time_rrt += end_time - start_time

        # if RRT_planner.found:
        #     success_rrt += 1
        #     length_rrt += RRT_planner.goal.cost


        # Search with PRM using Circle sampling
        start_time = time.time()
        PRM_planner.sample(n_pts=50, sampling_method="circle")
        PRM_planner.search(start, goal)
        end_time = time.time()
        total_time_circle += end_time - start_time
        

        if PRM_planner.goal_found:
            success_circle += 1
            length_circle += PRM_planner.path_length 

    # Calculate success rates
    success_rate_rrt= (success_rrt / total_runs) * 100
    success_rate_circle = (success_circle / total_runs) * 100

    # Calculate average time taken
    avg_time_rrt = total_time_rrt / total_runs
    avg_time_circle = total_time_circle / total_runs

    avg_length_rrt = (length_rrt)/total_runs
    avg_length_circle = (length_circle)/total_runs


#     success_rates = [success_rate_rrt, success_rate_circle]
#     avg_times = [avg_time_rrt, avg_time_circle]
#     avg_lengths = [avg_length_rrt, avg_length_circle]

#     # Create a single figure with multiple subplots
#     fig, axes = plt.subplots(1, 3, figsize=(16, 6))

#     # Subplot 1: Success Rates
#     axes[0].bar(['RRT', 'Circle'], success_rates, color=['blue', 'green'])
#     axes[0].set_ylabel('Success Rate (%)')
#     axes[0].set_title('Success Rate of RRT vs. Circle Sampling')

#     # Subplot 2: Average Times
#     axes[1].bar(['RRT', 'Circle'], avg_times, color=['blue', 'green'])
#     axes[1].set_ylabel('Average Time (seconds)')
#     axes[1].set_title('Average Time Taken of RRT vs. Circle Sampling')

#     # Subplot 3: Average Path Lengths
#     axes[2].bar(['RRT', 'Circle'], avg_lengths, color=['blue', 'green'])
#     axes[2].set_ylabel('Average Path Length')
#     axes[2].set_title('Average Path Length of RRT vs. Circle Sampling')

#     plt.tight_layout()
#     plt.savefig('performance_metrics.png')
#     plt.show()

    print("Success rate for RRT: %.2f%%" % success_rate_rrt)
    print("Success rate for Circle sampling: %.2f%%" % success_rate_circle)
    print("Average time taken for RRT: %.2f seconds" % avg_time_rrt)
    print("Average time taken for Circle sampling: %.2f seconds" % avg_time_circle)
    print("Average path length for RRT: %.2f" % avg_length_rrt)
    print("Average path length for Circle sampling: %.2f" % avg_length_circle)



    # Search with RRT
    # RRT_planner.RRT(n_pts=1000)


    # Bonus Part

    # Uncomment the below lines to run the bonus part


    # PRM_bonus = PRM_increment(map_array)
    # node_data = {}
    #
    # def table_create(nodes, path_length, path, case, sampling):
    #     data = {sampling:{
    #         'nodes': nodes,
    #         'path_length': path_length
    #         # 'path' : path
    #     }}
    #     node_data[f'Test case {case+1}'].append(data)
    #
    # for i in range(10):
    #     node_data[f'Test case {i+1}'] = []
    #     nodes, path_length, path = PRM_bonus.search(20000, start, goal, 'uniform')
    #     table_create(nodes, path_length, path, i, 'uniform')
    #     nodes, path_length, path = PRM_bonus.search(20000, start, goal, 'gaussian')
    #     table_create(nodes, path_length, path, i, 'gaussian')
    #     nodes, path_length, path = PRM_bonus.search(20000, start, goal, 'bridge')
    #     table_create(nodes, path_length, path, i, 'bridge')
    #     nodes, path_length, path = PRM_bonus.search(20000, start, goal, 'efficient')
    #     table_create(nodes, path_length, path, i, 'efficient')
    #
    # nodes_data = {}
    # for test_case, methods in node_data.items():
    #     nodes_data[test_case] = {}
    #     for method_data in methods:
    #         method_name, method_info = list(method_data.items())[0]
    #         nodes_data[test_case][method_name] = method_info['nodes']
    #
    # # Create a DataFrame for boxplot
    # df = pd.DataFrame.from_dict(nodes_data)
    # pd.set_option('display.max_rows', 10)  # Set the maximum number of rows to display
    # pd.set_option('display.max_columns', 20)  # Set the maximum number of columns to display
    # print(df)
    #
    # # Create boxplots using seaborn
    # sns.set(style="whitegrid")
    # plt.figure(figsize=(12, 6))
    # sns.boxplot(data=df, palette="Set3")
    # plt.title("Boxplots of Nodes for Each Test Case")
    # plt.xlabel("Test Cases")
    # plt.ylabel("Nodes")
    # plt.xticks(rotation=45)
    # plt.tight_layout()
    #
    # # Show the boxplots
    # plt.show()

