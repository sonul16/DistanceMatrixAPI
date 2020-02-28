import csv
from datetime import datetime
import distance_matrix_rest_api
import os
import schedule
import time

FILE_NAME = "distanceReport2.csv"


def job(firstRun=False):
    def originAddr(jsonObj):
        return jsonObj["origin_addresses"][0]

    def destAddr(jsonObj):
        return jsonObj["destination_addresses"][0]

    def distanceVal(jsonObj):
        return jsonObj["rows"][0]["elements"][0]["distance"]["value"]

    def durationVal(jsonObj):
        return jsonObj["rows"][0]["elements"][0]["duration"]["value"]

    result = distance_matrix_rest_api.distanceMatrixAPI()

    # open the csv file to which we will append the response to be analyzed over time
    # row headers of the csv file would contain the following fields
    # origins, destinations, distance(m), duration(seconds)

    fileObj = csv.writer(open(FILE_NAME, "a+"))
    if firstRun:
        originList = ["origins"] + [originAddr(jsonObj) for jsonObj in result]
        destList = ["destinations"] + [destAddr(jsonObj) for jsonObj in result]
        fileObj.writerow(originList)
        fileObj.writerow(destList)

    fileObj.writerow([datetime.now()])

    distanceRow = ["distance(m)"] + [distanceVal(jsonObj) for jsonObj in result]
    durationRow = ["duration(seconds)"] + [durationVal(jsonObj) for jsonObj in result]
    fileObj.writerow(distanceRow)
    fileObj.writerow(durationRow)


def main():
    try:
        os.remove(FILE_NAME)
    except OSError:
        pass

    # make the first script call instantly
    job(firstRun=True)

    # now schedule the distanceMatric API to be called every 10 minutes
    schedule.every(10).minutes.do(job)

    while True:
        schedule.run_pending()
        # this is to prevent cpu hog
        time.sleep(1)


if __name__ == "__main__":
    main()
