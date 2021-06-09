import pytest

import pandas as pd

from src.model import get_data, get_subset, get_namelist, recommend_topn

data = pd.read_csv("./test/data/steam.csv")
data[['tag1', 'tag2', 'tag3']] = data.steamspy_tags.str.split(';', expand=True)
data['pos_rate'] = data['positive_ratings'] / (data['positive_ratings'] + data['negative_ratings'])
data['name'] = data['name'].str.replace(r'[^\x00-\x7F]+', '')


def test_get_data():
    """test1 (get_data()): happy path for expected behavior"""
    df_test = data.head()
    cols = ['appid', 'name', 'release_date', 'english', 'developer', 'publisher',
            'platforms', 'required_age', 'categories', 'genres', 'steamspy_tags',
            'achievements', 'positive_ratings', 'negative_ratings',
            'average_playtime', 'median_playtime', 'owners', 'price', 'tag1',
            'tag2', 'tag3', 'pos_rate']
    indexs = range(5)

    df_true = pd.DataFrame([[10, 'Counter-Strike', '2000-11-01', 1, 'Valve', 'Valve',
                             'windows;mac;linux', 0,
                             'Multi-player;Online Multi-Player;Local Multi-Player;Valve Anti-Cheat enabled',
                             'Action', 'Action;FPS;Multiplayer', 0, 124534, 3339, 17612, 317,
                             '10000000-20000000', 7.19, 'Action', 'FPS', 'Multiplayer',
                             0.9738881546534452],
                            [20, 'Team Fortress Classic', '1999-04-01', 1, 'Valve', 'Valve',
                             'windows;mac;linux', 0,
                             'Multi-player;Online Multi-Player;Local Multi-Player;Valve Anti-Cheat enabled',
                             'Action', 'Action;FPS;Multiplayer', 0, 3318, 633, 277, 62,
                             '5000000-10000000', 3.99, 'Action', 'FPS', 'Multiplayer',
                             0.8397873955960516],
                            [30, 'Day of Defeat', '2003-05-01', 1, 'Valve', 'Valve',
                             'windows;mac;linux', 0, 'Multi-player;Valve Anti-Cheat enabled',
                             'Action', 'FPS;World War II;Multiplayer', 0, 3416, 398, 187, 34,
                             '5000000-10000000', 3.99, 'FPS', 'World War II', 'Multiplayer',
                             0.8956476140534871],
                            [40, 'Deathmatch Classic', '2001-06-01', 1, 'Valve', 'Valve',
                             'windows;mac;linux', 0,
                             'Multi-player;Online Multi-Player;Local Multi-Player;Valve Anti-Cheat enabled',
                             'Action', 'Action;FPS;Multiplayer', 0, 1273, 267, 258, 184,
                             '5000000-10000000', 3.99, 'Action', 'FPS', 'Multiplayer',
                             0.8266233766233766],
                            [50, 'Half-Life: Opposing Force', '1999-11-01', 1,
                             'Gearbox Software', 'Valve', 'windows;mac;linux', 0,
                             'Single-player;Multi-player;Valve Anti-Cheat enabled', 'Action',
                             'FPS;Action;Sci-fi', 0, 5250, 288, 624, 415, '5000000-10000000',
                             3.99, 'FPS', 'Action', 'Sci-fi', 0.9479956663055255]], columns=cols, index=indexs)

    assert df_test.equals(df_true)


def test_get_data_non_df():
    """test2 (get_data()): unhappy path for type error"""
    df_in = 100

    with pytest.raises(TypeError):
        get_data(df_in)


def test_get_subset():
    """test3 (get_subset()): happy path for expected behavior"""
    df_test = get_subset("Counter-Strike", data).head()
    cols = ['appid', 'name', 'release_date', 'english', 'developer', 'publisher',
            'platforms', 'required_age', 'categories', 'genres', 'steamspy_tags',
            'achievements', 'positive_ratings', 'negative_ratings',
            'average_playtime', 'median_playtime', 'owners', 'price', 'tag1',
            'tag2', 'tag3', 'pos_rate']
    indexs = df_test.index

    df_true = pd.DataFrame([[10, 'Counter-Strike', '2000-11-01', 1, 'Valve', 'Valve',
                             'windows;mac;linux', 0,
                             'Multi-player;Online Multi-Player;Local Multi-Player;Valve Anti-Cheat enabled',
                             'Action', 'Action;FPS;Multiplayer', 0, 124534, 3339, 17612, 317,
                             '10000000-20000000', 7.19, 'Action', 'FPS', 'Multiplayer',
                             0.9738881546534452],
                            [30, 'Day of Defeat', '2003-05-01', 1, 'Valve', 'Valve',
                             'windows;mac;linux', 0, 'Multi-player;Valve Anti-Cheat enabled',
                             'Action', 'FPS;World War II;Multiplayer', 0, 3416, 398, 187, 34,
                             '5000000-10000000', 3.99, 'FPS', 'World War II', 'Multiplayer',
                             0.8956476140534871],
                            [50, 'Half-Life: Opposing Force', '1999-11-01', 1,
                             'Gearbox Software', 'Valve', 'windows;mac;linux', 0,
                             'Single-player;Multi-player;Valve Anti-Cheat enabled', 'Action',
                             'FPS;Action;Sci-fi', 0, 5250, 288, 624, 415, '5000000-10000000',
                             3.99, 'FPS', 'Action', 'Sci-fi', 0.9479956663055255],
                            [70, 'Half-Life', '1998-11-08', 1, 'Valve', 'Valve',
                             'windows;mac;linux', 0,
                             'Single-player;Multi-player;Online Multi-Player;Steam Cloud;Valve Anti-Cheat enabled',
                             'Action', 'FPS;Classic;Action', 0, 27755, 1100, 1300, 83,
                             '5000000-10000000', 7.19, 'FPS', 'Classic', 'Action',
                             0.9618783573037601],
                            [80, 'Counter-Strike: Condition Zero', '2004-03-01', 1, 'Valve',
                             'Valve', 'windows;mac;linux', 0,
                             'Single-player;Multi-player;Valve Anti-Cheat enabled', 'Action',
                             'Action;FPS;Multiplayer', 0, 12120, 1439, 427, 43,
                             '10000000-20000000', 7.19, 'Action', 'FPS', 'Multiplayer',
                             0.8938712294416993]], columns=cols, index=indexs)
    assert df_test.equals(df_true)


def test_get_subset_non_df():
    """test4 (get_data()): unhappy path for attribute error"""
    name = "string"
    data = 2
    with pytest.raises(AttributeError):
        get_subset(name, data)


def test_get_namelist():
    """test5 (get_namelist()): happy path for expected behavior"""
    list_test = get_namelist(data)[:5]
    list_true = ['Counter-Strike: Global Offensive',
                 'Dota 2',
                 'Team Fortress 2',
                 "PLAYERUNKNOWN'S BATTLEGROUNDS",
                 "Garry's Mod"]
    assert list_test == list_true


def test_get_namelist_non_list():
    """test6 (get_namelist()): unhappy path for type error"""
    data = "2"
    with pytest.raises(TypeError):
        get_namelist(data,5)


def test_recommend_topn():
    """test7 (recommend_topn()): happy path for expected behavior"""
    dfmid = get_subset("Counter-Strike", data)
    df_test = recommend_topn(dfmid, 5)
    cols = ['name', 'price']
    indexs = df_test.index

    df_true = pd.DataFrame([['Counter-Strike: Source', 7.19],
       ['Half-Life', 7.19],
       ['Day of Defeat: Source', 7.19],
       ['Counter-Strike: Condition Zero', 7.19],
       ['Half-Life 2: Deathmatch', 3.99]],columns=cols,index=indexs)

    assert df_test.equals(df_true)


def test_recommend_topn_non_df():
    """test8 (recommend_topn()): unhappy path for type error"""
    data = 2
    with pytest.raises(TypeError):
        recommend_topn(data,5)