from typing import List, Dict, Any

def calculate_category_1_match_totals(predictions: Dict[str, str], actuals: Dict[str, str]) -> int:
    """
    Category 1: Match Totals (5 pts each)
    Predict TEAMS with most/fewest goals scored and conceded in the group stages.
    """
    score = 0
    # Expected keys: 'most_goals_scored', 'fewest_goals_scored', 'most_goals_conceded', 'fewest_goals_conceded'
    for key in ['most_goals_scored', 'fewest_goals_scored', 'most_goals_conceded', 'fewest_goals_conceded']:
        if key in predictions and key in actuals and predictions[key] == actuals[key]:
            score += 5
    return score

def calculate_category_2_group_qualification(predictions: Dict[str, List[str]], actuals: Dict[str, List[str]]) -> int:
    """
    Category 2: Group Qualification (2 pts each correct team + 1 pt bonus for exact order)
    predictions/actuals format: {'Group A': ['Team1', 'Team2'], ...}
    """
    score = 0
    for group, predicted_teams in predictions.items():
        actual_teams = actuals.get(group, [])
        if not actual_teams:
            continue
            
        # 2 points for each correct team progressing (Top 2)
        for team in predicted_teams:
            if team in actual_teams:
                score += 2
        
        # 1 point bonus for predicting exact 1st/2nd place order
        if len(predicted_teams) >= 2 and len(actual_teams) >= 2:
            if predicted_teams[0] == actual_teams[0] and predicted_teams[1] == actual_teams[1]:
                score += 1
    return score

def calculate_category_3_lucky_8(predicted_groups: List[str], actual_qualifying_groups: List[str]) -> int:
    """
    Category 3: The Lucky 8 (2 pts each)
    Predict which 8 specific groups (A-L) will have their 3rd-place team qualify.
    """
    score = 0
    for group in predicted_groups:
        if group in actual_qualifying_groups:
            score += 2
    return score

def calculate_category_4_rivalry_faceoffs(predictions: Dict[str, str], actuals: Dict[str, str]) -> int:
    """
    Category 4: Rivalry Face-Offs (2 pts each)
    USA vs Mexico, Canada vs Scotland, Brazil vs Argentina, England vs Scotland, France vs Norway & Spain vs Portugal
    """
    score = 0
    rivalries = [
        'usa_vs_mexico', 'canada_vs_scotland', 'brazil_vs_argentina',
        'england_vs_scotland', 'france_vs_norway', 'spain_vs_portugal'
    ]
    for rivalry in rivalries:
        if rivalry in predictions and rivalry in actuals and predictions[rivalry] == actuals[rivalry]:
            score += 2
    return score

def calculate_category_5_golden_boot_ranking(predicted_rank: List[str], actual_rank: List[str]) -> int:
    """
    Category 5: Golden Boot Ranking (2 pts per correct position)
    Rank: Mbappe, Haaland, Kane, Vinicius Jr, Yamal
    """
    score = 0
    # Both lists should be size 5
    for i in range(min(len(predicted_rank), len(actual_rank))):
        if predicted_rank[i] == actual_rank[i]:
            score += 2
    return score

def calculate_category_6_general_predictions(predictions: Dict[str, Any], actuals: Dict[str, Any]) -> int:
    """
    Category 6: General Predictions (5 pts each)
    Winner, Runner-up, 3rd Place, total penalty shootouts, host nation success, group stage wipeouts
    """
    score = 0
    keys = ['winner', 'runner_up', 'third_place', 'penalty_shootouts', 'host_success', 'wipeout_exists']
    for key in keys:
        if key in predictions and key in actuals and predictions[key] == actuals[key]:
            score += 5
    return score

def calculate_total_score(user_predictions: Dict[str, Any], tournament_actuals: Dict[str, Any]) -> Dict[str, int]:
    """
    Calculates scores for all categories and returns a breakdown.
    """
    breakdown = {
        'cat1': calculate_category_1_match_totals(user_predictions.get('cat1', {}), tournament_actuals.get('cat1', {})),
        'cat2': calculate_category_2_group_qualification(user_predictions.get('cat2', {}), tournament_actuals.get('cat2', {})),
        'cat3': calculate_category_3_lucky_8(user_predictions.get('cat3', []), tournament_actuals.get('cat3', [])),
        'cat4': calculate_category_4_rivalry_faceoffs(user_predictions.get('cat4', {}), tournament_actuals.get('cat4', {})),
        'cat5': calculate_category_5_golden_boot_ranking(user_predictions.get('cat5', []), tournament_actuals.get('cat5', [])),
        'cat6': calculate_category_6_general_predictions(user_predictions.get('cat6', {}), tournament_actuals.get('cat6', {}))
    }
    breakdown['total'] = sum(breakdown.values())
    return breakdown
