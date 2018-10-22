import json

from flask import Flask, request
from schema import Schema, Optional

# ToDo: Gérer les certificats SSL

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
        Optional("computeResources"): Schema(
            {
                "bidPercentage": int,
                "desiredvCpus": int,
                "ec2KeyPair": str,
                "imageId": str,
                "instanceRole": str,
                "instanceTypes": [str],
                "maxvCpus": int,
                "minvCpus": int,
                "securityGroupIds": [str],
                "spotIamFleetRole": str,
                "subnets": [str],
                "tags": {str: str},
            }
        ),
        "serviceRole": str,
        Optional("state"): str,
        "type": str
    },
    ignore_extra_keys=False
)

CONFIG_CREATE_JOB_QUEUE = Schema(
    {
        "computeEnvironmentOrder": [
            Schema(
                {
                    "computeEnvironment": str,
                    "order": int
                }
            )
        ],
        "jobQueueName": str,
        "priority": int,
        Optional("state"): str,
    },
    ignore_extra_keys=False
)

CONFIG_DELETE_COMPUTE_ENVIRONMENT = Schema(
    {
        "computeEnvironment": str
    },
    ignore_extra_keys=False
)

CONFIG_DELETE_JOB_QUEUE = Schema(
    {
        "jobQueue": str
    },
    ignore_extra_keys=False
)

CONFIG_DEREGISTER_JOB_DEFINITION = Schema(
    {
        "jobDefinition": str
    },
    ignore_extra_keys=False
)

CONFIG_DESCRIBE_COMPUTE_ENVIRONMENTS = Schema(
    {
        Optional("computeEnvironments"): [str],
        Optional("maxResults"): int,
        Optional("nextToken"): str,
    },
    ignore_extra_keys=False
)

CONFIG_DESCRIBE_JOB_DEFINITIONS = Schema(
    {
        Optional("jobDefinitionName"): str,
        Optional("jobDefinitions"): [str],
        Optional("maxResults"): int,
        Optional("nextToken"): str,
        Optional("status"): str,
    },
    ignore_extra_keys=False
)

CONFIG_DESCRIBE_JOB_QUEUES = Schema(
    {
        Optional("jobQueues"): [str],
        Optional("maxResults"): int,
        Optional("nextToken"): str,
    },
    ignore_extra_keys=False
)

CONFIG_DESCRIBE_JOBS = Schema({"jobs": [str]}, ignore_extra_keys=False)

CONFIG_LIST_JOBS = Schema(
    {
       Optional("arrayJobId"): str,
       Optional("jobQueue"): str,
       Optional("jobStatus"): str,
       Optional("maxResults"): int,
       Optional("nextToken"): str,
    },
    ignore_extra_keys=False
)

CONFIG_REGISTER_JOB_DEFINITION = Schema(
    {
        Optional("containerProperties"): Schema(
            {
                "command": [str],
                "environment": [Schema({"name": str, "value": str})],
                "image": str,
                "jobRoleArn": str,
                "memory": int,
                "mountPoints": [Schema({"containerPath": str, "readOnly": bool, "sourceVolume": str})],
                "privileged": bool,
                "readonlyRootFilesystem": bool,
                "ulimits": [Schema({"hardLimit": int, "name": str, "softLimit": int})],
                "user": str,
                "vcpus": int,
                "volumes": [Schema({"host": Schema({"sourcePath": str}), "name": str})],
            }
        ),
        "jobDefinitionName": str,
        Optional("parameters"): {str: str},
        Optional("retryStrategy"): Schema({"attempts": int}),
        Optional("timeout"): Schema({"attemptDurationSeconds": int}),
        "type": str
    },
    ignore_extra_keys=False
)

CONFIG_SUBMIT_JOB = Schema(
    {
        Optional("arrayProperties"): Schema({"size": int}),
        Optional("containerOverrides"): Schema(
            {
                "command": [str],
                "environment": [Schema({"name": str, "value": str})],
                "memory": int,
                "vcpus": int,
            }
        ),
        Optional("dependsOn"): [Schema({"jobId": str, "type": str})],
        "jobDefinition": str,
        "jobName": str,
        "jobQueue": str,
        Optional("parameters"): {str: str},
        Optional("retryStrategy"): Schema({"attempts": int}),
        Optional("timeout"): Schema({"attemptDurationSeconds": int}),
    },
    ignore_extra_keys=False
)

CONFIG_TERMINATE_JOB = Schema(
    {
        "jobId": str,
        "reason": str
    },
    ignore_extra_keys=False
)

CONFIG_UPDATE_COMPUTE_ENVIRONMENT = Schema(
    {
        "computeEnvironment": str,
        Optional("computeResources"): Schema({"desiredvCpus": int, "maxcCpus": int, "minvCpus": int}),
        Optional("serviceRole"): str,
        Optional("state"): str
    },
    ignore_extra_keys=False
)

CONFIG_UPDATE_JOB_QUEUE = Schema(
    {
        Optional("computeEnvironmentOrder"): [Schema({"computeEnvironment": str, "order": int})],
        "jobQueue": str,
        Optional("priority"): int,
        Optional("state"): str
    },
    ignore_extra_keys=False
)

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
    return "OK", 200


@app.route("/v1/createjobqueue", methods=["POST"])
def create_job_queue():
    data = json.loads(request.data, encoding="utf-8")
    CONFIG_CREATE_JOB_QUEUE.validate(data)
    return "OK", 200


@app.route("/v1/deletecomputeenvironment", methods=["POST"])
def delete_compute_environment():
    pass


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
    # app.run(ssl_context=('server.crt', 'server.key'))
    # app.run(ssl_context=('cert.pem', 'key.pem'))
    app.run(debug=True)
