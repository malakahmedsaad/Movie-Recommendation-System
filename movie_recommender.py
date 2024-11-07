import pandas as pd
import streamlit as st

movies_df = pd.read_csv('C:/Users/mohamedm/Downloads/movie_recommendations.csv')

# Step 2: Streamlit user interface
st.title("Movies Recommendation System 🎬")
st.write("Select a genre to get movie recommendations!")

# Step 3: Display available genres for selection
unique_genres = movies_df['Genres'].dropna().unique()  # Remove NaN values if present
unique_genres = [genre for genre in unique_genres if isinstance(genre, str)]
selected_genre = st.selectbox("Choose a genre", unique_genres)


def get_recommendations(genre, movies, top_n=3):
    # Filter movies based on the selected genre
    genre_movies = movies[movies['Genres'].str.contains(genre, case=False, na=False)]

    # Sort the movies by IMDb rating (descending order)
    genre_movies_sorted = genre_movies.sort_values(by='IMDb Rating', ascending=False)

    # Select the top N movies
    top_movies = genre_movies_sorted[['Title','URL', 'IMDb Rating', 'Year', 'Genres']].head(top_n)

    return top_movies


# Step 4: Get recommendations when the user selects a genre
if st.button("Get Recommendations"):
    top_recommendations = get_recommendations(selected_genre, movies_df)

    if top_recommendations.empty:
        st.write(f"No movies found for the genre '{selected_genre}'. Please try another genre.")
    else:
        st.write(f"\nTop {len(top_recommendations)} Movies in the '{selected_genre}' genre:")
        for index, row in top_recommendations.iterrows():
            st.write(f"**{row['Title']}** ({row['Year']}) - IMDb Rating: {row['IMDb Rating']}")
            st.write(f"Genres: {row['Genres']}")
            st.write(f"URL: [Link to IMDb]({row['URL']})")
            st.write("---")
