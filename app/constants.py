from datetime import datetime

# Tournament Deadline: June 11th 2026 20:00 BST
# BST is UTC+1. So 19:00 UTC.
DEADLINE = datetime(2026, 6, 11, 19, 0, 0)

# Tournament End: July 19th 2026 23:59 BST (22:59 UTC)
TOURNAMENT_END = datetime(2026, 7, 19, 22, 59, 0)

GROUPS = {
    'Group A': ['Mexico', 'South Africa', 'South Korea', 'Czechia'],
    'Group B': ['Canada', 'Bosnia and Herzegovina', 'Qatar', 'Switzerland'],
    'Group C': ['Brazil', 'Morocco', 'Haiti', 'Scotland'],
    'Group D': ['USA', 'Paraguay', 'Australia', 'Turkiye'],
    'Group E': ['Germany', 'Curacao', 'Ivory Coast', 'Ecuador'],
    'Group F': ['Netherlands', 'Japan', 'Sweden', 'Tunisia'],
    'Group G': ['Belgium', 'Egypt', 'Iran', 'New Zealand'],
    'Group H': ['Spain', 'Cabo Verde', 'Saudi Arabia', 'Uruguay'],
    'Group I': ['France', 'Senegal', 'Iraq', 'Norway'],
    'Group J': ['Argentina', 'Algeria', 'Austria', 'Jordan'],
    'Group K': ['Portugal', 'DR Congo', 'Uzbekistan', 'Columbia'],
    'Group L': ['England', 'Croatia', 'Ghana', 'Panama']
}

RIVALRIES = [
    ('usa_vs_mexico', 'USA vs Mexico'),
    ('canada_vs_scotland', 'Canada vs Scotland'),
    ('brazil_vs_argentina', 'Brazil vs Argentina'),
    ('england_vs_scotland', 'England vs Scotland'),
    ('france_vs_norway', 'France vs Norway'),
    ('spain_vs_portugal', 'Spain vs Portugal')
]

GOLDEN_BOOT_PLAYERS = [
    'Kylian Mbappe',
    'Erling Haaland',
    'Harry Kane',
    'Vinicius Junior',
    'Lamine Yamal'
]

# Mapping for rivalry internal names to display names
RIVALRY_TEAMS = {
    'usa_vs_mexico': ['USA', 'Mexico', 'Tie'],
    'canada_vs_scotland': ['Canada', 'Scotland', 'Tie'],
    'brazil_vs_argentina': ['Brazil', 'Argentina', 'Tie'],
    'england_vs_scotland': ['England', 'Scotland', 'Tie'],
    'france_vs_norway': ['France', 'Norway', 'Tie'],
    'spain_vs_portugal': ['Spain', 'Portugal', 'Tie']
}

CATEGORY_TITLES = {
    'cat1': 'Category 1: Match Totals',
    'cat2': 'Category 2: Group Qualification',
    'cat3': 'Category 3: The Lucky 8',
    'cat4': 'Category 4: Rivalry Face-Offs',
    'cat5': 'Category 5: Golden Boot Ranking',
    'cat6': 'Category 6: General Predictions'
}
