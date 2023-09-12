import json
import matplotlib.pyplot as plt
from matplotlib.dates import date2num, MonthLocator, DateFormatter
from datetime import datetime

# data obtained from https://www.tesla.com/teslaaccount/charging/api/history

# Load data from JSON
with open('data.json', 'r') as f:
    data = json.load(f)

session_data = data['data']

# Extract session IDs and corresponding start dates
session_ids = [entry['sessionId'] for entry in session_data]
dates = [date2num(datetime.fromisoformat(entry['chargeStartDateTime'].replace('Z', '+00:00'))) for entry in
         session_data]

# Plotting
fig, ax = plt.subplots(figsize=(10, 5))  # Increase the width to 12 inches

ax.plot(dates, session_ids, marker='o', linestyle='-', color='red', markersize=4)
ax.xaxis.set_major_locator(MonthLocator())
ax.xaxis.set_major_formatter(DateFormatter('%b %Y'))

# Custom y-tick formatting to display full numbers with commas
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '{:,.0f}'.format(x)))

plt.title('Charging Session ID over Time')
plt.xlabel('Time')
plt.ylabel('Session ID')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
