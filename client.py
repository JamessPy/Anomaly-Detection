import requests
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Create a list to store the last n data points and their labels
data_buffer = []
labels_buffer = []
n = 30  # Store the last 30 data points

# Define the value of k
k = 3  # Smaller k value allows for more sensitive control ---5

# Distance threshold for outlier detection
distance_threshold = 0.2  # A small distance threshold can yield more precise results -0.1

# Lists to store normal and outlier data
normal_data = []
outliers = []

# Function to add a new data point
def add_data_point(data, label):
    if len(data_buffer) >= n:
        data_buffer.pop(0)  # Remove the oldest element (FIFO)
        labels_buffer.pop(0)
    
    data_buffer.append(data)
    labels_buffer.append(label)

# Function to calculate Euclidean distance
def euclidean_distance(x1, x2):
    return math.sqrt((x2 - x1) ** 2)

# Function to detect outliers using KNN
def is_outlier(new_data):
    if len(data_buffer) < n:
        return False  # Do not perform outlier check if there isn't enough data
    
    # Calculate distances with all data points
    distances = []
    for i in range(len(data_buffer)):
        distance = euclidean_distance(data_buffer[i], new_data)
        distances.append(distance)
    
    # Sort distances in ascending order
    distances.sort()
    
    # Select the nearest k neighbors
    k_nearest_neighbors = distances[:k]
    
    # Calculate the average distance
    avg_distance = sum(k_nearest_neighbors) / k

    print("Average distance: " + str(avg_distance))
    
    # If the average distance exceeds the threshold, it's an outlier
    return avg_distance > distance_threshold

# Create a Matplotlib figure and axes
fig, ax = plt.subplots()
plt.title('Live Stream Data')
plt.xlabel('Data Index')
plt.ylabel('Value')

# Function to update live data
def update(frame):
    url = 'http://127.0.0.1:5000/stream'
    
    try:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8').strip()
                    
                    # Extract the data from the "data: " prefix
                    if line_str.startswith("data: "):
                        try:
                            # Get the part after "data: "
                            data_str = line_str.split("data: ")[1]
                            data = float(data_str)  # Convert the value to float
                            
                            print(f"Received: {data}")
                            
                            # Add the data point and label
                            label = data  # Currently using the data as the label; this can be changed
                            add_data_point(data, label)
                            
                            # Perform outlier detection after receiving n data points
                            if len(data_buffer) >= n:
                                if is_outlier(data):
                                    print(f"Outlier Detected: {data} \n")
                                    outliers.append(data)
                                    normal_data.append(float('nan'))  # No normal data for outlier
                                else:
                                    print(f"Data is normal: {data} \n")
                                    normal_data.append(data)
                                    outliers.append(float('nan'))  # No outlier data for normal data
                            
                            # Show only the last n data points
                            normal_plot_data = normal_data[-n:]
                            outlier_plot_data = outliers[-n:]
                            
                            # Update the plot
                            ax.clear()
                            ax.scatter(range(len(normal_plot_data)), normal_plot_data, label="Normal Data", color='blue', s=100)
                            ax.scatter(range(len(outlier_plot_data)), outlier_plot_data, label="Outliers", color='red', s=100)
                            
                            # Draw horizontal black lines at y=1 and y=3
                            ax.axhline(y=3, color='black', linestyle='--', label='Y=3')
                            ax.axhline(y=4, color='black', linestyle='--', label='Y=4')

                            ax.legend(loc='upper left')
                            ax.set_title("Live Stream")
                            ax.set_xlabel("Data Index")
                            ax.set_ylabel("Value")
                            
                        except ValueError:
                            print(f"Could not convert data to float: {line_str}")
                        break  # We only process one line of data at a time

    except requests.exceptions.RequestException as req_err:
        print(f"An unexpected error occurred: {req_err}")

# Start the animation
ani = FuncAnimation(fig, update, interval=250)  # Call the update function every 1 second (1000ms)
plt.show()
