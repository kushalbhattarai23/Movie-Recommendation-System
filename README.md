# Movie Recommendation System

A Django-based movie recommendation system that provides personalized movie suggestions using hybrid recommendation algorithms. The system combines content-based and collaborative filtering to deliver accurate recommendations based on user preferences and ratings.

## Features

### Core Functionality
- **User Authentication**: Secure registration, login, and logout system
- **Movie Database**: Comprehensive movie catalog with detailed information
- **Rating System**: Users can rate movies on a 1-5 scale
- **Hybrid Recommendations**: Combines content-based and collaborative filtering
- **Search Functionality**: Search movies by title, genre, or keywords
- **Responsive Design**: IMDb-inspired dark theme with mobile-friendly interface

### Recommendation Engine
- **Content-Based Filtering**: Recommends movies based on genres, keywords, and movie features
- **Collaborative Filtering**: Uses K-Nearest Neighbors (KNN) to find similar users
- **Hybrid Approach**: Combines both methods with configurable weights (65% content-based, 35% collaborative)
- **Real-time Updates**: Recommendations update as users rate more movies

## Technology Stack

### Backend
- **Django 5.0.1**: Web framework
- **Django REST Framework**: API development
- **SQLite**: Database (development)
- **Python 3.10+**: Programming language

### Frontend
- **HTML5/CSS3**: Structure and styling
- **JavaScript (ES6+)**: Interactive functionality
- **Bootstrap**: Responsive design components

### Machine Learning
- **scikit-learn**: Machine learning algorithms
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations
- **scipy**: Scientific computing

## Installation

### Prerequisites
- Python 3.10 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd movie-recommendation-system
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install django djangorestframework scikit-learn pandas numpy scipy
   ```

4. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Open your browser and navigate to `http://localhost:8000`
   - Admin panel: `http://localhost:8000/admin`

## Project Structure

```
movie-recommendation-system/
├── project/                    # Main Django project
│   ├── settings.py            # Project settings
│   ├── urls.py               # Main URL configuration
│   └── wsgi.py               # WSGI configuration
├── movies/                    # Movies app
│   ├── models.py             # Database models
│   ├── views.py              # API views
│   ├── serializers.py        # DRF serializers
│   ├── recommendations.py    # Recommendation engine
│   └── urls.py               # App URL patterns
├── frontend/                  # Frontend app
│   ├── views.py              # Template views
│   └── urls.py               # Frontend URL patterns
├── templates/                 # HTML templates
│   ├── base.html             # Base template
│   ├── home.html             # Homepage
│   ├── movie_detail.html     # Movie details page
│   ├── login.html            # Login page
│   └── register.html         # Registration page
├── staticfiles/              # Static files
│   ├── css/                  # Stylesheets
│   ├── js/                   # JavaScript files
│   ├── filtered_film.csv     # Movie dataset
│   └── filtered_ratings.csv  # Ratings dataset
└── manage.py                 # Django management script
```

## API Endpoints

### Movies
- `GET /api/movies/` - List all movies with pagination
- `GET /api/movies/{id}/` - Get movie details
- `GET /api/movies/?search={query}` - Search movies

### Ratings
- `POST /rate_movie/` - Submit a movie rating
- `GET /api/movieratings/` - List all ratings

### Authentication
- `POST /api/login/` - User login
- `POST /api/token/` - Get JWT token
- `POST /api/token/refresh/` - Refresh JWT token

## Database Models

### Cinema (Movie)
- `id`: Primary key
- `tmdbId`: The Movie Database ID
- `title`: Movie title
- `overview`: Movie description
- `genres`: Comma-separated genres
- `keywords`: Movie keywords
- `poster_path`: Poster image path
- `release_date`: Release date
- `tagline`: Movie tagline

### MovieRating
- `id`: Primary key
- `userId`: User ID (foreign key)
- `movieId`: Movie ID (foreign key)
- `rating`: Rating value (1-5)
- `timestamp`: Rating timestamp

## Recommendation Algorithm

The system uses a hybrid approach combining:

1. **Content-Based Filtering**:
   - Analyzes movie features (genres, keywords, overview, title)
   - Uses TF-IDF vectorization
   - Calculates cosine similarity between movies

2. **Collaborative Filtering**:
   - Implements K-Nearest Neighbors (KNN)
   - Finds users with similar rating patterns
   - Predicts ratings based on similar users

3. **Hybrid Combination**:
   - 65% weight for content-based recommendations
   - 35% weight for collaborative filtering
   - Combines results for final recommendations

## Usage

### For Users
1. **Register/Login**: Create an account or log in
2. **Browse Movies**: Explore the movie catalog
3. **Rate Movies**: Rate movies you've watched (1-5 stars)
4. **Get Recommendations**: View personalized recommendations on movie detail pages
5. **Search**: Use the search functionality to find specific movies

### For Developers
1. **Add New Movies**: Use Django admin or API to add movies
2. **Customize Recommendations**: Modify weights in `recommendations.py`
3. **Extend Features**: Add new fields to models or create new views
4. **API Integration**: Use the REST API for mobile apps or external services

## Configuration

### Recommendation Settings
In `movies/recommendations.py`, you can adjust:
- `k`: Number of similar users/movies to consider (default: 5)
- `cosine_weight`: Weight for content-based filtering (default: 0.65)
- `collaborative_weight`: Weight for collaborative filtering (default: 0.35)

### CORS Settings
In `project/settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Add your frontend URLs
]
```

## Data Sources

The system uses movie data from The Movie Database (TMDb):
- Movie metadata stored in `staticfiles/filtered_film.csv`
- User ratings stored in `staticfiles/filtered_ratings.csv`
- Poster images loaded from TMDb CDN

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- The Movie Database (TMDb) for movie data and poster images
- scikit-learn community for machine learning algorithms
- Django and Django REST Framework communities

## Support

For questions or issues, please:
1. Check the existing issues in the repository
2. Create a new issue with detailed description
3. Include steps to reproduce any bugs

## Future Enhancements

- Integration with external movie APIs
- Advanced filtering options
- Social features (friend recommendations)
- Movie watchlists
- Email notifications for new recommendations
- Mobile application
- Real-time recommendation updates
- A/B testing for recommendation algorithms
