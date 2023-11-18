import pandas as pd
from sklearn.datasets import make_blobs
import random

# creating dataset with 5 clusters
X, y = make_blobs(
   n_samples=1000, n_features=2,
   centers=5, cluster_std=2, # Here, I have increased std to 2 to spread out the blobs
   shuffle=True, random_state=0
)

# Generate User IDs and random votes
User_ID = [i for i in range(1000)]
random_votes = [random.randint(1, 3) for _ in range(1000)]

# create a data frame
df = pd.DataFrame(dict(User_ID=User_ID, x=X[:,0], y=X[:,1], Vote=random_votes))

# save to csv file
df.to_csv('VotingData.csv', index=False)

print("CSV file named 'VotingData.csv' has been created.")