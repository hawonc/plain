import matlab.engine
import random
import math
from google import genai
from aircraft import scale_and_position_aircraft
eng = matlab.engine.start_matlab()
eng.cd(r'../FAST-main', nargout=0)


def gen_nums(EngineType, Passengers, Range, BA, EA):
    out = eng.testFunction(EngineType,Passengers,Range,BA,EA, nargout=5)

    max_takeoff_weight = out[0]
    empty_op_weight = out[1]
    fuel_weight = out[2]
    length = out[3]
    height = length/8.0
    wingspan_area = out[4]
    chord_length = math.sqrt(wingspan_area*random.randint(7,10))
    engine_dia = 0.5 + (max_takeoff_weight - 15000) * (1.5 - 0.25) / (100000 - 15000)
    return([max_takeoff_weight, empty_op_weight, fuel_weight, length, height, wingspan_area, chord_length, engine_dia])


    # KG KG KG M M 
    # max-takeoff-weight empty-operating-weight fuel-weight width wingspan-area

    # find chord length with sqrt(wspa/rand(7,10))
    # find width/8

def winnable(EngineType, Passengers, Range):

    client = genai.Client(api_key="")

    response = client.models.generate_content(
        model="gemini-2.0-flash", contents="give me a cruising altitude for a plane with engine type " + EngineType + " number of passengers " + str(Passengers) + " people and range " + str(Range) + " meters. only return 1 number in range(22000, 45000)"
    )
    print(int(response.text))
    BA = matlab.double([[0], [0], [int(response.text)], [int(response.text)], [0]])
    EA = matlab.double([[0], [int(response.text)], [int(response.text)], [0], [0]])
    BA_result = eng.UnitConversionPkg.ConvLength(BA, 'ft', 'm', nargout=1)
    EA_result = eng.UnitConversionPkg.ConvLength(EA, 'ft', 'm', nargout=1)
    return(gen_nums(EngineType, Passengers, Range, BA_result, EA_result))

# climb cruise descent
# start and end altitudes of phases

a = input("Fan type: (Turbofan/Turboprop) ")
b = input("Number of Passengers: ")
c = input("Range: (in Kilometers) ")

params = winnable(a, float(b), float(c)* 1000)

print(scale_and_position_aircraft(params[3], params[4], params[5], params[6], params[7]))


# params = winnable("Turbofan", 1.0, 1.0)

# print(scale_and_position_aircraft(params[3], params[4], params[5], params[6], params[7]))
