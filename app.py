import streamlit as st
import pickle
import requests
import os
from dotenv import load_dotenv

# ---------------- LOAD ENV ----------------
load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")
if not API_KEY:
    st.error("TMDB API key not found. Please set TMDB_API_KEY in your .env file.")
    st.stop()

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Movie Recommendation System", layout="wide")

# ---------------- LOAD DATA ----------------
with open("movies.pkl", "rb") as f:
    movies = pickle.load(f)

with open("similarity.pkl", "rb") as f:
    similarity = pickle.load(f)

movies_list = movies["title"].values.tolist()

# ---------------- SESSION STATE ----------------
if "recs" not in st.session_state:
    st.session_state.recs = None

if "recs_movie" not in st.session_state:
    st.session_state.recs_movie = None

if "active_trailer" not in st.session_state:
    st.session_state.active_trailer = None

if "active_trailer_title" not in st.session_state:
    st.session_state.active_trailer_title = None


# ---------------- HELPER FUNCTIONS ----------------
@st.cache_data(ttl=3600)
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        data = r.json()
        poster_path = data.get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    except Exception:
        pass
    return None


@st.cache_data(ttl=3600)
def fetch_trailer_url(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={API_KEY}"
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        data = r.json()

        for v in data.get("results", []):
            if v.get("site") == "YouTube" and v.get("type") == "Trailer":
                return f"https://www.youtube.com/watch?v={v.get('key')}"
    except Exception:
        pass
    return None


def recommend(movie, n):
    idx = movies[movies["title"] == movie].index[0]
    distances = similarity[idx]

    recs = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:n + 1]

    names, posters, ids = [], [], []
    for i in recs:
        row = movies.iloc[i[0]]
        names.append(row.title)
        posters.append(fetch_poster(row.movie_id))
        ids.append(row.movie_id)

    return names, posters, ids


# ---------------- STYLES ----------------
st.markdown("""
<style>

/* ===============================
   GLOBAL BACKGROUND
   =============================== */
html, body {
    background-color: #020617;
}

/* App container */
.stApp {
    background: radial-gradient(circle at top, #020617 0%, #020617 45%, #000000 100%);
    color: white;
}

/* ===============================
   HEADER
   =============================== */
header[data-testid="stHeader"] {
    background: rgba(2,6,23,0.95);
}

/* ===============================
   SIDEBAR
   =============================== */
section[data-testid="stSidebar"] {
    background-color: #020617 !important;
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* Sidebar text */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span {
    color: white !important;
}

/* ===============================
   INPUTS (TEXT, SELECT, ETC.)
   =============================== */
section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] textarea {
    background-color: #020617 !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
}

/* Placeholder text */
section[data-testid="stSidebar"] ::placeholder {
    color: #94a3b8 !important;
}

/* ===============================
   SELECTBOX – CLOSED STATE
   =============================== */
section[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: #020617 !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
}

/* Selected value text */
section[data-testid="stSidebar"] [data-baseweb="select"] span {
    color: white !important;
}

/* ===============================
   SELECTBOX – DROPDOWN MENU
   =============================== */
div[data-baseweb="menu"] {
    background-color: #020617 !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    box-shadow: 0 15px 40px rgba(0,0,0,0.85) !important;
}

/* Dropdown list */
div[data-baseweb="menu"] ul {
    background-color: #020617 !important;
}

/* Dropdown items */
div[data-baseweb="menu"] li {
    background-color: #020617 !important;
    color: white !important;
    border-radius: 8px;
}

/* Hover */
div[data-baseweb="menu"] li:hover {
    background-color: #0f172a !important;
}

/* Selected item */
div[data-baseweb="menu"] li[aria-selected="true"] {
    background-color: #1e293b !important;
}

/* ===============================
   SLIDER
   =============================== */
section[data-testid="stSidebar"] [data-testid="stSlider"] {
    color: white;
}

/* ===============================
   BUTTONS
   =============================== */
section[data-testid="stSidebar"] button {
    background-color: #020617 !important;
    color: white !important;
    border: 2px solid #ef4444 !important;
    border-radius: 12px !important;
    font-weight: 600;
}

/* Button hover */
section[data-testid="stSidebar"] button:hover {
    background-color: #0f172a !important;
    border-color: #f87171 !important;
}

/* ===============================
   MAIN CONTENT WIDTH
   =============================== */
.main > div {
    max-width: 1400px;
    margin: auto;
    padding-top: 1rem;
}

/* ===============================
   MOVIE CARDS
   =============================== */
.movie-card {
    background-color: rgba(15,23,42,0.9);
    border-radius: 16px;
    padding: 12px;
    height: 360px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.6);
    transition: transform .2s ease, box-shadow .2s ease;
}

.movie-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 14px 25px rgba(0,0,0,0.8);
}

.movie-poster {
    width: 100%;
    height: 260px;
    border-radius: 12px;
    object-fit: cover;
}

.movie-title {
    margin-top: 8px;
    font-size: 14px;
    font-weight: 600;
    text-align: center;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

</style>
""", unsafe_allow_html=True)



# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("🎬 Movie Recommender")

    selected_movie = st.selectbox(
        "Pick a movie you like",
        ["--Select--"] + movies_list
    )

    num_recs = st.slider("Number of recommendations", 3, 10, 5)

    if st.button("🔍 Recommend movies"):
        if selected_movie == "--Select--":
            st.warning("Please select a movie first.")
        else:
            with st.spinner("Finding movies you’ll love 🍿"):
                st.session_state.recs = recommend(selected_movie, num_recs)
                st.session_state.recs_movie = selected_movie
                st.session_state.active_trailer = None
                st.session_state.active_trailer_title = None


# ---------------- HEADER ----------------
st.title("🍿 Movie Recommendation System")
st.caption("Discover movies similar to the one you love.")

# ---------------- EMPTY STATE ----------------
if selected_movie == "--Select--" and not st.session_state.recs:
    st.info("👈 Select a movie from the sidebar to see details and recommendations.")

# ---------------- SELECTED MOVIE DETAILS ----------------
if selected_movie != "--Select--":
    row = movies[movies["title"] == selected_movie].iloc[0]
    col1, col2 = st.columns([1, 2])

    with col1:
        poster = fetch_poster(row.movie_id)
        if poster:
            st.image(poster, use_column_width=True)
        else:
            st.write("Poster not available")

    with col2:
        st.subheader(row.title)
        tabs = st.tabs(["📖 Overview", "🎬 Trailer"])

        with tabs[0]:
            overview = row.get("overview")
            if isinstance(overview, list):
                overview = " ".join(overview)
            st.write(overview if overview else "Overview not available.")

        with tabs[1]:
            trailer = fetch_trailer_url(row.movie_id)
            if trailer:
                st.video(trailer)
            else:
                st.info("Trailer not available for this movie.")

# ---------------- RECOMMENDATIONS ----------------
if st.session_state.recs:
    st.markdown("---")
    names, posters, ids = st.session_state.recs

    st.subheader(
        f"Recommended because you liked **{st.session_state.recs_movie}**"
    )

    cols = st.columns(len(names))

    for i in range(len(names)):
        poster_url = posters[i] or "https://via.placeholder.com/300x450?text=No+Image"
        trailer = fetch_trailer_url(ids[i])

        tmdb_url = f"https://www.themoviedb.org/movie/{ids[i]}"

        with cols[i]:
            st.markdown(
                f"""
                <div class="movie-card">
                    <a href="{tmdb_url}" target="_blank">
                        <img class="movie-poster" src="{poster_url}">
                    </a>
                    <p class="movie-title">{names[i]}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            if trailer:
                if st.button("▶ Watch Trailer", key=f"trailer_{ids[i]}"):
                    st.session_state.active_trailer = trailer
                    st.session_state.active_trailer_title = names[i]



# ---------------- FULL WIDTH TRAILER ----------------
if st.session_state.active_trailer:
    st.markdown("---")
    col1, col2 = st.columns([6, 1])

    with col1:
        st.subheader(f"🎬 {st.session_state.active_trailer_title} – Trailer")

    with col2:
        if st.button("❌ Close Trailer"):
            st.session_state.active_trailer = None
            st.session_state.active_trailer_title = None
            st.rerun()

    st.video(st.session_state.active_trailer)
