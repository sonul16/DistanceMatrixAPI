import csv
from datetime import datetime
import distance_matrix_rest_api
import os
import schedule
import time

FILE_NAME = "distanceReport.csv"


def job():
    result = distance_matrix_rest_api.distanceMatrixAPI()

    # open the csv file to which we will append the response to be analyzed over time
    # column headers of the csv file would contain the following fields
    # origin, destination, distance(m), duration(seconds)

    fileObj = csv.writer(open(FILE_NAME, "a+"))
    # Append a blank row to create a gap with the previous set of values
    fileObj.writerow(tuple())
    fileObj.writerow((datetime.now(),))
    fileObj.writerow(["origin", "destination", "distance(m)", "duration(seconds)"])
    for jsonObj in result:
        fileObj.writerow(
            [
                jsonObj["origin_addresses"][0],
                jsonObj["destination_addresses"][0],
                jsonObj["rows"][0]["elements"][0]["distance"]["value"],
                jsonObj["rows"][0]["elements"][0]["duration"]["value"],
            ]
        )


def main():
    try:
        os.remove(FILE_NAME)
    except OSError:
        pass

    # make the first script call instantly
    job()

    # now schedule the distanceMatric API to be called every 10 minutes
    schedule.every(10).minutes.do(job)

    while True:
        schedule.run_pending()
        # this is to prevent cpu hog
        time.sleep(1)


if __name__ == "__main__":
    main()
