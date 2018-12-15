import boto3


client = boto3.client("batch", endpoint_url="http://localhost:5000", region_name='us-west-2')
client.create_compute_environment(computeEnvironmentName="Environment_1", serviceRole="ServiceRole", type="UNMANAGED")
client.create_job_queue(computeEnvironmentOrder=[{"computeEnvironment": "Environment_1", "order": 12}], jobQueueName="Queue_1", priority=12)
client.register_job_definition(
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
        "user": "RaphaelAslanian",
        "vcpus": 0,
        "volumes": []
    }
)
client.submit_job(
    jobDefinition="JobDefinition_1",
    jobName="Job_1",
    jobQueue="Queue_1",
)
print(client.describe_compute_environments())
