def extractVoltFromName(elemType: str, elemName: str) -> str:
    """extracts voltage level from element name of reporting software outage entry

    Args:
        elemType (str): element type, like TRANSFORMER, GENERATING_UNIT etc
        elemName (str): Name of the element

    Returns:
        str: voltage level
    """
    # TODO implement this
    elemVoltLvl: str = ''
    if elemType in ['FSC', 'AC_TRANSMISSION_LINE_CIRCUIT', 'LINE_REACTOR']:
        # FSC like '400KV-APL-MUNDRA-SAMI-1 FSC@ SAMI'
        # ac trans line ckt like '132KV-BINA-MP-MORWA-1'
        # line reactor like '400KV-AKOLA-AURANGABAD-2 L/R@ AKOLA - 400KV'
        # find the index of 'KV-' to get the voltage level string
        kvInd = elemName.index('KV-')
        elemVoltLvl = elemName[0:kvInd+2]
    elif elemType == 'HVDC_LINE_CIRCUIT':
        # HVDC400KV-Vindyachal(PS)-RIHAND-1
        # find the index of 'KV-' to get the voltage level string
        kvInd = elemName.index('KV-')
        elemVoltLvl = elemName[4:kvInd+2]
    elif elemType == 'BUS REACTOR':
        # AKOLA (2) - 765KV B/R 1
        # find the index of ' - ', 'KV B/R' to get the voltage level string
        kvStartInd = elemName.index(' - ') + 3
        kvInd = elemName.index('KV B/R')
        elemVoltLvl = elemName[kvStartInd:kvInd+2]
    elif elemType == 'TRANSFORMER':
        # 1200KV/400KV BINA-ICT-1
        # find the index of 'KV ' to get the voltage level string
        kvInd = elemName.index('KV ')
        elemVoltLvl = elemName[0:kvInd+2]
    elif elemType == 'HVDC POLE':
        hvdcPoleOwners[elemId] = ''
    elif elemType == 'BUS':
        busOwners[elemId] = ''
    elif elemType == 'Bay':
        bayOwners[elemId] = ''
    elif elemType in ['TCSC', 'FSC', 'MSR', 'MSC', 'STATCOM']:
        compensatorOwners[elemId] = ''
    return elemVoltLvl
