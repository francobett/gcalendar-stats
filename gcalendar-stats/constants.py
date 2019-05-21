# Dicts
events_dict = {
    'total': {
        'names': [],
        'time': 0.0,
    },
    'accepted': {  # Yes
        'names': [],
        'time': 0.0,
    },
    'needsAction': {  # No response
        'names': [],
        'time': 0.0,
    },
    'declined': {  # Declined
        'names': [],
        'time': 0.0,
    },
    'tentative': {  # Maybe
        'names': [],
        'time': 0.0,
    },
}

# CSV
csv_fields = ['Events type', 'Count', 'Time(h)', '% of total']
team_general = 'General'

# Events states
events_states = ['accepted', 'declined', 'tentative', 'needsAction', 'total']
