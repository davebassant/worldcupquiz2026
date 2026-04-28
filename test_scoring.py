from app.scoring import calculate_total_score

def test_scoring():
    predictions = {
        'cat1': {
            'most_goals_scored': 15,
            'fewest_goals_scored': 2,
            'most_goals_conceded': 10,
            'fewest_goals_conceded': 1
        },
        'cat2': {
            'Group A': ['USA', 'Mexico'],
            'Group B': ['England', 'Scotland']
        },
        'cat3': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
        'cat4': {
            'usa_vs_mexico': 'USA',
            'canada_vs_scotland': 'Canada'
        },
        'cat5': ['Mbappe', 'Haaland', 'Kane', 'Vinicius Jr', 'Yamal'],
        'cat6': {
            'winner': 'Brazil',
            'penalty_shootouts': 5
        }
    }

    actuals = {
        'cat1': {
            'most_goals_scored': 15,  # Correct (5)
            'fewest_goals_scored': 2,  # Correct (5)
            'most_goals_conceded': 8,  # Wrong
            'fewest_goals_conceded': 1  # Correct (5)
        },
        'cat2': {
            'Group A': ['USA', 'Mexico'], # Both correct (4) + Exact order (1) = 5
            'Group B': ['Scotland', 'England'] # Both correct (4) + Wrong order = 4
        },
        'cat3': ['A', 'B', 'I', 'J'], # A and B correct (4)
        'cat4': {
            'usa_vs_mexico': 'USA', # Correct (2)
            'canada_vs_scotland': 'Scotland' # Wrong
        },
        'cat5': ['Mbappe', 'Haaland', 'Vinicius Jr', 'Kane', 'Yamal'], # 1, 2, 5 correct (6)
        'cat6': {
            'winner': 'Brazil', # Correct (5)
            'penalty_shootouts': 4 # Wrong
        }
    }

    scores = calculate_total_score(predictions, actuals)
    
    print(f"Score Breakdown: {scores}")
    
    # Assertions
    assert scores['cat1'] == 15
    assert scores['cat2'] == 9
    assert scores['cat3'] == 4
    assert scores['cat4'] == 2
    assert scores['cat5'] == 6
    assert scores['cat6'] == 5
    assert scores['total'] == 41
    
    print("All tests passed!")

if __name__ == "__main__":
    test_scoring()
