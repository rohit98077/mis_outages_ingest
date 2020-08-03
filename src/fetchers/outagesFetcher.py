from typing import List, Tuple, TypedDict
import datetime as dt
import cx_Oracle
import pandas as pd
from src.utils.timeUtils import getTimeDeltaFromDbStr


class Outages(TypedDict):
    columns: List[str]
    rows: List[Tuple]


def fetchOutages(appConfig: dict, startDate: dt.datetime, endDate: dt.datetime) -> Outages:
    """fetches outages from reports database

    Args:
        appConfig (dict): application configuration
        startDate (dt.datetime): start date
        endDate (dt): end date

    Returns:
        Outages: Each tuple will have the following attributes
        column names should be
        'PWC_ID', 'ELEMENT_ID', 'ELEMENT_NAME', 'ENTITY_ID', 'ENTITY_NAME', 
        'INSTALLED_CAPACITY', 'OUTAGE_DATETIME', 'REVIVED_DATETIME', 
        'CREATED_DATETIME', 'MODIFIED_DATETIME', 'SHUTDOWN_TAG', 
        'SHUTDOWN_TAG_ID', 'SHUTDOWN_TYPENAME', 'SHUT_DOWN_TYPE_ID', 
        'OUTAGE_REMARKS', 'REASON', 'REASON_ID', 'REVIVAL_REMARKS', 
        'REGION_ID', 'SHUTDOWNREQUEST_ID'
    """
    # get the reports connection string
    reportsConnStr = appConfig['conStr']

    # connect to reports database
    con = cx_Oracle.connect(reportsConnStr)

    # sql query to fetch the outages
    outagesFetchSql = '''select rto.ID as pwc_id, rto.ELEMENT_ID,rto.ELEMENTNAME as ELEMENT_NAME,
    rto.ENTITY_ID, ent_master.ENTITY_NAME, gen_unit.installed_capacity, rto.OUTAGE_DATE as OUTAGE_DATETIME, 
    rto.REVIVED_DATE as REVIVED_DATETIME, rto.CREATED_DATE as CREATED_DATETIME, 
    rto.MODIFIED_DATE as MODIFIED_DATETIME, sd_tag.name as shutdown_tag,rto.SHUTDOWN_TAG_ID, 
    sd_type.name as shutdown_typename,rto.SHUT_DOWN_TYPE as SHUT_DOWN_TYPE_ID, rto.OUTAGE_REMARKS, 
    reas.reason,rto.REASON_ID, rto.REVIVAL_REMARKS, rto.REGION_ID, 
    rto.SHUTDOWNREQUEST_ID,rto.OUTAGE_TIME, rto.REVIVED_TIME
    from real_time_outage rto left join outage_reason reas on reas.id = rto.reason_id
    left join shutdown_outage_tag sd_tag on sd_tag.id = rto.shutdown_tag_id
    left join shutdown_outage_type sd_type on sd_type.id = rto.shut_down_type
    left join entity_master ent_master on ent_master.id = rto.ENTITY_ID
    left join generating_unit gen_unit on gen_unit.id = rto.element_id 
    where (rto.OUTAGE_DATE between :1 and :2) or (rto.revived_date between :1 and :2) 
    or (rto.MODIFIED_DATE between :1 and :2) or (rto.CREATED_DATE between :1 and :2)'''
    cur = con.cursor()
    cur.execute(outagesFetchSql, (startDate, endDate))
    colNames = [row[0] for row in cur.description]
    # print(colNames)
    colNames = colNames[0:-2]
    dbRows = cur.fetchall()
    # print(dbRows)
    outDateIndexInRow: int = 6
    revDateIndexInRow: int = 7
    for rIter in range(len(dbRows)):
        # convert tuple to list to facilitate manipulation
        dbRows[rIter] = list(dbRows[rIter])

        if not pd.isnull(dbRows[rIter][outDateIndexInRow]):
            # convert string to time delta
            outTimeStr = dbRows[rIter][-2]
            outTimeDelta = getTimeDeltaFromDbStr(outTimeStr)
            # add out time to out date to get outage timestamp
            dbRows[rIter][outDateIndexInRow] += outTimeDelta

        if not pd.isnull(dbRows[rIter][outDateIndexInRow]):
            # convert string to time delta
            revTimeStr = dbRows[rIter][-2]
            revTimeDelta = getTimeDeltaFromDbStr(revTimeStr)
            # add revival time to out date to get revival timestamp
            dbRows[rIter][revDateIndexInRow] += revTimeDelta

        # remove last 2 column of the row
        dbRows[rIter] = dbRows[rIter][0:-2]
        dbRows[rIter] = tuple(dbRows[rIter])

    return {'columns': colNames, 'rows': dbRows}
