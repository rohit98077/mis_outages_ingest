from typing import List, Dict
import cx_Oracle


def getOwnersForAcTransLineCktIds(reportsConnStr: str, ids: List[int]) -> Dict[int, str]:
    """fetches the owner names for a given list of 
    AC Transmission line ckt ids

    Args:
        reportsConnStr (str): connection string to reports database
        ids (List[int]): list of AC Transmission line ckt ids

    Returns:
        Dict[int, str]: keys will be unit Ids, values will be comma separated owner names
    """
    # requiredIds in tuple list form
    reqIdsTxt = ','.join(tuple(set([str(x) for x in ids])))

    # connect to reports database
    con = cx_Oracle.connect(reportsConnStr)

    # sql to fetch element owners
    fetchSql = '''select ckt.id as ckt_id,
                    owner_details.owners
                from ac_transmission_line_circuit ckt
                    left join ac_trans_line_master ac_line on ckt.line_id = ac_line.id
                    left join (
                        select LISTAGG(own.owner_name, ',') WITHIN GROUP (
                                ORDER BY owner_name
                            ) AS owners,
                            parent_entity_attribute_id as element_id
                        from entity_entity_reln ent_reln
                            left join owner own on own.id = ent_reln.child_entity_attribute_id
                        where ent_reln.CHILD_ENTITY = 'OWNER'
                            and ent_reln.parent_entity = 'AC_TRANSMISSION_LINE'
                            and ent_reln.CHILD_ENTITY_ATTRIBUTE = 'OwnerId'
                            and ent_reln.PARENT_ENTITY_ATTRIBUTE = 'Owner'
                        group by parent_entity_attribute_id
                    ) owner_details on owner_details.element_id = ac_line.id
                where ckt.id in ({0})
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
