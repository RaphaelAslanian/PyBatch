from schema import Schema, Optional


CONFIG_CANCEL_JOB = Schema(
    {
        "jobId": str,
        "reason": str
    },
    ignore_extra_keys=False
)

CONFIG_CREATE_COMPUTE_ENVIRONMENT = Schema(
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