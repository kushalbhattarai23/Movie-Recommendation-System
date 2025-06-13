document.addEventListener("DOMContentLoaded", function() {
    const moviesContainer = document.getElementById('movies-container');
    const paginationContainer = document.createElement('div');
    paginationContainer.id = 'pagination-container';
    document.body.appendChild(paginationContainer);

    async function fetchMovies(page = 1) {
        try {
            const response = await fetch(`/api/movies/?page=${page}`);
            const data = await response.json();
            displayMovies(data.results);
            setupPagination(data);
        } catch (error) {
            console.error('Error fetching movies:', error);
        }
    }

    function displayMovies(movies) {
        moviesContainer.innerHTML = '';
        movies.forEach(movie => {
            const movieElement = document.createElement('div');
            movieElement.className = 'movie';
            movieElement.dataset.movieId = movie.id; // Store movie ID for later use

            const genres = movie.genres.split('|').map(genre => `<span class="genre">${genre}</span>`).join(' ');

            movieElement.innerHTML = `
                <h2>${movie.title}</h2>
                <p>${movie.description}</p>
                <p>Rating: ${movie.rating}</p>
                <p>Genres: ${genres}</p>
            `;
            moviesContainer.appendChild(movieElement);

            // Add click event listener
            movieElement.addEventListener('click', () => {
                fetchMovieDetails(movie.id);
            });
        });
    }

    async function fetchMovieDetails(movieId) {
        try {
            const response = await fetch(`/api/movies/${movieId}/`);
            const movie = await response.json();
            displayMovieDetails(movie);
        } catch (error) {
            console.error('Error fetching movie details:', error);
        }
    }

    function displayMovieDetails(movie) {
        const genres = movie.genres.split('|').map(genre => `<span class="genre">${genre}</span>`).join(' ');

        moviesContainer.innerHTML = `
            <div class="movie-detail">
                <h2>${movie.title}</h2>
                <p>Rating: ${movie.rating}</p>
                <p>Genres: ${genres}</p>
            </div>
            <button id="back-button">Back to Movies</button>
        `;

        const backButton = document.getElementById('back-button');
        backButton.addEventListener('click', () => fetchMovies(1));
    }

    function setupPagination(data) {
        paginationContainer.innerHTML = '';

        if (data.previous) {
            const prevButton = document.createElement('button');
            prevButton.innerHTML = 'Previous';
            prevButton.addEventListener('click', () => fetchMovies(data.previous.split('page=')[1]));
            paginationContainer.appendChild(prevButton);
        }

        if (data.next) {
            const nextButton = document.createElement('button');
            nextButton.innerHTML = 'Next';
            nextButton.addEventListener('click', () => fetchMovies(data.next.split('page=')[1]));
            paginationContainer.appendChild(nextButton);
        }
    }

    fetchMovies();
});
