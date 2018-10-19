import json

from flask import Flask, request
from schema import Schema, Optional

app = Flask(__name__)

CONFIG_CANCEL_JOB = Schema(
    {
        "jobId": str,
        "reason": str
    },
    ignore_extra_keys=False
)

CONFIG_CREATE_COMPUTE_ENVIRONMENT = Schema(  # Todo Review the types and the required here
    {
        "computeEnvironmentName": str,
        Optional("computeResources"): str,
        "serviceRole": str,
        Optional("state"): str,
        "type": str
    },
    ignore_extra_keys=False
)


@app.route('/', methods=["GET"])
def home_page():
    return "Welcome"


@app.route("/v1/canceljob", methods=["POST"])
def cancel_job():
    data = json.loads(request.data, encoding="utf-8")
    CONFIG_CANCEL_JOB.validate(data)
    return "OK", 200


@app.route("/v1/createcomputeenvironment", methods=["POST"])
def create_compute_environment():
    data = json.loads(request.data, encoding="utf-8")
    CONFIG_CREATE_COMPUTE_ENVIRONMENT.validate(data)
    return "OK", 200

@app.route("/createjobqueue")
def create_job_queue():
    pass


@app.route("/deletecomputeenvironment")
def delete_compute_environment():
    pass


@app.route("/deletejobqueue")
def delete_job_queue():
    pass


@app.route("/deregistercomputeenvironment")
def deregister_compute_environment():
    pass


@app.route("/describejobdefinitions")
def describe_job_definitions():
    pass


@app.route("/describejobqueues")
def desbribe_job_queues():
    pass


@app.route("/describejobs")
def describe_jobs():
    pass


@app.route("/listjobs")
def list_jobs():
    pass


@app.route("/registerjobdefinition")
def register_job_definition():
    pass


@app.route("/submitjob")
def submit_job():
    pass


@app.route("/terminatejob")
def terminate_job():
    pass


@app.route("/updatecomputeenvironment")
def update_compute_environment():
    pass


@app.route("/updatejobqueue")
def update_job_queue():
    pass


if __name__ == "__main__":
    # app.run(ssl_context=('server.crt', 'server.key'))
    # app.run(ssl_context=('cert.pem', 'key.pem'))
    app.run(debug=True)
