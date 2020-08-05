from src.fetchers.outagesFetcher import fetchOutages
import datetime as dt
import cx_Oracle
from typing import List
from src.repos.outagesRepo import OutagesRepo


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
    localDbConStr = appConfig['localDb']

    # get the instance of outages repository
    outagesRepo = OutagesRepo(localDbConStr)

    # fetch outage events from reporting software db
    outages = fetchOutages(appConfig, startDate, endDate)

    # insert outages into db via the repository instance
    isRawDataInsSuccess = outagesRepo.insertOutages(outages)

    return isRawDataInsSuccess
