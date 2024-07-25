import requests
import json
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# URL сервера
BASE_URL = "http://localhost:8000/matchmaking"
TEST_NAME = "test1"  # Имя теста
EPOCH = "00000000-0000-0000-0000-000000000000"

def get_waiting_users(test_name, epoch):
    response = requests.get(f"{BASE_URL}/users", params={"test_name": test_name, "epoch": epoch})
    if response.status_code != 200:
        logger.error("Failed to get waiting users.")
        return None
    return response.json()

def post_match(test_name, epoch, teams):
    response = requests.post(f"{BASE_URL}/match", params={"test_name": test_name, "epoch": epoch}, json=teams)
    if response.status_code != 200:
        logger.error("Failed to post match data.")
        return None
    return response.json()

def calculate_team_mmr(team):
    return sum(player['mmr'] for player in team)

def calculate_mmr_difference(team1, team2):
    return abs(calculate_team_mmr(team1) - calculate_team_mmr(team2))

def assign_roles(players):
    roles = ['top', 'mid', 'bot', 'sup', 'jungle']
    preferences = {role: [] for role in roles}

    for player in players:
        for idx, role in enumerate(player['preferences']):
            preferences[role].append((player, idx))

    for role in roles:
        preferences[role].sort(key=lambda x: x[1])

    teams = {'team1': [], 'team2': []}
    for role in roles:
        if len(preferences[role]) >= 2:
            teams['team1'].append(preferences[role][0][0])
            teams['team2'].append(preferences[role][1][0])
    
    return teams

def main():
    epoch = EPOCH
    while epoch != "00000000-0000-0000-0000-000000000000":
        data = get_waiting_users(TEST_NAME, epoch)
        if not data:
            break
        
        players = data.get('players', [])
        if len(players) < 10:
            logger.warning("Not enough players to form two teams.")
            break

        teams = assign_roles(players)

        match_data = {
            "teams": {
                "team1": [player['name'] for player in teams['team1']],
                "team2": [player['name'] for player in teams['team2']]
            }
        }

        response = post_match(TEST_NAME, epoch, match_data)
        if not response:
            break

        epoch = response['epoch']
        logger.info(f"New epoch: {epoch}")

if __name__ == '__main__':
    main()
