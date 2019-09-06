import boto3
client = boto3.client('ec2')
response = client.describe_instances()
i = 0
u = 0
for reservation in response["Reservations"]:
    u = u+1
    k = 0
    for instance in reservation["Instances"]:
        i = i+1
        k = k+1 
        print(instance["InstanceId"])
    print("Instances in this reservation", k)
print("No. of reservations", u)
