# PyBatch
[![Build Status](https://travis-ci.com/RaphaelAslanian/PyBatch.svg?branch=develop)](https://travis-ci.com/RaphaelAslanian/PyBatch)

This project aims at mocking AWS Batch for local development purposes.
PyBatch reproduces AWS Batch internal logic so that the developer can test the different AWS Batch API calls locally.
The idea is to simulate the AWS Batch platform in the most transparent way possible.

## Getting Started

### Prerequisites

In order to use PyBatch you will need python >3.6 or Docker.

### Install from GitHub

After cloning the repository, you should install requirements:

```bash
pip install -r requirements.txt
```

You can now launch the PyBatch application:

```bash
python src/
```

### Launch with Docker

In order to launch the PyBatch using Docker, you first need [Docker installed](https://docs.docker.com/install/). 
Then you can launch the PyBatch container with the following command:

```bash
docker run --name <container_name> -p 5000:5000 pybatch:<version_tag>
```

For instance:

```bash
docker run --name my_first_pybatch_container -p 5000:5000 pybatch:latest
```

## Use cases

### How to use the API ? 

Since PyBatch aims at replicating AWS logic as closely as possible, it is designed to be used just like
the AWS Batch API. Therefore, to use the PyBatch API, you can refer to the [AWS Batch API documentation](https://docs.aws.amazon.com/batch/index.html#lang/en_us).

### How to run tests

Coming soon.

## Snippets

Coming soon.

## Troubleshooting

## Still Missing

- Integration with IAM policies and roles
- Multi Node jobs
- Pagination when calling _describe_ API routes

## Contributions ? 

Coming soon.
