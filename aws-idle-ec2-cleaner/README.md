
# 🧹 AWS Idle EC2 Instance Cleaner

This Python script scans EC2 instances across multiple AWS regions, identifies those that are **idle and older than a configured threshold**, and prompts for termination after displaying a detailed summary. Designed for safe, tag-aware cost optimization in multi-region environments.

---

## 🚀 Features

- ✅ Filters EC2 instances by tag (`Environment=dev` by default)
- 📊 Analyzes 30-day CPU usage with CloudWatch
- ⏳ Skips instances younger than a defined age (e.g., 30 days)
- 🧪 Dry-run style preview before termination
- 🌍 Supports multi-region scanning
- 🔐 Interactive confirmation to avoid accidental deletion

Ideal for teams aiming to reduce cloud costs without compromising operational integrity.

---

## 🛠️ Requirements

- Python 3.7+
- `boto3` library
- AWS credentials with:
  - `ec2:DescribeInstances`
  - `ec2:TerminateInstances`
  - `cloudwatch:GetMetricStatistics`

---

## ⚙️ Configuration

Update the following values directly in the script:
```python
TAG_KEY = 'Environment'       # Tag key to filter instances
TAG_VALUE = 'dev'             # Tag value to match
IDLE_THRESHOLD = 25           # Minimum number of idle days out of 30
AGE_THRESHOLD = 30            # Minimum age (days) since launch
regions = ['us-west-2', 'us-east-1', 'ap-south-1'] # Regions in which you need to clean instances
```
You can modify tag filters, thresholds, or add more regions as needed.

---

## 🧪 Dry Run Example

```
(.boto3) kishore@Kishores-MacBook-Air aws-idle-ec2-cleaner % python3 aws-idle-ec2-cleaner.py

🌐 Checking region: us-west-2

🔍 Instances Eligible for Termination:

1. i-0123456789abcdef0 | Age: 42d | Idle: 28/30 days | Tags: {'Environment': 'dev', 'Name': 'test-server'}

⚠️ Type 'yes' to proceed with termination: no

⏹️ No instances were terminated.
```
---

## ⚠️ Note

- CPU usage threshold is hardcoded at < 5% per day.
- Instances are checked for activity and age, not storage or network usage.
- Always verify the correct IAM role and region scope before use.

---

## 🙌 Contribute or Ask

Feel free to modify, fork, and adapt it to your environment.

---

## 🙋‍♂️ Author

Created by Kishore for proactive cost governance in AWS.

---
