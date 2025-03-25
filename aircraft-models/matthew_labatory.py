import matlab.engine
import random
import math
from google import genai
from aircraft import scale_and_position_aircraft
import sys
import os
os.chdir('/Users/hawonc/Desktop/plain/aircraft-models')

eng = matlab.engine.start_matlab()
eng.cd(r'../FAST-main', nargout=0)


import json
import math
import random

def gen_nums(EngineType, Passengers, Range, BA, EA):
    out = eng.testFunction(EngineType, Passengers, Range, BA, EA, nargout=5)

    max_takeoff_weight = out[0]
    empty_op_weight = out[1]
    fuel_weight = out[2]
    length = out[3]
    height = length / 8.0
    wingspan_area = out[4]
    chord_length = math.sqrt(wingspan_area * random.randint(7, 10))
    engine_dia = 0.5 + (max_takeoff_weight - 15000) * (1.1 - 0.25) / (100000 - 15000)

    # Creating a dictionary instead of a list
    result = {
        "max_takeoff_weight_kg": max_takeoff_weight,
        "empty_op_weight_kg": empty_op_weight,
        "fuel_weight_kg": fuel_weight,
        "length_m": length,
        "height_m": height,
        "wingspan_area_m2": wingspan_area,
        "chord_length_m": chord_length,
        "engine_dia_m": engine_dia
    }

    # Returning the dictionary as a JSON object
    return result

    # KG KG KG M M 
    # max-takeoff-weight empty-operating-weight fuel-weight width wingspan-area

    # find chord length with sqrt(wspa/rand(7,10))
    # find width/8

def winnable(EngineType, Passengers, Range):

    client = genai.Client(api_key="<api-key>")

    response = client.models.generate_content(
        model="gemini-2.0-flash", contents="give me a cruising altitude for a plane with engine type " + EngineType + " number of passengers " + str(Passengers) + " people and range " + str(Range) + " meters. only return 1 number in range(22000, 45000)"
    )
    BA = matlab.double([[0], [0], [int(response.text)], [int(response.text)], [0]])
    EA = matlab.double([[0], [int(response.text)], [int(response.text)], [0], [0]])
    BA_result = eng.UnitConversionPkg.ConvLength(BA, 'ft', 'm', nargout=1)
    EA_result = eng.UnitConversionPkg.ConvLength(EA, 'ft', 'm', nargout=1)
    return(gen_nums(EngineType, Passengers, Range, BA_result, EA_result))

# climb cruise descent
# start and end altitudes of phases
if len(sys.argv) != 2:
    sys.exit(len(sys.argv))

words = sys.argv[1].split()
a = words[0]
b = words[1]
c = words[2]

params = winnable(a, float(b), float(c)* 1000)

params['filename'] = scale_and_position_aircraft(params['length_m'], params['height_m'], params['wingspan_area_m2'], params['chord_length_m'], params['engine_dia_m'])

with open('out.json', 'w') as json_file:
    json.dump(params, json_file, indent=4)

# params = winnable("Turbofan", 1.0, 1.0)

# print(scale_and_position_aircraft(params[3], params[4], params[5], params[6], params[7]))
