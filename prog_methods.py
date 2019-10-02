import json, boto3
client = boto3.client('ec2')

#Get keypair for the current region. If the region has more than two keypairs, you need to delete one and use only one keypair.
def get_key_pair(region):
    client = boto3.client('ec2', region_name = region)
    keypairs = client.describe_key_pairs()
    keypairs = keypairs['KeyPairs']
    if len(keypairs)==0:
        message = "You do not have a KeyPair in ", region
        return message 
    else:
        keypair = keypairs[0]['KeyName']
        return keypair

#Get the "name" tag of the instance
def get_name_tag(list_tags_of_each_instance):
    name_key_present = 0
    for tag in list_tags_of_each_instance:
        if tag['Key'] == 'Name' :
            name_tag_of_instance=tag['Value']
            name_key_present=1
            return name_tag_of_instance
    if name_key_present==0:
        name_tag_of_instance="no_name_tag"
        return name_tag_of_instance

#Modify the shuttle.json file by passing the list of hosts from generate_list_of_instances()
def modify_shuttle_json(region,region_number):
    host_list=generate_list_of_dict_instances(region)
    with open('/Users/devired/.shuttle.json') as json_file:
        data = json.load(json_file)
        if region_number==0:
            data['hosts'] = host_list
        else:
            data['hosts'] = data['hosts']+host_list
    with open('/Users/devired/.shuttle.json', 'w') as json_file:
        json.dump(data,json_file)

def generate_list_of_dict_instances(region):
    client = boto3.client('ec2', region_name = region)
    print(region)
    #If there are no instances(in any state), return an empty list. If there is an instance in any state in this region, save the list of instances as raw_list_of_instances
    keypair = get_key_pair(region)
    print(keypair)
    list_of_dict_instances = []
    instance_number = 0
    response = client.describe_instances(Filters=[{"Name":"instance-state-name", "Values":["running"]}])
    if len(response['Reservations']) > 0:
        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                    if 'Platform' in instance :
                        pass
                    else:
                        each_instance = str(instance_number)
                        each_instance = {}
                        host_ip = instance["PublicIpAddress"]
                        each_instance["cmd"]= cmd_gen(keypair, host_ip)
                        list_of_dict_instances.append(each_instance)
                        if 'Tags' in instance:

                            list_tags_of_each_instance = instance["Tags"]
                        else: 
                            list_tags_of_each_instance = []
                        each_instance["name"]= region + " : " + get_name_tag(list_tags_of_each_instance)
                        each_instance["inTerminal"]= "tab"
        return(list_of_dict_instances)
    else:
        return(list_of_dict_instances)


def cmd_gen(keypair, host_ip):
    #command = "python3 /Users/devired/Desktop/Shuttle/start_stop.py"
    #command = 'for user_name in ec2-user ubuntu centos fedora admin bitnami root; do if gtimeout 3 ssh -i ' + '/Users/devired/Downloads/User_keys/' + keypair + '.pem' + ' $user_name@' + host_ip + ' true 2>/dev/#null; then ssh -i ' + keypair + '.pem' + ' $user_name@' + host_ip + '; fi; done'



    command = 'for user_name in ec2-user ubuntu centos fedora admin bitnami root; do if gtimeout 3 ssh -i ' + '/Users/devired/Downloads/User_keys/' + keypair + '.pem' + ' $user_name@' + host_ip + ' true 2>/dev/null; then ssh -i ' + keypair + '.pem' + ' $user_name@' + host_ip + '; fi; done'

    return command