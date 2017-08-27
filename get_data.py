""" Retrieve all data from DynamoDB and save to a local CSV file. """
import json

import boto3
import pandas as pd

client = boto3.client('dynamodb')

LIMIT = 1000000000

last_key = json.load(open('last_key.txt', 'r'))
df = pd.read_csv('tweets.csv')
tweets = df.to_dict('records')

res = client.scan(TableName='iot-tweets', Limit=LIMIT, ExclusiveStartKey=last_key)
tweets.extend(res['Items'])

i = 0
while 'LastEvaluatedKey' in res:
    i += 1
    res = client.scan(TableName='iot-tweets', ExclusiveStartKey=res['LastEvaluatedKey'],
                      Limit=LIMIT)
    tweets.extend(res['Items'])
    print(len(tweets))
    if i % 10 == 0:
        df = pd.DataFrame(tweets)
        df.to_csv('tweets.csv', index=None)
        json.dump(res['LastEvaluatedKey'], open('last_key.txt', 'w'))
        print('saved')

df = pd.DataFrame(tweets)
df.to_csv('tweets.csv', index=None)
