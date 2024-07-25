import logging
import requests
import json
from random import randrange, choice
import uuid
import random


fees=[0,2,3,5,8]

class user:
    # Конструктор класса (специальный метод):
    def __init__(self, user_id, mmr, roles, waitingTime):
        # Атрибуты экземпляра класса:
        self.user_id = user_id
        self.mmr = mmr
        self.roles = roles
        self.waitingTime = waitingTime

class candidate:
    # Конструктор класса (специальный метод):
    def __init__(self, uid, rating):
        # Атрибуты экземпляра класса:
        self.uid = uid
        self.rating = rating

logger = logging.getLogger(__name__)

# При локальном запуске http://server:8000 --> http://0.0.0.0:8000
if __name__ == "__main__":
    # Вызов, который вернёт игроков, ожидающих матча
    response = requests.get(
        'http://localhost:8000/matchmaking/users?test_name=test_0&epoch=00000000-0000-0000-0000-000000000000')
    logger.info(response.text)
    users1 = list(json.loads(response.text))
    users = []
    for x in users1:
        users.append(user(x['user_id'], x['mmr'], x['roles'], x['waitingTime']))

    top_candidates = []
    for i in range(len(users)):
        index_of_top = users[i].roles.index("top")
        fee = fees[index_of_top]
        top_candidates.append(candidate(users[i].user_id, users[i].mmr - fee + users[i].waitingTime))

    # print(top_candidates[3].rating)

    mid_candidates = []
    for i in range(len(users)):
        index_of_mid = users[i].roles.index('mid')
        fee = fees[index_of_mid]
        mid_candidates.append(candidate(users[i].user_id, users[i].mmr - fee + users[i].waitingTime))

    bot_candidates = []
    for i in range(len(users)):
        index_of_bot = users[i].roles.index('bot')
        fee = fees[index_of_bot]
        bot_candidates.append(candidate(users[i].user_id, users[i].mmr - fee + users[i].waitingTime))

    sup_candidates = []
    for i in range(len(users)):
        index_of_sup = users[i].roles.index('sup')
        fee = fees[index_of_sup]
        sup_candidates.append(candidate(users[i].user_id, users[i].mmr - fee + users[i].waitingTime))

    jungle_candidates = []
    for i in range(len(users)):
        index_of_jungle = users[i].roles.index('jungle')
        fee = fees[index_of_jungle]
        jungle_candidates.append(candidate(users[i].user_id, users[i].mmr - fee + users[i].waitingTime))

    top_candidates.sort(key=lambda x: x.rating)

    mid_candidates.sort(key=lambda x: x.rating)

    bot_candidates.sort(key=lambda x: x.rating)

    sup_candidates.sort(key=lambda x: x.rating)

    jungle_candidates.sort(key=lambda x: x.rating)

    sides_set = {"red", "blue"}

    teams = []
    while (True):
        if (len(top_candidates) >= 2 and len(mid_candidates) >= 2 and len(bot_candidates) >= 2 and len(
                sup_candidates) >= 2 and len(jungle_candidates) >= 2):
            svg = 0
        else:
            break

        if (len(top_candidates) < 2):
            break
        red_top_player = top_candidates[0]
        blue_top_player = top_candidates[1]
        top_candidates.remove(red_top_player)
        top_candidates.remove(blue_top_player)

        filtered = []
        for x in mid_candidates:
            if (x.uid == red_top_player.uid or x.uid == blue_top_player.uid):
                filtered.append(x)
        # filtered = filter(lambda x: x.uid == red_top_player.uid or x.uid == blue_top_player, mid_candidates)
        for f in filtered:
            mid_candidates.remove(f)

        filtered = []
        for x in bot_candidates:
            if (x.uid == red_top_player.uid or x.uid == blue_top_player.uid):
                filtered.append(x)

        # filtered = filter(lambda x:x.uid==red_top_player.uid or x.uid==blue_top_player, bot_candidates)
        for f in filtered:
            bot_candidates.remove(f)

        filtered = []
        for x in sup_candidates:
            if (x.uid == red_top_player.uid or x.uid == blue_top_player.uid):
                filtered.append(x)
        # filtered = filter(lambda x:x.uid==red_top_player.uid or x.uid==blue_top_player, sup_candidates)
        for f in filtered:
            sup_candidates.remove(f)

        filtered = []
        for x in jungle_candidates:
            if (x.uid == red_top_player.uid or x.uid == blue_top_player.uid):
                filtered.append(x)
        # filtered = filter(lambda x:x.uid==red_top_player.uid or x.uid==blue_top_player, jungle_candidates)
        for f in filtered:
            jungle_candidates.remove(f)

        if (len(mid_candidates) < 2):
            break
        red_mid_player = mid_candidates[1]
        blue_mid_player = mid_candidates[0]
        mid_candidates.remove(red_mid_player)
        mid_candidates.remove(blue_mid_player)

        filtered = []
        for x in top_candidates:
            if (x.uid == red_mid_player.uid or x.uid == blue_mid_player.uid):
                filtered.append(x)
        # filtered = filter(lambda x:x.uid==red_mid_player.uid or x.uid==blue_mid_player, top_candidates)
        for f in filtered:
            top_candidates.remove(f)

        filtered = []
        for x in bot_candidates:
            if (x.uid == red_mid_player.uid or x.uid == blue_mid_player.uid):
                filtered.append(x)
        # filtered = filter(lambda x:x.uid==red_mid_player.uid or x.uid==blue_mid_player, bot_candidates)
        for f in filtered:
            bot_candidates.remove(f)

        filtered = []
        for x in sup_candidates:
            if (x.uid == red_mid_player.uid or x.uid == blue_mid_player.uid):
                filtered.append(x)
        # filtered = filter(lambda x:x.uid==red_mid_player.uid or x.uid==blue_mid_player, sup_candidates)
        for f in filtered:
            sup_candidates.remove(f)

        filtered = []
        for x in jungle_candidates:
            if (x.uid == red_mid_player.uid or x.uid == blue_mid_player.uid):
                filtered.append(x)
        # filtered = filter(lambda x:x.uid==red_mid_player.uid or x.uid==blue_mid_player, jungle_candidates)
        for f in filtered:
            jungle_candidates.remove(f)

        if (len(bot_candidates) < 2):
            break
        red_bot_player = bot_candidates[0]
        blue_bot_player = bot_candidates[1]
        bot_candidates.remove(red_bot_player)
        bot_candidates.remove(blue_bot_player)

        filtered = []
        for x in top_candidates:
            if (x.uid == red_bot_player.uid or x.uid == blue_bot_player.uid):
                filtered.append(x)
        # filtered = filter(lambda x:x.uid==red_bot_player.uid or x.uid==blue_bot_player, top_candidates)
        for f in filtered:
            top_candidates.remove(f)
        filtered = []
        for x in mid_candidates:
            if (x.uid == red_bot_player.uid or x.uid == blue_bot_player.uid):
                filtered.append(x)
        # filtered = filter(lambda x: x.uid == red_top_player.uid or x.uid == blue_top_player, mid_candidates)
        for f in filtered:
            mid_candidates.remove(f)

        filtered = []
        for x in sup_candidates:
            if (x.uid == red_bot_player.uid or x.uid == blue_bot_player.uid):
                filtered.append(x)
        # filtered = filter(lambda x:x.uid==red_bot_player.uid or x.uid==blue_bot_player, sup_candidates)
        for f in filtered:
            sup_candidates.remove(f)

        filtered = []
        for x in jungle_candidates:
            if (x.uid == red_bot_player.uid or x.uid == blue_bot_player.uid):
                filtered.append(x)
        # filtered = filter(lambda x:x.uid==red_bot_player.uid or x.uid==blue_bot_player, jungle_candidates)
        for f in filtered:
            jungle_candidates.remove(f)

        if (len(sup_candidates) < 2):
            break
        red_sup_player = sup_candidates[1]
        blue_sup_player = sup_candidates[0]
        sup_candidates.remove(red_sup_player)
        sup_candidates.remove(blue_sup_player)

        filtered = []
        for x in top_candidates:
            if (x.uid == red_sup_player.uid or x.uid == blue_sup_player.uid):
                filtered.append(x)
        # filtered = filter(lambda x:x.uid==red_sup_player.uid or x.uid==blue_sup_player, top_candidates)
        for f in filtered:
            top_candidates.remove(f)

        filtered = []
        for x in mid_candidates:
            if (x.uid == red_sup_player.uid or x.uid == blue_sup_player.uid):
                filtered.append(x)
        # filtered = filter(lambda x:x.uid==red_sup_player.uid or x.uid==blue_sup_player, mid_candidates)
        for f in filtered:
            mid_candidates.remove(f)

        filtered = []
        for x in bot_candidates:
            if (x.uid == red_sup_player.uid or x.uid == blue_sup_player.uid):
                filtered.append(x)
        # filtered = filter(lambda x:x.uid==red_sup_player.uid or x.uid==blue_sup_player, bot_candidates)
        for f in filtered:
            bot_candidates.remove(f)

        filtered = []
        for x in jungle_candidates:
            if (x.uid == red_sup_player.uid or x.uid == blue_sup_player.uid):
                filtered.append(x)
        # filtered = filter(lambda x:x.uid==red_sup_player.uid or x.uid==blue_sup_player, jungle_candidates)
        for f in filtered:
            jungle_candidates.remove(f)

        if (len(jungle_candidates) < 2):
            break
        red_jungle_player = jungle_candidates[0]
        blue_jungle_player = jungle_candidates[1]
        jungle_candidates.remove(red_jungle_player)
        jungle_candidates.remove(blue_jungle_player)

        filtered = []
        for x in top_candidates:
            if (x.uid == red_jungle_player.uid or x.uid == blue_jungle_player.uid):
                filtered.append(x)
        # filtered = filter(lambda x:x.uid==red_jungle_player.uid or x.uid==blue_jungle_player, top_candidates)
        for f in filtered:
            top_candidates.remove(f)

        filtered = []
        for x in mid_candidates:
            if (x.uid == red_jungle_player.uid or x.uid == blue_jungle_player.uid):
                filtered.append(x)
        # filtered = filter(lambda x:x.uid==red_jungle_player.uid or x.uid==blue_jungle_player, mid_candidates)
        for f in filtered:
            mid_candidates.remove(f)

        filtered = []
        for x in bot_candidates:
            if (x.uid == red_jungle_player.uid or x.uid == blue_jungle_player.uid):
                filtered.append(x)
        # filtered = filter(lambda x:x.uid==red_jungle_player.uid or x.uid==blue_jungle_player, bot_candidates)
        for f in filtered:
            bot_candidates.remove(f)

        filtered = []
        for x in sup_candidates:
            if (x.uid == red_jungle_player.uid or x.uid == blue_jungle_player.uid):
                filtered.append(x)
        # filtered = filter(lambda x:x.uid==red_jungle_player.uid or x.uid==blue_jungle_player, sup_candidates)
        for f in filtered:
            sup_candidates.remove(f)

        teams.append({"side": "red", "users": [{"id": red_top_player.uid, "role": "top"},
                                               {"id": red_mid_player.uid, "role": "mid"},
                                               {"id": red_bot_player.uid, "role": "bot"},
                                               {"id": red_sup_player.uid, "role": "sup"},
                                               {"id": red_jungle_player.uid, "role": "jungle"}]})
        teams.append({"side": "blue", "users": [{"id": blue_top_player.uid, "role": "top"},
                                                {"id": blue_mid_player.uid, "role": "mid"},
                                                {"id": blue_bot_player.uid, "role": "bot"},
                                                {"id": blue_sup_player.uid, "role": "sup"},
                                                {"id": blue_jungle_player.uid, "role": "jungle"}]})

        if (len(top_candidates) >= 2 and len(mid_candidates) >= 2 and len(bot_candidates) >= 2 and len(
                sup_candidates) >= 2 and len(jungle_candidates) >= 2):
            svg = 0
        else:
            break
    data1 = {'match_id': str(uuid.uuid4()), 'teams': teams}
    print(data1)
    #data = json.dump(data1)
    # Вызов, который передаст составы матчей в проверяющую систему
    headers = {'Content-Type': 'application/json'}
    response = requests.post(
        'http://localhost:8000/matchmaking/match?test_name=test_0&epoch=00000000-0000-0000-0000-000000000000',
        headers=headers,
        json={"example": data1})
    logger.info(response.text)
    print(response.text)
