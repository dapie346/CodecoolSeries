from flask import Flask, render_template, url_for
from data import queries
import math
from dotenv import load_dotenv

load_dotenv()


app = Flask('codecool_series')


@app.route('/')
def index():
    shows = queries.get_shows()
    print(shows)
    return render_template('index.html', shows=shows)


@app.route('/design')
def design():
    return render_template('design.html')


@app.route('/shows/most-rated', methods=['GET'])
def highest_rated():
    shows = queries.get_highest_rated()
    for show in shows:
        show['rating'] = "{:.1f}".format(show['rating'])
        show['year'] = str(show['year'])[:4]
    if shows:
        return render_template('shows.html', shows=shows)
    else:
        return "Shows not found", 404


@app.route('/show/<int:show_id>', methods=['GET'])
def display_show(show_id):
    displayed_show = queries.get_show_by_id(show_id)
    if displayed_show:
        return render_template("show.html", show=displayed_show)
    else:
        return "Show not found", 404


def main():
    app.run(debug=False)


if __name__ == '__main__':
    main()
