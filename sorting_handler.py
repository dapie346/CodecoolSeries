SHOWS_PER_PAGE = 15


def get_shows(page, shows):
    per_page = SHOWS_PER_PAGE
    for show in shows:
        show['rating'] = str(show['rating'])[:3]
        show['year'] = str(show['year'])[:4]
    paginated_shows = shows[(int(page) - 1) * per_page:int(page) * per_page]
    return paginated_shows
