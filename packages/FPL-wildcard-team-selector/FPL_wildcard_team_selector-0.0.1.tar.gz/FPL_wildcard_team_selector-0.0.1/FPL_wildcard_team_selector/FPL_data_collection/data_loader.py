import pandas as pd
import json
import requests


def load_json_data_from_FPL_url(url:str):
    '''
    sends a Get request to the specified Fantasy Premier League url and returns the received json string as a dictionary. 

    Parameters:
        url (str): url to the fantasy premier league API

    Returns:
        data (dict): dictionary containing all the data from the url 
    '''
    server_response = requests.get(url) 
    data = json.loads(server_response.content) 
    return data


def parse_main_FPL_API(FPL_API_data_dict:dict):
    '''
    takes in all the data from the main Fantasy premier league API, and returns the most important data as DataFrames.

    The response from the FPL main API should be a json string with 8 main attributes:
    elements, element_stats, element_types, events, game_settings, phases, teams, total_players

    The most valuable info are in : elements, events, and teams
    elements: Player summary data such as total points and costs
    events: gameweek data such as id, deadline time, and highest scoring player
    Teams: Data for each team such as name, and id as well as scores for the team attack, defence, overall when home and away

    Parameters:
        FPL_API_data_dict (dict): dictionary containing all the data from the fantasy premier league main API

    Returns:
        players_df (DataFrame): pandas DataFrame containing all the data about the players from the input dictionary
        teams_df (DataFrame): pandas DataFrame containing all the data about the premier league teams from the input dictionary
        events_df (DataFrame): pandas DataFrame containing all the data about the premier league fixtures from the input dictionary
    '''
    players = FPL_API_data_dict['elements']
    teams = FPL_API_data_dict['teams']
    events = FPL_API_data_dict['events']

    players_df = pd.DataFrame(players)
    teams_df = pd.DataFrame(teams)
    events_df = pd.DataFrame(events)
    return players_df, teams_df, events_df


def get_players_future_games_info(player_id:int):
    '''
    Fantasy premier league assigns a unique url to every premier league player. These URLs contain information specific to each player.
    Fantasy premier league assigns every player a unique id which can be used to retrieve their unique URL. This function collects
    the fixture information for the player whos id is provided as an input

    Parameters:
        player_id (int): id of the player

    Returns:
        player_future_games_df (DataFrame): pandas DataFrame containing all the details about the upcoming fixtures for the player specified
    '''

    fpl_player_API_url = 'https://fantasy.premierleague.com/api/element-summary/'
    player_id_string = str(player_id) + '/'
    complete_player_url = fpl_player_API_url + player_id_string
    player_info_dict = load_json_data_from_FPL_url(complete_player_url)
    fixtures_dict = player_info_dict['fixtures']
    player_future_games_df = pd.DataFrame(fixtures_dict)
    return player_future_games_df
