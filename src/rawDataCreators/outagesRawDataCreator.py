from src.fetchers.outagesFetcher import fetchOutages
import datetime as dt
import cx_Oracle
from typing import List
from src.repos.outages.outagesRepo import OutagesRepo


def createOutageEventsRawData(appConfig: dict, startDate: dt.datetime, endDate: dt.datetime) -> bool:
    """fetches the outages data from reporting software 
    and pushes it to the raw data table

    Args:
        appConfig (dict): application configuration
        startDate (dt.datetime): start date
        endDate (dt.datetime): end date

    Returns:
        [bool]: returns True if succeded
    """
    # get the connection string of application db
    appDbConStr = appConfig['appDbConStr']

    # set batch size for scalability concerns
    fetchBatchNumDays = 100

    currDate = startDate
    
    isRawDataInsSuccess = False

    while currDate <= endDate:
        batchStartDate = currDate
        batchEndDate = batchStartDate + \
            dt.timedelta(days=fetchBatchNumDays) - dt.timedelta(seconds=1)
        if batchEndDate > endDate:
            batchEndDate = endDate
        
        # get the instance of outages repository
        outagesRepo = OutagesRepo(appDbConStr)

        # fetch outage events from reporting software db
        outages = fetchOutages(appConfig, batchStartDate, batchEndDate)

        # insert outages into db via the repository instance
        isRawDataInsSuccess = outagesRepo.insertOutages(outages)

        # update currDate
        currDate += dt.timedelta(days=fetchBatchNumDays)

    return isRawDataInsSuccess
