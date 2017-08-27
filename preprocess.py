""" Simple data conversion of the raw data retrieved from DynamoDB. """

import ast
import json


def _map_list(x):
    x = json.loads(x.replace("'", '"'))['L']
    if not x:
        return x
    return [o['S'].lower().replace('\n', ' ') for o in x]


def _map_string(x):
    return ast.literal_eval(x)['S'].lower().replace('\n', ' ')


def _map_num(x):
    return ast.literal_eval(x)['N']


def main(df):
    df.drop('user_id', axis=1, inplace=True)
    df.drop('coordinates', axis=1, inplace=True)
    df.drop('user_mentions', axis=1, inplace=True)

    df['user_name'] = df.user_name.transform(_map_string)
    df['text'] = df.text.transform(_map_string)
    df['lang'] = df.lang.transform(_map_string)
    df['n_retweets'] = df.n_retweets.transform(_map_num)
    df['tweet_id'] = df.tweet_id.transform(_map_num)
    df['timestamp'] = df.timestamp.transform(_map_num)
    df['urls'] = df.urls.transform(_map_list)
    df['hashtags'] = df.hastags.transform(_map_list)
    df.drop('hastags', axis=1, inplace=True)

    return df
