from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
np.bool = np.bool_
np.object = object


df = pd.read_csv('all_recipes_data.csv')


def recommend(user_pref, user_allergies, time, top_n, df=df):
    # Normalize feature matrix
    normalized_features = (df.drop(['name', 'link'], axis=1) - df.drop(
        ['name', 'link'], axis=1).mean()) / df.drop(['name', 'link'], axis=1).std()
    # Determine the minimum and maximum values of the time feature in the normalized_features DataFrame
    min_time_normalized = normalized_features['time'].min()
    max_time_normalized = normalized_features['time'].max()

    # Min-max scale the time feature to range between 0 and 1
    normalized_features['time'] = (normalized_features['time'] - min_time_normalized) / (max_time_normalized - min_time_normalized)

    # Ensure user preferences and allergies are included in the feature matrix columns
    user_features = user_pref + user_allergies
    missing_features = [
        feature for feature in user_features if feature not in normalized_features.columns]
    if missing_features:
        raise ValueError(
            f"The following user preferences/allergies are not found in the feature matrix columns: {missing_features}")

    # Create user profile vector with all zeros except for the favorite categories
    user_profile = pd.Series(0, index=normalized_features.columns)
    
    # Set favorite categories to 1
    for pref in user_pref:
        user_profile[pref] = 1

    # Set allergies to 0
    for allergy in user_allergies:
        user_profile[allergy] = 0

    min_time = df['time'].min()
    max_time = df['time'].max()
    user_profile['time'] = (time - min_time) / (max_time - min_time)

    # Calculate similarity between user profile and recipes
    user_similarities = cosine_similarity(
        [user_profile.values], normalized_features)

    # Get top recommendations
    # Get indices of top N most similar recipes
    top_indices = user_similarities.argsort()[0][::-1][:top_n]
    top_recipes = df.iloc[top_indices][['name', 'link', 'likes']]

    return top_recipes

if __name__ == '__main__':
    print(recommend(['oils'], [], 30, 10))