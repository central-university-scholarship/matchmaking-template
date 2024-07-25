import requests
import time

def get_waiting_players(test_name, epoch):
    response = requests.get(f'/matchmaking/match', params={'test_name': test_name, 'epoch': epoch})
    return response.json()

def assign_players_to_teams(players):
    teams = [[], []]
    player_roles = {role: [] for role in ['top', 'mid', 'bot', 'sup', 'jungle']}

    sorted_players = sorted(players, key=lambda p: p['mmr'], reverse=True)
    
    for player in sorted_players:
        role_preference = player['role_preference']
        role = role_preference[0]

        if len(teams[0]) <= len(teams[1]):
            teams[0].append(player)
        else:
            teams[1].append(player)

        player_roles[role].append(player)
    
    return teams

def evaluate_match_teams(team1, team2):
    team1_mmr = sum(player['mmr'] for player in team1)
    team2_mmr = sum(player['mmr'] for player in team2)
    median_mmr = abs(team1_mmr - team2_mmr) / 2

    mmr_role_diff = 0
    roles = ['top', 'mid', 'bot', 'sup', 'jungle']
    for role in roles:
        mmr_role_diff += abs(
            sum(player['mmr'] for player in player_roles[role][:len(team1)])
            - sum(player['mmr'] for player in player_roles[role][len(team1):])
        )

    return median_mmr + mmr_role_diff

def calculate_preference_score(players):
    score = 0
    for player in players:
        preference = player['role_preference']
        rank = preference.index(player['assigned_role']) + 1
        score += {1: 3, 2: 5, 3: 8, 4: 13, 5: 21}.get(rank, 0)
    return score

def calculate_waiting_time(start_time, end_time, pauses):
    return (end_time - start_time) + sum(pauses)

def submit_teams(test_name, epoch, teams):
    response = requests.post('/matchmaking/match', json={'test_name': test_name, 'epoch': epoch, 'teams': teams})
    return response.json()

def matchmaking_process(test_name, epoch):
    while epoch != '00000000-0000-0000-0000-000000000000':
        players = get_waiting_players(test_name, epoch)
        if len(players) <= 9:
            teams = assign_players_to_teams(players)
            submit_response = submit_teams(test_name, epoch, teams)
            epoch = submit_response['new_epoch']
        else:
            break

if __name__ == "__main__":
    test_name = "test_case"
    epoch = "initial_epoch"
    matchmaking_process(test_name, epoch)
