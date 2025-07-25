import boto3
from datetime import datetime, timedelta, timezone

ec2 = boto3.client('ec2')
cloudwatch = boto3.client('cloudwatch')

# Config
TAG_KEY = 'Environment'
TAG_VALUE = 'dev'
IDLE_THRESHOLD = 00 # min idle days in 30
AGE_THRESHOLD = 00 # min age in days

now = datetime.now(timezone.utc)
termination_candidates = []

# Define regions to check
regions = ['us-west-2', 'us-east-1', 'ap-south-1']  # Add/modify as needed

for region in regions:
    print(f"\n🌐 Checking region: {region}")
    ec2 = boto3.client('ec2', region_name=region)
    cloudwatch = boto3.client('cloudwatch', region_name=region)

    # Step 1: Get running instances with specific tag
    instances = ec2.describe_instances(
        Filters=[
            {'Name': 'instance-state-name', 'Values': ['running']},
            {'Name': f'tag:{TAG_KEY}', 'Values': [TAG_VALUE]}
        ]
    )

    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            instance_launch_time = instance['LaunchTime']
            age_days = (now - instance_launch_time).days

            if age_days < AGE_THRESHOLD:
                continue

            # Step 2: Get CPU utilization
            cpu_data = cloudwatch.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='CPUUtilization',
                Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
                StartTime=now - timedelta(days=30),
                EndTime=now,
                Period=86400,
                Statistics=['Average']
            )

            datapoints = cpu_data['Datapoints']
            idle_days = sum(1 for dp in datapoints if dp['Average'] < 5.0)

            # Check if the instance is idle for the threshold period
            if idle_days >= IDLE_THRESHOLD:
                tags = {t['Key']: t['Value'] for t in instance.get('Tags', [])}
                termination_candidates.append({
                    'InstanceId': instance_id,
                    'Age': age_days,
                    'IdleDays': idle_days,
                    'Tags': tags
                })

    # Step 3: Show instances and ask for confirmation
    if termination_candidates:
        print("\n🔍 Instances Eligible for Termination:\n")
        for i, inst in enumerate(termination_candidates, 1):
            print(f"{i}. {inst['InstanceId']} | Age: {inst['Age']}d | Idle: {inst['IdleDays']}/30 days | Tags: {inst['Tags']}")

        confirm = input("\n⚠️ Type 'yes' to proceed with termination: ").strip().lower()
        if confirm == 'yes':
            for inst in termination_candidates:
                ec2.terminate_instances(InstanceIds=[inst['InstanceId']])
                print(f"✅ Terminated: {inst['InstanceId']}")
                termination_candidates = []
        else:
            print("\n⏹️ No instances were terminated.")
            termination_candidates = []
    else:
        print("✅ No eligible instances found.")
    # End of script