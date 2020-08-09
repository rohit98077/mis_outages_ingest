from typing import List, Dict
import cx_Oracle


def getOwnersForLineReactorIds(reportsConnStr: str, ids: List[int]) -> Dict[int, str]:
    """fetches the owner names for a given list of 
    LineReactor ids

    Args:
        reportsConnStr (str): connection string to reports database
        ids (List[int]): list of LineReactor ids

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
    fetchSql = '''SELECT line_reactor.id,
                    owner_details.owners
                FROM line_reactor line_reactor
                    LEFT JOIN (
                        SELECT LISTAGG(own.owner_name, ',') WITHIN GROUP(
                                ORDER BY owner_name
                            ) AS owners,
                            parent_entity_attribute_id AS element_id
                        FROM entity_entity_reln ent_reln
                            LEFT JOIN owner own ON own.id = ent_reln.child_entity_attribute_id
                        WHERE ent_reln.child_entity = 'OWNER'
                            AND ent_reln.parent_entity = 'LINE_REACTOR'
                            AND ent_reln.child_entity_attribute = 'OwnerId'
                            AND ent_reln.parent_entity_attribute = 'Owner'
                        GROUP BY parent_entity_attribute_id
                    ) owner_details ON owner_details.element_id = line_reactor.id
                where line_reactor.id in ({0})
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
