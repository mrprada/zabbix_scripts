import json
import requests
import argparse
import urllib3
import creds
import sys

urllib3.disable_warnings() #"Disable the WARNINGs about NOSECURE Request ""

params_prod = (
('env', 'Prod'),
)

params_stage = (
('env', 'Stage'),
)



"""Item for prod & stage"""
prod_items = ['db-dump', 'rsync-from-app-server	','rsync-to-other-region','duplicity-backup-s3','duplicity-backup-s3']
stage_items = ['rsync-one-day', 'db-dump', 'rsync-from-app-server', 'rsync-to-other-region']


"""Geting information from cloudcc API """
r_prod = requests.get('%s' %creds.url(), params=params_prod, verify=False, auth=('%s' %creds.user(), '%s' %creds.PASS()))
r_stage = requests.get('%s' %creds.url(), params=params_stage, verify=False, auth=('%s' %creds.user(), '%s' %creds.PASS()))


def main ():
    parser = argparse.ArgumentParser(description='Getting a dictionary with all new zabbix_items')
    parser.add_argument('Type', metavar='T', type=str, help='Select type of Environment "prod|stage"')
    args = parser.parse_args()
    Type = args.Type




    get_dict(Type)



def get_dict(Type):
    if Type == 'stage':
        r = r_stage
        items = stage_items
    if Type == 'prod':
        r = r_prod
        items = prod_items
    else :
        sys.exit("\nWrong format !!! select from prod|stage\n")
    result = r.json()
    gen_list = []
    result_list = []
    rlist = []
    for element in result[:]:
        for key, value in element.iteritems():
            items_list = []
            if key == "clm_instance_name":
                for item_type in items[:]:
                    current_item  = str(value + '_' + item_type).split()     #build item from item_list
                    items_list = (items_list + current_item )                #create a list of items
                    gen_list = items_list                                    # save list for current Environment
                    data_list = []                                           # clear dictionary with item
                dlist = []                                                   #create empty dictionary object
                for value in gen_list[:]:
                    data_step = {}
                    data_step['{#CLM_BACKUP_NAME}'] = value                  #create dictianary item
                    dlist.append(data_step.copy())                           # update dictionary with new item
                rlist = rlist + dlist
    main = [rlist]
    for value in main[:]:
        data = {}
        data['data'] = value

    json_data = json.dumps(data)
    parsed = json.loads(json_data)
    dictionary =  json.dumps(parsed, indent=1, sort_keys=True)
    print (dictionary)


main()
