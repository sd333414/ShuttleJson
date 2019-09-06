import json, boto3
client = boto3.client('ec2')

def get_key_pair(region):
    lient = boto3.client('ec2', region_name = region)
#Get keypair for the current region. If the region has more than 2 keypairs, you need to delete one and use only one keypair.
    keypairs = client.describe_key_pairs()
    keypairs = keypairs['KeyPairs']
    if len(keypairs)==0:
        message = "You do not have a KeyPair in ", i
        return message 
    else:
        keypair = keypairs[0]['KeyName']
        return keypair

def generate_list_of_dict_instances(region):
    client = boto3.client('ec2', region_name = region)
    print(region)
#If there are no instances(in any state), return an empty list. If there is an instance in any state in this region, save the list of instances as raw_list_of_instances
    keypair = get_key_pair(region)
    list_of_dict_instances = []
    instance_number = 0
    response = client.describe_instances(Filters=[{"Name":"instance-state-name", "Values":["running"]}])
    if len(response['Reservations']) > 0:
        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                each_instance = str(instance_number)
                each_instance = {}
                command = 'ssh -i ' + '/Users/devired/Downloads/Downloads1/User_keys/'+ keypair +'.pem ' + 'ubuntu@' + instance["PublicIpAddress"]
                each_instance["cmd"]= command
                list_of_dict_instances.append(each_instance)
                list_tags_of_each_instance = instance["Tags"]
                each_instance["name"]=get_name_tag(list_tags_of_each_instance)
                each_instance["inTerminal"]= "tab"
        return(list_of_dict_instances)
    else:
            return(list_of_dict_instances)


def get_name_tag(list_tags_of_each_instance):
#Get the "name" tag of the instance
    name_key_present = 0
    for tag in list_tags_of_each_instance:
        #print(tag)
        if tag['Key'] == 'Name' :
            name_tag_of_instance=tag['Value']
            name_key_present=1
            return name_tag_of_instance
    if name_key_present==0:
        name_tag_of_instance="no_name_tag"
        return name_tag_of_instance

def modify_shuttle_json(region,region_number):
    
#Modify the shuttle.json file by passing the list of hosts from generate_list_of_instances()
    host_list=generate_list_of_dict_instances(region)
    with open('/Users/devired/.shuttle.json') as json_file:
        data = json.load(json_file)
        if region_number==0:
            data['hosts'] = host_list
        else:
            data['hosts'] = data['hosts']+host_list

    with open('/Users/devired/.shuttle.json', 'w') as json_file:
        json.dump(data,json_file)

def main():
    ec2_regions=[region['RegionName'] for region in client.describe_regions()['Regions']]
    #ec2_regions=['us-east-1','us-east-2']
    region_number = 0
    for region in ec2_regions:
        region_number=region_number+1
        modify_shuttle_json(region,region_number)

if __name__ == "__main__":
    main()
