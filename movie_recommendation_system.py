import pandas as pd
import streamlit as st

# Load the dataset
movies_df = pd.read_csv('C:/Users/mohamedm/Downloads/fa6dfd81-a89e-43b7-81f9-e540af938a72.csv')

# Step 2: Streamlit user interface
st.title("Movies Recommendation System")
st.write("Select a genre to get movie recommendations!")

# Step 3: Display available genres for selection
unique_genres = movies_df['Genres'].dropna().unique()  # Remove NaN values if present
unique_genres = [genre for genre in unique_genres if isinstance(genre, str)]
selected_genre = st.selectbox("Choose a genre", unique_genres)

# Step 4: Add Filters for Year and IMDb Rating Range
min_year, max_year = st.slider(
    "Select a year range",
    min_value=int(movies_df['Year'].min()),
    max_value=int(movies_df['Year'].max()),
    value=(2000, 2020)
)

min_rating, max_rating = st.slider(
    "Select IMDb Rating range",
    min_value=float(movies_df['IMDb Rating'].min()),
    max_value=float(movies_df['IMDb Rating'].max()),
    value=(6.0, 10.0),
    step=0.1
)

# Step 5: Add Sorting Option
sort_by = st.selectbox("Sort recommendations by", ["IMDb Rating", "Year"])


# Function to get movie recommendations
def get_recommendations(genre, movies, min_year, max_year, min_rating, max_rating, top_n=3):
    # Filter movies based on genre and rating/year range
    genre_movies = movies[movies['Genres'].str.contains(genre, case=False, na=False)]
    genre_movies = genre_movies[
        (genre_movies['Year'] >= min_year) &
        (genre_movies['Year'] <= max_year) &
        (genre_movies['IMDb Rating'] >= min_rating) &
        (genre_movies['IMDb Rating'] <= max_rating)
        ]

    # Sort the movies by IMDb rating or Year based on the user's choice
    if sort_by == "IMDb Rating":
        genre_movies_sorted = genre_movies.sort_values(by='IMDb Rating', ascending=False)
    else:  # Sort by Year
        genre_movies_sorted = genre_movies.sort_values(by='Year', ascending=False)

    # Return the top N movies
    top_movies = genre_movies_sorted[['Title', 'URL', 'IMDb Rating', 'Year', 'Genres', 'Poster']].head(top_n)

    return top_movies


# Step 6: Get recommendations when the user clicks the button
if st.button("Get Recommendations"):
    top_recommendations = get_recommendations(selected_genre, movies_df, min_year, max_year, min_rating, max_rating)

    if top_recommendations.empty:
        st.write(f"No movies found for the genre '{selected_genre}'. Please try another genre.")
    else:
        st.write(f"\nTop {len(top_recommendations)} Movies in the '{selected_genre}' genre:")
        for index, row in top_recommendations.iterrows():
            st.write(f"**{row['Title']}** ({row['Year']}) - IMDb Rating: {row['IMDb Rating']}")
            st.write(f"Genres: {row['Genres']}")
            if pd.notna(row['Poster']):
                st.image(row['Poster'], width=100, caption=row['Title'])  # Show the poster
            st.write(f"URL: [Link to IMDb]({row['URL']})")
            st.write("---")
