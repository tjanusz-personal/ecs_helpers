# ECS Helpers
This project is a sample set of helpers I created when using ECS.

Basic Use Cases:
 * I need a listing of all task arns with their associated docker images being executed on them
 * I need to ask inspector2 which currently ECS tasks have images with HIGH/CRITICAL security events being reported
 * I need to figure out which currently running ECS tasks' docker images don't match our current base image standard

Utils include:
 * **docker_image_analyzer** - extracts out docker image info from the full ECS returned image info string (e.g. image location, full tag, base tag)
 * **ecs_utils** - ECS cluster commands to look for running tasks and pull out docker files running in their container so can get image info
 * **inspector2_utils** - AWS inspector wrapper to look for listing of critical/high findings being reported for a given set of docker hashes

# Assumptions
This project assumes you have the following already intalled/configured

* **homebrew** - homebrew package manager
* **AWS account** - personal aws account with active credentials in ~/.aws
* **AWS ECS cluster w/Services/Tasks** - existing AWS account has ECS Cluster w/services and tasks defined
* **AWS CLI** - existing AWS CLI installed locally
* **AWS Inspector2 running against images w/in docker repo**

## Python Setup

```bash
# install python 3.9
brew install python@3.9

# verify version is install
python3 --version

# location
which python3
# /opt/homebrew/bin/python3

### create venv to install packages
# Create directory for venvs
mkdir python_virtualenvs
cd python_virtualenvs

# create venv for all our stuff (ecs_helpers_env)
python3 -m venv ecs_helpers_env

# activate this env
source ecs_helpers_env/bin/activate

# or if running from other directory (ecs_helpers)
source ../python_virtualenvs/ecs_helpers_env/bin/activate
# verify python location
which python3
# xxxxxxx/python_virtualenvs/ecs_helpers_env/bin/python3

```

## Python Requirements
With an active virutal env configured load the required packages via the requirements.txt file.

I'm doing this to keep them separate from my global python installations!

```bash
pip install -r requirements.txt

```

## Unit Testing
I created some simple pytest unit tests to help me ensure I'm creating the correct sturctures in my code.

```bash
# run at command line (and show output)
python -m pytest tests -s
```

I also have some 'unit' tests that invoke actual AWS endpoints. These are automatically disabled by default. Refer to conftest.py.

```bash
# run all tests (including aws_integration tests)
python -m pytest tests -s --aws_integration

# run only the aws integration tests
python -m pytest tests -s -m aws_integration --aws_integration

# run only the aws_integration test for a given py test file.
python -m pytest tests/test_inspector2Utils.py -s -m aws_integration --aws_integration
```

