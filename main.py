import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# data pulled from https://fleet-api.prd.na.vn.cloud.tesla.com/api/1/dx/charging/history

# Load data from JSON file
with open('data.json') as file:
    data = json.load(file)

# Convert JSON data to a DataFrame
df = pd.DataFrame(data['data'])

# Convert the chargeStartDateTime to a datetime object
df['chargeStartDateTime'] = pd.to_datetime(df['chargeStartDateTime'], utc=True)

# Sort the DataFrame by chargeStartDateTime
df = df.sort_values(by='chargeStartDateTime')

# Extract datetime and session ID for regression
x = df['chargeStartDateTime'].map(pd.Timestamp.toordinal).values
y = df['sessionId'].values

# Calculate polynomial regression (degree 2)
coefficients = np.polyfit(x, y, 2)
poly_regression_line = np.polyval(coefficients, x)

# Create future dates up to 2026
last_date = df['chargeStartDateTime'].max().date()
future_dates = pd.date_range(start=last_date, end='2025-12-31', freq='D')
future_dates_ord = future_dates.map(pd.Timestamp.toordinal).values
future_poly_regression_line = np.polyval(coefficients, future_dates_ord)

# Combine current and future data for plotting
all_dates = np.concatenate((x, future_dates_ord))
all_dates_datetime = pd.to_datetime([pd.Timestamp.fromordinal(int(date)) for date in all_dates], utc=True)
all_poly_regression_line = np.concatenate((poly_regression_line, future_poly_regression_line))

# Plot the data
plt.figure(figsize=(14, 7))
ax = plt.gca()  # Get current axes
ax.plot(df['chargeStartDateTime'], df['sessionId'], marker='o', markersize=3, linestyle='None', label='Data Points')
ax.plot(all_dates_datetime, all_poly_regression_line, color='red', label='Trend Line')

ax.set_title('Charging Session ID Over Time')
ax.set_xlabel('Time')
ax.set_ylabel('Session ID')
ax.grid(True)

# Custom y-tick formatting
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '{:,.0f}'.format(x)))

plt.xticks(rotation=45)
plt.tight_layout()
plt.legend()

# Show the plot
plt.show()
