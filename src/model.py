import logging
import re

import boto3
import botocore
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


def get_data():
    """Read local data after downloading from s3.
    Args:
        N/A
    Returns:
        data (dataframe): raw dataframe read from downloaded .csv
    """
    data = pd.read_csv("./data/sample/steam.csv")
    data[['tag1', 'tag2', 'tag3']] = data.steamspy_tags.str.split(';', expand=True)
    data['pos_rate'] = data['positive_ratings'] / (data['positive_ratings'] + data['negative_ratings'])
    data['name'] = data['name'].str.replace(r'[^\x00-\x7F]+', '')
    return data


def get_subset(name, data):
    """Subset the dataframe for a given game.
    Args:
        name (string): input game name to control the subset
        data (datafram): input raw dataframe
    Returns:
        subset (dataframe): filtered dataframe using given input game
    """
    input_row = data[data.name == name]
    # print(input_row)
    rating_cap = float(input_row.pos_rate.iloc[0] - 0.1)
    tag_list = [str(input_row.tag1.values[0]), str(input_row.tag2.values[0]), str(input_row.tag3.values[0])]

    subset = data.loc[(data.name != name) & (data.pos_rate >= rating_cap) & (data.tag1.isin(tag_list))].copy()
    subset = pd.concat([input_row, subset])
    return subset


def recommend_topn(data, n):
    """Recommend games based on similarties.
    Args:
        data (dataframe): subset dataframe that is the output of function get_subset()
        n (integer): number of games to recommend
    Returns:
        topn_list (dataframe): datafram that contained the information of recommended games
    """
    nu_ma = data[["english", "achievements", "average_playtime", "median_playtime", "price"]].copy()
    data['cor'] = abs(nu_ma.T.corr().iloc[0])
    if n > data.shape[0]:
        topn_list = pd.DataFrame({"name":["No Game"],"price": [-1]})
    else:
        topn_list = data[["name", "cor","price"]].sort_values("cor", ascending=False)[1:n + 1][["name","price"]]
    return topn_list

def get_namelist(data):
    """Get all names of games that have positive ratings > 500.
    Args:
        data (dataframe): raw input dataframe
    Returns:
        name_list (list): a list of all games names that have positive ratings > 500
    """
    over_500_pos = data[data.positive_ratings>500].sort_values('positive_ratings',ascending = False)
    name_list = over_500_pos.name.tolist()
    return name_list
