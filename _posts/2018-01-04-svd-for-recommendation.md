---
layout: post
title: Creating a movie recommendation system
date: 2018-01-04 11:59:00-0400
description: 
categories: recommendation machine-learning svd python 
---

In my undergraduate degree, I built a movie recommendation system using Singular Value Decomposition (SVD). It was the first time I got to see the power of machine learning in action, and the results really
surprised me in a good way.

I will go through the process used in the project, and the code for this is available in my [Github](https://github.com/dipespandey/movie-recommendation-system).

### Data Collection
One of the most famous movie data APIs, Open Movie Database (OMDB) was used to get the movie data. The data was then stored in a CSV file. The data consists of 10000 movies and their corresponding ratings from 1000 users. Let's take a look at the structure of the data.

Let's have a quick look at the data. While there are other files in the dataset, we will only be using the `u.data` file because it has all the ratings
information we need.
```
user_id item_id rating timestamp
196	242	3	881250949
186	302	3	891717742
22	377	1	878887116
244	51	2	880606923
166	346	1	886397596
```

### Data Preprocessing
```python
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import random


# Load data from disk
def ratings_reader():
   names = ['user_id', 'item_id', 'rating', 'timestamp']
   df = pd.read_csv('dataset/u.data', sep='\t', names=names)
   n_users = df.user_id.unique().shape[0]
   n_items = df.item_id.unique().shape[0]

   # Create r_{ui}, our ratings matrix
   ratings = np.zeros((n_users, n_items))
   for row in df.itertuples():
       ratings[row[1]-1, row[2]-1] = row[3]

   return ratings

ratings = ratings_reader()
n_users = ratings.shape[0]
n_items = ratings.shape[1]
```


### Test-Train Split

```python
def test_train_split(ratings):
   test = np.zeros(ratings.shape)
   train = ratings.copy()

   for user in range(ratings.shape[0]):
      test_ratings = np.random.choice(ratings[user, :].nonzero()[0],
      size = 10, replace=False)

      train[user, test_ratings] = 0
      test[user, test_ratings] = ratings[user, test_ratings]

   assert(np.all((train * test) == 0))

   return train, test


train, test = test_train_split(ratings)



def get_rmse(actual, pred):
   pred = pred[actual.nonzero()].flatten()
   actual = actual[actual.nonzero()].flatten()
   mse = mean_squared_error(pred, actual)
   return mse**0.5
```


### Training the model
##### Set hyperparameters
```python
n_iters = 200
gamma = 0.001
lmbda = 0.01

k = 80

users, items = train.nonzero()

Bu = np.zeros(n_users)
Bi = np.zeros(n_items)
P = np.random.rand(n_users, k)
Q = np.random.rand(n_items, k)
global_bias = np.mean(train[np.where(train != 0)])
train_rmses = []
test_rmses = []
```


##### Matrix Factorization Algorithm for Collaborative Filtering

Before we start, let's try to visualize how the algorithm works. The algorithm is called SVD (Singular Value Decomposition)-based Matrix Factorization. There's a very intuitive video on youtube by [Visual Kernel](https://www.youtube.com/@visualkernel) that explains the algorithm. Feel free to watch it.

<iframe width="720" height="500" style="width: 100%;"
src="https://www.youtube.com/embed/vSczTbgc8Rc">
</iframe>

The following is a detailed breakdown of applying SVD to the given user-item matrix.  
Consider the following user-item matrix:
<table class="table table-bordered">
<tr>
<td>User</td>
<td>Indiana Jones</td>
<td>Star Wars</td>
<td>Empire Strikes Back</td>
<td>Incredibles</td>
<td>Casablanca</td>
</tr>
<tr>
<td>Bob</td>
<td>4</td>
<td>5</td>
<td>?</td>
<td>?</td>
<td>?</td>
</tr>
<tr>
<td>Ted</td>
<td>?</td>
<td>?</td>
<td>?</td>
<td>?</td>
<td>1</td>
</tr>
<tr>
<td>Ann</td>
<td>?</td>
<td>5</td>
<td>5</td>
<td>5</td>
<td>?</td>
</tr>
</table>

Step 1: Initialize the User-Item Matrix \( R \)
- Fill missing values with the average rating or zeros for simplicity:  
  $$
  R = \begin{bmatrix}
  4 & 5 & 0 & 0 & 0 \\
  0 & 0 & 0 & 0 & 1 \\
  0 & 5 & 5 & 5 & 0
  \end{bmatrix}
  $$
  

Step 2: Apply SVD
- Decompose $$ R $$ into three matrices $$ U $$, $$ \Sigma $$, and $$ V^T $$ such that $$ R \approx U \Sigma V^T $$.

Example decomposition:   
  
  $$
  U = \begin{bmatrix}
  0.58 & 0.58 & 0.58 \\
  0.29 & -0.71 & 0.65 \\
  0.76 & -0.41 & -0.50
  \end{bmatrix}
  $$
  
  $$
  \Sigma = \begin{bmatrix}
  9 & 0 & 0 \\
  0 & 5 & 0 \\
  0 & 0 & 2
  \end{bmatrix}
  $$
  
  $$
  V^T = \begin{bmatrix}
  0.58 & 0.58 & 0.58 & 0.29 & 0.29 \\
  0.29 & -0.71 & 0.65 & 0.29 & -0.29 \\
  0.76 & -0.41 & -0.50 & 0.29 & 0.29
  \end{bmatrix}
  $$

Step 3: Reconstruct the Matrix
- Use the top $$ k $$ singular values to approximate $$ R $$:
  $$
  R' = U_k \Sigma_k V_k^T
  $$

How does this work?
- The matrix $$ R $$ is decomposed into three matrices: $$ U $$, $$ \Sigma $$, and $$ V^T $$.
- $$ U $$ contains the left singular vectors, $$ \Sigma $$ is a diagonal matrix with singular values, and $$ V^T $$ contains the right singular vectors.
- By selecting the top $$ k $$ singular values, we reduce the dimensionality of the matrices while retaining the most significant features.
- The product of these reduced matrices $$ U_k \Sigma_k V_k^T $$ gives us an approximation of the original matrix $$ R $$, denoted as $$ R' $$.
- This approximation helps in reconstructing the matrix with reduced noise and improved generalization for predicting missing values.

Step 4: Predict Missing Ratings
- Use the reconstructed matrix $$ R' $$ to fill in missing ratings:
  $$
  R' = \begin{bmatrix}
  4 & 5 & 3 & 2 & 1 \\
  2 & 1 & 1 & 1 & 1 \\
  3 & 5 & 5 & 5 & 2
  \end{bmatrix}
  $$

The predicted ratings for missing values are derived from the reconstructed matrix $$ R' $$.


Matrix Factorization is a collaborative filtering algorithm used to predict user-item interactions. The goal is to factorize the user-item interaction matrix into two lower-dimensional matrices, representing users and items, respectively. These matrices are then used to predict missing entries in the original matrix.

Mathematically, we aim to decompose the user-item interaction matrix $$ R $$ into two matrices $$ P $$ and $$ Q $$ such that:
$$
R \approx P \cdot Q^T
$$

where:
- $$ R $$ is the $$ n \times m $$ user-item interaction matrix.
- $$ P $$ is the $$ n \times k $$ user-feature matrix.
- $$ Q $$ is the $$ m \times k $$ item-feature matrix.
- $$ k $$ is the number of latent features.  

The predicted rating $$ \hat{r}_{ui} $$ for user $$ u $$ and item $$ i $$ is given by:

$$
\hat{r}_{ui} = P_u \cdot Q_i^T + B_u + B_i + \mu
$$

where:
- $$ P_u $$ is the $$ u $$-th row of matrix $$ P $$
- $$ Q_i $$ is the $$ i $$-th row of matrix $$ Q $$
- $$ B_u $$ is the bias term for user $$ u $$
- $$ B_i $$ is the bias term for item $$ i $$
- $$ \mu $$ is the global bias term, representing the average rating.

To learn the matrices $$ P $$ and $$ Q $$, we minimize the following regularized squared error loss function using Stochastic Gradient Descent (SGD):

$$ \min_{P, Q, B_u, B_i} \sum_{(u,i) \in \mathcal{K}} \left( r_{ui} - \hat{r}_{ui} \right)^2 + \lambda \left( \|P_u\|^2 + \|Q_i\|^2 + B_u^2 + B_i^2 \right) $$

where:
- $$ \mathcal{K} $$ is the set of user-item pairs for which the ratings are known.
- $$ \lambda $$ is the regularization parameter to prevent overfitting.

The update rules for SGD are as follows:

$$ P_u \leftarrow P_u + \gamma \left( e_{ui} \cdot Q_i - \lambda \cdot P_u \right) $$  
$$ Q_i \leftarrow Q_i + \gamma \left( e_{ui} \cdot P_u - \lambda \cdot Q_i \right) $$  
$$ B_u \leftarrow B_u + \gamma \left( e_{ui} - \lambda \cdot B_u \right) $$  
$$ B_i \leftarrow B_i + \gamma \left( e_{ui} - \lambda \cdot B_i \right) $$  

where:
- $$ e_{ui} = r_{ui} - \hat{r}_{ui} $$ is the prediction error.
- $$ \gamma $$ is the learning rate.

By iteratively updating the matrices $$ P $$ and $$ Q $$, and the bias terms $$ B_u $$ and $$ B_i $$, we can minimize the loss function and obtain the optimal factorized matrices for predicting user-item interactions.


Now, let's implement the algorithm.

```python
def trainer(n_iters, users, items, P, Q, Bu, Bi, global_bias, trainer, tester, gamma, lmbda):
   # use the stochastic gradient descent approach to mimimize the error in prediction
   train_rmses = []
   test_rmses = []

   for n in range(n_iters):
      for u,i in zip(users, items):
         prediction = P[u,:].dot(Q[i,:].T) + Bu[u] + Bi[i] + global_bias
         e = train[u,i] - prediction
         Bu[u] += gamma * (e - lmbda * Bu[u])
         Bi[i] += gamma * (e - lmbda * Bi[i])
         P[u,:] += gamma * (e * Q[i,:] - lmbda * P[u,:])
         Q[i,:] += gamma * (e * P[u,:] - lmbda * Q[i,:])
      
      pred = np.zeros((P.shape[0], Q.shape[0]))

      for u in range(P.shape[0]):
         for i in range(Q.shape[0]):
            pred[u,i] = P[u,:].dot(Q[i,:].T) + Bu[u] + Bi[i] + global_bias

      train_rmse = get_rmse(train, pred)
      test_rmse = get_rmse(test, pred)
      train_rmses.append(train_rmse)
      test_rmses.append(test_rmse)
      print(n+1, train_rmse, test_rmse)
      return(train_rmses, test_rmses)


# Start training the model
train_rmses, test_rmses = trainer(n_iters, users, items, P, Q, Bu, Bi, global_bias, train, test, gamma, lmbda)
```


### Plotting the learning curves
```python
def draw_learning_curve(n_iters, train_rmse, test_rmse):
   # use this function to use the above train_rmses and test_rmses to plot the rmse curves, 
   # see how they converge
   plt.plot(range(n_iters), train_rmse, label = 'Train', linewidth = 5)
   plt.plot(range(n_iters), test_rmse, label = 'Test', linewidth = 5)
   plt.xlabel('Iterations')
   plt.ylabel('RMSE')
   plt.legend(loc='best', fontsize=30)


def cosine_similarity(Q):
   # finds the cosine similarity based on item feature matrix
   # parameter: Q ( item latent feature matrix)
   sim = Q.dot(Q.T)
   norms = np.array([np.sqrt(np.diagonal(sim))])
   return sim/ norms/ norms.T


def get_top_k(sims, movie_id, k):
   # return the tuple of top k movies using the similarity matrix and movie_id
   movie_indices = np.argsort(sims[movie_id,:])[::-1]
   top_k = movie_indices[1:k]   
   top_k = tuple(top_k)
   return top_k
```


### Inference

```python
def infer(user_id, item_id, P, Q, Bu, Bi, global_bias):
    """
    Make a prediction for a given user and item using the trained matrices.
    
    Parameters:
    user_id (int): The ID of the user.
    item_id (int): The ID of the item.
    P (numpy array): User latent feature matrix.
    Q (numpy array): Item latent feature matrix.
    Bu (numpy array): User biases.
    Bi (numpy array): Item biases.
    global_bias (float): The global bias.
    
    Returns:
    float: The predicted rating.
    """
    prediction = P[user_id, :].dot(Q[item_id, :].T) + Bu[user_id] + Bi[item_id] + global_bias
    return prediction

# Example usage:
user_id = 0  # example user ID
item_id = 0  # example item ID
predicted_rating = infer(user_id, item_id, P, Q, Bu, Bi, global_bias)
print(f"Predicted rating for user {user_id} and item {item_id}: {predicted_rating}")
```

The fullstack project with the code is available [here](https://github.com/Genalize/movieRecommendations).

References:
- https://www.ethanrosenthal.com/2016/01/09/explicit-matrix-factorization-sgd-als/
- https://www.youtube.com/watch?v=vSczTbgc8Rc