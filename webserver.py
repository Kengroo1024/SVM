import multiprocessing

import bottle
import paste

# from main import main

app = bottle.Bottle()


@app.route("/upload", method="POST")
def upload():
    data = bottle.request.files.get("data")
    data.save(f"test/{data.filename}")
    return None


app.run(port=7735, server="paste")
