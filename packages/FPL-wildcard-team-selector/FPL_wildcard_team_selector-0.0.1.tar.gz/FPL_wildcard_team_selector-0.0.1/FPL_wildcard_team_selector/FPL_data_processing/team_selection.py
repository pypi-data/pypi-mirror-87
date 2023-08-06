import pulp as p 
import pandas as pd
from .utilities import split_based_on_teams_and_players_positions, add_players_full_name, score_and_cost_dict_creator


def team_selection_using_linear_optimization(players_info):
    '''
    takes in a DataFrame containing all the players info that was read from the main fantasy premier league API,
    and all the calculated metrics that were added as columns. This function defines and solves a linear optimization problem
    to select the 15 players that would provide the best returns given the constraints of the game.

    Parameters:
        players_info (DataFrame): DataFrame containing all the players info that was read from the main fantasy premier league API,
                                    and all the calculated metrics that were added as columns

    Returns:
        list_of_selected_goalies (list): list containing the 2 selected goalies
        list_of_selected_defenders (list): list containing the 5 selected defender
        list_of_selected_midfielders (list): list containing the 5 selected midfielders
        list_of_selected_strikers (list): list containing the 3 selected strikers
        cash_left (float): the amount of cash left after selecting all the players
    '''
    number_of_prem_teams = 20
    number_of_playing_positions = 4
    add_players_full_name(players_info)
    players_info_list_of_dataframes = split_based_on_teams_and_players_positions(players_info)

    list_of_teams = []
    for i in range(number_of_prem_teams):
        list_of_positions = []
        for j in range(number_of_playing_positions):
            list_of_dictionaries = []
            players_names_list, players_scores_dict, players_cost_dict = score_and_cost_dict_creator(players_info_list_of_dataframes[i][j])
            list_of_dictionaries.extend([players_names_list, players_scores_dict, players_cost_dict])
            list_of_positions.append(list_of_dictionaries)
        list_of_teams.append(list_of_positions)

    # Create a LP Maximization problem 
    Lp_prob = p.LpProblem('Select_Team_of_15_with_highest_expected_returns', p.LpMaximize)  

    #Create problem variables
    team_variables = []
    for i in range(number_of_prem_teams):
        positions_variables = []
        goalies_variables = p.LpVariable.dict("Gol", list_of_teams[i][0][0], lowBound = 0, cat='Binary')   # Create a variable x >= 0 
        defenders_variables = p.LpVariable.dict("Def",list_of_teams[i][1][0], lowBound = 0, cat='Binary')   # Create a variable x >= 0 
        midfielders_variables = p.LpVariable.dict("Mid", list_of_teams[i][2][0], lowBound = 0, cat='Binary')   # Create a variable x >= 0 
        strikers_variables = p.LpVariable.dict("Str", list_of_teams[i][3][0], lowBound = 0, cat='Binary')   # Create a variable x >= 0 
        positions_variables.extend([goalies_variables, defenders_variables, midfielders_variables, strikers_variables])
        team_variables.append(positions_variables)

    # Objective Function
    sum_of_segments = 0
    for i in range(number_of_prem_teams):
        objective_func_segment_One = p.lpSum([list_of_teams[i][0][1][j] * team_variables[i][0][j] for j in list_of_teams[i][0][0]])
        objective_func_segment_Two = p.lpSum([list_of_teams[i][1][1][j] * team_variables[i][1][j] for j in list_of_teams[i][1][0]])
        objective_func_segment_Three = p.lpSum([list_of_teams[i][2][1][j] * team_variables[i][2][j] for j in list_of_teams[i][2][0]])
        objective_func_segment_Four = p.lpSum([list_of_teams[i][3][1][j] * team_variables[i][3][j] for j in list_of_teams[i][3][0]])
        sum_of_segments = (sum_of_segments + objective_func_segment_One 
                          + objective_func_segment_Two + objective_func_segment_Three
                          + objective_func_segment_Four)
    Lp_prob += sum_of_segments

    # Constraints: We will have 25 constraints for this optimization problem
    # Cost constraint:
    sum_of_segments = 0
    for i in range(number_of_prem_teams):
        constraint_segment_One = p.lpSum([list_of_teams[i][0][2][j] * team_variables[i][0][j] for j in list_of_teams[i][0][0]])
        constraint_segment_Two = p.lpSum([list_of_teams[i][1][2][j] * team_variables[i][1][j] for j in list_of_teams[i][1][0]])
        constraint_segment_Three = p.lpSum([list_of_teams[i][2][2][j] * team_variables[i][2][j] for j in list_of_teams[i][2][0]])
        constraint_segment_Four = p.lpSum([list_of_teams[i][3][2][j] * team_variables[i][3][j] for j in list_of_teams[i][3][0]])
        sum_of_segments = (sum_of_segments + constraint_segment_One 
                          + constraint_segment_Two + constraint_segment_Three
                          + constraint_segment_Four)
    Lp_prob += (sum_of_segments) <= 1000

    #Number Of Players in each position constraints:
    sum_of_gol_segments = 0
    sum_of_def_segments = 0
    sum_of_mid_segments = 0
    sum_of_str_segments = 0

    for i in range(number_of_prem_teams):
        goalie_segment = p.lpSum([team_variables[i][0][j] for j in list_of_teams[i][0][0]])
        def_segment = p.lpSum([team_variables[i][1][j] for j in list_of_teams[i][1][0]])
        mid_segment = p.lpSum([team_variables[i][2][j] for j in list_of_teams[i][2][0]])
        str_segment = p.lpSum([team_variables[i][3][j] for j in list_of_teams[i][3][0]])
        sum_of_gol_segments = sum_of_gol_segments + goalie_segment
        sum_of_def_segments = sum_of_def_segments + def_segment
        sum_of_mid_segments = sum_of_mid_segments + mid_segment
        sum_of_str_segments = sum_of_str_segments + str_segment

    Lp_prob += (sum_of_gol_segments) == 2
    Lp_prob += (sum_of_def_segments) == 5
    Lp_prob += (sum_of_mid_segments) == 5
    Lp_prob += (sum_of_str_segments) == 3

    #Max of 3 Players from each Team Constraint. This will be 20 different constraints 
    for i in range(number_of_prem_teams):
        goalie_segment = p.lpSum([team_variables[i][0][j] for j in list_of_teams[i][0][0]])
        def_segment = p.lpSum([team_variables[i][1][j] for j in list_of_teams[i][1][0]])
        mid_segment = p.lpSum([team_variables[i][2][j] for j in list_of_teams[i][2][0]])
        str_segment = p.lpSum([team_variables[i][3][j] for j in list_of_teams[i][3][0]])
        team_members_segment = goalie_segment + def_segment + mid_segment + str_segment
        Lp_prob += (team_members_segment) <= 3
  
    Lp_prob.solve(p.apis.PULP_CBC_CMD(msg=0))   

    list_of_selected_defenders = []
    list_of_selected_midfielders = []
    list_of_selected_strikers = []
    list_of_selected_goalies = []
    cash_left = 1000

    for constraint in Lp_prob.constraints:
        Constraint_Value = Lp_prob.constraints[constraint].value() - Lp_prob.constraints[constraint].constant
        if(Constraint_Value > 800):
            cash_left = (1000 - Constraint_Value) / 10

    for variable in Lp_prob.variables():
        if variable.varValue > 0:            
            if variable.name[0] == 'G':
                list_of_selected_goalies.append(variable.name)
            elif variable.name[0] == 'D':   
                list_of_selected_defenders.append(variable.name)
            elif variable.name[0] == 'M':
                list_of_selected_midfielders.append(variable.name)
            elif variable.name[0] == 'S': 
                list_of_selected_strikers.append(variable.name)
            else:
                raise ValueError("Variable name used in the linear optimization problem cant be deciphered by the algorithm")
    return list_of_selected_goalies, list_of_selected_defenders, list_of_selected_midfielders, list_of_selected_strikers, cash_left
