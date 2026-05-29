### Network Security Projects For Phising Data

**Why Python uses pyproject.toml:**
PEP 518 (2016) standardized `pyproject.toml` as the single config file for Python projects. Tools like `pip`, `black`, `ruff`, `pytest` all read from it — so instead of having separate config files for each tool, everything lives in one place.

## Installation

**Option 1 — using `pyproject.toml` (recommended):**
```bash
pip install -e .          # install project + production dependencies
pip install -e ".[dev]"   # install project + production + dev dependencies
```

**Option 2 — using `requirements.txt`:**
```bash
pip install -r requirements.txt      # install production + dev dependencies (everything)
pip install -r requirements-dev.txt  # install dev tools only
```

**Option 3 — using `setup.py` (legacy):**
```bash
python setup.py install    # install the package
python setup.py develop    # install in editable/dev mode (equivalent to pip install -e .)
python setup.py sdist      # build source distribution
python setup.py bdist_wheel # build wheel distribution
```
> Note: Running `setup.py` directly is deprecated. Prefer `pip install -e .` instead.


Setup github secrets:
AWS_ACCESS_KEY_ID=

AWS_SECRET_ACCESS_KEY=

AWS_REGION = us-east-1 # euro-west-3  etc.

AWS_ECR_LOGIN_URI = 788614365622.dkr.ecr.us-east-1.amazonaws.com/networkssecurity
ECR_REPOSITORY_NAME = networkssecurity


Docker Setup In EC2 commands to be Executed
#optinal

sudo apt-get update -y

sudo apt-get upgrade

#required

curl -fsSL https://get.docker.com -o get-docker.sh

sudo sh get-docker.sh

sudo usermod -aG docker ubuntu

newgrp docker


## Add here the ruff and blakc & task and github action integrations