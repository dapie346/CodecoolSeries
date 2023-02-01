from data import data_manager


def get_shows():
    return data_manager.execute_select('SELECT id, title FROM shows;')


def get_by_rating():
    return data_manager.execute_select(
        """
        SELECT shows.id as show_id, shows.title, shows.year, shows.runtime, shows.trailer, shows.homepage, AVG(shows.rating) as rating,
       string_agg(genres.name, ', ') as genres
        FROM shows
        JOIN show_genres ON shows.id = show_genres.show_id
        JOIN genres ON show_genres.genre_id = genres.id
        GROUP BY shows.id, shows.title, shows.year, shows.runtime, shows.trailer, shows.homepage
        ORDER BY AVG(shows.rating) DESC
        
        """)


def get_by_runtime():
    return data_manager.execute_select(
        """
        SELECT shows.id as show_id, shows.title, shows.year, shows.runtime, shows.trailer, shows.homepage, AVG(shows.rating) as rating,
       string_agg(genres.name, ', ') as genres
        FROM shows
        JOIN show_genres ON shows.id = show_genres.show_id
        JOIN genres ON show_genres.genre_id = genres.id
        GROUP BY shows.id, shows.title, shows.year, shows.runtime, shows.trailer, shows.homepage
        ORDER BY shows.runtime DESC

        """)


def get_by_title():
    return data_manager.execute_select(
        """
        SELECT shows.id as show_id, shows.title, shows.year, shows.runtime, shows.trailer, shows.homepage, 
        AVG(shows.rating) as rating, string_agg(genres.name, ', ') as genres
        FROM shows
        JOIN show_genres ON shows.id = show_genres.show_id
        JOIN genres ON show_genres.genre_id = genres.id
        GROUP BY shows.id, shows.title, shows.year, shows.runtime, shows.trailer, shows.homepage
        ORDER BY shows.title DESC

        """)


def get_by_year():
    return data_manager.execute_select(
        """
        SELECT shows.id as show_id, shows.title, shows.year, shows.runtime, shows.trailer, shows.homepage, AVG(shows.rating) as rating,
       string_agg(genres.name, ', ') as genres
        FROM shows
        JOIN show_genres ON shows.id = show_genres.show_id
        JOIN genres ON show_genres.genre_id = genres.id
        GROUP BY shows.id, shows.title, shows.year, shows.runtime, shows.trailer, shows.homepage
        ORDER BY shows.year DESC

        """)


def get_show_by_id(show_id):
    return data_manager.execute_select(
        """
        SELECT
            AVG(shows.runtime) AS avg_runtime,
            shows.rating AS rating,
            STRING_AGG(DISTINCT genres.name, ', ' ORDER BY genres.name) AS genres,
            STRING_AGG(DISTINCT actors.name, ', ' ORDER BY actors.name) AS actors,
            shows.title,
            shows.trailer,
            shows.overview,
            shows.year
        FROM
            shows
        JOIN
            show_genres ON show_genres.show_id = shows.id
        JOIN
            genres ON genres.id = show_genres.genre_id
        JOIN
            show_characters ON show_characters.show_id = shows.id
        JOIN
            actors ON actors.id = show_characters.actor_id
        WHERE
            shows.id = %(show_id)s
        GROUP BY
            shows.id, shows.rating, shows.trailer, shows.overview, shows.year;
        """
        , {'show_id': show_id})


def get_seasons_by_show_id(show_id):
    return data_manager.execute_select(
        """
        SELECT season_number, title, overview
        FROM seasons
        WHERE show_id = %(show_id)s;
        """
        , {'show_id': show_id})
