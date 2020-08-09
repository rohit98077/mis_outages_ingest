from typing import List, Dict
import cx_Oracle


def getOwnersForBusIds(reportsConnStr: str, ids: List[int]) -> Dict[int, str]:
    """fetches the owner names for a given list of 
    Bus ids

    Args:
        reportsConnStr (str): connection string to reports database
        ids (List[int]): list of Bus ids

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
    fetchSql = '''SELECT bus.id,
                    owner_details.owners
                FROM bus bus
                    left join associate_substation subs on subs.id = bus.fk_substation_id
                    LEFT JOIN (
                        SELECT LISTAGG(own.owner_name, ',') WITHIN GROUP(
                                ORDER BY owner_name
                            ) AS owners,
                            parent_entity_attribute_id AS element_id
                        FROM entity_entity_reln ent_reln
                            LEFT JOIN owner own ON own.id = ent_reln.child_entity_attribute_id
                        WHERE ent_reln.child_entity = 'OWNER'
                            AND ent_reln.parent_entity = 'ASSOCIATE_SUBSTATION'
                            AND ent_reln.child_entity_attribute = 'OwnerId'
                            AND ent_reln.parent_entity_attribute = 'Owner'
                        GROUP BY parent_entity_attribute_id
                    ) owner_details ON owner_details.element_id = subs.id
                where bus.id in ({0})
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
