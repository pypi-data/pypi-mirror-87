from __future__ import annotations

import datetime
from typing import Union

from typing_extensions import Literal

from .._measures.calculated_measure import CalculatedMeasure, Operator
from ..measure import Measure, _convert_to_measure

DateOrMeasure = Union[Measure, datetime.date, datetime.datetime]

_Unit = Literal[  # pylint: disable=invalid-name
    "seconds", "minutes", "hours", "days", "weeks", "months", "years"
]


def date_diff(
    from_date: DateOrMeasure, to_date: DateOrMeasure, *, unit: _Unit = "days",
) -> Measure:
    """Return a measure equal to the difference between two dates.

    If one of the date is ``N/A`` then ``None`` is returned.

    Example:
        .. code::

            m["diff"] = atoti.date_diff(m["start_date"], m["end_date"])

        +------------+------------+------+
        | start_date | end_date   | diff |
        +============+============+======+
        | 2020-01-01 | 2020-01-02 | 1    |
        +------------+------------+------+
        | 2020-02-01 | 2020-02-21 | 20   |
        +------------+------------+------+
        | 2020-03-20 | N/A        |      |
        +------------+------------+------+
        | 2020-05-15 | 2020-04-15 | -30  |
        +------------+------------+------+


    Args:
        from_date: The first date measure or object.
        to_date: The second date measure or object.
        unit: The difference unit.
            Seconds, minutes and hours are only allowed if the dates contain time information.

    """
    return CalculatedMeasure(
        Operator(
            "datediff",
            [_convert_to_measure(from_date), _convert_to_measure(to_date), unit],
        )
    )
