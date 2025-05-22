# AWS Cost Automation – T2S Test Environment

This repository contains scripts to automate the creation and cleanup of cost-driving AWS resources used for development, testing, and training.

The scripts are tools I use to automate the creation and cleanup of unwanted resources to help my clients reduce spending as they use Cloud services.
 

## Features

- Create & destroy **EC2, EBS, EIP, RDS, S3, ALB**, or other Cloud resources
- Uses naming convention: `t2s-test-*`
- Works with **Python (`boto3`)** and **Bash (AWS CLI)**
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

---
## <div align="center">About the Author</div>

<div align="center">
  <img src="assets/emmanuel-naweji.jpg" alt="Emmanuel Naweji" width="120" height="120" style="border-radius: 50%;" />
</div>

**Emmanuel Naweji** is a **seasoned Cloud, DevOps, and SRE Engineer** with years of experience helping companies architect and deploy secure, scalable infrastructure. He is the founder of initiatives that train and mentor individuals seeking careers in IT and has helped hundreds transition into Cloud, DevOps, and Infrastructure roles.

- Book a free consultation: [https://here4you.setmore.com](https://here4you.setmore.com)
- Connect on LinkedIn: [https://www.linkedin.com/in/ready2assist/](https://www.linkedin.com/in/ready2assist/)

Let's connect and discuss how I can help you build reliable, automated infrastructure the right way.

---

MIT License © 2025 Emmanuel Naweji

You are free to use, copy, modify, merge, publish, distribute, sublicense, or sell copies of this software and its associated documentation files (the “Software”), provided that the copyright and permission notice appears in all copies or substantial portions of the Software.

This Software is provided “as is,” without any warranty — express or implied — including but not limited to merchantability, fitness for a particular purpose, or non-infringement. In no event will the authors be liable for any claim, damages, or other liability arising from the use of the Software.
