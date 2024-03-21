import multiprocessing
import queue

import bottle
import requests

from main import main
import motor


app = bottle.Bottle()


@app.route("/upload", method="POST")
def upload():
    files = bottle.request.files
    files.get("file").save(f"test/{files.get("file").filename}")


app.run(port=7735, server="paste")
