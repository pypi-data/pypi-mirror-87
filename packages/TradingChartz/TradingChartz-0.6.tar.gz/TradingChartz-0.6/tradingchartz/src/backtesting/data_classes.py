# import standard
from dataclasses import dataclass


@dataclass
class TripleBarrierSetter:
    """
    Consist of six components:
    Upper: Risk reward ratio
    Lower: multiplier of price move field to set the stop loss level.
        definition of upper and lower will be reversed fro short position.
    Vertical: # of bars to set the investment time stamp.
    Price move field: Field based on which lower barrier is calculated by substracting from entry price.
    Lower_min: To add minimum stop loss condition i.e 0.02 value will ensure there is no stop loss less than 2%
    Lower_max: To add maximum stop loss condition i.e. 0.1 value will ensure there is no stop loss bigger than 10%
    if price move is none, barriers will be calculated based on entry point price.
    """
    ratio: float = 1
    vertical: int = 0
    lower_barrier_field: str = "Close"
    lower_min: float = None
    lower_max: float = None


@dataclass
class TripleBarrier:
    """
    Consist of four components:
    Upper: multiplier of price move field to set the profit booking level.
    Lower: multiplier of price move field to set the stop loss level.
        definition of upper and lower will be reversed fro short position.
    Vertical: # of bars to set the investment time stamp.
    Price move field: % return field based on which barrier will be calculated. Default wil be set to 1.
    if price move is none, barriers will be calculated based on entry point price.
    """
    upper: float = 0.0
    lower: float = 0.0
    vertical: int = 0
    price_move_field: str = None


@dataclass
class TripleBarrierConfig:
    """

    """
    entry_point_field: 'str'
