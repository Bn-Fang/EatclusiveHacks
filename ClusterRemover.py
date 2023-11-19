import pandas as pd

csv_path = "VotingSampleData.csv"

# Load data from CSV file
df = pd.read_csv(csv_path)

# Ask for the ClusterID
cluster_id = int(input("Enter ClusterID: "))

# Find all rows with the same ClusterID and change Vote to 0
df.loc[df['ClusterId'] == cluster_id, 'Vote'] = 0

# Save the updated DataFrame back to the CSV file
df.to_csv(csv_path, index=False)

print('The CSV file has been updated.')