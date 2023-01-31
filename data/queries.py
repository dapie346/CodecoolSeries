from data import data_manager


def get_shows():
    return data_manager.execute_select('SELECT id, title FROM shows;')


def get_highest_rated():
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


def get_show_by_id(show_id):
    return data_manager.execute_select(
        """
        SELECT * FROM shows WHERE id= %(show_id)s;
        """
        , {'show_id': show_id})
