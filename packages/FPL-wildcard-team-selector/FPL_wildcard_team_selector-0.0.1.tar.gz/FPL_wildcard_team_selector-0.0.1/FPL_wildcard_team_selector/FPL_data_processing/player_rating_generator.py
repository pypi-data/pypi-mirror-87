import pandas as pd
from .player_metrics import get_players_ROI, get_players_future_games_scores
from .utilities import set_range_one_to_ten


def calculate_players_scores_weighted_avg_sum(players_info, weights):
    '''
    takes in a DataFrame containing all the players info, and a list containing all the weights that will be used in the 
    weighted sum. 

    Parameters:
        players_info (DataFrame): DataFrame containing all the players info that was read from the main fantasy premier league API
        weights (list): list containing the weights of [form, ROI, ptspergame, ict, ep_next, future games score] in that order

    Returns:
        players_info (DataFrame): DataFrame containing the important metrics from the players info, along with an added column
                                called Algorithm Score which is the final score out of 10 given to each player
        
    '''
    #Players_Filtered = players_info[players_info['minutes'] > 270]
    #Midfielder_Final_Filter = Defender_Initial_Filter[Goalies_Initial_Filter['chance_of_playing_next_round'] == 100] 
    get_players_ROI(players_info)
    get_players_future_games_scores(players_info)
    
    columns_to_normalize = ['form','points_per_game','ict_index','influence','ep_next','ROI','Future Games Score']
    set_range_one_to_ten(players_info, columns_to_normalize)

    sum_of_weights = weights[0] + weights[1] + weights[2] + weights[3] + weights[4]
    players_info.loc[:,'Algorithm Score'] = ((players_info['form'].multiply(weights[0])) 
                                        + (players_info['ROI'].multiply(weights[1])) 
                                        + (players_info['points_per_game'].multiply(weights[2]))
                                        + (players_info['ict_index'].multiply(weights[3]))
                                        + (players_info['ep_next'].multiply(weights[4]))                          
                                        + (players_info['Future Games Score'].multiply(weights[5]))) / sum_of_weights                       
    players_info.sort_values(by='Algorithm Score', inplace = True, ascending=False) 
    return players_info[['first_name','second_name','web_name','ep_next','element_type'
                        ,'now_cost','team','form','ict_index','points_per_game'
                        ,'ROI','Future Games Score','Algorithm Score']]
