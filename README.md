# AWS Cost Automation – T2S Test Environment

This repository contains scripts to automate the creation and cleanup of cost-driving AWS resources used for development, testing, and training.

## Features

- Create & destroy EC2, EBS, EIP, RDS, S3, and ALB resources
- Uses naming convention: `t2s-test-*`
- Works with Python (`boto3`) and Bash (AWS CLI)
- Modular automation for DevOps and Cloud teams

## Setup

```bash
git clone https://github.com/your-username/aws-cost-automation-t2s.git
cd aws-cost-automation-t2s
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file from `.env.example` and export AWS credentials.

## Scripts

| Task              | Bash                         | Python                          |
|------------------|------------------------------|----------------------------------|
| Create Resources | `scripts/create_resources.sh` | `scripts/create_resources.py`    |
| Cleanup Resources| `scripts/delete_resources.sh` | `scripts/delete_resources.py`    |

## Example

```bash
bash scripts/create_resources.sh
bash scripts/delete_resources.sh
```
