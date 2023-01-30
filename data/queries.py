from data import data_manager


def get_shows():
    return data_manager.execute_select('SELECT id, title FROM shows;')


def get_most_rated():
    return data_manager.execute_select(
        """
        SELECT shows.id, shows.title, shows.year, shows.runtime, shows.rating, genres.name
        FROM shows
        JOIN show_genres ON shows.id = show_genres.show_id
        JOIN genres ON show_genres.genre_id = genres.id
        ORDER BY shows.rating
        DESC 
        LIMIT 15;
        """)
