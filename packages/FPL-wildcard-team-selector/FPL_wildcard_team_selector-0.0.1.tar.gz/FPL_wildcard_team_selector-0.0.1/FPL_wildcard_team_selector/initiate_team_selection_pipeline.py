import sys
from .FPL_data_collection import load_json_data_from_FPL_url, parse_main_FPL_API
from .FPL_data_processing import calculate_players_scores_weighted_avg_sum, team_selection_using_linear_optimization, turn_series_to_float
from .FPL_data_visualization import visualize_team_selection_442, visualize_team_selection_352, visualize_team_selection_343, visualize_team_selection_433


def play_wildcard(formation_to_draw:int):
    valid_formations = [433, 442, 352, 343]
    if formation_to_draw not in valid_formations:
        raise ValueError("Undefined formation requested. Please select one of the following formations: 442, 433, 352, 343")

    print("currently selecting the best 15 players for your wildcard, please be patient. This may take a few minutes")
    FPL_API_url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    JSON_Data = load_json_data_from_FPL_url(FPL_API_url)
    players_info, teams_info, events_info = parse_main_FPL_API(JSON_Data)

    columns_to_turn_to_floats = ['form','points_per_game','ict_index','influence','ep_next']
    players_info = turn_series_to_float(players_info, columns_to_turn_to_floats)

    #form, ROI, ptsPerGame, ICT index, ep_next, Future Games Score
    Regular_Scoring_Weights = [0.2, 0.0 , 0.3, 0.1, 0.15, 0.25] 
    players_info = calculate_players_scores_weighted_avg_sum(players_info, Regular_Scoring_Weights)

    ListOfGoalies, ListOfDef, ListOfMid, ListOfStr, Cash_Left = team_selection_using_linear_optimization(players_info)

    if formation_to_draw == 442:
        visualization_object = visualize_team_selection_442(ListOfGoalies, ListOfDef, ListOfMid, ListOfStr, Cash_Left)
    elif formation_to_draw == 433:
        visualization_object = visualize_team_selection_433(ListOfGoalies, ListOfDef, ListOfMid, ListOfStr, Cash_Left)
    elif formation_to_draw == 352:
        visualization_object = visualize_team_selection_352(ListOfGoalies, ListOfDef, ListOfMid, ListOfStr, Cash_Left)
    elif formation_to_draw == 343:
        visualization_object = visualize_team_selection_343(ListOfGoalies, ListOfDef, ListOfMid, ListOfStr, Cash_Left)
    else:
        raise ValueError("Undefined formation requested. Please select one of the following formations: 442, 433, 352, 343")

    print("Team selection is done. To exit the program, you can close the graphics tab")
    visualization_object.run_visualization()


if __name__ == "__main__":
    formation = int(sys.argv[1])
    play_wildcard(formation)