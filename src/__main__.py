import json
import logging

import coloredlogs
from flask import Flask, request, jsonify
from schema import SchemaError
from werkzeug.exceptions import abort

from compute_environment import ComputeEnvironment
from job import Job
from job_definition import JobDefinition
from job_queue import JobQueue
from json_configuration import CONFIG_CREATE_COMPUTE_ENVIRONMENT, CONFIG_CREATE_JOB_QUEUE, \
    CONFIG_DELETE_COMPUTE_ENVIRONMENT, CONFIG_DELETE_JOB_QUEUE, CONFIG_DEREGISTER_JOB_DEFINITION, \
    CONFIG_DESCRIBE_COMPUTE_ENVIRONMENTS, CONFIG_DESCRIBE_JOB_DEFINITIONS, CONFIG_DESCRIBE_JOB_QUEUES, \
    CONFIG_LIST_JOBS, CONFIG_REGISTER_JOB_DEFINITION, CONFIG_SUBMIT_JOB

# ToDo: Gérer les certificats SSL
# ToDo: Implement orders inside queues - compute environments (Almost done)
# ToDO: Kill threads
# ToDo: return coherent values for AWS calls
# ToDo: add documentation
# ToDo: handle dependencies
# ToDo: add tests
# ToDO: add login
# ToDo: add UI
# ToDo: add linter
# ToDo: possible ThreadPool somewhere ?
# ToDo: handle tokens
# ToDo: handle multiNode jobs
# ToDo: handle arrayJob


from scheduler import Scheduler

app = Flask(__name__)


@app.route("/v1/canceljob", methods=["POST"])
def cancel_job():
    pass


@app.route("/v1/createcomputeenvironment", methods=["POST"])
def create_compute_environment():
    data = json.loads(request.data, encoding="utf-8")
    # Check
    CONFIG_CREATE_COMPUTE_ENVIRONMENT.validate(data)
    if data["computeEnvironmentName"] in compute_environments:
        abort(400, "Compute environment already exists.")
    # Action
    new_compute_environment = ComputeEnvironment(**data)
    compute_environments[data["computeEnvironmentName"]] = new_compute_environment
    new_compute_environment.start()
    return jsonify(new_compute_environment.describe(everything=False))


@app.route("/v1/createjobqueue", methods=["POST"])
def create_job_queue():
    data = json.loads(request.data, encoding="utf-8")
    # Checks
    CONFIG_CREATE_JOB_QUEUE.validate(data)
    if data["jobQueueName"] in job_queues:
        abort(400, "Job queue already exists.")
    for ce in data["computeEnvironmentOrder"]:
        if ce["computeEnvironment"] not in compute_environments:
            abort(400, f"Compute environment {ce} does not exist")
        if compute_environments[ce["computeEnvironment"]].state != ComputeEnvironment.STATE_ENABLED:
            abort(400, f"Compute environment {ce} is not enabled.")
    if not (0 < len(data["computeEnvironmentOrder"]) < 3):
        abort(400, f"Invalid number ({len(data['computeEnvironmentOrder'])}) of compute environments selected")
    orders = set()
    for ce in data["computeEnvironmentOrder"]:
        if ce["order"] in orders:
            abort(400, f"Two compute environments have the same order.")
        orders.add(ce["order"])
    # Action
    new_job_queue = JobQueue(**data)
    job_queues[data["jobQueueName"]] = new_job_queue
    return jsonify(new_job_queue.describe(everything=False))


@app.route("/v1/deletecomputeenvironment", methods=["POST"])
def delete_compute_environment():
    data = json.loads(request.data, encoding="utf-8")
    CONFIG_DELETE_COMPUTE_ENVIRONMENT.validate(data)
    if data["computeEnvironment"] not in compute_environments:
        abort(400, "Compute environment does not exist.")
    if compute_environments[data["computeEnvironment"]].state != ComputeEnvironment.STATE_DISABLED:
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
    job_queues.pop(job_queues[data["jobQueue"]])
    return jsonify({})


@app.route("/v1/deregisterjobdefinition", methods=["POST"])
def deregister_job_definition():
    # ToDo: data sent must be of format 'jobDefinitionName:revision' --> needs checking OR Arn
    data = json.loads(request.data, encoding="utf-8")
    # Checks
    CONFIG_DEREGISTER_JOB_DEFINITION.validate(data)
    job_definition_name, revision_to_remove = data["jobDefinition"].split(":")
    revision_to_remove = int(revision_to_remove)
    if job_definition_name not in job_definitions:
        abort(400, "Job Definition does not exist")
    if revision_to_remove not in [jd.revision for jd in job_definitions[job_definition_name]]:
        abort(400, "Revision of this job definition does not exist")
    to_remove = None
    for jd in job_definitions[job_definition_name]:
        if jd.revision == revision_to_remove:
            to_remove = jd
            break
    job_definitions[job_definition_name].remove(to_remove)
    return jsonify({})


@app.route("/v1/describecomputeenvironments", methods=["POST"])
def describe_compute_environments():
    data = json.loads(request.data, encoding="utf-8")
    CONFIG_DESCRIBE_COMPUTE_ENVIRONMENTS.validate(data)
    if data["computeEnvironments"]:
        ce_to_describe = [compute_environments[ce_name].describe(everything=True)
                          for ce_name in data["computeEnvironments"] if ce_name in compute_environments]
    else:
        ce_to_describe = [ce.describe() for ce in compute_environments.values()]
    res = {"computeEnvironments": ce_to_describe, "nextToken": "nextToken"}
    return jsonify(res)


@app.route("/v1/describejobdefinitions", methods=["POST"])
def describe_job_definitions():
    data = json.loads(request.data, encoding="utf-8")
    CONFIG_DESCRIBE_JOB_DEFINITIONS.validate(data)
    if data["jobDefinitions"]:
        jd_to_describe = [job_definitions[jd_name] for jd_name in data["jobDefinitions"] if jd_name in job_definitions]
    else:
        jd_to_describe = job_definitions.values()
    jds = [revision.describe(everything=True) for jd in jd_to_describe for revision in jd]
    res = {"jobDefinitions": jds, "nextToken": "nextToken"}
    return jsonify(res)


@app.route("/v1/describejobqueues", methods=["POST"])
def describe_job_queues():
    data = json.loads(request.data, encoding="utf-8")
    CONFIG_DESCRIBE_JOB_QUEUES.validate(data)
    if data["jobQueues"]:
        queues_to_describe = [
            job_queues[queue_name].describe(everything=True)
            for queue_name in data["jobQueues"] if queue_name in job_queues
        ]
    else:
        queues_to_describe = [queue.describe(everything=True) for queue in job_queues.values()]
    res = {"jobQueues": queues_to_describe, "nextToken": "nextToken"}
    return jsonify(res)


@app.route("/describejobs", methods=["POST"])
def describe_jobs():
    pass


@app.route("/v1/listjobs", methods=["POST"])
def list_jobs():
    data = json.loads(request.data, encoding="utf-8")
    CONFIG_LIST_JOBS.validate(data)
    if data["jobQueue"] not in job_queues:
        abort(400, "Job queue does not exist")
    job_summary_list = [job.summary() for job in jobs.values() if job.jobQueue == data["jobQueue"]]
    res = {"jobSummaryList": job_summary_list, "nextToken": "nextToken"}
    return jsonify(res)


@app.route("/v1/registerjobdefinition", methods=["POST"])
def register_job_definition():
    data = json.loads(request.data, encoding="utf-8")
    try:
        CONFIG_REGISTER_JOB_DEFINITION.validate(data)
    except SchemaError as se:
        abort(400, f"Invalid request {se}")
    # Action
    if data["jobDefinitionName"] in job_definitions:
        new_job_revision = len(job_definitions[data["jobDefinitionName"]]) + 1
        new_job = JobDefinition(revision=new_job_revision, **data)
        job_definitions[data["jobDefinitionName"]].append(new_job)
    else:
        new_job_revision = 1
        new_job = JobDefinition(revision=new_job_revision, **data)
        job_definitions[data["jobDefinitionName"]] = [new_job]
    return jsonify(new_job.describe(everything=False))


@app.route("/v1/submitjob", methods=["POST"])
def submit_job():
    data = json.loads(request.data, encoding="utf-8")
    try:
        CONFIG_SUBMIT_JOB.validate(data)
    except SchemaError as se:
        abort(400, f"Invalid request {se}")
    if data["jobDefinition"] not in job_definitions:
        abort(400, f"Job definition {data['jobDefinition']} does not exist.")
    if data["jobQueue"] not in job_queues:
        abort(400, f"Job queue {data['jobQueue']} does not exist.")
    data["jobDefinitionData"] = job_definitions[data["jobDefinition"]][-1]
    job = Job(**data)
    jobs[data["jobDefinition"]] = job
    job_queues[data["jobQueue"]].put_nowait(job)
    return jsonify({})


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
    coloredlogs.install(level="INFO", fmt="%(asctime)s %(name)s %(levelname)s - %(message)s", datefmt="%d-%b-%y %H:%M:%S")
    logger = logging.getLogger("MainApplication")
    compute_environments = {}
    job_queues = {}
    job_definitions = {}
    jobs = {}
    scheduler = Scheduler(job_queues, compute_environments)
    scheduler.start()
    try:
        # app.run(ssl_context=('server.crt', 'server.key'))
        # app.run(ssl_context=('cert.pem', 'key.pem'))
        app.run(debug=True, threaded=True, host="0.0.0.0")
    except KeyboardInterrupt:
        pass
    finally:
        scheduler.stop_event.set()
        for ce in compute_environments.values():
            ce.stop_event.set()
