"""gilda_opts_web implements a simple web server."""

import os

from flask import Flask, jsonify, request
from waitress import serve

from gilda_opts.system import System
from gilda_opts.system_lp import SystemLP

#
# Some definitions
#

# Gilda default port
GILDAOPTS_ADDR = "0.0.0.0"
# Gilda default port
GILDAOPTS_PORT = 5012
# 400 is the HTTP status code for Bad Request
BAD_REQUEST = 400
# 200 is the HTTP status code for OK
OK_REQUEST = 200

#
# Create an instance of the Flask class
#
app = Flask(__name__)  # __name__ determines the root path of the application


@app.route("/optimize", methods=["POST"])
def optimize_json():
    """Optimize the JSON system and respond with the JSON optimal scheduling.

    :return: JSON response with the optimized scheduling.
    :rtype: flask.Response
    :raises: BAD_REQUEST Bad Request if the incoming request is not valid.

    """
    app.logger.info("Gilda-opts processing optimize request")

    # Retrieves the incoming JSON request data
    data = request.data.decode("utf-8")

    if not data:
        return jsonify({"error": "Invalid or missing JSON"}), BAD_REQUEST

    try:
        system = System.from_json(data)
    except Exception as e:  # pylint: disable=W0718
        return jsonify({"error": print(e)}), BAD_REQUEST

    system_lp = SystemLP(system)
    status = system_lp.solve()

    if status != "ok":
        return jsonify({"error": "Invalid problem, no solution"}), BAD_REQUEST

    sched = system_lp.get_sched()
    response_data = sched.to_json(indent=4)

    app.logger.info("Gilda-opts solution Ok. Processing solver time %s", sched.solver_time)
    return response_data, OK_REQUEST


def run():
    """Run the server."""
    address = os.environ.get("GILDAOPTS_ADDR", GILDAOPTS_ADDR)
    port = int(os.environ.get("GILDAOPTS_PORT", GILDAOPTS_PORT))

    app.logger.info("Launching gilda_opts server at: http://%s:%s", address, port)

    serve(app, host=address, port=port, threads=4)


if __name__ == "__main__":
    run()
