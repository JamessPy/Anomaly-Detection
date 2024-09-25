import socketio
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Initialize SocketIO client
sio = socketio.Client()

# Create a list to store the last n data points and their labels
data_buffer = []
labels_buffer = []
n = 30  # Store the last 30 data points

# Define the value of k
k = 3  

# Distance threshold for outlier detection
distance_threshold = 0.2  

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

# Function to handle incoming data from WebSocket
@sio.on('data_update')
def handle_data(data):
    try:
        value = data['value']  # Get the data value from the message
        print(f"Received: {value}")
        
        # Add the data point and label
        label = value  # Currently using the data as the label; this can be changed
        add_data_point(value, label)
        
        # Perform outlier detection after receiving n data points
        if len(data_buffer) >= n:
            if is_outlier(value):
                print(f"Outlier Detected: {value} \n")
                outliers.append(value)
                if len(outliers) > n:
                    outliers.pop(0)  # Maintain size of outliers list
                normal_data.append(float('nan'))  # No normal data for outlier
            else:
                print(f"Data is normal: {value} \n")
                normal_data.append(value)
                if len(normal_data) > n:
                    normal_data.pop(0)  # Maintain size of normal_data list
                outliers.append(float('nan'))  # No outlier data for normal data
                if len(outliers) > n:
                    outliers.pop(0)  # Maintain size of outliers list
        
    except Exception as e:
        print(f"Error processing data: {e}")

# Function to update the plot
def update_plot(frame):
    # Show only the last n data points
    normal_plot_data = normal_data[-n:]
    outlier_plot_data = outliers[-n:]
    
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

# Start the SocketIO client and connect to the server
def start_socketio():
    try:
        sio.connect('http://127.0.0.1:5000')  # Update with your WebSocket server URL
    except Exception as e:
        print(f"Connection error: {e}")

# Start the SocketIO connection in a separate thread
import threading
threading.Thread(target=start_socketio).start()

# Start the animation
ani = FuncAnimation(fig, update_plot, interval=1000, cache_frame_data=False, save_count=n)  # Call the update function every 1 second
plt.show()
