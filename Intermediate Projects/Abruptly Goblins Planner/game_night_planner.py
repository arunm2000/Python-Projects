gamers = []

def add_gamer(gamer, gamers_list):
    if gamer.get("name") and gamer.get("availability"):
        gamers_list.append(gamer)
    else:
        print("Gamer is missing information")

kimberly = {"name" : "Kimberly Warner", "availability" : ["Monday", "Tuesday", "Friday"]}

add_gamer(kimberly, gamers)
add_gamer({'name':'Thomas Nelson','availability': ["Tuesday", "Thursday", "Saturday"]}, gamers)
add_gamer({'name':'Joyce Sellers','availability': ["Monday", "Wednesday", "Friday", "Saturday"]}, gamers)
add_gamer({'name':'Michelle Reyes','availability': ["Wednesday", "Thursday", "Sunday"]}, gamers)
add_gamer({'name':'Stephen Adams','availability': ["Thursday", "Saturday"]}, gamers)
add_gamer({'name': 'Joanne Lynn', 'availability': ["Monday", "Thursday"]}, gamers)
add_gamer({'name':'Latasha Bryan','availability': ["Monday", "Sunday"]}, gamers)
add_gamer({'name':'Crystal Brewer','availability': ["Thursday", "Friday", "Saturday"]}, gamers)
add_gamer({'name':'James Barnes Jr.','availability': ["Tuesday", "Wednesday", "Thursday", "Sunday"]}, gamers)
add_gamer({'name':'Michel Trujillo','availability': ["Monday", "Tuesday", "Wednesday"]}, gamers)

#print(gamers)

def build_daily_frequency_table():
    return {
    "Monday": 0,
    "Tuesday": 0,
    "Wednesday": 0,
    "Thursday": 0,
    "Friday": 0,
    "Saturday": 0,
    "Sunday": 0
    }

count_availability = build_daily_frequency_table()

def calculate_availability(gamers_list, available_frequency):
    for gamer in gamers_list:
        for day in gamer["availability"]:
            available_frequency[day] += 1

calculate_availability(gamers, count_availability)

#print(count_availability)

def find_best_night(availability_table):
    best_availability = 0
    for day, availability in availability_table.items():
        if availability > best_availability:
            best_night = day
            best_availability = availability
    return best_night

game_night = find_best_night(count_availability)

#print(game_night)

def available_on_night(gamers_list, day):
    return [gamer for gamer in gamers_list if day in gamer["availability"]]

attending_game_night = available_on_night(gamers, game_night)

#print(attending_game_night)

form_email = """
Dear {name},

We are hosting {game} night on {day_of_week}.
See you there!

From
Sorcery Society
"""

def send_email(gamers_who_can_attend, day, game):
    for gamer in gamers_who_can_attend:
        print(form_email.format(name=gamer["name"], game=game, day_of_week=day))

#send_email(attending_game_night, game_night, "Abruptly Goblins")

unable_to_attend_best_night = [gamer for gamer in gamers if game_night not in gamer["availability"]]

second_night_availability = build_daily_frequency_table()

calculate_availability(unable_to_attend_best_night, second_night_availability)

second_night = find_best_night(second_night_availability)

available_second_game_night = available_on_night(gamers, second_night)

#send_email(available_second_game_night, second_night, "Abruptly Goblins")
