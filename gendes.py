import json, boto3

def generate_list_of_instances():
    #Generate list of instances using boto3
    list_of_instances = []
    client = boto3.client('ec2')
    response = client.describe_instances()
    #If there are no instances(in any state), return an empty list
    if len(response['Reservations']) > 0:
        raw_list_of_instances= response['Reservations'][1]['Instances']
        keypairs = client.describe_key_pairs()
        keypairs = keypairs['KeyPairs']
        if len(keypairs)==0:
            print("You do not have a KeyPair in ", i)
        else:
            keypair = keypairs[0]['KeyName']
        for i in range(0,len(raw_list_of_instances)):
            each_instance = str(i)
            each_instance = {}
            command = 'ssh -i ' + keypair +'.pem ' + 'ubuntu@' + raw_list_of_instances[i]["PublicIpAddress"]
            each_instance["cmd"]= command
            each_instance["name"]="NameTag"
            list_of_instances.append(each_instance)
        return(list_of_instances)
    else:
        return(list_of_instances)

def modify_shuttle_json():
    #Modify the shuttle.json file by passing the list of hosts from generate_list_of_instances()
    host_list=generate_list_of_instances()
    with open('/Users/devired/.shuttle.json') as json_file:
        data = json.load(json_file)
        data['hosts'] = host_list
    with open('/Users/devired/.shuttle.json', 'w') as json_file:
        json.dump(data,json_file)

def main():
    modify_shuttle_json()

if __name__ == "__main__":
    main()
