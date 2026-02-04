# 🎬 Movie Recommendation System

An interactive **content-based movie recommendation system** built with **Python** and **Streamlit**.  
The app recommends movies similar to a selected title and displays **real-time posters, trailers, and movie details** using the **TMDB API**.

---

## ✨ Features

- 🎥 Content-based movie recommendations (cosine similarity)
- 🖼️ Movie posters fetched dynamically from TMDB
- 🎬 Trailer playback
  - Selected movie trailer inside tabs
  - Full-width cinematic trailer for recommended movies
- 🔗 Clickable movie posters redirect to TMDB for full details
- ⚡ Optimized API calls with caching
- 🔐 Secure API key management using environment variables
- 🎨 Modern dark UI with custom CSS

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit**
- **Pandas**
- **Pickle**
- **TMDB API**
- **Cosine Similarity**
- **python-dotenv**

---

## 🧠 How It Works

1. Movie metadata is preprocessed and stored using pickle files.
2. A cosine similarity matrix is used to compute similarity between movies.
3. When a user selects a movie:
   - The poster, overview, and trailer are displayed.
   - Similar movies are recommended visually.
4. Clicking a recommended movie poster opens its TMDB page.
5. Trailers are fetched dynamically and displayed within the app.

---

## 🚀 Getting Started

### 1️⃣ Clone the repository

git clone https://github.com/Sourav1331/Movie-Recommendation-System.git
cd movie-recommendation-system

---

## ⚠️ Data Files

The `.pkl` files are not included due to GitHub size limits.

To run the project:
1. Preprocess the dataset
2. Generate `movies.pkl` and `similarity.pkl`
