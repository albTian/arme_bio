import pandas as pd
import matplotlib.pyplot as plt

def visualize_csv_data(csv_file_path):
    # Load CSV data into a pandas DataFrame
    df = pd.read_csv(csv_file_path, header=None)

    # Compute the row-wise mean of the data
    row_means = df.mean(axis=1)

    # # Create a time index for the data
    # time_index = pd.date_range(start='00:00:00', end='00:00:29', freq='1S')

    ax = row_means.plot(style='.', linestyle='-', markersize=5)

    # Add vertical lines every 5 seconds
    for i in range(5, 30, 5):
        ax.axvline(x=row_means.index[i], color='gray', linestyle='--')

    ax.set_xlabel('Time (s)')
    ax.set_ylabel('% EMG contraction')
    ax.set_title('EMG Contraction Over Time')
    plt.show()