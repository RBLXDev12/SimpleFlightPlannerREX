import json
import os


BASE_PATH = os.path.join(
    os.path.dirname(__file__),
    "storage"
)


FILES = {
    "config": "config.json",
    "presets": "presets.json",
    "flights": "flights.json"
}


def ensure_storage():

    if not os.path.exists(BASE_PATH):
        os.makedirs(BASE_PATH)


    for file in FILES.values():

        path = os.path.join(BASE_PATH, file)

        if not os.path.exists(path):

            with open(path, "w") as f:
                json.dump({}, f, indent=4)



def load(name):

    ensure_storage()

    path = os.path.join(
        BASE_PATH,
        FILES[name]
    )


    with open(path, "r") as f:
        return json.load(f)



def save(name, data):

    ensure_storage()

    path = os.path.join(
        BASE_PATH,
        FILES[name]
    )


    with open(path, "w") as f:
        json.dump(
            data,
            f,
            indent=4
        )