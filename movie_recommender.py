import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load the ratings data
ratings = pd.read_csv('Data/u.data', sep='\t', header=None, names=['userId', 'movieId', 'rating', 'timestamp'])

# Create a user-movie matrix
user_movie_matrix = ratings.pivot(index='userId', columns='movieId', values='rating')
user_movie_matrix = user_movie_matrix.fillna(0)  # Fill NaN values with 0

# Compute user similarity matrix using cosine similarity
user_similarity = cosine_similarity(user_movie_matrix)
user_similarity = pd.DataFrame(user_similarity, index=user_movie_matrix.index, columns=user_movie_matrix.index)


def get_recommendations(user_id, user_similarity, ratings_matrix, top_n=10):
    if user_id not in ratings_matrix.index:
        raise ValueError("User ID not found in ratings matrix.")

    # Get similar users
    similar_users = user_similarity.loc[user_id]

    # Predict ratings for the user
    user_ratings = ratings_matrix.loc[user_id]
    weighted_sum = np.dot(similar_users, ratings_matrix.fillna(0))
    similarity_sum = np.sum(similar_users)

    # Avoid division by zero
    predicted_ratings = weighted_sum / (similarity_sum if similarity_sum != 0 else 1)

    # Convert predicted_ratings to a pandas Series
    predicted_ratings = pd.Series(predicted_ratings, index=ratings_matrix.columns)

    # Get the top_n movie recommendations
    unrated_movies = user_ratings[user_ratings == 0].index
    recommendations = []
    for movie in unrated_movies:
        if movie in predicted_ratings.index:
            recommendations.append((movie, predicted_ratings[movie]))

    recommendations.sort(key=lambda x: x[1], reverse=True)

    return recommendations[:top_n]


# Example usage
user_id = 1  # Example user ID
top_recommendations = get_recommendations(user_id, user_similarity, user_movie_matrix, top_n=10)

print(f"\nTop Recommendations for User {user_id}:")
for movie_id, rating in top_recommendations:
    print(f"Movie ID: {movie_id}, Predicted Rating: {rating:.2f}")
