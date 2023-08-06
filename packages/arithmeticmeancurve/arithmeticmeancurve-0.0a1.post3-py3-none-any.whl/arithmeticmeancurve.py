import re
from abc import ABC, abstractmethod
from collections import namedtuple
from typing import Union, Iterable, List, Dict, Generator, Tuple, Optional
import numpy
import pandas
from scipy import stats
from pandas import DataFrame, Series
from trashpanda import cut_after

__version__ = "0.0a1.post3"

__all__ = [
    "ArithmeticMeanCurve",
    "convert_set_to_family_of_curves",
    "FrozenStdExtrapolation",
    "merge_set_of_curves_to_family",
    "_merge_two_curves",
]


Curves = Union[numpy.ndarray, DataFrame]
Curve = Union[numpy.ndarray, DataFrame]
AnArray = Union[numpy.ndarray, Iterable[Union[int, float]]]


SetOfCurves = List[DataFrame]
"""
A set of unique curves with separately x-values.
"""

RawFamilyOfCurves = DataFrame
"""
A family of unique curves with common x-values and only their original y-values.
"""

FamilyOfCurves = DataFrame
"""
A family of unique curves with common x-values and interpolated y-values. 
"""

ValidationResult = namedtuple("ValidationMessage", "correct error_message error_type")

_NON_MATCHING_COLUMN_COUNT_MESSAGE = (
    "Column-count of the provided curves doesn't match."
)
_NON_MONOTONIC_INCREASING_X = "x-values needs to be monotonic increasing."


DEFAULT_STD_CIRCLE_NAME = "std circle"

_MATCHES_NAME_WITH_NUMBER_POSTFIX = re.compile(r"(.*)(_[0-9]+)$")


def _get_column_basename(column_name: str) -> str:
    """

    Args:
        column_name:

    Returns:

    Test:
        >>> from arithmeticmeancurve import _get_column_basename
        >>> _get_column_basename("column_1")
        'column'
        >>> _get_column_basename("column_12")
        'column'
        >>> _get_column_basename("column")
        'column'
        >>> _get_column_basename("column")
        'column'
        >>> _get_column_basename("a key_0")
        'a key'
        >>> _get_column_basename("a_0")
        'a'

    """
    matched_column_name = _MATCHES_NAME_WITH_NUMBER_POSTFIX.match(column_name)
    found_no_match_because_no_postfix = matched_column_name is None
    if found_no_match_because_no_postfix:
        return column_name
    return matched_column_name.group(1)


def _group_column_names_with_postfixed_numbers(
    column_names_with_postfixes: List[str],
) -> Dict[str, List[str]]:
    """
    Sorts column names into groups.

    Args:
        column_names_with_postfixes(str):
            Column names which got a postfix by
            :func:`arithmeticmeancurve._number_column_name`.

    Returns:
        Dict[str, List[str]]:
            A mapping with the group base name as key and this groups column
            names.

    Examples:
        >>> from arithmeticmeancurve import _group_column_names_with_postfixed_numbers
        >>> _group_column_names_with_postfixed_numbers(
        ...     ["column_0", "z_0", "a key_0", "column_1", "z_1", "a key_1"]
        ... )
        {'column': ['column_0', 'column_1'], 'z': ['z_0', 'z_1'], 'a key': ['a key_0', 'a key_1']}
    """
    column_groups = {}
    for name_with_postfix in column_names_with_postfixes:
        base_name = _get_column_basename(name_with_postfix)
        if base_name not in column_groups:
            column_groups[base_name] = []
        column_groups[base_name].append(name_with_postfix)
    return column_groups


def _number_column_name(column_name: str, number: int) -> str:
    """
    Adds a postfix to a column.

    Args:
        column_name(st):
            Column name which gets the postfix.

        number(int):
            The number for the column.

    Returns:
        str
    """
    return "{}_{}".format(column_name, number)


def _all_ndarrays_have_equal_column_count(
    different_curves: List[numpy.ndarray],
) -> bool:
    """
    Validates if all curves have an equal column count.

    Args:
        different_curves(numpy.ndarray):
            Different (x, y-1, ...) curves, which consist of at least 2 columns.

    Returns:
        bool

    Test:
        >>> from arithmeticmeancurve import _all_ndarrays_have_equal_column_count
        >>> import numpy as np
        >>> _all_ndarrays_have_equal_column_count(
        ...     [numpy.arange(9).reshape(3, 3), numpy.arange(12).reshape(4, 3)]
        ... )
        True
        >>> _all_ndarrays_have_equal_column_count(
        ...     [numpy.arange(8).reshape(4, 2), numpy.arange(12).reshape(4, 3)]
        ... )
        False
        >>> _all_ndarrays_have_equal_column_count(
        ...     [numpy.arange(12).reshape(4, 3), numpy.arange(8).reshape(4, 2)]
        ... )
        False
    """
    first_curve: numpy.ndarray = different_curves[0]
    first_column_count = first_curve.shape[1]
    for curves in different_curves[1:]:
        column_count_of_curves = curves.shape[1]
        if first_column_count != column_count_of_curves:
            return False
    return True


def _all_dataframes_have_equal_column_count(different_curves: List[DataFrame]) -> bool:
    """


    Args:
        different_curves(numpy.ndarray):
            Different (x, y-1, ...) curves, which consist of at least 2 columns.

    Returns:

    Test:
        >>> from arithmeticmeancurve import _all_dataframes_have_equal_column_count
        >>> import numpy as np
        >>> from pandas import DataFrame
        >>> _all_dataframes_have_equal_column_count(
        ...     [
        ...         DataFrame(numpy.arange(9).reshape(3, 3)),
        ...         DataFrame(numpy.arange(12).reshape(4, 3))
        ...     ]
        ... )
        True
        >>> _all_dataframes_have_equal_column_count(
        ...     [
        ...         DataFrame(numpy.arange(8).reshape(4, 2)),
        ...         DataFrame(numpy.arange(12).reshape(4, 3))
        ...     ]
        ... )
        False
        >>> _all_dataframes_have_equal_column_count(
        ...     [
        ...         DataFrame(numpy.arange(12).reshape(4, 3)),
        ...         DataFrame(numpy.arange(8).reshape(4, 2))
        ...     ]
        ... )
        False

    """
    first_column_count = len(different_curves[0].columns)
    for curves in different_curves[1:]:
        column_count_of_curves = len(curves.columns)
        if first_column_count != column_count_of_curves:
            return False
    return True


def _ndarray_has_monotonic_increasing_x(curves: numpy.ndarray) -> bool:
    """

    Args:
        curves:

    Returns:

    Raises:

    Test:
        >>> import numpy
        >>> from arithmeticmeancurve import _ndarray_has_monotonic_increasing_x
        >>> _ndarray_has_monotonic_increasing_x(numpy.array([[1, 4], [2, 4], [3, 5]]))
        True
        >>> _ndarray_has_monotonic_increasing_x(numpy.array([[2, 4], [1, 4], [3, 5]]))
        False

    """
    x_values = curves[:, 0]
    return numpy.all(numpy.diff(x_values) > 0)


def _dataframe_has_monotonic_increasing_x(curves: DataFrame) -> bool:
    """
    Checks if curves have monotonic increasing abzissa values (x-values).

    Args:
        curves(DataFrame):
            Curves which should be checked for monotonic increasing index.

    Returns:

    Raises:
        ValueError:
            If not a 1-dimensional array.

    Test:
        >>> import numpy
        >>> from arithmeticmeancurve import _dataframe_has_monotonic_increasing_x
        >>> _dataframe_has_monotonic_increasing_x(DataFrame([1, 2, 3], index=[1, 2, 3]))
        True
        >>> _dataframe_has_monotonic_increasing_x(DataFrame([1, 2, 3], index=[2, 1, 3]))
        False

    """
    x_values = curves.index
    return numpy.all(numpy.diff(x_values) > 0)


def _dataframes_are_valid_for_calculation(*different_curves,) -> ValidationResult:
    """

    Args:
        *different_curves(numpy.ndarray):
            Different (x, y-1, ...) curves, which consist of at least 2 columns.

    Returns:

    Notes:
        Tested via _input_curves_are_valid_for_calculation docstring

    """
    if not _all_dataframes_have_equal_column_count(*different_curves):
        return ValidationResult(False, _NON_MATCHING_COLUMN_COUNT_MESSAGE, ValueError)
    return ValidationResult(True, None, None)


def _ndarrays_are_valid_for_calculation(*different_curves,) -> ValidationResult:
    """

    Args:
        *different_curves(Iterable[numpy.ndarray]):
            Different (x, y-1, ...) curves, which consist of at least 2 columns.

    Returns:

    Notes:
        Tested via _input_curves_are_valid_for_calculation docstring

    """
    if not _all_ndarrays_have_equal_column_count(*different_curves):
        return ValidationResult(False, _NON_MATCHING_COLUMN_COUNT_MESSAGE, ValueError)
    return ValidationResult(True, None, None)


def _input_curves_are_valid_for_calculation(
    different_curves: List[numpy.ndarray],
) -> ValidationResult:
    """

    Args:
        different_curves:

    Returns:
        ValidationResult

    Test:
        >>> from arithmeticmeancurve import _input_curves_are_valid_for_calculation
        >>> import numpy as np
        >>> _input_curves_are_valid_for_calculation(
        ...     [numpy.arange(9).reshape(3, 3), numpy.arange(12).reshape(4, 3)]
        ... )
        ValidationMessage(correct=True, error_message=None, error_type=None)
        >>> _input_curves_are_valid_for_calculation(
        ...     [numpy.arange(8).reshape(4, 2), numpy.arange(12).reshape(4, 3)]
        ... )
        ValidationMessage(correct=False, error_message="Column-count of the provided curves doesn't match.", error_type=<class 'ValueError'>)
        >>> _input_curves_are_valid_for_calculation(
        ...     [numpy.arange(12).reshape(4, 3), numpy.arange(8).reshape(4, 2)]
        ... )
        ValidationMessage(correct=False, error_message="Column-count of the provided curves doesn't match.", error_type=<class 'ValueError'>)
        >>> _input_curves_are_valid_for_calculation(
        ...     [
        ...         DataFrame(numpy.arange(9).reshape(3, 3)),
        ...         DataFrame(numpy.arange(12).reshape(4, 3))
        ...     ]
        ... )
        ValidationMessage(correct=True, error_message=None, error_type=None)
        >>> _input_curves_are_valid_for_calculation(
        ...     [
        ...         DataFrame(numpy.arange(8).reshape(4, 2)),
        ...         DataFrame(numpy.arange(12).reshape(4, 3))
        ...     ]
        ... )
        ValidationMessage(correct=False, error_message="Column-count of the provided curves doesn't match.", error_type=<class 'ValueError'>)
        >>> _input_curves_are_valid_for_calculation(
        ...     [
        ...         DataFrame(numpy.arange(12).reshape(4, 3)),
        ...         DataFrame(numpy.arange(8).reshape(4, 2))
        ...     ]
        ... )
        ValidationMessage(correct=False, error_message="Column-count of the provided curves doesn't match.", error_type=<class 'ValueError'>)
    """
    first_curves = different_curves[0]
    if isinstance(first_curves, numpy.ndarray):
        return _ndarrays_are_valid_for_calculation(different_curves)
    if isinstance(first_curves, DataFrame):
        return _dataframes_are_valid_for_calculation(different_curves)
    raise NotImplementedError("The given type of curves could not be validated.")


def _merge_two_curves(
    left: DataFrame, right: DataFrame, copy_at_concat: bool = True
) -> DataFrame:
    """
    Merges two curves into a single pandas.DataFrame with a common index.

    Args:
        left(DataFrame):
            Left curve to be merged with the right one.

        right(DataFrame):
            Right curve, which will merge to the left one.

    Returns:

    Test:
        >>> from arithmeticmeancurve import _merge_two_curves
        >>> from pathlib import Path
        >>> import pandas
        >>> import examplecurves
        >>> left, right = examplecurves.get(
        ...     group_name="10", cut_curves_at=3, curve_selection=[1, 2]
        ... )
        >>> left.columns = ["left"]
        >>> right.columns = ["right"]
        >>> from doctestprinter import doctest_print
        >>> doctest_print(_merge_two_curves(left, right))
                 left     right
        x
        0.000  0.0000  0.000000
        0.100  1.5625       NaN
        0.111     NaN  1.607654
        0.200  3.0000       NaN
        0.222     NaN  3.085479

    """
    equal_indexes = right.index.intersection(left.index)
    different_indexes = right.index.difference(left.index)
    combined = pandas.concat([left, right.loc[different_indexes]], copy=copy_at_concat)
    combined.loc[equal_indexes, right.columns] = right.loc[equal_indexes]
    return combined.sort_index()


def merge_set_of_curves_to_family(set_of_curves: SetOfCurves) -> RawFamilyOfCurves:
    """
    Merges a set into a family (of curves). Each curve within theresulting
    RawFamilyOfCurves will only contain its own y-values. All other values of
    the common x-values will be NaN.

    Args:
        set_of_curves(SetOfCurves):
            A set of unique curves, which doesn't share common x-values.

    Returns:
        RawFamilyOfCurves

    Test:
        >>> from pathlib import Path
        >>> import pandas
        >>> import examplecurves
        >>> from doctestprinter import doctest_print
        >>> example_curves = examplecurves.get(group_name="10", cut_curves_at=3)
        >>> doctest_print(merge_set_of_curves_to_family(set_of_curves=example_curves))
                   y_0     y_1       y_2       y_3       y_4
        x
        0.000  0.00000  0.0000  0.000000  0.000000  0.000000
        0.090      NaN     NaN       NaN       NaN  1.796875
        0.096      NaN     NaN       NaN  1.796875       NaN
        0.100      NaN  1.5625       NaN       NaN       NaN
        0.111      NaN     NaN  1.607654       NaN       NaN
        0.115  1.40625     NaN       NaN       NaN       NaN
        0.180      NaN     NaN       NaN       NaN  3.450000
        0.192      NaN     NaN       NaN  3.450000       NaN
        0.200      NaN  3.0000       NaN       NaN       NaN
        0.222      NaN     NaN  3.085479       NaN       NaN
        0.230  2.70000     NaN       NaN       NaN       NaN
        >>> example_curves = examplecurves.get(
        ...     group_name="10",
        ...     cut_curves_at=3,
        ...     offsets=examplecurves.SAMPLE_CURVE_OFFSETS["10"][1]
        ... )
        >>> merged_family = merge_set_of_curves_to_family(set_of_curves=example_curves)
        >>> doctest_print(merged_family)
                   y_0     y_1       y_2       y_3       y_4
        x
        0.010      NaN     NaN       NaN  0.080000       NaN
        0.020      NaN     NaN       NaN       NaN  0.000000
        0.050      NaN     NaN  0.100000       NaN       NaN
        0.080  0.01000     NaN       NaN       NaN       NaN
        0.100      NaN  0.0500       NaN       NaN       NaN
        0.106      NaN     NaN       NaN  1.876875       NaN
        0.110      NaN     NaN       NaN       NaN  1.796875
        0.161      NaN     NaN  1.707654       NaN       NaN
        0.195  1.41625     NaN       NaN       NaN       NaN
        0.200      NaN  1.6125       NaN       NaN  3.450000
        0.202      NaN     NaN       NaN  3.530000       NaN
        0.272      NaN     NaN  3.185479       NaN       NaN
        0.300      NaN  3.0500       NaN       NaN       NaN
        0.310  2.71000     NaN       NaN       NaN       NaN

    """
    different_numbered_curves = []
    for index, curves in enumerate(set_of_curves):
        numbered_curves = curves.copy()
        numbered_curves.columns = [
            "{}_{}".format(column_name, index) for column_name in curves.columns
        ]
        different_numbered_curves.append(numbered_curves)

    first_left, second_right = different_numbered_curves[:2]
    all_in_one = _merge_two_curves(first_left, second_right, copy_at_concat=False)
    for additional_curves in different_numbered_curves[2:]:
        all_in_one = _merge_two_curves(
            all_in_one, additional_curves, copy_at_concat=False
        )

    return all_in_one


def interpolate_family_of_curves(
    raw_family_of_curves: RawFamilyOfCurves,
) -> FamilyOfCurves:
    """
    Perform default interpolation of a merged family of curves.

    Args:
        raw_family_of_curves(DataFrame):


    Returns:
        DataFrame

    Test:
        >>> import examplecurves
        >>> from arithmeticmeancurve import (
        ...     merge_set_of_curves_to_family, interpolate_family_of_curves
        ... )
        >>> from doctestprinter import doctest_print
        >>> example_curves = examplecurves.get(
        ...     group_name="10",
        ...     cut_curves_at=3,
        ...     offsets=examplecurves.SAMPLE_CURVE_OFFSETS["10"][1]
        ... )
        >>> merged_family = merge_set_of_curves_to_family(set_of_curves=example_curves)
        >>> doctest_print(merged_family)
                   y_0     y_1       y_2       y_3       y_4
        x
        0.010      NaN     NaN       NaN  0.080000       NaN
        0.020      NaN     NaN       NaN       NaN  0.000000
        0.050      NaN     NaN  0.100000       NaN       NaN
        0.080  0.01000     NaN       NaN       NaN       NaN
        0.100      NaN  0.0500       NaN       NaN       NaN
        0.106      NaN     NaN       NaN  1.876875       NaN
        0.110      NaN     NaN       NaN       NaN  1.796875
        0.161      NaN     NaN  1.707654       NaN       NaN
        0.195  1.41625     NaN       NaN       NaN       NaN
        0.200      NaN  1.6125       NaN       NaN  3.450000
        0.202      NaN     NaN       NaN  3.530000       NaN
        0.272      NaN     NaN  3.185479       NaN       NaN
        0.300      NaN  3.0500       NaN       NaN       NaN
        0.310  2.71000     NaN       NaN       NaN       NaN
        >>> interpolated_family = interpolate_family_of_curves(
        ...     raw_family_of_curves=merged_family
        ... )
        >>> doctest_print(interpolated_family)
                    y_0       y_1       y_2       y_3       y_4
        x
        0.010       NaN       NaN       NaN  0.080000       NaN
        0.020       NaN       NaN       NaN  0.267174  0.000000
        0.050       NaN       NaN  0.100000  0.828698  0.598958
        0.080  0.010000       NaN  0.534501  1.390221  1.197917
        0.100  0.254565  0.050000  0.824168  1.764570  1.597222
        0.106  0.327935  0.143750  0.911069  1.876875  1.717014
        0.110  0.376848  0.206250  0.969002  1.945755  1.796875
        0.161  1.000489  1.003125  1.707654  2.823978  2.733646
        0.195  1.416250  1.534375  2.160321  3.409460  3.358160
        0.200  1.472500  1.612500  2.226890  3.495560  3.450000
        0.202  1.495000  1.641250  2.253517  3.530000       NaN
        0.272  2.282500  2.647500  3.185479       NaN       NaN
        0.300  2.597500  3.050000       NaN       NaN       NaN
        0.310  2.710000       NaN       NaN       NaN       NaN

    """
    return raw_family_of_curves.interpolate(method="index", limit_area="inside")


def convert_set_to_family_of_curves(set_of_curves: SetOfCurves) -> FamilyOfCurves:
    """
    Merges and interpolates a set into a family (of curves).

    Notes:
        The *family of curves* is the basis for a mean curve calculation.

    Args:
        set_of_curves(SetOfCurves):
            A set of unique curves, which doesn't share common x-values.

    Returns:
        DataFrame

    Test:
        >>> import examplecurves
        >>> from arithmeticmeancurve import convert_set_to_family_of_curves
        >>> from doctestprinter import doctest_print
        >>> example_curves = examplecurves.get(
        ...     group_name="10",
        ...     cut_curves_at=3,
        ...     offsets=examplecurves.SAMPLE_CURVE_OFFSETS["10"][1]
        ... )
        >>> sample_family = convert_set_to_family_of_curves(example_curves)
        >>> doctest_print(sample_family)
                    y_0       y_1       y_2       y_3       y_4
        x
        0.010       NaN       NaN       NaN  0.080000       NaN
        0.020       NaN       NaN       NaN  0.267174  0.000000
        0.050       NaN       NaN  0.100000  0.828698  0.598958
        0.080  0.010000       NaN  0.534501  1.390221  1.197917
        0.100  0.254565  0.050000  0.824168  1.764570  1.597222
        0.106  0.327935  0.143750  0.911069  1.876875  1.717014
        0.110  0.376848  0.206250  0.969002  1.945755  1.796875
        0.161  1.000489  1.003125  1.707654  2.823978  2.733646
        0.195  1.416250  1.534375  2.160321  3.409460  3.358160
        0.200  1.472500  1.612500  2.226890  3.495560  3.450000
        0.202  1.495000  1.641250  2.253517  3.530000       NaN
        0.272  2.282500  2.647500  3.185479       NaN       NaN
        0.300  2.597500  3.050000       NaN       NaN       NaN
        0.310  2.710000       NaN       NaN       NaN       NaN


    """
    raw_family = merge_set_of_curves_to_family(set_of_curves=set_of_curves)
    return interpolate_family_of_curves(raw_family_of_curves=raw_family)


def calculate_arithmetic_mean_curves(curves: List[Curves]) -> Curves:
    """

    Args:
        curves:

    Returns:

    """
    validation_message = _input_curves_are_valid_for_calculation(curves=curves)
    if not validation_message.correct:
        raise validation_message.error_type(validation_message.error_message)

    curve_frame = merge_set_of_curves_to_family(curves)
    curve_groups = _group_column_names_with_postfixed_numbers(curves.columns)
    raise NotImplementedError(
        "This function needs to group the different curves and calculate "
        "a mean curve for each. Afterwards merge the mean curves into one result."
    )


BlockSectionPositions = namedtuple(
    "BlockSectionPositions", "start_position end_position"
)


def _estimate_block_section_positions(
    curve_group_frame: DataFrame,
) -> BlockSectionPositions:
    """
    Estimates the positions of the middle value block.

    Returns:
        BlockSectionPositions

    Test:
        >>> import examplecurves
        >>> from arithmeticmeancurve import (
        ...     _estimate_block_section_positions,
        ...     merge_set_of_curves_to_family
        ... )
        >>> sample_curves = examplecurves.get(
        ...     group_name="10",
        ...     curve_selection=[2, 3],
        ...     offsets=[0.11, 0.0]
        ... )
        >>> merged_curves = merge_set_of_curves_to_family(sample_curves)
        >>> group_frame = merged_curves.interpolate(method="index", limit_area="inside")
        >>> value_block_positions = _estimate_block_section_positions(group_frame)
        >>> value_block_positions
        BlockSectionPositions(start_position=2, end_position=18)

        Here is the resulting frame.

        >>> from doctestprinter import doctest_print
        >>> enumerated_frame = group_frame.copy()
        >>> enumerated_frame["number"] = list(range(len(enumerated_frame)))
        >>> doctest_print(enumerated_frame.iloc[:4])
                    y_0       y_1  number
        x
        0.000       NaN  0.000000       0
        0.096       NaN  1.796875       1
        0.110  0.000000  2.037956       2
        0.192  1.187636  3.450000       3
        >>> doctest_print(enumerated_frame.iloc[-4:])
                     y_0   y_1  number
        x
        0.960   8.986780  11.5      18
        0.998   9.226026   NaN      19
        1.109   9.795051   NaN      20
        1.220  10.234246   NaN      21

        Block slicing test.

        >>> value_block_start, value_block_end = value_block_positions
        >>> doctest_print(enumerated_frame.iloc[:value_block_start])
               y_0       y_1  number
        x
        0.000  NaN  0.000000       0
        0.096  NaN  1.796875       1
        >>> doctest_print(enumerated_frame.iloc[value_block_start:value_block_end+1])
                    y_0        y_1  number
        x
        0.110  0.000000   2.037956       2
        0.192  1.187636   3.450000       3
        0.221  1.607654   3.905957       4
        0.288  2.499674   4.959375       5
        0.332  3.085479   5.585286       6
        0.384  3.716973   6.325000       7
        0.443  4.433475   7.075944       8
        0.480  4.839531   7.546875       9
        0.554  5.651643   8.377930      10
        0.576  5.867350   8.625000      11
        0.665  6.739982   9.491243      12
        0.672  6.800429   9.559375      13
        0.768  7.629410  10.350000      14
        0.776  7.698492  10.403906      15
        0.864  8.355465  10.996875      16
        0.887  8.527174  11.117415      17
        0.960  8.986780  11.500000      18
        >>> doctest_print(enumerated_frame.iloc[value_block_end+1:])
                     y_0  y_1  number
        x
        0.998   9.226026  NaN      19
        1.109   9.795051  NaN      20
        1.220  10.234246  NaN      21

    """
    index_mask_of_middle_value_block = curve_group_frame.notna().all(axis=1)
    all_indexes = curve_group_frame.index.copy()
    all_indexes_count = len(all_indexes)
    numbered_indexes = Series(numpy.arange(all_indexes_count), index=all_indexes)

    indexes_of_mid_value_block = numbered_indexes.loc[index_mask_of_middle_value_block]
    integer_start_index_of_middle_value_block = indexes_of_mid_value_block.iloc[0]
    integer_end_index_of_middle_value_block = indexes_of_mid_value_block.iloc[-1]
    return BlockSectionPositions(
        start_position=integer_start_index_of_middle_value_block,
        end_position=integer_end_index_of_middle_value_block,
    )


class AMeanCurve(ABC):
    @abstractmethod
    def get_current_value_block(self) -> DataFrame:
        """
        Returns the section of the family of curves, which contains only values.

        Returns:
            DataFrame
        """
        pass

    @abstractmethod
    def get_current_end_cap(self) -> DataFrame:
        """
        Returns the trailing section of the family of curves, at which the first
        Nan occurs.

        Returns:
            DataFrame
        """


class Extrapolates(ABC):
    @abstractmethod
    def prepare_extrapolation(self, a_mean_curve: AMeanCurve):
        """
        Prepares the extrapolation for the given mean curve.

        Args:
            a_mean_curve(AMeanCurve):
                A mean curve.

        """
        pass

    @abstractmethod
    def iter_extrapolate_row(
        self, values_at_x: Series
    ) -> Generator[Series, None, None]:
        """
        Extrapolates the y-values of all curves at an equal x-value.

        Yields:
            Series
        """
        pass

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass


FROZEN_STD_EXTRAPOLATION_STRING_TEMPLATE = """{class_name}
    Target standard deviation (std): {target_std}
    Curve's relative std positions:
        {relative_std_positions}
"""


def _extract_end_points_of_family(family_of_curves: FamilyOfCurves) -> numpy.ndarray:
    """
    Extracts the end points of

    Args:
        family_of_curves(DataFrame):
            A dataframe containing a family of curves, which are related to

    Returns:

    Test:
        >>> import examplecurves
        >>> from doctestprinter import doctest_print
        >>> from arithmeticmeancurve import (
        ...     convert_set_to_family_of_curves, _extract_end_points_of_family
        ... )
        >>> example_curves = examplecurves.get(
        ...     group_name="10",
        ...     offsets=examplecurves.SAMPLE_CURVE_OFFSETS["10"][1]
        ... )
        >>> sample_family = convert_set_to_family_of_curves(example_curves)
        >>> doctest_print(sample_family.loc[0.9:])
                    y_0        y_1        y_2        y_3        y_4
        x
        0.900  7.571957   9.050000   9.086780  11.213138  11.388194
        0.920  7.679565   9.162500   9.212699  11.317956  11.500000
        0.938  7.776413   9.263750   9.326026  11.412292        NaN
        0.970  7.948587   9.443750   9.490069  11.580000        NaN
        1.000  8.110000   9.612500   9.643860        NaN        NaN
        1.000  8.110000   9.612500   9.643860        NaN        NaN
        1.049  8.325707   9.826875   9.895051        NaN        NaN
        1.100  8.550217  10.050000  10.096843        NaN        NaN
        1.115  8.616250        NaN  10.156194        NaN        NaN
        1.160  8.770326        NaN  10.334246        NaN        NaN
        1.230  9.010000        NaN        NaN        NaN        NaN
        >>> _extract_end_points_of_family(sample_family)
        array([[ 1.23      ,  9.01      ],
               [ 1.1       , 10.05      ],
               [ 1.16      , 10.33424587],
               [ 0.97      , 11.58      ],
               [ 0.92      , 11.5       ]])


    """
    end_points_of_curves = []

    for label, curve in family_of_curves.iteritems():
        value_indexes = curve.index[curve.isna() == False]
        value_curve = curve.loc[value_indexes]
        last_value_of_curve = value_curve.iloc[-1]
        last_x_value_of_curve = value_curve.index[-1]

        end_points_of_curves.append([last_x_value_of_curve, last_value_of_curve])
    return numpy.array(end_points_of_curves)


def _extract_end_points_of_set(set_of_curves: SetOfCurves) -> numpy.ndarray:
    """
    Extracts the end points of

    Args:
        set_of_curves(SetOfCurves):

    Returns:

    Test:
        >>> import examplecurves
        >>> from doctestprinter import doctest_iter_print
        >>> from arithmeticmeancurve import (
        ...     convert_set_to_family_of_curves, _extract_end_points_of_family
        ... )
        >>> example_curves = examplecurves.get(
        ...     group_name="10",
        ...     offsets=examplecurves.SAMPLE_CURVE_OFFSETS["10"][1]
        ... )
        >>> doctest_iter_print(example_curves, edits_item=lambda x: x.iloc[-3:])
                     y
        x
        1.000  8.11000
        1.115  8.61625
        1.230  9.01000
                   y
        x
        0.9   9.0500
        1.0   9.6125
        1.1  10.0500
                       y
        x
        0.938   9.326026
        1.049   9.895051
        1.160  10.334246
                       y
        x
        0.778  10.430000
        0.874  11.076875
        0.970  11.580000
                      y
        x
        0.74  10.350000
        0.83  10.996875
        0.92  11.500000
        >>> _extract_end_points_of_set(example_curves)
        array([[ 1.23      ,  9.01      ],
               [ 1.1       , 10.05      ],
               [ 1.16      , 10.33424587],
               [ 0.97      , 11.58      ],
               [ 0.92      , 11.5       ]])


    """
    end_points_of_curves = []

    for curve in set_of_curves:
        value_indexes = curve.notna()
        value_curve = curve[value_indexes]
        last_value_of_curve = value_curve.iloc[-1][0]
        last_x_value_of_curve = value_curve.index[-1]

        end_points_of_curves.append([last_x_value_of_curve, last_value_of_curve])
    return numpy.array(end_points_of_curves)


def extract_end_points(
    set_or_family: Union[SetOfCurves, FamilyOfCurves]
) -> numpy.ndarray:
    """

    Args:
        set_or_family:

    Returns:

    Test:
        >>> import examplecurves
        >>> from doctestprinter import doctest_print
        >>> from arithmeticmeancurve import (
        ...     convert_set_to_family_of_curves, _extract_end_points_of_family
        ... )
        >>> example_curves = examplecurves.get(
        ...     group_name="10",
        ...     offsets=examplecurves.SAMPLE_CURVE_OFFSETS["10"][1]
        ... )
        >>> sample_family = convert_set_to_family_of_curves(example_curves)
        >>> end_points = extract_end_points(example_curves)
        >>> doctest_print(end_points)
        [[ 1.23        9.01      ]
         [ 1.1        10.05      ]
         [ 1.16       10.33424587]
         [ 0.97       11.58      ]
         [ 0.92       11.5       ]]
        >>> end_points = extract_end_points(sample_family)
        >>> doctest_print(end_points)
        [[ 1.23        9.01      ]
         [ 1.1        10.05      ]
         [ 1.16       10.33424587]
         [ 0.97       11.58      ]
         [ 0.92       11.5       ]]
    """
    if isinstance(set_or_family, list):
        return _extract_end_points_of_set(set_of_curves=set_or_family)
    if isinstance(set_or_family, DataFrame):
        return _extract_end_points_of_family(family_of_curves=set_or_family)
    raise TypeError("{} is not supported.".format(type(set_or_family)))


class FrozenStdExtrapolation(Extrapolates):
    """
    >>> import examplecurves
    >>> from doctestprinter import doctest_print
    >>> from arithmeticmeancurve import ArithmeticMeanCurve, FrozenStdExtrapolation
    >>> sample_curves = examplecurves.get(group_name="10")
    >>> a_mean_curve = ArithmeticMeanCurve(sample_curves)
    >>> extrapolator = FrozenStdExtrapolation()
    >>> extrapolator.prepare_extrapolation(a_mean_curve=a_mean_curve)
    >>> extrapolator
    FrozenStdExtrapolation
        Target standard deviation (std): 1.443992337458438
        Curve's relative std positions:
            [-1.32494113 -0.23760247 -0.42801722  0.88639717  1.10416365]
    <BLANKLINE>
    >>> end_cap = a_mean_curve.get_current_end_cap()
    >>> doctest_print(end_cap)
                y_0        y_1        y_2        y_3  y_4
    x
    0.920  8.100000   9.650000   9.390069  11.290365  NaN
    0.960  8.276087   9.825000   9.595123  11.500000  NaN
    0.999  8.447772   9.995625   9.795051        NaN  NaN
    1.000  8.452174  10.000000   9.799007        NaN  NaN
    1.035  8.606250        NaN   9.937492        NaN  NaN
    1.110  8.863043        NaN  10.234246        NaN  NaN
    1.150  9.000000        NaN        NaN        NaN  NaN
    >>> extrapolated_end_cap = end_cap.apply(extrapolator, axis=1)
    >>> doctest_print(extrapolated_end_cap)
                y_0        y_1        y_2        y_3        y_4
    x
    0.920  8.100000   9.650000   9.390069  11.290365  11.596589
    0.960  8.276087   9.825000   9.595123  11.500000  11.784239
    0.999  8.447772   9.995625   9.795051  11.639294  11.953747
    1.000  8.452174  10.000000   9.799007  11.639294  11.953747
    1.035  8.606250  10.171315   9.937492  11.794362  12.108815
    1.110  8.863043  10.447860  10.234246  12.070907  12.385360
    1.150  9.000000  10.520036  10.245078  12.143083  12.457536

    """

    MAXIMUM_ALLOWED_INTERPOLATIONS = 50
    TARGET_THRESHOLD = 0.001

    def __init__(
        self,
        use_previous_iteration: bool = True,
        maximum_allowed_iterations: Optional[int] = None,
        target_threshold: Optional[float] = None,
    ):
        """
        Extrapolates with last standard deviation as target. The current default
        extrapolation method of the *ArithmeticMeanCurve*.

        Notes:
            By default the mean value curve is calculated until the
            relative deviation of the mean curve in regard of the previous
            iteration step's mean value is 0.1% (`figure 1`_). For more
            precise values the *target_threshold* can be lowered.

            For a faster calculation the previous row's result is used as
            the entry point for the next calculation. It can be disabled
            via the argument *use_previous_iteration*.

        Args:
            use_previous_iteration(bool):
                Default True; indicates if the results of the previous
                calculation are used as starting point within the next
                one.

            maximum_allowed_iterations(int):
                Default 50; maximum count of iterations of each row's
                extrapolation calculation.

            target_threshold(float):
                Default 0.001 (or 0.1%); the relative deviation, which
                marks the iterations target. Lowering this value might
                need an increase of *maximum_allowed_iterations*.

        Examples:

            The default extrapolation is tweaked comparing `figure 1`_ with
            `figure 2`_.

            .. _figure 1:

            .. plot::

                from visualtester import plot_extrapolation_test
                import examplecurves
                from arithmeticmeancurve import FrozenStdExtrapolation
                sample_curves = examplecurves.get(group_name="10")

                plot_extrapolation_test(
                    curves=sample_curves, extrapolates=FrozenStdExtrapolation()
                )

            **Figure 1:** Extrapolation with default settings.
            Top diagram; iteration per extrapolated row (abscissa number).
            Bottom diagram; Original and extrapolated curves.

            .. _figure 2:

            .. plot::

                from visualtester import plot_extrapolation_test
                import examplecurves
                from arithmeticmeancurve import FrozenStdExtrapolation
                sample_curves = examplecurves.get(group_name="10")

                plot_extrapolation_test(
                    curves=sample_curves,
                    extrapolates=FrozenStdExtrapolation(use_previous_iteration=False)
                )

            **Figure 2:** Extrapolation with *use_previous_iteration* turned off.
            Top diagram; iteration per extrapolated row (abscissa number).
            Bottom diagram; Original and extrapolated curves.

        """
        self._use_last_mean_value = use_previous_iteration
        self._relative_std_positions = None
        self._target_extrapolation = None
        self._maximum_allowed_interpolations = None
        self._target_threshold = None

        if maximum_allowed_iterations is None:
            maximum_allowed_iterations = self.MAXIMUM_ALLOWED_INTERPOLATIONS
        if target_threshold is None:
            target_threshold = self.TARGET_THRESHOLD
        self._init_arguments(
            maximum_allowed_iterations=maximum_allowed_iterations,
            target_threshold=target_threshold,
        )
        self._previous_iterations_mean_value = None

    def _init_arguments(self, maximum_allowed_iterations: int, target_threshold: float):
        try:
            maximum_allowed_iterations = int(maximum_allowed_iterations)
        except TypeError:
            raise TypeError(
                "maximum_allowed_interpolations is expected to be an integer."
            )
        if maximum_allowed_iterations < 1:
            raise ValueError("maximum_allowed_interpolations must be greater than 0")
        self._maximum_allowed_interpolations = maximum_allowed_iterations

        try:
            target_threshold = float(target_threshold)
        except:
            raise TypeError("target_threshold is expected to be a float.")
        self._target_threshold = target_threshold

    def __repr__(self):
        return FROZEN_STD_EXTRAPOLATION_STRING_TEMPLATE.format(
            class_name=self.__class__.__name__,
            target_std=self._target_extrapolation_std,
            relative_std_positions=self._relative_std_positions,
        )

    def prepare_extrapolation(self, a_mean_curve: AMeanCurve):
        middle_value_block = a_mean_curve.get_current_value_block()
        last_value_row = middle_value_block.iloc[-1:]

        last_middle_block_mean = last_value_row.mean(axis=1)
        last_middle_block_std = last_value_row.std(axis=1)

        relative_std_positions = last_value_row.copy()
        for column_name in last_value_row.columns:
            relative_std_positions[column_name] -= last_middle_block_mean
            relative_std_positions[column_name] /= last_middle_block_std
        target_extrapolation_std = last_middle_block_std.iloc[-1]

        self._relative_std_positions = relative_std_positions.to_numpy()[0]
        self._target_extrapolation_std = target_extrapolation_std
        self._previous_iterations_mean_value = last_middle_block_mean.iloc[0]

    def iter_extrapolate_row(
        self, values_at_x: Series
    ) -> Generator[Series, None, None]:
        """

        Args:
            values_at_x:

        Returns:

        Test:
            >>> import examplecurves
            >>> from doctestprinter import doctest_print
            >>> from arithmeticmeancurve import (
            ...     ArithmeticMeanCurve, FrozenStdExtrapolation
            ... )
            >>> sample_curves = examplecurves.get(group_name="10")
            >>> a_mean_curve = ArithmeticMeanCurve(sample_curves)
            >>> extrapolator = FrozenStdExtrapolation()
            >>> extrapolator.prepare_extrapolation(a_mean_curve=a_mean_curve)
            >>> sample_values = a_mean_curve.get_current_end_cap().iloc[-3]
            >>> for iteration, values in enumerate(
            ...     extrapolator.iter_extrapolate_row(sample_values)
            ... ):
            ...     print(iteration, values.to_numpy())
            0 [ 8.60625     9.5625      9.93749225 11.18554688 11.5       ]
            1 [ 8.60625     9.81526168  9.93749225 11.43830855 11.75276168]
            2 [ 8.60625     9.96691868  9.93749225 11.58996556 11.90441868]
            3 [ 8.60625    10.05791289  9.93749225 11.68095976 11.99541289]
            4 [ 8.60625    10.11250941  9.93749225 11.73555628 12.05000941]
            5 [ 8.60625    10.14526732  9.93749225 11.7683142  12.08276732]
            6 [ 8.60625    10.16492207  9.93749225 11.78796895 12.10242207]
            7 [ 8.60625    10.17671492  9.93749225 11.79976179 12.11421492]




        """
        extrapolate_mask = values_at_x.isna()
        current_values = values_at_x

        if self._use_last_mean_value:
            last_mean_value = self._previous_iterations_mean_value
        else:
            last_mean_value = numpy.nanmean(current_values)

        for iteration in range(self._maximum_allowed_interpolations):
            extrapolated_values = (
                self._relative_std_positions[extrapolate_mask]
                * self._target_extrapolation_std
            )
            extrapolated_values += last_mean_value
            current_values = current_values.copy()
            current_values.loc[extrapolate_mask] = extrapolated_values
            iteration_mean_value = numpy.nanmean(current_values)

            mean_diff = abs(last_mean_value - iteration_mean_value) / last_mean_value
            if float(mean_diff) < self._target_threshold:
                yield current_values
                self._previous_iterations_mean_value = last_mean_value
                return None

            last_mean_value = iteration_mean_value
            yield current_values

    def __call__(self, current_values: Series, *args, **kwargs):
        for current_result in self.iter_extrapolate_row(values_at_x=current_values):
            extrapolated_values = current_result
        return extrapolated_values


def extrapolate_by_frozen_std(
    current_values: Series, relative_sigma_positions, target_std
):
    extrapolate_mask = current_values.isna()
    last_mean_value = numpy.nanmean(current_values)
    maximum_allowed_iterations = 20
    targeted_relative_deviation_threshold = 0.0001
    for iteration in range(maximum_allowed_iterations):
        extrapolated_values = relative_sigma_positions[extrapolate_mask] * target_std
        extrapolated_values += last_mean_value
        current_values.loc[extrapolate_mask] = extrapolated_values
        iteration_mean_value = numpy.nanmean(current_values)
        mean_diff = abs(last_mean_value - iteration_mean_value) / last_mean_value
        if mean_diff < targeted_relative_deviation_threshold:
            break
        last_mean_value = iteration_mean_value
    return current_values


def _calculate_nominal_circular_arc_points(
    start_angle: float, end_angle: float, number_of_points: int
) -> numpy.ndarray:
    """

    Args:
        start_angle:
        end_angle:
        number_of_points:

    Returns:

    Test:
        >>> from arithmeticmeancurve import _calculate_nominal_circular_arc_points
        >>> import numpy
        >>> points = _calculate_nominal_circular_arc_points(
        ...     start_angle=0.0, end_angle=2.0*numpy.pi, number_of_points=8
        ... )
        >>> numpy.round(points, 3)
        array([[ 1.   ,  0.   ],
               [ 0.707,  0.707],
               [ 0.   ,  1.   ],
               [-0.707,  0.707],
               [-1.   ,  0.   ],
               [-0.707, -0.707],
               [-0.   , -1.   ],
               [ 0.707, -0.707]])

    """
    angle_steps = (end_angle - start_angle) / number_of_points
    full_circle_angles = numpy.arange(start_angle, end_angle, angle_steps)

    x_point_values = numpy.cos(full_circle_angles)
    y_point_values = numpy.sin(full_circle_angles)
    return numpy.stack([x_point_values, y_point_values], axis=1)


def _calculate_end_point_mean_std(end_points: numpy.ndarray) -> dict:
    """

    Args:
        family_of_curves:

    Returns:
        dict

    Test:
        >>> from arithmeticmeancurve import extract_end_points
        >>> import examplecurves
        >>> from doctestprinter import doctest_iter_print
        >>> sample_curves = examplecurves.get(
        ...     group_name="10",
        ...     offsets=examplecurves.SAMPLE_CURVE_OFFSETS["10"][1]
        ... )
        >>> end_points = extract_end_points(set_or_family=sample_curves)
        >>> doctest_iter_print(
        ...     _calculate_end_point_mean_std(end_points=end_points),
        ...     edits_item=lambda x: round(x, 3)
        ... )
        x_mean:
          1.076
        x_std:
          0.116
        y_mean:
          10.495
        y_std:
          0.961
    """
    x_values = end_points[:, 0]
    y_values = end_points[:, 1]

    return {
        "x_mean": numpy.mean(x_values),
        "x_std": numpy.std(x_values),
        "y_mean": numpy.mean(y_values),
        "y_std": numpy.std(y_values),
    }


def _calculate_shear_slopes(end_points: numpy.ndarray) -> float:
    """

    Args:
        end_points(numpy.ndarray):
            End x, y points for which the shear slope should be returned.

    Returns:
        float

    Examples:
        >>> from arithmeticmeancurve import _calculate_shear_slopes
        >>>
    """
    x = end_points[:, 0]
    y = end_points[:, 1]
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    angle = numpy.arctan(slope)
    half_circle = numpy.pi / 2.0
    quarter_circle = numpy.pi / 4.0
    target_angle = angle
    if angle > quarter_circle:
        target_angle = half_circle - angle
    elif angle < -quarter_circle:
        target_angle = -half_circle - angle
    slopes = numpy.tan(target_angle)
    return slopes


class StatisticsOfPoints(object):
    def __init__(self, points: numpy.ndarray):
        self._x_mean = numpy.mean(points[:, 0])
        self._y_mean = numpy.mean(points[:, 1])
        self._x_std = numpy.std(points[:, 0])
        self._y_std = numpy.std(points[:, 1])
        x, y = points[:, 0], points[:, 1]
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        self._slope = slope
        self._intercept = intercept
        self._r_value = r_value
        self._p_value = p_value
        self._std_err = std_err

    @property
    def x_mean(self):
        return self._x_mean

    @property
    def y_mean(self):
        return self._y_mean

    @property
    def x_std(self):
        return self._x_std

    @property
    def y_std(self):
        return self._y_std

    @property
    def slope(self):
        return self._slope


def _calculate_std_bars(
    points_statistics: StatisticsOfPoints,
) -> Tuple[numpy.ndarray, numpy.ndarray]:
    """

    Returns:

    """
    x_mean = points_statistics.x_mean
    x_std = points_statistics.x_std
    y_mean = points_statistics.y_mean
    y_std = points_statistics.y_std

    horizontal_bar = [
        [x_mean - x_std, y_mean],
        [x_mean, y_mean],
        [x_mean + x_std, y_mean],
    ]
    vertical_bar = [
        [x_mean, y_mean - y_std],
        [x_mean, y_mean],
        [x_mean, y_mean + y_std],
    ]

    return (
        numpy.array(horizontal_bar),
        numpy.array(vertical_bar),
    )


def _calculate_std_circle(points_statistics: StatisticsOfPoints,) -> numpy.ndarray:
    number_of_points = 32

    nominal_circle = _calculate_nominal_circular_arc_points(
        start_angle=0.0, end_angle=2.0 * numpy.pi, number_of_points=number_of_points
    )

    nominal_circle = numpy.append(nominal_circle, [nominal_circle[0].copy()], axis=0)

    circle_x_midpoint = points_statistics.x_mean
    circle_y_midpoint = points_statistics.y_mean
    circle_width = points_statistics.x_std
    circle_height = points_statistics.y_std

    std_circle = nominal_circle * [circle_width, circle_height]
    std_circle += numpy.array([circle_x_midpoint, circle_y_midpoint])

    return std_circle


def shear_points_vertical(
    points: numpy.ndarray, slope: float, center_point: Optional[numpy.ndarray] = None
) -> numpy.ndarray:
    """

    Args:
        points:
        slope:
        center_point:

    Returns:
        >>> import numpy
        >>> sample_points = numpy.array([[1.0, 1.0], [2.0, 1.0]])
        >>> shear_points_vertical(sample_points, -0.5)
        array([[1. , 0.5],
               [2. , 0. ]])
        >>> shear_points_vertical(sample_points, 0.5)
        array([[1. , 1.5],
               [2. , 2. ]])
        >>> shear_points_vertical(sample_points, 0.5, numpy.array([1.0, 1.0]))
        array([[1. , 1. ],
               [2. , 1.5]])
        >>> shear_points_vertical(sample_points, -0.5, numpy.array([1.0, 1.0]))
        array([[1. , 1. ],
               [2. , 0.5]])
    """
    shear_around_center = center_point is not None
    if shear_around_center:
        points_at_center = points - center_point
    else:
        points_at_center = points

    shear_vector = numpy.array([[1, slope], [0, 1]])
    sheared_points = points_at_center.dot(shear_vector)

    if shear_around_center:
        sheared_points += center_point
    return sheared_points


def calculate_std_circle(family_of_curves: FamilyOfCurves) -> Series:
    """

    Args:
        family_of_curves:

    Returns:

    Test:
        >>> import examplecurves
        >>> from doctestprinter import doctest_print
        >>> from arithmeticmeancurve import (
        ...     merge_set_of_curves_to_family, calculate_std_circle
        ... )
        >>> sample_curves = examplecurves.get(group_name="10")
        >>> sample_family = merge_set_of_curves_to_family(sample_curves)
        >>> doctest_print(calculate_std_circle(sample_family).iloc[::4])
        x
        1.117081     9.613475
        1.089818    10.532583
        1.024000    11.401470
        0.958182    11.711152
        0.930919    11.280223
        0.958182    10.361115
        1.024000     9.492229
        1.089818     9.182546
        Name: std circle, dtype: float64

    """
    number_of_points = 32

    nomimal_circle = _calculate_nominal_circular_arc_points(
        start_angle=0.0, end_angle=2.0 * numpy.pi, number_of_points=number_of_points
    )

    end_points = extract_end_points(set_or_family=family_of_curves)
    slope, *items = stats.linregress(end_points[:, 0], end_points[:, 1])

    end_point_statistics = _calculate_end_point_mean_std(end_points=end_points)
    circle_x_midpoint = end_point_statistics["x_mean"]
    circle_y_midpoint = end_point_statistics["y_mean"]
    circle_width = end_point_statistics["x_std"]
    circle_height = end_point_statistics["y_std"]

    std_circle = nomimal_circle * [circle_width, circle_height]

    y_shearing = numpy.array([slope, 0])
    sheared_scatter_circle_y = std_circle.dot(y_shearing)

    x_translations = numpy.full(len(std_circle), circle_x_midpoint)
    y_translations = sheared_scatter_circle_y + circle_y_midpoint

    translation_to_end_position = numpy.stack([x_translations, y_translations], axis=1)
    scatter_circle = std_circle + translation_to_end_position

    circle_x_points = scatter_circle[:, 0]
    circle_y_points = scatter_circle[:, 1]

    x_column_name = family_of_curves.index.name
    std_circle = Series(
        circle_y_points,
        index=pandas.Index(circle_x_points, name=x_column_name),
        name=DEFAULT_STD_CIRCLE_NAME,
    )

    return std_circle


_DEFAULT_KEY = "default"
_EXTRAPOLATION_METHODS = {
    _DEFAULT_KEY: FrozenStdExtrapolation,
    "frozen_std": FrozenStdExtrapolation,
}


class Bar(object):
    def __init__(self, points: numpy.ndarray):
        self._points: numpy.ndarray = points

    @property
    def points(self):
        return self._points

    def __getitem__(self, item):
        return self._points[item]

    def __iter__(self):
        yield self._points[:, 0]
        yield self._points[:, 1]

    def __len__(self):
        return 2


class StdBars(object):
    def __init__(self, points_statistics: StatisticsOfPoints, do_shear: bool = False):
        self._mid_point: numpy.ndarray = numpy.full(2, 0.0)
        self._horizontal_std_bar: numpy.ndarray = None
        self._vertical_std_bar: numpy.ndarray = None
        self._do_shear = do_shear
        self._calculate(points_statistics)

    def _calculate(self, points_statistics: StatisticsOfPoints):
        horizontal_bar, vertical_bar = _calculate_std_bars(
            points_statistics=points_statistics
        )
        mid_point = numpy.array((points_statistics.x_mean, points_statistics.y_mean))
        slope = points_statistics.slope
        if self._do_shear:
            horizontal_bar = shear_points_vertical(horizontal_bar, slope, mid_point)
            vertical_bar = shear_points_vertical(vertical_bar, slope, mid_point)

        self._horizontal_std_bar = Bar(horizontal_bar)
        self._vertical_std_bar = Bar(vertical_bar)
        self._mid_point = mid_point

    @property
    def horizontal(self) -> numpy.ndarray:
        return self._horizontal_std_bar

    @property
    def vertical(self) -> numpy.ndarray:
        return self._vertical_std_bar


class StdCircle(Iterable):
    def __init__(
        self,
        points_statistics: StatisticsOfPoints,
        do_shear: bool = False,
        index_name: Optional[str] = None,
    ):
        self._point_statistics: StatisticsOfPoints = points_statistics
        self._mid_point: numpy.ndarray = numpy.array(
            points_statistics.x_mean, points_statistics.y_mean
        )
        self._do_shear = do_shear
        self._points: numpy.ndarray = None
        self._std_bars: StdBars = StdBars(
            points_statistics=points_statistics, do_shear=do_shear
        )
        if index_name is None:
            self._index_name = "x"
        else:
            self._index_name = index_name
        self._calculate()

    def _calculate(self):
        self._points = _calculate_std_circle(points_statistics=self._point_statistics)
        if self._do_shear:
            self._points = shear_points_vertical(
                self._points, self._point_statistics.slope, self._mid_point
            )

    @property
    def std_bars(self):
        return self._std_bars

    def __getitem__(self, item):
        return self._points[item]

    def __len__(self):
        return 2

    def __iter__(self):
        yield self._points[:, 0]
        yield self._points[:, 1]

    def to_series(self):
        x_values, y_values = self._points[:, 0], self._points[:, 1]
        return Series(
            y_values,
            index=pandas.Index(x_values, name=self._index_name),
            name=DEFAULT_STD_CIRCLE_NAME,
        )


class FamilyOfCurveStatistics(object):
    def __init__(self, family_of_curves: FamilyOfCurves):
        self._stats = self.get_curves_statistics(family_of_curves)

    @staticmethod
    def get_curves_statistics(family_of_curves: FamilyOfCurves) -> DataFrame:
        """

        Returns:

        Examples:
            >>> import examplecurves
            >>> from arithmeticmeancurve import (
            ...     FamilyOfCurveStatistics,
            ...     convert_set_to_family_of_curves
            ... )
            >>> sample_curves = examplecurves.get(
            ...     group_name="10",
            ...     offsets=examplecurves.SAMPLE_CURVE_OFFSETS["10"][1]
            ... )
            >>> example_family = convert_set_to_family_of_curves(sample_curves)
            >>> stats = FamilyOfCurveStatistics.get_curves_statistics(example_family)
            >>> stats
                     end_x      end_y     min_x  ...      max_y   start_x   start_y
            mean  1.076000  10.494849  0.052000  ...  10.494849  0.052000  0.048000
            std   0.129345   1.074284  0.038341  ...   1.074284  0.038341  0.043243
            <BLANKLINE>
            [2 rows x 8 columns]
            >>> stats.loc["mean", "end_x"]
            1.076

        """
        values_of_curves = []
        for label, curve in family_of_curves.iteritems():
            value_indexes = curve.index[curve.isna() == False]
            value_curve = curve.loc[value_indexes]
            last_value_of_curve = value_curve.iloc[-1]
            last_x_value_of_curve = value_curve.index[-1]
            first_x_value_of_curve = value_curve.index[0]
            first_value_of_curve = value_curve.iloc[0]
            curve_index_of_maximum = value_curve.idxmax()
            maximum_value_of_curve = value_curve.loc[curve_index_of_maximum]
            curve_index_of_minimum = value_curve.idxmin()
            minimum_value_of_curve = value_curve.loc[curve_index_of_minimum]

            values_of_curves.append(
                {
                    "end_x": last_x_value_of_curve,
                    "end_y": last_value_of_curve,
                    "min_x": curve_index_of_minimum,
                    "min_y": minimum_value_of_curve,
                    "max_x": curve_index_of_maximum,
                    "max_y": maximum_value_of_curve,
                    "start_x": first_x_value_of_curve,
                    "start_y": first_value_of_curve,
                }
            )
        group_sample = DataFrame(values_of_curves)
        test = {
            "mean": group_sample.mean().to_dict(),
            "std": group_sample.std().to_dict(),
        }
        return DataFrame(test).transpose()

    @property
    def end_x_mean(self):
        return self._stats.loc["mean", "end_x"]

    @property
    def end_x_std(self):
        return self._stats.loc["std", "end_x"]

    @property
    def end_y_mean(self):
        return self._stats.loc["mean", "end_y"]

    @property
    def end_y_std(self):
        return self._stats.loc["std", "end_y"]

    @staticmethod
    def extract_end_points_from_family(family_of_curves: DataFrame) -> numpy.ndarray:
        """
        Extracts the end points of

        Args:
            family_of_curves(DataFrame):
                A dataframe containing a family of curves, which are related to

        Returns:

        Test:
            >>> import examplecurves
            >>> from doctestprinter import doctest_print
            >>> from arithmeticmeancurve import (
            ...     convert_set_to_family_of_curves, FamilyOfCurveStatistics
            ... )
            >>> example_curves = examplecurves.get(
            ...     group_name="10",
            ...     cut_curves_at=3,
            ...     offsets=examplecurves.SAMPLE_CURVE_OFFSETS["10"][1]
            ... )
            >>> sample_family = convert_set_to_family_of_curves(example_curves)
            >>> doctest_print(sample_family.loc[0.2:])
                      y_0      y_1       y_2      y_3   y_4
            x
            0.200  1.4725  1.61250  2.226890  3.49556  3.45
            0.202  1.4950  1.64125  2.253517  3.53000   NaN
            0.272  2.2825  2.64750  3.185479      NaN   NaN
            0.300  2.5975  3.05000       NaN      NaN   NaN
            0.310  2.7100      NaN       NaN      NaN   NaN
            >>> FamilyOfCurveStatistics.extract_end_points_from_family(sample_family)
            array([[0.31      , 2.71      ],
                   [0.3       , 3.05      ],
                   [0.272     , 3.18547893],
                   [0.202     , 3.53      ],
                   [0.2       , 3.45      ]])


        """
        end_points_of_curves = []

        for label, curve in family_of_curves.iteritems():
            value_indexes = curve.index[curve.isna() == False]
            value_curve = curve.loc[value_indexes]
            last_value_of_curve = value_curve.iloc[-1]
            last_x_value_of_curve = value_curve.index[-1]

            end_points_of_curves.append([last_x_value_of_curve, last_value_of_curve])
        return numpy.array(end_points_of_curves)


def _get_extrapolation_method(method: Optional[str] = None) -> Extrapolates:
    if method is None:
        method = _DEFAULT_KEY
    try:
        extrapolator_class = _EXTRAPOLATION_METHODS[method]
    except KeyError:
        known_methods = "', '".join(_EXTRAPOLATION_METHODS)
        raise ValueError(
            "'{}' is not a valid method. Pick one of '{}'.".format(known_methods)
        )
    return extrapolator_class()


class ArithmeticMeanCurve(AMeanCurve):
    def __init__(
        self, curves: Union[SetOfCurves, FamilyOfCurves], method: Optional[str] = None
    ):
        """
        Represents a family of curves.

        Args:
            curves(Union[SetOfCurves, FamilyOfCurves]):
                A '*set of unique curves*' with seperated x-values or a
                'family of curves' with common x-values.

            method(str):
                Default 'frozen_std'; extrapolation method to use.

        Examples:
            >>> import examplecurves
            >>> from doctestprinter import doctest_print, doctest_iter_print
            >>> sample_curves = examplecurves.get(group_name="10")
            >>> doctest_iter_print(sample_curves, edits_item=lambda x: x.iloc[:3])
                         y
            x
            0.000  0.00000
            0.115  1.40625
            0.230  2.70000
                      y
            x
            0.0  0.0000
            0.1  1.5625
            0.2  3.0000
                          y
            x
            0.000  0.000000
            0.111  1.607654
            0.222  3.085479
                          y
            x
            0.000  0.000000
            0.096  1.796875
            0.192  3.450000
                         y
            x
            0.00  0.000000
            0.09  1.796875
            0.18  3.450000
            >>> from arithmeticmeancurve import ArithmeticMeanCurve
            >>> a_mean_curve = ArithmeticMeanCurve(curves=sample_curves)
            >>> doctest_print(a_mean_curve.family_of_curves.loc[:0.2])
                        y_0       y_1       y_2       y_3       y_4
            x
            0.000  0.000000  0.000000  0.000000  0.000000  0.000000
            0.090  1.100543  1.406250  1.303503  1.684570  1.796875
            0.096  1.173913  1.500000  1.390403  1.796875  1.907083
            0.100  1.222826  1.562500  1.448337  1.865755  1.980556
            0.111  1.357337  1.720625  1.607654  2.055176  2.182604
            0.115  1.406250  1.778125  1.660909  2.124056  2.256076
            0.180  2.137500  2.712500  2.526302  3.243359  3.450000
            0.192  2.272500  2.885000  2.686067  3.450000  3.651250
            0.200  2.362500  3.000000  2.792577  3.575781  3.785417


            .. plot:: ./pyplots/example_10_full.py

            **Figure**: Extrapolated mean curve with scatter curve.

        """
        self.curves = None
        self._family_of_curves = None
        self._mid_value_block_positions: BlockSectionPositions = None
        self._numbered_index = None
        self._std_curve = None
        self._std_scatter_curve = None
        self._curves_end_points = None
        self._statistics = None
        self._std_circle = None

        self._initialize(curves=curves)
        self._extrapolation_method = _get_extrapolation_method(method=method)
        self.calculate()

    def _initialize(self, curves: Union[List[Curves], DataFrame]):
        if isinstance(curves, DataFrame):
            self._family_of_curves = curves
        else:
            merged_frame = merge_set_of_curves_to_family(curves)
            self._family_of_curves = merged_frame.interpolate(
                method="index", limit_area="inside"
            )
        self._mid_value_block_positions = _estimate_block_section_positions(
            curve_group_frame=self._family_of_curves
        )
        self._numbered_index = DataFrame(
            numpy.arange(len(self._family_of_curves)),
            index=self._family_of_curves.index.copy(),
        )
        self._statistics = FamilyOfCurveStatistics(
            family_of_curves=self._family_of_curves
        )

    def _provide_statistics(self):
        if self._curve_statistics is None:
            self._get_curves_end_statistics()

    @property
    def statistics(self) -> FamilyOfCurveStatistics:
        """
        Provides statistics of the family of curves. Contains mean and standard
        deviation for starting, minimum, maximum and ending of the family of curves.

        Returns:
            FamilyOfCurveStatistics
        """
        return self._statistics

    @property
    def std_bars(self) -> StdBars:
        """

        Returns:

        """
        return self._std_circle.std_bars

    @property
    def std_circle(self) -> StdCircle:
        """
        Represents the standard deviation as a circle.

        Returns:
            StdCircle

        Examples:

            The task of the standard deviation circle is to depict the x-y
            relation of the family of curves end points (figure 1). Its purpose
            is to give a quick visual impression of the family of curves deviation,
            within in a plot of multiple mean curves. Plotting all family of curves
            in such cases might visually overburden the figure. Std circles are
            best used accompanied with scatter curves.

            .. plot::

                import numpy
                import examplecurves
                from arithmeticmeancurve import extract_end_points, ArithmeticMeanCurve

                sample_curves = examplecurves.get(
                    group_name="10", offsets=examplecurves.SAMPLE_CURVE_OFFSETS["10"][1],
                )
                a_mean_curve = ArithmeticMeanCurve(curves=sample_curves)
                end_points = extract_end_points(a_mean_curve.family_of_curves)
                x_values, y_values = end_points[:, 0], end_points[:, 1]

                import matplotlib.pyplot as plt

                # Setup figure
                fig = plt.figure(figsize=(9, 5), dpi=96)
                gspec = fig.add_gridspec(1, 1)
                axis = fig.add_subplot(gspec[0, 0])
                axis.set_title("extrapolated arithmetic mean curve")

                axis.plot(
                    *a_mean_curve.std_bars.horizontal,
                    "-|",
                    markersize=20,
                    label="Horizontal standard deviation",
                )
                axis.plot(
                    *a_mean_curve.std_bars.vertical,
                    "-_",
                    markersize=20,
                    label="Vertical standard deviation",
                )
                axis.plot(
                    x_values,
                    y_values,
                    "ok",
                    markersize=8,
                    label="end points of family of curves",
                )
                axis.plot(a_mean_curve.std_circle, "--k", label="Standard deviation circle")
                axis.plot(a_mean_curve.family_of_curves)
                # Finishing touch
                axis.set_xlim(0.9, 1.4)
                axis.set_ylim(8.5, 12.0)

                # Finishing touch
                axis.legend()
                plt.show()

            **Figure 1** Standard deviation circle.

            .. _figure 2:

            .. plot::

                import numpy
                import examplecurves
                from arithmeticmeancurve import extract_end_points, ArithmeticMeanCurve

                sample_curves = examplecurves.get(
                    group_name="10", offsets=examplecurves.SAMPLE_CURVE_OFFSETS["10"][1],
                )
                a_mean_curve = ArithmeticMeanCurve(curves=sample_curves)
                end_points = extract_end_points(a_mean_curve.family_of_curves)
                x_values, y_values = end_points[:, 0], end_points[:, 1]

                import matplotlib.pyplot as plt

                # Setup figure
                fig = plt.figure(figsize=(9, 5), dpi=96)
                gspec = fig.add_gridspec(1, 1)
                axis = fig.add_subplot(gspec[0, 0])
                axis.set_title("extrapolated arithmetic mean curve")

                axis.plot(
                    x_values,
                    y_values,
                    "ok",
                    markersize=8,
                    label="end points of family of curves",
                )
                axis.plot(a_mean_curve.std_circle, "--k", label="Standard deviation circle")
                axis.boxplot(x_values, positions=[numpy.mean(y_values)], vert=False, manage_ticks=False)
                axis.boxplot(y_values, positions=[numpy.mean(x_values)], manage_ticks=False)
                # Finishing touch
                axis.set_xlim(0.9, 1.4)
                axis.set_ylim(8.5, 12.0)

                # Finishing touch
                axis.legend()
                plt.show()

            **Figure 2** Standard deviation circle versus box plots.

        """
        return self._std_circle.to_series()

    @property
    def value_block_end_position(self) -> int:
        """

        Returns:

        """
        return self._mid_value_block_positions.end_position

    @property
    def family_of_curves(self) -> DataFrame:
        """
        The curves within a DataFrame interpolated.

        Returns:
            DataFrame

        Examples:
            >>> from pandas import DataFrame
            >>> import numpy
            >>> from arithmeticmeancurve import ArithmeticMeanCurve
            >>> curve_1 = DataFrame(
            ...     [1, 2, 3], index=[0.1, 0.2, 0.3], columns=["y"]
            ... )
            >>> curve_2 = DataFrame(
            ...     [1, 2, 3], index=[0.11, 0.19, 0.31], columns=["y"]
            ... )
            >>> curve_3 = DataFrame(
            ...     [1, 2, 3], index=[0.1, 0.21, 0.30], columns=["y"]
            ... )

            All single curves are being mapped onto a common index. Empty
            values are interpolated, within the curves inner boundaries.

            >>> a_mean_curve = ArithmeticMeanCurve([curve_1, curve_2, curve_3])
            >>> a_mean_curve.family_of_curves
                  y_0       y_1       y_2
            0.10  1.0       NaN  1.000000
            0.11  1.1  1.000000  1.090909
            0.19  1.9  2.000000  1.818182
            0.20  2.0  2.083333  1.909091
            0.21  2.1  2.166667  2.000000
            0.30  3.0  2.916667  3.000000
            0.31  NaN  3.000000       NaN


        **Comparision in between 'set of curves' and 'family of curves'**

            *Top figure*; the ingoing 'set of curves' is a set of
            unique curves with seperated absisa values (x-values).

            *Bottom figure*; the 'family of curves' share common abisa values
            (x-values). This is an necessary step towards the mean value curve
            calculation.


            .. plot::

               import examplecurves
               from arithmeticmeancurve import ArithmeticMeanCurve

               sample_curves = examplecurves.get(
                   group_name="10",
                   offsets=examplecurves.SAMPLE_CURVE_OFFSETS["10"][1],
               )
               a_mean_curve = ArithmeticMeanCurve(sample_curves)
               family_of_curves = a_mean_curve.family_of_curves

               import matplotlib.pyplot as plt

               fig = plt.figure(figsize=(8, 10), dpi=96)
               gspec = fig.add_gridspec(2, 1)
               top_axis = fig.add_subplot(gspec[0, :])
               top_axis.set_title("Ingoing 'set of curves' (List[DataFrame])")
               for index, curve in enumerate(sample_curves):
                   current_label = "Sample curve {}".format(index)
                   top_axis.plot(curve, marker="o", markersize=3, label=current_label)

               bottom_axis = fig.add_subplot(gspec[1, :])
               bottom_axis.set_title("Curves with common index. (DataFrame)")
               for index, (label, curve) in enumerate(family_of_curves.iteritems()):
                   current_label = "Sample curve {}".format(index)
                   bottom_axis.plot(curve, marker="o", markersize=3, label=current_label)

               fig.tight_layout()
               plt.show()


        """
        return self._family_of_curves

    @property
    def mean_curve(self) -> DataFrame:
        """
        Arithmetic mean curve of the sample curves.

        Returns:
            DataFrame

        Examples:

            .. plot::

               import examplecurves
               from arithmeticmeancurve import ArithmeticMeanCurve

               sample_curves = examplecurves.get(
                   group_name="10",
                   offsets=examplecurves.SAMPLE_CURVE_OFFSETS["10"][1],
               )
               a_mean_curve = ArithmeticMeanCurve(sample_curves)
               mean_curve = a_mean_curve.calculate_mean_curve()
               scatter_curve = a_mean_curve.calculate_scatter_curve()
               import matplotlib.pyplot as plt

               fig = plt.figure(figsize=(8, 5), dpi=96)
               gspec = fig.add_gridspec(1, 3)
               axis = fig.add_subplot(gspec[:, :2])
               for index, curve in enumerate(sample_curves):
                   current_label = "Sample curve {}".format(index)
                   axis.plot(curve, marker="o", markersize=3, label=current_label)

               axis.plot(mean_curve, "--ko", markersize=5, label="Arithmetic mean curve")

               axis.legend(bbox_to_anchor=(1.05, 1.02), loc='upper left')
               plt.show()

        """
        return self._mean_curve

    @property
    def std_curve(self):
        return self._std_curve

    @property
    def scatter_curve(self):
        """
        Scatter curve representing the standard deviation.

        Returns:

        Arithmetic mean curve of the sample curves.

        Returns:
            DataFrame

        Examples:

            .. plot::

               import examplecurves
               from arithmeticmeancurve import ArithmeticMeanCurve

               sample_curves = examplecurves.get(
                   group_name="10",
                   offsets=examplecurves.SAMPLE_CURVE_OFFSETS["10"][1],
               )
               a_mean_curve = ArithmeticMeanCurve(sample_curves)
               mean_curve = a_mean_curve.calculate_mean_curve()
               scatter_curve = a_mean_curve.calculate_scatter_curve()
               import matplotlib.pyplot as plt

               fig = plt.figure(figsize=(8, 5), dpi=96)
               gspec = fig.add_gridspec(1, 3)
               axis = fig.add_subplot(gspec[:, :2])
               for index, curve in enumerate(sample_curves):
                   current_label = "Sample curve {}".format(index)
                   axis.plot(curve, marker="o", markersize=3, label=current_label)

               axis.plot(scatter_curve, ":k", label="Scatter curve")

               axis.legend(bbox_to_anchor=(1.05, 1.02), loc='upper left')
               plt.show()

        """
        return self._std_scatter_curve

    def calculate_scatter_curve(self) -> Series:
        mean_curve = self._mean_curve
        std_curve = self._std_curve
        upper_bound_curve = mean_curve + std_curve
        lower_bound_curve = mean_curve - std_curve
        upper_bound_curve = upper_bound_curve.reindex(upper_bound_curve.index[::-1])

        end_points = extract_end_points(self._family_of_curves)
        smallest_x = numpy.amin(end_points, axis=0)[0]

        upper_bound_curve = cut_after(
            source_to_cut=upper_bound_curve, cutting_index=smallest_x
        )
        lower_bound_curve = cut_after(
            source_to_cut=lower_bound_curve, cutting_index=smallest_x
        )

        blank_line = DataFrame([numpy.nan], index=pandas.Index([smallest_x]))

        scatter_curve = pandas.concat(
            (lower_bound_curve, blank_line, upper_bound_curve)
        )
        self._std_scatter_curve = scatter_curve
        return scatter_curve

    def calculate_mean_curve(self):
        self._extrapolation_method.prepare_extrapolation(a_mean_curve=self)

        middle_value_block = self.get_current_value_block()

        target_end_cap = cut_after(
            source_to_cut=self.get_current_end_cap(),
            cutting_index=self.statistics.end_x_mean,
        )
        extrapolated_end_cap = target_end_cap.apply(self._extrapolation_method, axis=1)

        end_mean_curve = extrapolated_end_cap.mean(axis=1)
        mean_curve = pandas.concat([middle_value_block.mean(axis=1), end_mean_curve])
        self._mean_curve = mean_curve

        end_std = extrapolated_end_cap.std(axis=1)
        middle_block_std = middle_value_block.std(axis=1)
        std_curve = pandas.concat([middle_block_std, end_std])
        self._std_curve = std_curve

        return self._mean_curve.copy()

    def _calculate_std_circle(self):
        end_points = extract_end_points(self._family_of_curves)
        points_statistics = StatisticsOfPoints(end_points)
        self._std_circle = StdCircle(points_statistics, do_shear=False)

    def calculate(self):
        self.calculate_mean_curve()
        self.calculate_scatter_curve()
        self._calculate_std_circle()

    def get_position_of_index(self, index: float) -> int:
        return self._numbered_index.loc[index]

    def get_current_value_block(self):
        start_position, end_position = self._mid_value_block_positions
        return self._family_of_curves.iloc[start_position : end_position + 1]

    def get_current_end_cap(self):
        start_position_of_end_cap = self._mid_value_block_positions.end_position + 1
        return self._family_of_curves.iloc[start_position_of_end_cap:]
