import requests
import json


coordinates = [
    ((51.72756055, 5.547473487), (51.673471, 5.604358)),
    ((51.6134128, 5.453728131), (51.673471, 5.604358)),
    ((50.6772072, 5.5959908), (50.814113, 5.166075)),
    ((50.9442881, 5.4674197), (50.814113, 5.166075)),
    ((52.3802093, 4.872755698), (51.953257, 4.55655)),
    ((52.34397807, 4.825849925), (51.953257, 4.55655)),
]


def distanceMatrixAPI():
    result = []
    parameters = {
        "mode": "driving",
        "key": "AIzaSyA5TUjA0llTsdyMfY75JOPydyjyUcRjGyA",
    }

    for origin, destination in coordinates:
        # walking the coordinates list  pairwise and setting the origins and destinations parameter
        parameters["origins"] = "{},{}".format(origin[0], origin[1])
        parameters["destinations"] = "{},{}".format(destination[0], destination[1])
        response = requests.get(
            "https://maps.googleapis.com/maps/api/distancematrix/json",
            params=parameters,
        )

        result.append(response.json())

    # print(result)
    return result
