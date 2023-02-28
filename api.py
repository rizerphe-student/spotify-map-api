"""A minimal API for retrieving the map for a given artist."""
import os
import threading

import dotenv
import flask
import spotify_minimal_client

from map import map_for_artist

dotenv.load_dotenv()

client = spotify_minimal_client.Spotify(
    client_id=os.environ["CLIENT_ID"],
    client_secret=os.environ["CLIENT_SECRET"],
)

app = flask.Flask(__name__)
maps = {}
in_progress = set()


def add_map(query: str) -> None:
    """Add a map to the cache

    Args:
        query (str): The artist name to search for.
    """
    # Probably should have used a queue or something here
    # but like eh
    if query not in in_progress:
        in_progress.add(query)
        maps[query] = map_for_artist(client, query)


@app.route("/")
def index() -> str:
    """The index form

    Returns:
        str: The HTML code for the index form.
    """
    return (
        "<form method='post'><input name='artist' type='text' />"
        "<input type='submit' /></form>"
    )


@app.route("/", methods=["POST"])
def index_post() -> flask.Response:
    """The index form, after a POST request

    Returns:
        flask.Response: A redirect to the map page.
    """
    artist = flask.request.form["artist"]
    return flask.redirect(f"/{artist}")


@app.route("/<artist>")
def artist_map(artist: str) -> str:
    """The map for an artist

    Args:
        artist (str): The artist name.

    Returns:
        str: The HTML code for the map, or an loading page.
    """
    if artist not in maps:
        threading.Thread(target=add_map, args=[artist]).start()
        return "<meta http-equiv='refresh' content='2'><h1>Generating map...</h1>"
    return maps[artist] or "<h1>No artist found</h1>"


if __name__ == "__main__":
    app.run(debug=True)
