import boto3


client = boto3.client("batch", endpoint_url="http://localhost:5000", region_name='us-west-2')
print("CREATION OF ENVIRONMENT")
a = client.create_compute_environment(computeEnvironmentName="Environment_1", serviceRole="ServiceRole", type="UNMANAGED")
print(a)
print("CREATION OF JOB QUEUE")
b = client.create_job_queue(computeEnvironmentOrder=[{"computeEnvironment": "Environment_1", "order": 12}], jobQueueName="Queue_1", priority=12)
print(b)
print("REGISTERING JOB DEFINITION")
c = client.register_job_definition(
    jobDefinitionName="JobDefinition_1",
    type="container",
    containerProperties={
        "command": [],
        "environment": [],
        "image": "hello-world",
        "jobRoleArn": "jobRoleArn",
        "memory": 0,
        "mountPoints": [],
        "privileged": False,
        "readonlyRootFilesystem": False,
        "ulimits": [],
        "user": "",
        "vcpus": 0,
        "volumes": []
    }
)
print(c)
print("DESCRIBING COMPUTE ENVIRONMENTS")
print(client.describe_compute_environments(computeEnvironments=["Environment_1"]))
print("DESCRIBING JOB QUEUES")
print(client.describe_job_queues(jobQueues=["Queue_1"]))
print("DESCRIBING JOB DEFINITIONS")
print(client.describe_job_definitions(jobDefinitions=["JobDefinition_1"]))
print("RE REGISTERING JOB DEFINITION")
c = client.register_job_definition(
    jobDefinitionName="JobDefinition_1",
    type="container",
    containerProperties={
        "command": [],
        "environment": [],
        "image": "hello-world",
        "jobRoleArn": "jobRoleArn",
        "memory": 0,
        "mountPoints": [],
        "privileged": False,
        "readonlyRootFilesystem": False,
        "ulimits": [],
        "user": "",
        "vcpus": 0,
        "volumes": []
    }
)
print(c)
print("DESCRIBING JOB DEFINITIONS")
print(client.describe_job_definitions(jobDefinitions=["JobDefinition_1"]))
print("DEREGISTERING JOB DEFINITION")
print(client.deregister_job_definition(jobDefinition="JobDefinition_1:1"))
print("DESCRIBING JOB DEFINITIONS")
print(client.describe_job_definitions(jobDefinitions=["JobDefinition_1"]))
print("LISTING JOBS")
print(client.list_jobs(jobQueue="Queue_1"))
print("SUBMITTING JOB")
d = client.submit_job(
    jobDefinition="JobDefinition_1",
    jobName="Job_1",
    jobQueue="Queue_1",
)
print(d)
print("LISTING JOBS")
# print(client.list_jobs(jobQueue="Queue_1"))
# print("UPDATE COMPUTE ENVIRONMENT")
# f = client.update_compute_environment(computeEnvironment="Environment_1", state="DISABLED")
# print(f)
# print("DELETION OF COMPUTE ENVIRONMENT")
# e = client.delete_compute_environment(computeEnvironment="Environment_1")
# print(e)
