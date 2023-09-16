from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from datetime import datetime, timedelta
import matplotlib.pyplot as plt



# Custom Chart class representing Channels vs Time watched...
class CustomChart():
    def __init__(self):
        self.figure = plt.figure(figsize=(6, 4))
        self.canvas = FigureCanvas(self.figure)
        
    
    def plot_custom_chart(self, groups, earliest_start_time, latest_finish_time):
        # Clear the figure area and add subplot...
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # Create Horizontal bars for each Channel...
        for idx, channel_id in enumerate(groups):
            bar_margin_left = []
            bar_durations = []
            for row in groups[channel_id]:
                bar_margin_left.append((row[2] - earliest_start_time).total_seconds() / 60)
                bar_durations.append(row[1])
                    
            y = [idx] * len(bar_margin_left)

            ax.barh(y, bar_durations, left=bar_margin_left, height=0.9, align="center")

        # Set y-axis labels as Channels...
        ax.set_yticks(range(len(groups)))
        ax.set_yticklabels(["Channel " + str(channel_id) for channel_id in groups])
        
        # Set x-axis labels with 6-minute intervals...
        time_interval = timedelta(minutes=6)
        num_intervals = round(((latest_finish_time-earliest_start_time).total_seconds() / 60) / 6) + 1
        x_labels = [earliest_start_time + i * time_interval for i in range(num_intervals)]
        ax.set_xticks([(time - earliest_start_time).total_seconds() / 60 for time in x_labels])
        ax.set_xticklabels([f"{time.hour:02d}:{time.minute:02d}" for time in x_labels])
        ax.invert_yaxis()

        # Set other labels and Draw the chart...
        ax.set_xlabel("Time")
        ax.set_ylabel("Channel ID")
        ax.set_title("Channel Watching Durations")
        
        ax.grid(True)

        plt.tight_layout()

        self.canvas.draw()