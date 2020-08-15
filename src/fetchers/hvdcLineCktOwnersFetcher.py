from typing import List, Dict
import cx_Oracle


def getOwnersForHvdcLineCktIds(reportsConnStr: str, ids: List[int]) -> Dict[int, str]:
    """fetches the owner names for a given list of 
    HvdcLineCkt ids

    Args:
        reportsConnStr (str): connection string to reports database
        ids (List[int]): list of HvdcLineCkt ids

    Returns:
        Dict[int, str]: keys will be element Ids, values will be comma separated owner names
    """
    if len(ids) == 0:
        return {}
    # requiredIds in tuple list form
    reqIdsTxt = ','.join(tuple(set([str(x) for x in ids])))

    # connect to reports database
    con = cx_Oracle.connect(reportsConnStr)

    # sql to fetch element owners
    fetchSql = '''SELECT hvdc_ckt.id,
                    owner_details.owners
                FROM REPORTING_WEB_UI_UAT.hvdc_line_circuit hvdc_ckt
                    LEFT JOIN (
                        SELECT LISTAGG(own.owner_name, ',') WITHIN GROUP(
                                ORDER BY owner_name
                            ) AS owners,
                            parent_entity_attribute_id AS element_id
                        FROM REPORTING_WEB_UI_UAT.entity_entity_reln ent_reln
                            LEFT JOIN REPORTING_WEB_UI_UAT.owner own ON own.id = ent_reln.child_entity_attribute_id
                        WHERE ent_reln.child_entity = 'OWNER'
                            AND ent_reln.parent_entity = 'HVDC_LINE'
                            AND ent_reln.child_entity_attribute = 'OwnerId'
                            AND ent_reln.parent_entity_attribute = 'Owner'
                        GROUP BY parent_entity_attribute_id
                    ) owner_details ON owner_details.element_id = hvdc_ckt.id
                where hvdc_ckt.id in ({0})
    '''.format(reqIdsTxt)
    # get cursor for querying
    cur = con.cursor()

    # execute fetch sql
    cur.execute(fetchSql, [])
    dbRows = cur.fetchall()
    ownersDict: Dict[int, str] = {}
    for row in dbRows:
        ownersDict[row[0]] = row[1]
    # print(dbRows)
    # print(ownersDict)
    return ownersDict
