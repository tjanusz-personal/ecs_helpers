# ECS Helpers
This project is a sample set of helpers I created when using ECS.

# Assumptions
This project assumes you have the following already intalled/configured

* **homebrew** - homebrew package manager
* **AWS account** - personal aws account with active credentials in ~/.aws
* **AWS ECS cluster w/Services/Tasks** - existing AWS account has ECS Cluster w/services and tasks defined
* **AWS CLI** - existing AWS CLI installed locally

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