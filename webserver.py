import multiprocessing
from json import dump
from time import time
from os.path import join

import bottle
import paste

# from main import main

app = bottle.Bottle()


@app.route("/upload", method="POST")
def upload():
    data = bottle.request.json
    with open(join("test", f"{int(time()*100)}.json"), "w") as f:
        dump(data, f)
    return None


app.run(port=7735, server="paste")
