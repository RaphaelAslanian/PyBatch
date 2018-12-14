import json
from _blake2 import blake2b

from flask import Flask, request, jsonify
from schema import SchemaError
from werkzeug.exceptions import abort

from compute_environment import ComputeEnvironment
from job_definition import JobDefinition
from job_queue import JobQueue
from json_configuration import *

# ToDo: Gérer les certificats SSL


app = Flask(__name__)


@app.route('/', methods=["GET"])
def home_page():
    return "Hello World !", 200


@app.route("/v1/canceljob", methods=["POST"])
def cancel_job():
    pass


@app.route("/v1/createcomputeenvironment", methods=["POST"])
def create_compute_environment():
    data = json.loads(request.data, encoding="utf-8")
    CONFIG_CREATE_COMPUTE_ENVIRONMENT.validate(data)
    if data["computeEnvironmentName"] in compute_environments:
        abort(400, "Compute environment already exists.")
    compute_environments[data["computeEnvironmentName"]] = ComputeEnvironment(**data)
    return jsonify(
        {
            "computeEnvironmentArn": data["computeEnvironmentName"],
            "computeEnvironmentName": data["computeEnvironmentName"]
        }
    )


@app.route("/v1/createjobqueue", methods=["POST"])
def create_job_queue():
    data = json.loads(request.data, encoding="utf-8")
    CONFIG_CREATE_JOB_QUEUE.validate(data)
    # Checks
    if data["jobQueueName"] in job_queues:
        abort(400, "Job queue already exists.")
    for ce in data["computeEnvironmentOrder"]:
        if ce["computeEnvironment"] not in compute_environments:
            abort(400, f"Compute environment {ce} does not exist")
        if compute_environments[ce["computeEnvironment"]].state != "ENABLED":
            abort(400, f"Compute environment {ce} is not enabled.")
    if not (0 < len(data["computeEnvironmentOrder"]) < 3):
        abort(400, f"Invalid number ({len(data['computeEnvironmentOrder'])}) of compute environments selected")
    orders = set()
    for ce in data["computeEnvironmentOrder"]:
        if ce["order"] in orders:
            abort(400, f"Two compute environments have the same order.")
        orders.add(ce["order"])
    # Action
    job_queues[data["jobQueueName"]] = JobQueue(**data)
    return jsonify({"jobQueueArn": data["jobQueueName"], "jobQueueName": data["jobQueueName"]})


@app.route("/v1/deletecomputeenvironment", methods=["POST"])
def delete_compute_environment():
    data = json.loads(request.data, encoding="utf-8")
    CONFIG_DELETE_COMPUTE_ENVIRONMENT.validate(data)
    if data["computeEnvironment"] not in compute_environments:
        abort(400, "Compute environment does not exist.")
    if compute_environments[data["computeEnvironment"]].state != "DISABLED":
        abort(400, "Compute environment is not disabled.")
    for jq in job_queues.values():
        if data["computeEnvironment"] in [ce_jq["computeEnvironment"] for ce_jq in jq["computeEnvironmentOrder"]]:
            abort(400, f"Compute environment still active in jobQueue {jq['JobQueue']}")
    compute_environments.pop(data["computeEnvironment"])
    return jsonify({})


@app.route("/v1/deletejobqueue", methods=["POST"])
def delete_job_queue():
    data = json.loads(request.data, encoding="utf-8")
    CONFIG_DELETE_JOB_QUEUE.validate(data)
    if data["jobQueue"] not in job_queues:
        abort(400, "Job queue does not exist")
    job_queues.pop(data["jobQueueName"])
    return jsonify({})


@app.route("/v1/deregisterjobdefinition", methods=["POST"])
def deregister_job_definition():
    data = json.loads(request.data, encoding="utf-8")
    CONFIG_DEREGISTER_JOB_DEFINITION.validate(data)
    if data["jobDefinition"] not in job_definitions:
        abort(400, "Job definition does not exist.")
    job_definitions.pop(data["jobDefinition"])
    return jsonify({})


@app.route("/v1/describecomputeenvironments", methods=["POST"])
def describe_compute_environments():
    res = [repr(val) for val in compute_environments.values()]
    res = {"computeEnvironments": res, "nextToken": "nextToken"}
    return jsonify(res)


@app.route("/v1/describejobdefinitions", methods=["POST"])
def describe_job_definitions():
    res = [repr(val) for val in job_definitions.values()]
    res = {"jobDefinitions": res, "nextToken": "nextToken"}
    return jsonify(res)


@app.route("/v1/describejobqueues", methods=["POST"])
def desbribe_job_queues():
    res = [repr(val) for val in job_queues.values()]
    res = {"jobQueues": res, "nextToken": "nextToken"}
    return jsonify(res)


@app.route("/describejobs", methods=["POST"])
def describe_jobs():
    pass


@app.route("/listjobs", methods=["POST"])
def list_jobs():
    pass


@app.route("/v1/registerjobdefinition", methods=["POST"])
def register_job_definition():
    data = json.loads(request.data, encoding="utf-8")
    try:
        CONFIG_REGISTER_JOB_DEFINITION.validate(data)
    except SchemaError as se:
        abort(400, f"Invalid request {se}")
    if data["jobDefinitionName"] in job_definitions:
        abort(400, "Job definition does exist")
    job_definitions[data["jobDefinitionName"]] = JobDefinition(**data)
    return jsonify({})


@app.route("/submitjob", methods=["POST"])
def submit_job():
    pass


@app.route("/terminatejob", methods=["POST"])
def terminate_job():
    pass


@app.route("/updatecomputeenvironment", methods=["POST"])
def update_compute_environment():
    pass


@app.route("/updatejobqueue", methods=["POST"])
def update_job_queue():
    pass


if __name__ == "__main__":
    compute_environments = {}
    job_queues = {}
    job_definitions = {}
    jobs = {}
    # app.run(ssl_context=('server.crt', 'server.key'))
    # app.run(ssl_context=('cert.pem', 'key.pem'))
    app.run(debug=True, threaded=True)
