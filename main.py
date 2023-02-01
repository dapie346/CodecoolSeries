from flask import Flask, render_template, url_for, redirect, jsonify
from data import queries
import math
from functools import wraps
from dotenv import load_dotenv
from data_formatter import change_format

load_dotenv()


app = Flask('codecool_series')


def json_response(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        return jsonify(func(*args, **kwargs))
    return decorated_function


@app.route('/')
def index():
    return redirect(url_for('highest_rated'))


@app.route('/design')
def design():
    return render_template('design.html')


@app.route('/shows/<sorting_type>/', methods=['GET'])
def shows_page(sorting_type):
    if sorting_type == 'title':
        return queries.get_by_title()
    if sorting_type == 'year':
        return queries.get_by_year()
    elif sorting_type == 'runtime':
        return queries.get_by_runtime()
    elif sorting_type == 'rating':
        return queries.get_by_rating()


@app.route('/shows/most-rated', methods=['GET'])
def highest_rated():
    return render_template('shows.html')


@app.route('/show/<int:show_id>', methods=['GET'])
def display_show(show_id):
    displayed_show = queries.get_show_by_id(show_id)
    seasons = queries.get_seasons_by_show_id(show_id)
    if displayed_show:
        show = change_format(displayed_show[0])
        return render_template("show.html", show=show, seasons=seasons)
    else:
        return "Show not found", 404


def main():
    app.run(debug=False)


if __name__ == '__main__':
    main()
