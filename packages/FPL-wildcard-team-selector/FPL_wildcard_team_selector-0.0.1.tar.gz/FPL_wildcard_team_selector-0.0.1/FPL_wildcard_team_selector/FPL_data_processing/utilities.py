import pandas as pd


def split_based_on_player_position(players_info):
    '''
    takes in a DataFrame containing all the players info, and splits that DataFrame into multiple DataFrames based on player positions

    Parameters:
        players_info (DataFrame): DataFrame containing all the players info that was read from the main fantasy premier league API

    Returns:
        GoalKeepers (DataFrame): DataFrame containing all the players info who are goalkeepers
        Defenders (DataFrame): DataFrame containing all the players info who are defenders
        Midfielders (DataFrame): DataFrame containing all the players info who are midfielders
        Strikers (DataFrame): DataFrame containing all the players info who are strikers
    '''

    GoalKeepers = players_info[players_info['element_type'] == 1]
    Defenders = players_info[players_info['element_type'] == 2]
    Midfielders = players_info[players_info['element_type'] == 3]
    Strikers = players_info[players_info['element_type'] == 4]
    return GoalKeepers, Defenders, Midfielders, Strikers


def split_based_on_teams(players_info):
    '''
    takes in a DataFrame containing all the players info, and splits that DataFrame into multiple DataFrames based on the players team 

    Parameters:
        players_info (DataFrame): DataFrame containing all the players info that was read from the main fantasy premier league API

    Returns:
        List_Of_DataFrames (list): list containing 20 DataFrames, where each DataFrame has the players info for a specific club
    '''

    Num_Of_PremTeams = 20
    List_Of_DataFrames = []
    for i in range(1,Num_Of_PremTeams + 1):
        Selected_Team_Players = players_info[players_info['team'] == i]
        List_Of_DataFrames.append(Selected_Team_Players)    
    return List_Of_DataFrames


def split_based_on_teams_and_players_positions(players_info):
    '''
    takes in a DataFrame containing all the players info, and splits that DataFrame into multiple DataFrames based on the players team and position 

    Parameters:
        players_info (DataFrame): DataFrame containing all the players info that was read from the main fantasy premier league API

    Returns:
        Outer_List_Of_DataFrames (list): returns a main list which contains 20 sub-lists. 
                                        Each of the 20 sub-lists contains the player info for a specific club
                                        Each of the 20 sub-lists contains 4 DataFrames, which have the players info split by position.
                                         
    '''
    Num_Of_PremTeams = 20
    Outer_List_Of_DataFrames = []
    for i in range(1,Num_Of_PremTeams + 1):
        Inner_List_Of_DataFrames = []
        Selected_Team_Players = players_info[players_info['team'] == i]
        GoalKeepers, Defenders, Midfielders, Strikers = split_based_on_player_position(Selected_Team_Players)
        Inner_List_Of_DataFrames.extend([GoalKeepers, Defenders, Midfielders, Strikers])
        Outer_List_Of_DataFrames.append(Inner_List_Of_DataFrames)    
    return Outer_List_Of_DataFrames


def set_range_one_to_ten(players_info, columns_to_adjust):
    '''
    takes in a DataFrame containing all the players info, and normalizes the values in the specified column to be in range of 0-10 

    Parameters:
        players_info (DataFrame): DataFrame containing all the players info that was read from the main fantasy premier league API
        column_to_adjust (list): list containing the names of the columns in the Dataframe that you would like to normalize

    '''
    for column in columns_to_adjust:
        players_info.sort_values(by=column, inplace = True, ascending=False)
        Highest_Value_In_Col = players_info[column].values[0]
        players_info.loc[:,column] = (players_info[column]/Highest_Value_In_Col) * 10


def turn_series_to_float(players_info, columns_to_adjust):
    '''
    takes in a DataFrame containing all the players info, and changes all numbers in the columns specified to floats.
    Primarily useful when number are loaded from the urls as strings. Eg: "2.5" -> 2.5

    Parameters:
        players_info (DataFrame): DataFrame containing all the players info that was read from the main fantasy premier league API
        column_to_adjust (list): list containing the names of the columns in the Dataframe that you would like to change to floats

    Returns:
        players_info (DataFrame): DataFrame containing all the players info, with the numbers in the specified columns changed to floats

    '''
    columns_dtype_conversion_dict = {}
    for column in columns_to_adjust:
        columns_dtype_conversion_dict[column] = 'float'
    players_info = players_info.astype(columns_dtype_conversion_dict)
    return players_info


def add_players_full_name(players_info): 
    '''
    takes in a DataFrame containing all the players info, and adds a column series containing the full name of the player 

    Parameters:
        players_info (DataFrame): DataFrame containing all the players info that was read from the main fantasy premier league API

    '''
    players_info.loc[:,'full_name'] = players_info['first_name'].str.replace(" ","_") + "_" + players_info['second_name'].str.replace(" ","_")


def score_and_cost_dict_creator(players_info):
    '''
    takes in a DataFrame containing all the players info, creates two dictionaries that map the players names to their algorithm scores and cost

    Parameters:
        players_info (DataFrame): DataFrame containing all the players info that was read from the main fantasy premier league API

    Returns:
        players_names_list (list): list containing the names of all the players
        players_score_dict (dict): dictionary matching player names to their algorithm scores
        players_cost_dict (dict): dictionary matching player names to their cost
    '''
    players_names_list = pd.Series.tolist(players_info['full_name'])
    players_ratings = pd.Series.tolist(players_info['Algorithm Score'])
    players_costs = pd.Series.tolist(players_info['now_cost'])
    players_score_dict = dict(zip(players_names_list, players_ratings))
    players_cost_dict = dict(zip(players_names_list, players_costs))
    return players_names_list, players_score_dict, players_cost_dict
