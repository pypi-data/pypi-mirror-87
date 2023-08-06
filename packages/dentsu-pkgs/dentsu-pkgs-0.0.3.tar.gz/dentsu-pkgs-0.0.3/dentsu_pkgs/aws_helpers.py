#!/usr/bin/env python3

import boto3
import json

def get_secret(secret_name, region_name):
    secret_name = secret_name
    region_name = region_name

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )
    secret = get_secret_value_response['SecretString']
    return secret

def get_mappings(database, table):
    glue = boto3.client('glue')
    response = glue.get_table(
        DatabaseName = database,
        Name = table
    )
    mappings = [(x['Name'], x['Type'], x['Name'].replace(' ','_').replace('%','percentage').replace('(','').replace(')',''), x['Type']) for x in response['Table']['StorageDescriptor']['Columns']]
    print(mappings)