#############################################
# Functions made here to declutter the code #
#############################################
def to_24h(timestamp: str) -> str:
    """Transform 12h (ie: 10:35:51 PM) format to 24h format (ie: 22:35:51)

    Args:
        timestamp (str): the timestamp in 12h format

    Returns:
        str: the timestamp in 24h format
    """    
    time, indicator = timestamp.split(" ")
    h, m, s = map(int, time.split(":"))

    if indicator == "PM" and h != 12:
        h += 12
    if indicator == "AM" and h == 12:
        h = 0

    return f"{h}:{m}:{s}"                   # !! Problème d'affichage des heures si AM -> 0:0:0 au lieu de 00:00:00
