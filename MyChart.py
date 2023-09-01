from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from datetime import datetime, timedelta
import matplotlib.pyplot as plt



# Custom Chart class representing Channels vs Time watched...
class CustomChart():
    def __init__(self):
        self.figure = plt.figure(figsize=(7, 4))
        self.canvas = FigureCanvas(self.figure)
        
    
    def plot_custom_chart(self, data):
        # Clear the figure area and add subplot...
        self.figure.clear()
        sub_plot = self.figure.add_subplot(111)

        channel_ids = set()
        all_start_times = []
        all_finish_times = []
        for row in data:
            channel_ids.add(row[2])
            all_start_times.append(row[3])
            all_finish_times.append(row[4])
        earliest_start_time = min(all_start_times)
        latest_finish_time = max(all_finish_times)

        for idx, channel_id in enumerate(channel_ids):
            x = []
            durations = []
            for row in data:
                if row[2] == channel_id:
                    durations.append(row[1])
                    x.append((row[3] - earliest_start_time).total_seconds() / 60)
                    
            y = [idx] * len(x)

            sub_plot.barh(y, durations, left=x, height=0.9, align="center")

        sub_plot.set_yticks(range(len(channel_ids)))
        sub_plot.set_yticklabels(["Channel " + str(int(channel_id)) for channel_id in channel_ids])
        
        # Set x-sub_plotis labels with 6-minute intervals
        time_interval = timedelta(minutes=6)
        num_intervals = round(((latest_finish_time-earliest_start_time).total_seconds() / 60) / 6) + 1
        x_labels = [earliest_start_time + i * time_interval for i in range(num_intervals)]
        sub_plot.set_xticks([(time - earliest_start_time).total_seconds() / 60 for time in x_labels])
        sub_plot.set_xticklabels([f"{time.hour:02d}:{time.minute:02d}" for time in x_labels])
        sub_plot.invert_yaxis()

        sub_plot.set_xlabel("Time")
        sub_plot.set_ylabel("Channel ID")
        sub_plot.set_title("Channel Watching Durations")

        plt.tight_layout()

        self.canvas.draw()