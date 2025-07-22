import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

# Paths
csv_file = 'Attendance.csv'
today = datetime.now().strftime("%Y-%m-%d")
excel_file = f'Attendance_Report_{today}.xlsx'
chart_file = f'attendance_chart_{today}.png'

# Load Attendance CSV
df = pd.read_csv(csv_file)
df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S')

# Save to Excel
df.to_excel(excel_file, index=False)
print(f"[INFO] Report saved as {excel_file}")

# Plot Attendance Chart
attendance_count = df['Name'].value_counts()

plt.figure(figsize=(8, 5))
attendance_count.plot(kind='bar', color='skyblue')
plt.title(f"Attendance Report ({today})")
plt.xlabel("Names")
plt.ylabel("Number of Entries")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(chart_file)
plt.close()

print(f"[INFO] Attendance chart saved as {chart_file}")
