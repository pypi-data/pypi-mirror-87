#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import warnings
from typing import (
    Optional,
    List,
    Any,
    Union,
    overload,
    Iterable,
)

# create LOGGER with this namespace's name
import numpy
import pandas
from pandas import DataFrame, Series

_logger = logging.getLogger("trashpanda")
_logger.setLevel(logging.ERROR)
# create console handler and set level to debug
writes_logs_onto_console = logging.StreamHandler()
# add formatter to ch
writes_logs_onto_console.setFormatter(
    logging.Formatter(
        "%(asctime)s - %(name)s - %(module)s - %(funcName)s "
        "- %(lineno)s - %(levelname)s - %(message)s"
    )
)


__version__ = "0.4b0"
__all__ = [
    "add_blank_rows",
    "add_blank_rows_to_dataframe",
    "add_columns_to_dataframe",
    "add_missing_indexes_to_series",
    "cut_after",
    "cut_dataframe_after_max",
    "cut_series_after_max",
    "get_intersection",
    "override_left_with_right_dataframe",
    "override_left_with_right_series",
]


DEFAULT_NA = pandas.NA


@overload
def get_intersection(
    source: DataFrame, targeted_indexes: Union[List, pandas.Index]
) -> DataFrame:
    pass


@overload
def get_intersection(
    source: Series, targeted_indexes: Union[List, pandas.Index]
) -> Series:
    pass


def get_intersection(
    source: Union[DataFrame, Series], targeted_indexes: Union[List, pandas.Index]
) -> Union[DataFrame, Series]:
    """
    Intersects Series or DataFrame by requested indexes. A subsection from the
    *source* is made for the *targeted_indexes*, which must not necessaraly
    be whithin the *source*.

    Args:
        source(Union[DataFrame, Series]):
            Values from which an intersection will be retrieved.

        targeted_indexes(Index):
            The indexes which the returned Series should contain.

    Returns:
        Union[DataFrame, Series]

    Examples:

        *Usage with pandas.Series*

        >>> from pandas import Series
        >>> sample_series = Series(list(range(3)), index=list(iter("abc")), name="foo")
        >>> get_intersection(sample_series, ["b", "c", "d"])
        b    1
        c    2
        Name: foo, dtype: int64
        >>> get_intersection(sample_series, ["x", "y", "z"])
        Series([], Name: foo, dtype: int64)

        *Usage with pandas.DataFrame*

        >>> from pandas import DataFrame
        >>> sample_series = DataFrame(
        ...     list(range(3)), index=list(iter("abc")), columns=["foo"]
        ... )
        >>> get_intersection(sample_series, ["b", "c", "d"])
           foo
        b    1
        c    2
        >>> get_intersection(sample_series, ["x", "y", "z"])
        Empty DataFrame
        Columns: [foo]
        Index: []

    """
    existing_indexes = source.index
    possible_indexes = existing_indexes.intersection(targeted_indexes)
    requested_series = source.loc[possible_indexes]
    return requested_series


@overload
def cut_after(source_to_cut: Series, cutting_index: float) -> Series:
    pass


@overload
def cut_after(source_to_cut: DataFrame, cutting_index: float) -> DataFrame:
    pass


def cut_after(
    source_to_cut: Union[Series, DataFrame], cutting_index: float
) -> Union[Series, DataFrame]:
    """
    Cuts a dataframe dropping the part after the cutting index. The cutting
    index will be added to the frame, which values are being interpolated, if inside.

    Args:
        source_to_cut(Union[Series, DataFrame]):
            Source frame to be cut at the cutting index.

        cutting_index(float):
            Cutting index at which the source frame should be cut.

    Returns:
        Union[Series, DataFrame]

    Examples:

        *Usage with pandas.Series*

        >>> import numpy
        >>> from pandas import Series, Index
        >>> from doctestprinter import doctest_print
        >>> from trashpanda import cut_after
        >>> sample_series = Series(
        ...     numpy.arange(3.0),
        ...     index=Index([0.1, 0.2, 0.3], name="x"),
        ...     name="y"
        ... )
        >>> sample_series
        x
        0.1    0.0
        0.2    1.0
        0.3    2.0
        Name: y, dtype: float64
        >>> cut_after(sample_series, 0.14)
        x
        0.10    0.0
        0.14    0.4
        Name: y, dtype: float64
        >>> cut_after(sample_series, 0.2)
        x
        0.1    0.0
        0.2    1.0
        Name: y, dtype: float64
        >>> cut_after(sample_series, 0.31)
        x
        0.10    0.0
        0.20    1.0
        0.30    2.0
        0.31    NaN
        Name: y, dtype: float64
        >>> cut_after(sample_series, 0.0)
        Series([], Name: y, dtype: float64)

        *Usage with a pandas.DataFrame*

        >>> import numpy
        >>> from pandas import DataFrame, Index
        >>> from doctestprinter import doctest_print
        >>> from trashpanda import cut_after
        >>> sample_frame = DataFrame(
        ...     numpy.arange(6.0).reshape(3, 2),
        ...     columns=["a", "b"],
        ...     index=Index([0.1, 0.2, 0.3], name="x")
        ... )
        >>> doctest_print(sample_frame)
               a    b
        x
        0.1  0.0  1.0
        0.2  2.0  3.0
        0.3  4.0  5.0
        >>> doctest_print(cut_after(sample_frame, 0.14))
                a    b
        x
        0.10  0.0  1.0
        0.14  0.8  1.8
        >>> doctest_print(cut_after(sample_frame, 0.2))
               a    b
        x
        0.1  0.0  1.0
        0.2  2.0  3.0
        >>> doctest_print(cut_after(sample_frame, 0.31))
                a    b
        x
        0.10  0.0  1.0
        0.20  2.0  3.0
        0.30  4.0  5.0
        0.31  NaN  NaN
        >>> cut_after(sample_frame, 0.0)
        Empty DataFrame
        Columns: [a, b]
        Index: []

    """
    if isinstance(source_to_cut, Series):
        return _cut_series_after(
            series_to_cut=source_to_cut, cutting_index=cutting_index
        )
    elif isinstance(source_to_cut, DataFrame):
        return _cut_dataframe_after(
            frame_to_cut=source_to_cut, cutting_index=cutting_index
        )
    raise TypeError(
        "Wrong type for `source`. "
        "Either pandas.Series or pandas.DataFrame are supported. "
        "Got {} instead.".format(type(source_to_cut))
    )


@overload
def add_blank_rows(
    source: Series,
    indexes_to_add: Union[Iterable, pandas.Index],
    fill_value: Optional[Any] = None,
    override: bool = False,
) -> Series:
    pass


@overload
def add_blank_rows(
    source: DataFrame,
    indexes_to_add: Union[Iterable, pandas.Index],
    fill_value: Optional[Any] = None,
    override: bool = False,
) -> DataFrame:
    pass


def add_blank_rows(
    source: Union[Series, DataFrame],
    indexes_to_add: Union[Iterable, pandas.Index],
    fill_value: Optional[Any] = None,
    override: bool = False,
) -> Union[Series, DataFrame]:
    """
    Adds blank rows into a Series or DataFrame with `numpy.nan` by default. Double
    indexes are either overriden if argumend *override* is True or ignored.
    
    Args:
        source(Union[Series, DataFrame]):
            Series or DataFrame in which additional 'blank' rows should be filled.

        indexes_to_add(Union[Iterable, pandas.Index]):
            The targeted indexes, which are going to be added or overriden.

        fill_value(Optional[Any]):
            Default `numpy.nan`; value which is going to be used as the
            added rows values.

        override(bool):
            States if the *indexes to add* are overriding the source or ignored.

    Returns:
        Union[Series, DataFrame]

    Examples:

        *Usage with a pandas.Series*

        >>> from pandas import Series, Index
        >>> import numpy as np
        >>> from doctestprinter import doctest_print
        >>> from trashpanda import add_blank_rows
        >>> sample_series = Series(
        ...     np.arange(3.0), name="a", index=Index([0.1, 0.2, 0.3], name="x")
        ... )
        >>> prepared_frame = add_blank_rows(
        ...     source=sample_series, indexes_to_add=[0.15, 0.3, 0.35]
        ... )
        >>> doctest_print(prepared_frame)
        x
        0.10    0.0
        0.15    NaN
        0.20    1.0
        0.30    2.0
        0.35    NaN
        Name: a, dtype: float64
        >>> doctest_print(
        ...     prepared_frame.interpolate(method="index", limit_area="inside")
        ... )
        x
        0.10    0.0
        0.15    0.5
        0.20    1.0
        0.30    2.0
        0.35    NaN
        Name: a, dtype: float64
        >>> doctest_print(
        ...     add_blank_rows(
        ...         source=sample_series,
        ...         indexes_to_add=[0.15, 0.3, 0.35],
        ...         override=True
        ...     )
        ... )
        x
        0.10    0.0
        0.15    NaN
        0.20    1.0
        0.30    NaN
        0.35    NaN
        Name: a, dtype: float64
        >>> doctest_print(
        ...     add_blank_rows(
        ...         source=sample_series, indexes_to_add=[],
        ...     )
        ... )
        x
        0.1    0.0
        0.2    1.0
        0.3    2.0
        Name: a, dtype: float64

        *Usage with a pandas.DataFrame*

        >>> from pandas import DataFrame, Index
        >>> import numpy as np
        >>> from doctestprinter import doctest_print
        >>> from trashpanda import add_blank_rows
        >>> sample_series = DataFrame(
        ...     np.arange(6.0).reshape(3, 2),
        ...     columns=["a", "b"],
        ...     index=Index([0.1, 0.2, 0.3], name="x")
        ... )
        >>> prepared_frame = add_blank_rows(
        ...     source=sample_series, indexes_to_add=[0.15, 0.3, 0.35]
        ... )
        >>> doctest_print(prepared_frame)
                a    b
        x
        0.10  0.0  1.0
        0.15  NaN  NaN
        0.20  2.0  3.0
        0.30  4.0  5.0
        0.35  NaN  NaN
        >>> doctest_print(
        ...     prepared_frame.interpolate(method="index", limit_area="inside")
        ... )
                a    b
        x
        0.10  0.0  1.0
        0.15  1.0  2.0
        0.20  2.0  3.0
        0.30  4.0  5.0
        0.35  NaN  NaN
        >>> doctest_print(
        ...     add_blank_rows(
        ...         source=sample_series,
        ...         indexes_to_add=[0.15, 0.3, 0.35],
        ...         override=True
        ...     )
        ... )
                a    b
        x
        0.10  0.0  1.0
        0.15  NaN  NaN
        0.20  2.0  3.0
        0.30  NaN  NaN
        0.35  NaN  NaN
        >>> doctest_print(
        ...     add_blank_rows(
        ...         source=sample_series, indexes_to_add=[],
        ...     )
        ... )
               a    b
        x
        0.1  0.0  1.0
        0.2  2.0  3.0
        0.3  4.0  5.0

    """
    if isinstance(source, Series):
        return _add_blank_rows_to_series(
            source_series=source,
            indexes_to_add=indexes_to_add,
            fill_value=fill_value,
            override=override,
        )
    elif isinstance(source, DataFrame):
        return _add_blank_rows_to_dataframe(
            source_frame=source,
            indexes_to_add=indexes_to_add,
            fill_value=fill_value,
            override=override,
        )
    raise TypeError(
        "Wrong type for `source`. "
        "Either pandas.Series or pandas.DataFrame are supported. "
        "Got {} instead.".format(type(source))
    )


def _add_blank_rows_to_dataframe(
    source_frame: DataFrame,
    indexes_to_add: Union[Iterable, pandas.Index],
    fill_value: Optional[Any] = None,
    override: bool = False,
) -> DataFrame:
    """
    Adds blank rows into the DataFrame with `numpy.nan` by default. Double
    indexes are either overriden if argumend *override* is True or ignored.


    Args:
        source_frame(DataFrame):
            Frame in which additional 'blank' rows should be filled.

        indexes_to_add(Union[Iterable, pandas.Index]):
            The targeted indexes, which are going to be added or overriden.

        fill_value(Optional[Any]):
            Default `numpy.nan`; value which is going to be used as the
            added rows values.

        override(bool):
            States if the *indexes to add* are overriding the source or ignored.

    Returns:
        DataFrame

    Examples:
        >>> from pandas import DataFrame, Index
        >>> import numpy as np
        >>> from doctestprinter import doctest_print
        >>> # access to protected member for doctest
        >>> # noinspection PyProtectedMember
        >>> from trashpanda import _add_blank_rows_to_dataframe
        >>> sample_series = DataFrame(
        ...     np.arange(6.0).reshape(3, 2),
        ...     columns=["a", "b"],
        ...     index=Index([0.1, 0.2, 0.3], name="x")
        ... )
        >>> prepared_frame = _add_blank_rows_to_dataframe(
        ...     source_frame=sample_series, indexes_to_add=[0.15, 0.3, 0.35]
        ... )
        >>> doctest_print(prepared_frame)
                a    b
        x
        0.10  0.0  1.0
        0.15  NaN  NaN
        0.20  2.0  3.0
        0.30  4.0  5.0
        0.35  NaN  NaN
        >>> doctest_print(
        ...     prepared_frame.interpolate(method="index", limit_area="inside")
        ... )
                a    b
        x
        0.10  0.0  1.0
        0.15  1.0  2.0
        0.20  2.0  3.0
        0.30  4.0  5.0
        0.35  NaN  NaN
        >>> doctest_print(
        ...     _add_blank_rows_to_dataframe(
        ...         source_frame=sample_series,
        ...         indexes_to_add=[0.15, 0.3, 0.35],
        ...         override=True
        ...     )
        ... )
                a    b
        x
        0.10  0.0  1.0
        0.15  NaN  NaN
        0.20  2.0  3.0
        0.30  NaN  NaN
        0.35  NaN  NaN
        >>> doctest_print(
        ...     _add_blank_rows_to_dataframe(
        ...         source_frame=sample_series, indexes_to_add=[],
        ...     )
        ... )
               a    b
        x
        0.1  0.0  1.0
        0.2  2.0  3.0
        0.3  4.0  5.0

    """
    if fill_value is None:
        fill_value = numpy.nan

    nothing_do_add_just_copy_source = len(indexes_to_add) == 0
    if nothing_do_add_just_copy_source:
        return source_frame.copy()

    column_count = len(source_frame.columns)
    index_count = len(indexes_to_add)

    double_indexes = source_frame.index.intersection(indexes_to_add)

    just_need_to_add = len(double_indexes) == 0
    if just_need_to_add:
        blank_lines = [[fill_value] * column_count] * index_count
        rows_to_add = DataFrame(
            blank_lines, index=indexes_to_add, columns=source_frame.columns.copy(),
        )
        requested_frame = pandas.concat((source_frame, rows_to_add), axis=0, sort=True)
        requested_frame.sort_index(inplace=True)
        requested_frame.index.name = source_frame.index.name
        return requested_frame

    ignore_equal_adding_row_indexes_to_source = not override
    if ignore_equal_adding_row_indexes_to_source:
        actual_indexes_to_add = pandas.Index(indexes_to_add).drop(double_indexes)
        blank_lines = [[fill_value] * column_count] * len(actual_indexes_to_add)
        rows_to_add = DataFrame(
            blank_lines,
            index=actual_indexes_to_add,
            columns=source_frame.columns.copy(),
        )
        requested_frame = pandas.concat((source_frame, rows_to_add), axis=0, sort=True)
        requested_frame.sort_index(inplace=True)
        requested_frame.index.name = source_frame.index.name
        return requested_frame

    blank_lines = [[fill_value] * column_count] * len(indexes_to_add)
    rows_to_add = DataFrame(
        blank_lines, index=indexes_to_add, columns=source_frame.columns.copy(),
    )
    different_indexes = source_frame.index.difference(double_indexes)
    requested_frame = pandas.concat(
        (source_frame.loc[different_indexes], rows_to_add), axis=0, sort=True
    )
    requested_frame.sort_index(inplace=True)
    requested_frame.index.name = source_frame.index.name
    return requested_frame


def add_blank_rows_to_dataframe(
    source_frame: DataFrame,
    indexes_to_add: Union[Iterable, pandas.Index],
    fill_value: Optional[Any] = None,
    override: bool = False,
) -> DataFrame:
    """
    Adds blank rows into the DataFrame with `numpy.nan` by default. Double
    indexes are either overriden if argumend *override* is True or ignored.

    .. warning::

        This function will be deprecated within the the next release.
        Use :func:`tashpandas.add_blank_rows` instead.

    Args:
        source_frame(DataFrame):
            Frame in which additional 'blank' rows should be filled.

        indexes_to_add(Union[Iterable, pandas.Index]):
            The targeted indexes, which are going to be added or overriden.

        fill_value(Optional[Any]):
            Default `numpy.nan`; value which is going to be used as the
            added rows values.

        override(bool):
            States if the *indexes to add* are overriding the source or ignored.

    Returns:
        DataFrame

    Examples:
        >>> from pandas import DataFrame, Index
        >>> import numpy as np
        >>> from doctestprinter import doctest_print
        >>> from trashpanda import add_blank_rows_to_dataframe
        >>> sample_series = DataFrame(
        ...     np.arange(6.0).reshape(3, 2),
        ...     columns=["a", "b"],
        ...     index=Index([0.1, 0.2, 0.3], name="x")
        ... )
        >>> prepared_frame = add_blank_rows_to_dataframe(
        ...     source_frame=sample_series, indexes_to_add=[0.15, 0.3, 0.35]
        ... )
        >>> doctest_print(prepared_frame)
                a    b
        x
        0.10  0.0  1.0
        0.15  NaN  NaN
        0.20  2.0  3.0
        0.30  4.0  5.0
        0.35  NaN  NaN
        >>> doctest_print(
        ...     prepared_frame.interpolate(method="index", limit_area="inside")
        ... )
                a    b
        x
        0.10  0.0  1.0
        0.15  1.0  2.0
        0.20  2.0  3.0
        0.30  4.0  5.0
        0.35  NaN  NaN
        >>> doctest_print(
        ...     add_blank_rows_to_dataframe(
        ...         source_frame=sample_series,
        ...         indexes_to_add=[0.15, 0.3, 0.35],
        ...         override=True
        ...     )
        ... )
                a    b
        x
        0.10  0.0  1.0
        0.15  NaN  NaN
        0.20  2.0  3.0
        0.30  NaN  NaN
        0.35  NaN  NaN
        >>> doctest_print(
        ...     add_blank_rows_to_dataframe(
        ...         source_frame=sample_series, indexes_to_add=[],
        ...     )
        ... )
               a    b
        x
        0.1  0.0  1.0
        0.2  2.0  3.0
        0.3  4.0  5.0

    """
    warnings.warn(
        "`add_blank_rows_to_dataframe` is deprecated, "
        "being replaced by `add_blank_rows`.",
        DeprecationWarning,
    )
    return _add_blank_rows_to_dataframe(
        source_frame=source_frame,
        indexes_to_add=indexes_to_add,
        fill_value=fill_value,
        override=override,
    )


def add_columns_to_dataframe(
    frame_to_enlarge: DataFrame,
    column_names: List[str],
    fill_value: Optional[Any] = None,
) -> DataFrame:
    """
    Adds columns to a dataframe. By default the columns are filled with
    pandas.NA values if no *fill_value* is explizitly given.

    Args:
        frame_to_enlarge(DataFrame):
            pandas.DataFrame which gets additional columns.

        column_names(List[str]):
            Names of additional columns to create.

        fill_value(Optional[Any]):
            Value which will fill the newly created columns. Default pandas.NA

    Returns:
        DataFrame

    Examples:
        >>> from pandas import DataFrame
        >>> import numpy
        >>> sample_series = DataFrame(numpy.arange(4).reshape((2,2)), columns=["a", "b"])
        >>> sample_series
           a  b
        0  0  1
        1  2  3
        >>> add_columns_to_dataframe(sample_series, ["c", "d"], "+")
           a  b  c  d
        0  0  1  +  +
        1  2  3  +  +
        >>> add_columns_to_dataframe(sample_series, ["c", "d"])
           a  b     c     d
        0  0  1  <NA>  <NA>
        1  2  3  <NA>  <NA>
    """
    if fill_value is None:
        fill_value = DEFAULT_NA

    for column_name_to_add in column_names:
        frame_to_enlarge[column_name_to_add] = fill_value
    return frame_to_enlarge


def _cut_dataframe_after(frame_to_cut: DataFrame, cutting_index: float) -> DataFrame:
    """
    Cuts a dataframe dropping the part after the cutting index. The cutting
    index will be added to the frame, which values are being interpolated, if inside.

    Args:
        frame_to_cut(DataFrame):
            Source frame to be cut at the cutting index.

        cutting_index(float):
            Cutting index at which the source frame should be cut.

    Returns:
        DataFrame

    Examples:
        >>> import numpy
        >>> from pandas import DataFrame, Index
        >>> from doctestprinter import doctest_print
        >>> sample_frame = DataFrame(
        ...     numpy.arange(6.0).reshape(3, 2),
        ...     columns=["a", "b"],
        ...     index=Index([0.1, 0.2, 0.3], name="x")
        ... )
        >>> doctest_print(sample_frame)
               a    b
        x
        0.1  0.0  1.0
        0.2  2.0  3.0
        0.3  4.0  5.0
        >>> doctest_print(_cut_dataframe_after(sample_frame, 0.14))
                a    b
        x
        0.10  0.0  1.0
        0.14  0.8  1.8
        >>> doctest_print(_cut_dataframe_after(sample_frame, 0.2))
               a    b
        x
        0.1  0.0  1.0
        0.2  2.0  3.0
        >>> doctest_print(_cut_dataframe_after(sample_frame, 0.31))
                a    b
        x
        0.10  0.0  1.0
        0.20  2.0  3.0
        0.30  4.0  5.0
        0.31  NaN  NaN
        >>> _cut_dataframe_after(sample_frame, 0.0)
        Empty DataFrame
        Columns: [a, b]
        Index: []
    """
    if cutting_index <= frame_to_cut.index.min():
        return DataFrame(columns=frame_to_cut.columns.copy())
    if cutting_index in frame_to_cut:
        return frame_to_cut.loc[frame_to_cut.index <= cutting_index].deepcopy()
    prepared_frame = _add_blank_rows_to_dataframe(
        source_frame=frame_to_cut, indexes_to_add=[cutting_index]
    )
    interpolated_frame = prepared_frame.interpolate(
        method="index", axis=0, limit_area="inside"
    )
    return interpolated_frame.loc[interpolated_frame.index <= cutting_index].copy()


def cut_dataframe_after(frame_to_cut: DataFrame, cutting_index: float) -> DataFrame:
    """
    Cuts a dataframe dropping the part after the cutting index. The cutting
    index will be added to the frame, which values are being interpolated, if inside.

    .. warning::

        This function will will be deprecated within the the next release.
        Use :func:`trashpandas.cut_after` instead.

    Args:
        frame_to_cut(DataFrame):
            Source frame to be cut at the cutting index.

        cutting_index(float):
            Cutting index at which the source frame should be cut.

    Returns:
        DataFrame

    Examples:
        >>> import numpy
        >>> from pandas import DataFrame, Index
        >>> from doctestprinter import doctest_print
        >>> sample_frame = DataFrame(
        ...     numpy.arange(6.0).reshape(3, 2),
        ...     columns=["a", "b"],
        ...     index=Index([0.1, 0.2, 0.3], name="x")
        ... )
        >>> doctest_print(sample_frame)
               a    b
        x
        0.1  0.0  1.0
        0.2  2.0  3.0
        0.3  4.0  5.0
        >>> doctest_print(_cut_dataframe_after(sample_frame, 0.14))
                a    b
        x
        0.10  0.0  1.0
        0.14  0.8  1.8
        >>> doctest_print(_cut_dataframe_after(sample_frame, 0.2))
               a    b
        x
        0.1  0.0  1.0
        0.2  2.0  3.0
        >>> doctest_print(_cut_dataframe_after(sample_frame, 0.31))
                a    b
        x
        0.10  0.0  1.0
        0.20  2.0  3.0
        0.30  4.0  5.0
        0.31  NaN  NaN
        >>> _cut_dataframe_after(sample_frame, 0.0)
        Empty DataFrame
        Columns: [a, b]
        Index: []
    """
    warnings.warn(
        "`cut_dataframe_after` is deprecated, being replaced by `cut_after`.",
        DeprecationWarning,
    )
    return _cut_dataframe_after(frame_to_cut=frame_to_cut, cutting_index=cutting_index)


def cut_dataframe_after_max(
    frame_to_cut: DataFrame, condition_column: Optional[Union[str, int]] = None
) -> DataFrame:
    """
    Cuts a DataFrame after the maximum value of its *condition column*. If the
    DataFrame contains only 1 column, then this column is the *condition column*.

    Args:
        frame_to_cut(DataFrame):
            Source frame to be cut at the cutting index.

        condition_column(Union[str, int]):
            Column or its integer position, which contains the conditional
            maximum value.

    Returns:
        DataFrame

    Examples:
        >>> from pandas import DataFrame, Index
        >>> import numpy as np
        >>> from doctestprinter import doctest_print
        >>> v1, v2 = np.arange(0.0, np.pi, np.pi/4.0), np.arange(4)
        >>> test_data = np.stack((np.sin(v1), v2), axis=1)
        >>> test_frame = DataFrame(
        ...     data=test_data,
        ...     columns=["a", "b"],
        ...     index=Index(numpy.arange(0.0, 0.4, 0.1), name="x")
        ... )
        >>> doctest_print(test_frame)
                    a    b
        x
        0.0  0.000000  0.0
        0.1  0.707107  1.0
        0.2  1.000000  2.0
        0.3  0.707107  3.0
        >>> doctest_print(cut_dataframe_after_max(test_frame, "a"))
                    a    b
        x
        0.0  0.000000  0.0
        0.1  0.707107  1.0
        0.2  1.000000  2.0
        >>> doctest_print(cut_dataframe_after_max(test_frame, 0))
                    a    b
        x
        0.0  0.000000  0.0
        0.1  0.707107  1.0
        0.2  1.000000  2.0
    """
    target_column_is_not_clear = (
        condition_column is None and len(frame_to_cut.columns) > 1
    )
    if target_column_is_not_clear:
        raise ValueError(
            "Only a 1-column DataFrame can be cut without defining a condition_column."
        )

    condition_column = condition_column
    if condition_column is None:
        condition_column = frame_to_cut.columns[0]
    column_at_position_is_requested = (
        isinstance(condition_column, int)
        and condition_column not in frame_to_cut.columns
    )
    if column_at_position_is_requested:
        condition_column = frame_to_cut.columns[condition_column]

    cutting_index = frame_to_cut[condition_column].idxmax()
    return _cut_dataframe_after(frame_to_cut=frame_to_cut, cutting_index=cutting_index)


def override_left_with_right_dataframe(
    left_target: DataFrame, overriding_right: DataFrame
) -> DataFrame:
    """
    Overrides overlapping items of left with right.

    Args:
        left_target(DataFrame):
            Dataframe which should be overridden.

        overriding_right(DataFrame):
            The new values as frame, which overrides the *left target*.

    Returns:
        DataFrame

    Examples:
        >>> from pandas import DataFrame
        >>> import numpy as np
        >>> left = DataFrame(np.full(3, 1), index=list(iter("abc")), columns=["v"])
        >>> left
           v
        a  1
        b  1
        c  1
        >>> right = DataFrame(np.full(2, 2), index=list(iter("ad")), columns=["v"])
        >>> right
           v
        a  2
        d  2
        >>> override_left_with_right_dataframe(left, right)
           v
        a  2
        b  1
        c  1
        d  2
        >>> double_data = [list(range(1, 3)) for i in range(3)]
        >>> left = DataFrame(double_data, index=list(iter("abc")), columns=["m", "x"])
        >>> left
           m  x
        a  1  2
        b  1  2
        c  1  2
        >>> double_data = [list(range(3, 5)) for i in range(2)]
        >>> right = DataFrame(double_data, index=list(iter("ad")), columns=["x", "m"])
        >>> right
           x  m
        a  3  4
        d  3  4
        >>> override_left_with_right_dataframe(left, right)
           m  x
        a  4  3
        b  1  2
        c  1  2
        d  4  3
        >>> right = DataFrame(double_data, index=list(iter("ad")), columns=["z", "m"])
        >>> right
           z  m
        a  3  4
        d  3  4
        >>> override_left_with_right_dataframe(left, right)
           m    x     z
        a  4  2.0     3
        b  1  2.0  <NA>
        c  1  2.0  <NA>
        d  4  NaN     3

    """
    old_frame = left_target.copy()
    columns_to_add = overriding_right.columns.difference(left_target.columns)
    if not columns_to_add.empty:
        for column_name in columns_to_add:
            old_frame[column_name] = pandas.NA
    targeted_columns = overriding_right.columns
    same_indexes = overriding_right.index.intersection(old_frame.index)
    new_indexes = overriding_right.index.difference(old_frame.index)
    old_frame.loc[same_indexes, targeted_columns] = overriding_right.loc[same_indexes]
    new_rows = overriding_right.loc[new_indexes]
    overridden_frame = pandas.concat([old_frame, new_rows], sort=True)
    return overridden_frame


def _add_blank_rows_to_series(
    source_series: Series,
    indexes_to_add: Union[Iterable, pandas.Index],
    fill_value: Optional[Any] = None,
    override: bool = False,
) -> Series:
    """
    Adds blank rows into the Series with `numpy.nan` by default. Double
    indexes are either overriden if argumend *override* is True or ignored.


    Args:
        source_series(Series):
            Series in which additional 'blank' rows should be filled.

        indexes_to_add(Union[Iterable, pandas.Index]):
            The targeted indexes, which are going to be added or overriden.

        fill_value(Optional[Any]):
            Default `numpy.nan`; value which is going to be used as the
            added rows values.

        override(bool):
            States if the *indexes to add* are overriding the source or ignored.

    Returns:
        Series

    Examples:
        >>> from pandas import DataFrame, Index
        >>> import numpy as np
        >>> from doctestprinter import doctest_print
        >>> # access to protected member for doctest
        >>> # noinspection PyProtectedMember
        >>> from trashpanda import _add_blank_rows_to_dataframe
        >>> sample_series = Series(
        ...     np.arange(3.0), name="a", index=Index([0.1, 0.2, 0.3], name="x")
        ... )
        >>> prepared_frame = _add_blank_rows_to_series(
        ...     source_series=sample_series, indexes_to_add=[0.15, 0.3, 0.35]
        ... )
        >>> doctest_print(prepared_frame)
        x
        0.10    0.0
        0.15    NaN
        0.20    1.0
        0.30    2.0
        0.35    NaN
        Name: a, dtype: float64
        >>> doctest_print(
        ...     prepared_frame.interpolate(method="index", limit_area="inside")
        ... )
        x
        0.10    0.0
        0.15    0.5
        0.20    1.0
        0.30    2.0
        0.35    NaN
        Name: a, dtype: float64
        >>> doctest_print(
        ...     _add_blank_rows_to_series(
        ...         source_series=sample_series,
        ...         indexes_to_add=[0.15, 0.3, 0.35],
        ...         override=True
        ...     )
        ... )
        x
        0.10    0.0
        0.15    NaN
        0.20    1.0
        0.30    NaN
        0.35    NaN
        Name: a, dtype: float64
        >>> doctest_print(
        ...     _add_blank_rows_to_series(
        ...         source_series=sample_series, indexes_to_add=[],
        ...     )
        ... )
        x
        0.1    0.0
        0.2    1.0
        0.3    2.0
        Name: a, dtype: float64

    """
    if fill_value is None:
        fill_value = numpy.nan

    nothing_do_add_just_copy_source = len(indexes_to_add) == 0
    if nothing_do_add_just_copy_source:
        return source_series.copy()

    index_count = len(indexes_to_add)

    double_indexes = source_series.index.intersection(indexes_to_add)

    just_need_to_add = len(double_indexes) == 0
    if just_need_to_add:
        blank_lines = [fill_value] * index_count
        rows_to_add = Series(
            blank_lines, index=indexes_to_add, name=source_series.name,
        )
        requested_series = pandas.concat(
            (source_series, rows_to_add), axis=0, sort=True
        )
        requested_series.sort_index(inplace=True)
        requested_series.index.name = source_series.index.name
        return requested_series

    ignore_equal_adding_row_indexes_to_source = not override
    if ignore_equal_adding_row_indexes_to_source:
        actual_indexes_to_add = pandas.Index(indexes_to_add).drop(double_indexes)
        blank_lines = [fill_value] * len(actual_indexes_to_add)
        rows_to_add = Series(
            blank_lines, index=actual_indexes_to_add, name=source_series.name,
        )
        requested_series = pandas.concat(
            (source_series, rows_to_add), axis=0, sort=True
        )
        requested_series.sort_index(inplace=True)
        requested_series.index.name = source_series.index.name
        return requested_series

    blank_lines = [fill_value] * len(indexes_to_add)
    rows_to_add = Series(blank_lines, index=indexes_to_add, name=source_series.name,)
    different_indexes = source_series.index.difference(double_indexes)
    requested_series = pandas.concat(
        (source_series.loc[different_indexes], rows_to_add), axis=0, sort=True
    )
    requested_series.sort_index(inplace=True)
    requested_series.index.name = source_series.index.name
    return requested_series


def add_missing_indexes_to_series(
    target_series: Series, new_indexes: pandas.Index, fill_value: Optional[Any] = None
) -> Series:
    """
    Adds different (missing) indexes to series.

    Args:
        target_series(Series):
            Series in which missing indexes should be added.

        new_indexes(pandas.Index):
            Indexes, which should be in the *target series*.

        fill_value(Optional[Any]):
            An optional fill value for the freshly added items.

    Returns:
        Series

    Examples:
        >>> from pandas import Series, Index, Int16Dtype
        >>> import numpy as np
        >>> target = Series(
        ...     np.full(3, 1), index=list(iter("abc")), name="foo", dtype=Int16Dtype()
        ... )
        >>> target
        a    1
        b    1
        c    1
        Name: foo, dtype: Int16
        >>> new_indexes_to_add = Index(list(iter("ad")))
        >>> add_missing_indexes_to_series(target, new_indexes_to_add)
        a       1
        b       1
        c       1
        d    <NA>
        Name: foo, dtype: object
        >>> add_missing_indexes_to_series(target, new_indexes_to_add, "X")
        a    1
        b    1
        c    1
        d    X
        Name: foo, dtype: object

    """
    if fill_value is None:
        fill_value = DEFAULT_NA

    old_series = target_series.copy()
    try:
        missing_indexes = new_indexes.difference(old_series.index)
    except AttributeError:
        raise TypeError("new_indexes must be of pandas.Index type.")
    new_rows = Series([fill_value] * len(missing_indexes), index=missing_indexes)
    overridden_series = pandas.concat([old_series, new_rows], sort=True)
    overridden_series.name = old_series.name
    return overridden_series


def _cut_series_after(
    series_to_cut: Series, cutting_index: Union[float, pandas.Index]
) -> Series:
    """
    Cuts a pandas.Series dropping the part after the cutting index. The cutting
    index will be added to the frame, which values are being interpolated, if inside.

    Args:
        series_to_cut(Series):
            Source Series to be cut at the cutting index.

        cutting_index(Union[float, pandas.Index]):
            Cutting index at which the source frame should be cut.

    Returns:
        Series

    Examples:
        >>> import numpy
        >>> from pandas import Series, Index
        >>> sample_series = Series(
        ...     numpy.arange(3.0),
        ...     index=Index([0.1, 0.2, 0.3], name="x"),
        ...     name="y"
        ... )
        >>> sample_series
        x
        0.1    0.0
        0.2    1.0
        0.3    2.0
        Name: y, dtype: float64
        >>> _cut_series_after(sample_series, 0.14)
        x
        0.10    0.0
        0.14    0.4
        Name: y, dtype: float64
        >>> _cut_series_after(sample_series, 0.2)
        x
        0.1    0.0
        0.2    1.0
        Name: y, dtype: float64
        >>> _cut_series_after(sample_series, 0.31)
        x
        0.10    0.0
        0.20    1.0
        0.30    2.0
        0.31    NaN
        Name: y, dtype: float64
        >>> _cut_series_after(sample_series, 0.0)
        Series([], Name: y, dtype: float64)
    """
    if cutting_index <= series_to_cut.index.min():
        return Series(
            name=series_to_cut.name,
            index=pandas.Index([], name=series_to_cut.index.name),
        )
    if cutting_index in series_to_cut:
        return series_to_cut.loc[series_to_cut.index <= cutting_index].copy()
    prepared_frame = _add_blank_rows_to_series(
        source_series=series_to_cut, indexes_to_add=[cutting_index]
    )
    interpolated_frame = prepared_frame.interpolate(
        method="index", axis=0, limit_area="inside"
    )
    return interpolated_frame.loc[interpolated_frame.index <= cutting_index].copy()


def cut_series_after_max(series_to_cut: Series) -> Series:
    """
    Cuts a Series after its maximum value.

    Args:
        series_to_cut(Series):
            Source frame to be cut at the cutting index.

    Returns:
        Series

    Examples:
        >>> from pandas import Series, Index
        >>> import numpy as np
        >>> from doctestprinter import doctest_print
        >>> from trashpanda import cut_series_after_max
        >>> sample_data = np.sin(np.arange(0.0, np.pi, np.pi/4.0))
        >>> sample_series = Series(
        ...     data=sample_data,
        ...     name="a",
        ...     index=Index(numpy.arange(0.0, 0.4, 0.1), name="x")
        ... )
        >>> doctest_print(sample_series)
        x
        0.0    0.000000
        0.1    0.707107
        0.2    1.000000
        0.3    0.707107
        Name: a, dtype: float64
        >>> cut_sample = cut_series_after_max(sample_series)
        >>> doctest_print(cut_sample)
        x
        0.0    0.000000
        0.1    0.707107
        0.2    1.000000
        Name: a, dtype: float64
        >>> doctest_print(cut_series_after_max(cut_sample))
        x
        0.0    0.000000
        0.1    0.707107
        0.2    1.000000
        Name: a, dtype: float64
    """
    cutting_index = series_to_cut.idxmax()
    return _cut_series_after(series_to_cut=series_to_cut, cutting_index=cutting_index)


def override_left_with_right_series(
    left_target: Series, overriding_right: Series
) -> Series:
    """
    Overrides overlapping items of left with right.

    Args:
        left_target(DataFrame):
            Series which should be overridden.

        overriding_right(DataFrame):
            The new values as Series, which overrides the *left target*.

    Returns:
        Series

    Examples:
        >>> from pandas import Series, Int16Dtype
        >>> import numpy as np
        >>> left = Series(np.full(3, 1), index=list(iter("abc")), dtype=Int16Dtype())
        >>> left
        a    1
        b    1
        c    1
        dtype: Int16
        >>> right = Series(np.full(2, 2), index=list(iter("ad")), dtype=Int16Dtype())
        >>> right
        a    2
        d    2
        dtype: Int16
        >>> override_left_with_right_series(left, right)
        a    2
        b    1
        c    1
        d    2
        dtype: Int16

    """
    old_series = left_target.copy()
    same_indexes = overriding_right.index.intersection(old_series.index)
    new_indexes = overriding_right.index.difference(old_series.index)
    old_series.loc[same_indexes] = overriding_right.loc[same_indexes]
    new_items = overriding_right.loc[new_indexes]
    overridden_series = pandas.concat([old_series, new_items], sort=True)
    return overridden_series


if __name__ == "__main__":
    import doctest

    doctest.testmod()
