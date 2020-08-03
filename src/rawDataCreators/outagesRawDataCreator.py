from src.fetchers.outagesFetcher import fetchOutages
import datetime as dt
import cx_Oracle
from typing import List


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
    # get connection with raw data table
    conLocal = cx_Oracle.connect(appConfig['localDb'], mode=cx_Oracle.SYSDBA)

    isRawDataInsSuccess = True
    try:
        # fetch outage events from reporting software db
        outages = fetchOutages(appConfig, startDate, endDate)
        # column names of the raw data table
        colNames = outages['columns']
        # get cursor for raw data table
        curLocal = conLocal.cursor()

        # text for sql place holders
        sqlPlceHldrsTxt = ','.join([':{0}'.format(x+1)
                                    for x in range(len(colNames))])

        # delete the rows which are already present
        pwcIdColInd = colNames.index('PWC_ID')
        pwcIds = [(x[pwcIdColInd],) for x in outages['rows']]
        curLocal.executemany(
            "delete from outage_events where PWC_ID=:1", pwcIds)

        # insert the raw data
        ouatageEvntsInsSql = 'insert into outage_events({0}) values ({1})'.format(
            ','.join(colNames), sqlPlceHldrsTxt)

        curLocal.executemany(ouatageEvntsInsSql, outages['rows'])

        # commit the changes
        conLocal.commit()
    except Exception as e:
        isRawDataInsSuccess = False
        print('Error while bulk insertion of outage events into raw data db')
        print(e)
    finally:
        # closing database cursor and connection
        if curLocal is not None:
            curLocal.close()
        conLocal.close()
    return isRawDataInsSuccess
