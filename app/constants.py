from datetime import datetime

# Tournament Deadline: June 11th 2026 20:00 BST
# BST is UTC+1. So 19:00 UTC.
DEADLINE = datetime(2026, 6, 11, 19, 0, 0)

# Tournament End: July 19th 2026 23:59 BST (22:59 UTC)
TOURNAMENT_END = datetime(2026, 7, 19, 22, 59, 0)

GROUPS = {
    'Group A': ['Mexico', 'South Korea', 'Denmark', 'Mali'],
    'Group B': ['Canada', 'Belgium', 'Chile', 'Oman'],
    'Group C': ['USA', 'Netherlands', 'Senegal', 'New Zealand'],
    'Group D': ['France', 'Switzerland', 'Uruguay', 'Saudi Arabia'],
    'Group E': ['Brazil', 'Norway', 'Egypt', 'Australia'],
    'Group F': ['England', 'Poland', 'Ecuador', 'Iraq'],
    'Group G': ['Spain', 'Portugal', 'Nigeria', 'Panama'],
    'Group H': ['Argentina', 'Austria', 'Japan', 'Cameroon'],
    'Group I': ['Germany', 'Sweden', 'Morocco', 'Jamaica'],
    'Group J': ['Italy', 'Croatia', 'Colombia', 'Uzbekistan'],
    'Group K': ['Portugal', 'Turkey', 'Ghana', 'Honduras'],
    'Group L': ['Belgium', 'Ukraine', 'Algeria', 'Costa Rica']
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
    'usa_vs_mexico': ['USA', 'Mexico'],
    'canada_vs_scotland': ['Canada', 'Scotland'],
    'brazil_vs_argentina': ['Brazil', 'Argentina'],
    'england_vs_scotland': ['England', 'Scotland'],
    'france_vs_norway': ['France', 'Norway'],
    'spain_vs_portugal': ['Spain', 'Portugal']
}
