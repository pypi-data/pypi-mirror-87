from .._measures.calculated_measure import CalculatedMeasure, Operator
from ..measure import Measure, MeasureLike, _convert_to_measure


def abs(measure: Measure) -> Measure:  # pylint: disable=redefined-builtin
    """Return a measure equal to the absolute value of the passed measure."""
    return CalculatedMeasure(Operator("abs", [measure]))


def exp(measure: Measure) -> Measure:
    """Return a measure equal to the exponential value of the passed measure."""
    return CalculatedMeasure(Operator("exp", [measure]))


def log(measure: Measure) -> Measure:
    """Return a measure equal to the natural logarithm (base *e*) of the passed measure."""
    return CalculatedMeasure(Operator("log", [measure]))


def log10(measure: Measure) -> Measure:
    """Return a measure equal to the base 10 logarithm of the passed measure."""
    return CalculatedMeasure(Operator("log10", [measure]))


def floor(measure: Measure) -> Measure:
    """Return a measure equal to the largest integer <= to the passed measure."""
    return CalculatedMeasure(Operator("floor", [measure]))


def ceil(measure: Measure) -> Measure:
    """Return a measure equal to the smallest integer that is >= to the passed measure."""
    return CalculatedMeasure(Operator("ceil", [measure]))


def round(measure: Measure) -> Measure:  # pylint: disable=redefined-builtin
    """Return a measure equal to the closest integer to the passed measure."""
    return CalculatedMeasure(Operator("round", [measure]))


def sin(measure: Measure) -> Measure:
    """Return a measure equal to the sine of the passed measure in radians."""
    return CalculatedMeasure(Operator("sin", [measure]))


def cos(measure: Measure) -> Measure:
    """Return a measure equal to the cosine of the passed measure in radians."""
    return CalculatedMeasure(Operator("cos", [measure]))


def tan(measure: Measure) -> Measure:
    """Return a measure equal to the tangent of the passed measure in radians."""
    return CalculatedMeasure(Operator("tan", [measure]))


def sqrt(measure: Measure) -> Measure:
    """Return a measure equal to the square root of the passed measure."""
    return measure ** 0.5


def max(*measures: MeasureLike) -> Measure:  # pylint: disable=redefined-builtin
    """Return a measure equal to the maximum of the passed arguments."""
    if len(measures) < 2:
        raise ValueError(
            "This function is not made to compute the maximum of a single measure."
            " To find the maximum value of this measure on the levels it is expressed,"
            " use atoti.agg.max() instead."
        )
    return CalculatedMeasure(
        Operator("max", [_convert_to_measure(measure) for measure in measures])
    )


def min(*measures: MeasureLike) -> Measure:  # pylint: disable=redefined-builtin
    """Return a measure equal to the minimum of the passed arguments."""
    if len(measures) < 2:
        raise ValueError(
            "You can not calculate the min of a single measure using this function. "
            "If you want to find the minimum value of this measure on the levels it is defined on, use atoti.agg.min"
        )
    return CalculatedMeasure(
        Operator("min", [_convert_to_measure(measure) for measure in measures])
    )


def erf(measure: MeasureLike) -> Measure:
    """Return the error function of the input measure.

    This can be used to compute traditional statistical measures such as the cumulative standard normal distribution.

    For more information read:

      * Python's built-in :func:`math.erf`
      * `scipy.special.erf <https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.erf.html>`_
      * `The Wikipedia page <https://en.wikipedia.org/wiki/Error_function#Numerical_approximations>`_
    """
    return CalculatedMeasure(Operator("erf", [_convert_to_measure(measure)]))


def erfc(measure: MeasureLike) -> Measure:
    """Return the complementary error function of the input measure.

    This is the complementary of :func:`atoti.math.erf`.
    It is defined as ``1.0 - erf``.
    It can be used for large values of x where a subtraction from one would cause a loss of significance.
    """
    return CalculatedMeasure(Operator("erfc", [_convert_to_measure(measure)]))
