from typing import Literal
import requests
import json
from flask import Flask, jsonify, request, json
from flask.wrappers import Response

app = Flask(__name__)
s = requests.Session()
sensor_dict = dict()
host = ""


@app.route("/toggle_entity", methods=["POST"])
def toggle_entity() -> tuple[Response, Literal[200]] | tuple[Response, Literal[400]]:
    if request.headers["Content-Type"] == "application/json":
        data = request.json
        token = data["token"]
        entity = data["entity"]
        entity_dict = dict()
        entity_dict["entity_id"] = entity
        r = s.post(
            f"{host}/api/services/switch/toggle",
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
            json=entity_dict,
        )

        return jsonify({"Status": "Ok"}), 200
    else:
        return jsonify({"Status": "Error"}), 400


@app.route("/sensors", methods=["POST"])
def get_sensors() -> Response | tuple[Response, Literal[400]]:
    if request.headers["Content-Type"] == "application/json":
        data = request.json
        token = data["token"]
        r = s.get(
            f"{host}/api/states",
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
        )
        js = r.json()
        return_dict = dict()
        for sensor in js:
            if sensor["entity_id"] in sensor_dict:
                return_dict[sensor_dict[sensor["entity_id"]]] = sensor["state"]

        return jsonify(return_dict)
    else:
        return jsonify({"Status": "Error"}), 400


if __name__ == "__main__":
    with open("config.json") as fd:
        json_dict = json.load(fd)
    host = json_dict["host"]
    json_dict.pop("host")
    sensor_dict = json_dict
    app.run(host="0.0.0.0", port=8888, debug=False, ssl_context="adhoc")
