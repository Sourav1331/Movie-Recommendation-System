# 🎬 Movie Recommendation System

A **content-based movie recommendation system** built using **Python** and **Streamlit**.  
The app suggests movies similar to the one you like and lets you explore posters and trailers using the **TMDB API**.

---

## 🚀 Live Preview

👉 **[🔴 Open Live App](https://movie-recommendation-system-013.streamlit.app/)**

---

## ✨ Features

- 🎥 Content-based movie recommendations
- 🖼️ Movie posters fetched dynamically from TMDB
- 🎬 Watch trailers inside the app
- 🔗 Clickable movie posters redirect to TMDB
- ⚡ Cached API calls for better performance
- 🔐 Secure API key handling using environment variables
- 🎨 Modern dark UI with custom CSS

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit**
- **Pandas**
- **TMDB API**
- **Cosine Similarity**
- **Pickle**
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

## ▶ Run Locally

```bash
git clone https://github.com/Sourav1331/Movie-Recommendation-System.git
cd Movie-Recommendation-System
pip install -r requirements.txt
streamlit run app.py
```

---


## 🔑 Environment Variables

Create a `.env` file in the project root directory and add:

```env
TMDB_API_KEY=your_api_key_here
```