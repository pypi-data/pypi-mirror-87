from enum import Enum


class LINE_STYLE(Enum):

    solid = 1
    dashed = 2
    dashdot = 3
    dotted = 4


class CAP_STYLE(Enum):

    butt = 1
    round = 2
    projecting = 3


class JOIN_STYLE(Enum):

    miter = 1
    round = 2
    bevel = 3


class ARROW_STYLE(Enum):

    Curve = 1
    CurveB = 2
    BracketB = 3
    CurveFilledB = 4
    CurveA = 5
    CurveAB = 6
    CurveFilledA = 7
    CurveFilledAB = 8
    BracketA = 9
    BracketAB = 10
    Fancy = 11
    Simple = 12
    Wedge = 13
    BarAB = 14

    def get_name(self):

        return {
            'Curve': '-',
            'CurveB': '->',
            'BracketB': '-[',
            'CurveFilledB': '-|>',
            'CurveA': '<-',
            'CurveAB': '<->',
            'CurveFilledA': '<|-',
            'CurveFilledAB': '<|-|>',
            'BracketA': ']-',
            'BracketAB': ']-[',
            'Fancy': 'fancy',
            'Simple': 'simple',
            'Wedge': 'wedge',
            'BarAB': '|-|',
        }[self.name]


class CONNECTION_STYLE(Enum):

    angle = 1
    angle3 = 2
    arc = 3
    arc3 = 4
    bar = 5
