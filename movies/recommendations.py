from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import csr_matrix
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import numpy as np
from .models import *
class MovieRecommender:


    def __init__(self):
        self.content_vectorizer = TfidfVectorizer(stop_words='english')
        self.movie_similarity = None
        self.cosine_sim = None
        self.hybrid_similarity = None
        self.movie_ids = None


    def recommend_movies(self, movie_id, user_id):
        # Load the datasets with limited rows
        movies_df = pd.read_csv('staticfiles/filtered_film.csv')
        ratings_df = pd.read_csv('staticfiles/filtered_ratings.csv')
        # Get all fields from the Movie model
        # #movies_queryset = Cinema.objects.all().values()

        # movies_df = pd.DataFrame(list(movies_queryset))
    
        # ratings_queryset = MovieRating.objects.all().values()

        # ratings_df = pd.DataFrame(list(ratings_queryset))   
        k= 5
        cosine_weight=0.65
        collaborative_weight=0.35
        # Optimize data types for memory efficiency
        ratings_df['userId'] = ratings_df['userId'].astype('int32')
        ratings_df['movieId'] = ratings_df['movieId'].astype('int32')
        ratings_df['rating'] = ratings_df['rating'].astype('float32')

        # Ensure consistency in movie IDs
        movies_df = movies_df[movies_df['id'].isin(ratings_df['movieId'])]
        top_users = ratings_df['userId'].value_counts().index
        top_movies = movies_df['id'].tolist()

        filtered_ratings_df = ratings_df[(
            ratings_df['userId'].isin(top_users)) & 
            (ratings_df['movieId'].isin(top_movies))
        ]

        # Create user-item matrix
        user_item_matrix = filtered_ratings_df.pivot(index='userId', columns='movieId', values='rating').fillna(0)

        # Convert to sparse matrix for memory efficiency
        sparse_user_item_matrix = csr_matrix(user_item_matrix.values)

        # Content-Based Filtering
        movies_df['combined_features'] = movies_df['genres'] + " " + movies_df['keywords'] + movies_df['overview'] + " " + movies_df['title']
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(movies_df['combined_features'])
        cosine_sim = cosine_similarity(tfidf_matrix)

        # Collaborative Filtering with KNN
        knn = NearestNeighbors(n_neighbors=k, metric='cosine')
        knn.fit(sparse_user_item_matrix)  # Fit the KNN model to the user-item matrix

        # Function to get KNN-based similar users
        def get_knn_users(user_idx):
            distances, indices = knn.kneighbors(sparse_user_item_matrix[user_idx], n_neighbors=k)
            return indices.flatten(), distances.flatten()

        # Recommendation function for KNN with movie IDs
        def recommend_movies_knn(user_id, top_n=k, alpha=collaborative_weight):
            # Assuming user_item_matrix.index.tolist() is the list of user IDs
            user_idx_list = user_item_matrix.index.tolist()

            # Check if user_id exists in the list
            if user_id in user_idx_list:
                user_idx = user_idx_list.index(user_id)
                user_idx = user_item_matrix.index.tolist().index(user_id)
                similar_users, _ = get_knn_users(user_idx)
                predicted_ratings = []
                for similar_user in similar_users:
                    similar_user_ratings = user_item_matrix.iloc[similar_user].values
                    predicted_ratings.append(similar_user_ratings)
                predicted_ratings = np.mean(predicted_ratings, axis=0)
                recommended_indices = np.argsort(predicted_ratings)[::-1][:top_n]
                recommended_movie_ids = user_item_matrix.columns[recommended_indices].tolist()
                print(recommended_movie_ids)
                return recommended_movie_ids  # Return only movie IDs
            else:
                return []


            

        # Recommendation function using content-based filtering
        def recommend_movies_content(movie_id, similarity_matrix, movie_ids, top_n=k):
            idx = movie_ids.index(movie_id)
            sim_scores = list(enumerate(similarity_matrix[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            top_movies = [movie_ids[i[0]] for i in sim_scores[1:top_n+1]]
            print(top_movies)
            return top_movies

        movie_ids = movies_df['id'].tolist()

        # Show example recommendations for a user
        user_recommendations = recommend_movies_knn(user_id)  # Use provided user ID

        content_based_recommendations = recommend_movies_content(movie_id, cosine_sim, movie_ids)  # Use provided movie ID

        collaborative_percent = user_recommendations[:int(len(user_recommendations) * collaborative_weight)]
        content_percent = content_based_recommendations[:int(len(content_based_recommendations) * cosine_weight)]
        total_recommendations = 5

        # Ensure we have exactly 5 recommendations
        if len(collaborative_percent) + len(content_percent) < total_recommendations:
            remaining = total_recommendations - len(collaborative_percent) - len(content_percent)
            content_percent.extend(content_based_recommendations[len(content_percent):len(content_percent)+remaining])

        # Combine the two parts to form the final list
        final_recommendations = collaborative_percent + content_percent
        hybrid = final_recommendations
        print("Recommendations based on Hybrid:", hybrid)
        return hybrid



