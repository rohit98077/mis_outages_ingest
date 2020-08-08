from typing import List, Dict
import cx_Oracle


def getOwnersForFscIds(reportsConnStr: str, ids: List[int]) -> Dict[int, str]:
    """fetches the owner names for a given list of 
    Fsc ids

    Args:
        reportsConnStr (str): connection string to reports database
        ids (List[int]): list of Fsc ids

    Returns:
        Dict[int, str]: keys will be element Ids, values will be comma separated owner names
    """
    # requiredIds in tuple list form
    reqIdsTxt = ','.join(tuple(set([str(x) for x in ids])))

    # connect to reports database
    con = cx_Oracle.connect(reportsConnStr)

    # sql to fetch element owners
    fetchSql = '''SELECT fsc.id,
                    owner_details.owners
                FROM fsc fsc
                    LEFT JOIN (
                        SELECT LISTAGG(own.owner_name, ',') WITHIN GROUP(
                                ORDER BY owner_name
                            ) AS owners,
                            parent_entity_attribute_id AS element_id
                        FROM entity_entity_reln ent_reln
                            LEFT JOIN owner own ON own.id = ent_reln.child_entity_attribute_id
                        WHERE ent_reln.child_entity = 'OWNER'
                            AND ent_reln.parent_entity = 'FSC'
                            AND ent_reln.child_entity_attribute = 'OwnerId'
                            AND ent_reln.parent_entity_attribute = 'Owner'
                        GROUP BY parent_entity_attribute_id
                    ) owner_details ON owner_details.element_id = fsc.id
                where fsc.id in ({0})
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
