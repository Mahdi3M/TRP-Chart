from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from datetime import timedelta
import matplotlib.pyplot as plt
import mplcursors



# Custom Chart class representing Channels vs Time watched...
class CustomChart():
    def __init__(self):
        self.figure = plt.figure(figsize=(11, 5))
        self.canvas = FigureCanvas(self.figure)
        self.bars = []
        self.bars_data = []
        
    
    def plot_custom_chart(self, groups):
        # Clear the figure area and add subplot...
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        earliest_start_time = min(row[2] for channel in groups for row in groups[channel])
        latest_finish_time = max(row[3] for channel in groups for row in groups[channel])

        # Create Horizontal bars for each Channel...
        for idx, channel_id in enumerate(groups):
            bar_margin_left = []
            bar_durations = []
            bars_data = []
            for row in groups[channel_id]:
                bar_margin_left.append((row[2] - earliest_start_time).total_seconds() / 60)
                bar_durations.append(row[1])
                bars_data.append({'start': row[2], 'end': row[3], 'duration': row[1]})
                    
            y = [idx] * len(bar_margin_left)

            bars = ax.barh(y, bar_durations, left=bar_margin_left, height=0.9, align="center")
            self.bars.append(bars)
            self.bars_data.append(bars_data)
        
        
        # Set y-axis labels as Channels...
        ax.set_yticks(range(len(groups)))
        ax.set_yticklabels(["Channel " + str(channel_id) for channel_id in groups])
        ax.set_ylim(top=7)
        
        # Set x-axis labels with 5-minute intervals...
        time_interval = timedelta(minutes=5)
        num_intervals = round(((latest_finish_time-earliest_start_time).total_seconds() / 60) / 5) + 1
        x_labels = [earliest_start_time + i * time_interval for i in range(num_intervals)]
        ax.set_xticks([(time - earliest_start_time).total_seconds() / 60 for time in x_labels])
        ax.set_xticklabels([f"{time.hour:02d}:{time.minute:02d}" for time in x_labels])
        ax.invert_yaxis()

        # Set other labels and Draw the chart...
        ax.set_xlabel("Time")
        ax.set_ylabel("Channel ID")
        ax.set_title("Channel Watching Durations")
        
        ax.grid(True)
            
        # Add start and finish time annotations using mplcursors
        cursor = mplcursors.cursor(self.bars, hover=True)
        cursor.connect("add", self.show_annotation)
        
        plt.tight_layout()

        self.canvas.draw()
        
        
    def show_annotation(self, sel):
        channel = round(sel.target[1])
        bar = sel.index
        start_time = self.bars_data[channel][bar]['start'].strftime("%d/%m/%Y %H:%M")
        finish_time = self.bars_data[channel][bar]['end'].strftime("%d/%m/%Y %H:%M")
        duration = self.bars_data[channel][bar]['duration']
        annotation_text = f"Start: {start_time}\nFinish: {finish_time}\nDuration: {duration}"
        sel.annotation.set_text(annotation_text)