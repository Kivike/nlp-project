from enum import Enum

"""
London area postcodes can be found from https://www.milesfaster.co.uk/postcodes/ and
additional details and links from https://www.milesfaster.co.uk/london-postcodes-list.htm
"""

class PostCodeArea(Enum):
    """Post code areas.
    """
    LONDON_AREA = [ "E", "EC", "N", "NW", "SE", "SW", "W", "WC" ]

class PostCodeDistrict(Enum):
    """Post code districts.
    """
    LONDON_CENTRAL = [ "W1", "W2", "W8", "W9", "SW1", "SW3", "SW5", "SW6", "SW7", "SW10", "SW11", "WC1", "WC2" ]
    LONDON_CENTRAL_EAST = [ "EC1", "EC2", "EC3", "EC4" ]
    LONDON_NORTH = [ "N1", "N3", "N4", "N10", "N12", "N14", "N19", "N20", "NW1", "NW2", "NW3", "NW4", "NW6", "NW7", "NW8", "NW9", "NW10", "NW11" ]
    LONDON_EAST = [ "E1", "E2", "E3", "E4", "E6", "E7", "E8", "E9", "E10", "E13", "E14", "E15", "E16", "E17", "E20" ]
    LONDON_SOUTH = [ "SE1", "SE3", "SE5", "SE9", "SE10", "SE16", "SE18", "SE19", "SE24", "SW4", "SW8", "SW12", "SW15", "SW16", "SW18", "SW19" ]
    LONDON_WEST = [ "W2", "W3", "W4", "W5", "W6", "W7", "W8", "W9", "W11", "W12", "W13", "W14" ]
