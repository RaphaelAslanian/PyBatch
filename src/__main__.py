import json

from flask import Flask, request, jsonify, Response

from json_configuration import *

# ToDo: Gérer les certificats SSL


app = Flask(__name__)


@app.route('/', methods=["GET"])
def home_page():
    return "Hello World !", 200


@app.route("/v1/canceljob", methods=["POST"])
def cancel_job():
    data = json.loads(request.data, encoding="utf-8")
    CONFIG_CANCEL_JOB.validate(data)
    return "OK", 200


@app.route("/v1/createcomputeenvironment", methods=["POST"])
def create_compute_environment():
    data = json.loads(request.data, encoding="utf-8")
    CONFIG_CREATE_COMPUTE_ENVIRONMENT.validate(data)
    # TODO: Perform verification checks before accepting new compute environment
    # TODO: Create ARN and add it to saved data
    compute_environments[data["computeEnvironmentName"]] = data
    # TODO: correct returned values
    return jsonify({"computeEnvironmentArn": "12345", "computeEnvironmentName": "MyFirstJob2"})


@app.route("/v1/createjobqueue", methods=["POST"])
def create_job_queue():
    data = json.loads(request.data, encoding="utf-8")
    CONFIG_CREATE_JOB_QUEUE.validate(data)
    # TODO: Perform verification checks before accepting new job queue
    # TODO: Create ARN and add it to saved data
    job_queues[data["jobQueueName"]] = data
    # TODO: correct returned values
    return jsonify({"jobQueueArn": "12345", "jobQueueName": data["jobQueueName"]})


@app.route("/v1/deletecomputeenvironment", methods=["POST"])
def delete_compute_environment():
    data = json.loads(request.data, encoding="utf-8")
    CONFIG_DELETE_COMPUTE_ENVIRONMENT.validate(data)
    return "OK", 200


@app.route("/v1/deletejobqueue", methods=["POST"])
def delete_job_queue():
    pass


@app.route("/v1/deregisterjobdefinition", methods=["POST"])
def deregister_job_definition():
    pass


@app.route("/describecomputeenvironments", methods=["POST"])
def describe_compute_environments():
    pass


@app.route("/describejobdefinitions", methods=["POST"])
def describe_job_definitions():
    pass


@app.route("/describejobqueues", methods=["POST"])
def desbribe_job_queues():
    pass


@app.route("/describejobs", methods=["POST"])
def describe_jobs():
    pass


@app.route("/listjobs", methods=["POST"])
def list_jobs():
    pass


@app.route("/registerjobdefinition", methods=["POST"])
def register_job_definition():
    pass


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
    app.run(debug=True)
