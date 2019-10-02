import json, boto3
from prog_methods import *
client = boto3.client('ec2')
def main():
    ec2_regions=[region['RegionName'] for region in client.describe_regions()['Regions']]
    region_number = 0
    for region in ec2_regions:
        modify_shuttle_json(region,region_number)
        region_number=region_number+1        
if __name__ == "__main__":
    main()


