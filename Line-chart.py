from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
import pandas as pd
from datetime import datetime
import re

file_path = "soal_chart_bokeh.txt"


timestamps = []
bitrates = []

with open(file_path, "r") as file:
    current_timestamp = None
    for line in file:
        if line.startswith("Timestamp:"):
            timestamp_str = " ".join(line.split(" ")[1:3])
            try:
                current_timestamp = datetime.strptime(timestamp_str.strip(), "%Y-%m-%d %H:%M:%S")
            except ValueError as e:
                print(f"Error parsing timestamp: {timestamp_str} -> {e}")

        if "sec" in line:
            match = re.search(r'(\d+\.\d+)-(\d+\.\d+)\s+sec.*?(\d+\.\d+)\s+Mbits/sec', line)
            if match and current_timestamp:
                interval_start = float(match.group(1))
                interval_end = float(match.group(2))
                bitrate = float(match.group(3))

                timestamps.append(current_timestamp)
                bitrates.append(bitrate)

                current_timestamp = None

data = pd.DataFrame({
    "Timestamp": timestamps,
    "Bitrate (Mbits/sec)": bitrates
})

source = ColumnDataSource(data)

p = figure(x_axis_type="datetime", title="Testing Jaringan", height=400, width=800)
p.line(x='Timestamp', y='Bitrate (Mbits/sec)', source=source, line_width=2, color="blue")

p.xaxis.axis_label = "DATETIME"
p.yaxis.axis_label = "Speed (Mbps)"
p.legend.location = "top_left"
p.legend.click_policy = "hide"


p.grid.grid_line_alpha = 0.5

show(p)
print(data)
