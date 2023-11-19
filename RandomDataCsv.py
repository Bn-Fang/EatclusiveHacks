import pandas as pd
from sklearn.datasets import make_blobs
import random

csv_path = "VotingSampleData.csv"
num_samples = 100

# creating dataset with 5 clusters
X, y = make_blobs(
   n_samples=num_samples, n_features=2,
   centers=5, cluster_std=0.5, # 
   shuffle=True, random_state=1
)

# Generate User IDs and random votes
User_ID = [i for i in range(num_samples)]
random_votes = [random.randint(1, 3) for _ in range(num_samples)]

# create a data frame
df = pd.DataFrame(dict(User_ID=User_ID, x=X[:,0], y=X[:,1], Vote=random_votes, ClusterId=0))

# save to csv file
df.to_csv(csv_path, index=False)

print(f"CSV file named {csv_path} has been created.")