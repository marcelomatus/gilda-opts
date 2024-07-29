"""gilda_opts_web implements a simple web server."""

from flask import Flask, request, jsonify
from gilda_opts.system import System
from gilda_opts.system_lp import SystemLP
from waitress import serve


# Create an instance of the Flask class
app = Flask(__name__)  # __name__ determines the root path of the application


@app.route("/process", methods=["POST"])
def process_json():
    """
    Process the JSON data from a POST request and respond with a JSON object.

    The function reads JSON data from the incoming POST request, adds a 'status' key
    to the JSON object with the value 'processed', and returns the modified JSON object.

    :return: JSON response with the modified data.
    :rtype: flask.Response
    :raises: 400 Bad Request if the incoming request does not contain valid JSON.
    """
    # Retrieves the incoming JSON request data
    data = request.data.decode("utf-8")

    if not data:
        # 400 is the HTTP status code for Bad Request
        return jsonify({"error": "Invalid or missing JSON"}), 400

    try:
        system = System.from_json(data)
    except Exception as e:  # pylint: disable=W0718
        return jsonify({"error": print(e)}), 400

    system_lp = SystemLP(system)
    status = system_lp.solve()

    if status != "ok":
        # 400 is the HTTP status code for Bad Request
        return jsonify({"error": "Invalid LP, no solution"}), 400

    sched = system_lp.get_sched()
    response_data = sched.to_json(indent=4)

    return response_data, 200  # 200 is the HTTP status code for OK


def run():
    """
    Run the Flask development server.

    This starts the Flask web server in debug mode, which provides detailed
    error messages and automatically restarts the server when code changes are
    detected.
    """
    web_ui_url = "0.0.0.0"
    port = 5012

    serve(app, host=web_ui_url, port=port, threads=8)


if __name__ == "__main__":
    """Run the app."""
    run()
