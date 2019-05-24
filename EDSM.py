from urllib.request import urlopen
import json
import math
import time
import Launchpad

config_filepath = "config.yml"


def get_commander_system(commander_name):

    # Get the dataset
    url = 'https://www.edsm.net/api-logs-v1/get-position?commanderName=' + commander_name
    response = urlopen(url)

    # Convert bytes to string type and string type to dict
    string = response.read().decode('utf-8')
    json_obj = json.loads(string)

    try:
        final_string = json_obj['system']
    except:
        final_string = "Commander was not found in the database"

    return final_string


def get_system_coordinates(system_name):

    # Get the dataset
    url = 'https://www.edsm.net/api-v1/system?systemName=' + system_name + "&showCoordinates=1"
    response = urlopen(url)

    # Convert bytes to string type and string type to dict
    string = response.read().decode('utf-8')
    json_obj = json.loads(string)

    try:
        return json_obj["coords"]
    except:
        print("System was not found in database or coordinates are not known")
        return False


def distance(system1_coordinates, system2_coordinates):

    a = system1_coordinates["x"] - system2_coordinates["x"]
    b = system1_coordinates["y"] - system2_coordinates["y"]

    c = math.sqrt(a*a + b*b)

    a2 = c
    b2 = system1_coordinates["z"] - system2_coordinates["z"]

    c2 = math.sqrt(a2*a2 + b2*b2)

    return round(c2, 2)


def is_known(commander_name):
    # Get the dataset
    url = 'https://www.edsm.net/api-logs-v1/get-position?commanderName=' + commander_name
    response = urlopen(url)

    # Convert bytes to string type and string type to dict
    string = response.read().decode('utf-8')
    json_obj = json.loads(string)

    if json_obj['msg'] == "OK":
        return True
    else:
        return False


def write_to_yaml(key, value):

    old_content = {}
    new_content = {}

    file = open(config_filepath, "r")
    content = file.readlines()
    lines = []

    # remove \n
    for i in content:
        i = i.replace("\n", "")
        lines.append(i)

    # convert content to dictionary
    for n in lines:
        content_list = n.split(": ")
        old_content[content_list[0]] = content_list[1]

    if key in old_content:
        new_content[key] = value
        del old_content[key]
    else:
        new_content[key] = value

    for f in old_content:
        new_content[f] = old_content[f]

    file.close()

    # actual writing
    new_file = open(config_filepath, "w")

    # creating new string
    final_string = ""
    for element in new_content:
        final_string += element
        final_string += ": "
        final_string += new_content[element]
        final_string += "\n"

    new_file.write(final_string)
    new_file.close()


def read_yaml(key):

    file_content = {}
    file = open(config_filepath, "r")
    content = file.readlines()
    lines = []

    # remove \n
    for i in content:
        i = i.replace("\n", "")
        lines.append(i)

    # convert content to dictionary
    for n in lines:
        content_list = n.split(": ")
        file_content[content_list[0]] = content_list[1]

    try:
        return file_content[key]
    except:
        return "key not found in config"


def settings():
    commander_name = input("Commander Name:\n")
    if is_known(commander_name):
        write_to_yaml("commander_name", commander_name)
    else:
        settings()
        return
    start_system = input("Start System:\n")
    write_to_yaml("start_system", start_system)
    end_system = input("End System:\n")
    write_to_yaml("end_system", end_system)


def run(refresh_time=60, pixel_amount=64):

    commander_name = read_yaml("commander_name")
    start_system = read_yaml("start_system")
    end_sytem = read_yaml("end_system")

    print("commander_name:", commander_name)
    print("start_system:", start_system)
    print("end_system:", end_sytem)

    try:
        start_system_coordinates = get_system_coordinates(start_system)
        end_sytem_coordinates = get_system_coordinates(end_sytem)
    except:
        time.sleep(refresh_time)
        run()
        return

    total_distance = distance(start_system_coordinates, end_sytem_coordinates)
    print("total_distance:", total_distance)

    distance_per_pixel = round(total_distance / pixel_amount, 2)
    print("distance_per_pixel:", distance_per_pixel)

    while 1:
        distance_left = distance(get_system_coordinates(get_commander_system(commander_name)),
                                 end_sytem_coordinates)
        print("distance_left:", distance_left)

        pixels_active = int(round(distance_left / distance_per_pixel, 0))
        print("pixels_active:", pixels_active)

        Launchpad.display(pixels_active)

        time.sleep(refresh_time)


def refresh(pixel_amount=64):

    commander_name = read_yaml("commander_name")
    start_system = read_yaml("start_system")
    end_sytem = read_yaml("end_system")

    print("commander_name:", commander_name)
    print("start_system:", start_system)
    print("end_system:", end_sytem)

    start_system_coordinates = get_system_coordinates(start_system)
    end_sytem_coordinates = get_system_coordinates(end_sytem)

    total_distance = distance(start_system_coordinates, end_sytem_coordinates)
    print("total_distance:", total_distance)

    distance_per_pixel = round(total_distance / pixel_amount, 2)
    print("distance_per_pixel:", distance_per_pixel)

    distance_left = distance(get_system_coordinates(get_commander_system(commander_name)),
                             end_sytem_coordinates)
    print("distance_left:", distance_left)

    pixels_active = int(round(distance_left / distance_per_pixel, 0))
    print("pixels_active:", pixels_active)

    Launchpad.display(pixels_active)


if int(input("1=60sek refresh, 2=manual refresh\n")) == 1:

    if read_yaml("commander_name") == "key not found in config":
        settings()
    elif read_yaml("start_system") == "key not found in config":
        settings()
    elif read_yaml("end_system") == "key not found in config":
        settings()
    run()

else:
    # TODO
    pass
