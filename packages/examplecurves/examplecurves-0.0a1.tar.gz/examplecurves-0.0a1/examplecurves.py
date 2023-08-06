import copy
from collections import namedtuple
from pathlib import Path
import numpy
import numpy as np
from scipy.interpolate import CubicSpline
from typing import (
    Tuple,
    Iterable,
    Union,
    Dict,
    Optional,
    overload,
    Sequence,
    Generator,
)
from typing import List
from pandas import DataFrame
import pandas


__version__ = "0.0a1"
__all__ = ["CreatesCurves", "create", "make_family_overview_plots"]

_SAMPLE_CURVE_ROOT_PATH = Path(__file__).parent.joinpath("curves")
_DEFAULT_ABSCISSA_NAME = "x"
_DEFAULT_COLUMN_LABELS = "abcdefghqrstvy"

BasePoints = List[Tuple[float, float]]
"""
*Base points* should not contain a large amount of x, y points compared to a 
curve.
"""

AnArray = Union[numpy.ndarray, Iterable[float]]
"""
In this context an iterable of floats is meant by an array.
"""


def _split_first_column(curves: numpy.ndarray) -> Tuple[numpy.ndarray, numpy.ndarray]:
    """

    Args:
        curves:

    Returns:

    Examples:
        >>> import numpy
        >>> xy_curves = numpy.arange(12).reshape(4, 3)
        >>> xy_curves
        array([[ 0,  1,  2],
               [ 3,  4,  5],
               [ 6,  7,  8],
               [ 9, 10, 11]])
        >>> outer_left_column, remaining_columns = _split_first_column(xy_curves)
        >>> outer_left_column
        array([0, 3, 6, 9])
        >>> remaining_columns
        array([[ 1,  2],
               [ 4,  5],
               [ 7,  8],
               [10, 11]])

    """
    return curves[:, 0], curves[:, 1:]


def _calculate_curve_by_cubic_spline(
    base_points: BasePoints, target_x: AnArray
) -> DataFrame:
    """

    Args:
        base_points:
        target_x:

    Returns:
        numpy.ndarray

    Raises:
        ValueError:
            If base points shape exceeds (n, m).

    Examples:
        >>> from doctestprinter import doctest_print
        >>> sample_base_points = [(0, 0), (2, 3), (8, 9), (10, 10)]
        >>> requested_x_values = list(range(6))
        >>> sample_curve = _calculate_curve_by_cubic_spline(
        ...     base_points=sample_base_points, target_x=requested_x_values
        ... )
        >>> doctest_print(sample_curve)
                  y
        x
        0.0  0.0000
        1.0  1.5625
        2.0  3.0000
        3.0  4.3125
        4.0  5.5000
        5.0  6.5625

    """
    base_points = np.array(base_points, dtype=np.float)
    deeply_multidimensional_array = len(base_points.shape) > 2
    if deeply_multidimensional_array:
        raise ValueError(
            "Only (n, m) shaped arrays are supported. Got to many dimensions."
        )
    not_enough_values = len(base_points.shape) < 2
    if not_enough_values:
        raise ValueError(
            "Only (n, m) shaped arrays are supported. Got only 1-dimension."
        )
    independent_x, multiple_y = _split_first_column(base_points)
    requested_x = np.array(target_x)
    cubic_spline = CubicSpline(independent_x, multiple_y)
    spline_y_values = cubic_spline(requested_x)
    requested_curve = DataFrame(
        spline_y_values.astype(float), index=pandas.Index(requested_x.astype(float))
    )
    requested_curve.index.name = _DEFAULT_ABSCISSA_NAME
    requested_curve.columns = [_DEFAULT_COLUMN_LABELS[-1]]
    return requested_curve


def _offset_curves(
    curves: DataFrame, offsets: Optional[Union[float, Iterable[float]]] = None
) -> DataFrame:
    """

    Args:
        curves:
        offsets:

    Returns:

    Test:
        # Suppression Justification; Private member imported only for testing.
        >>> # noinspection PyProtectedMember
        >>> from examplecurves import _offset_curves
        >>> from pandas import DataFrame
        >>> sample_frame = DataFrame([[1, 2, 3]], index=[0], columns=list(iter("abc")))
        >>> from doctestprinter import doctest_print
        >>> doctest_print(_offset_curves(sample_frame))
           a  b  c
        0  1  2  3
        >>> doctest_print(_offset_curves(sample_frame, 0.1))
             a  b  c
        0.1  1  2  3
        >>> doctest_print(_offset_curves(sample_frame, [0.1, 0.2, 0.3]))
               a    b  c
        0.1  1.2  2.3  3
        >>> doctest_print(_offset_curves(sample_frame, [0.1, 0.2, 0.3, 0.4, 0.5]))
               a    b    c
        0.1  1.2  2.3  3.4
    """
    if offsets is None:
        return curves

    if not isinstance(offsets, (list, tuple)):
        offsets = [offsets]

    x_offset, *y_offsets = offsets
    requested_curves = curves.copy()
    requested_curves.index += x_offset
    curve_count = len(requested_curves.columns)
    for index, y_offset in enumerate(y_offsets[:curve_count]):
        active_columns = requested_curves.columns[index]
        requested_curves[active_columns] += y_offset

    return requested_curves


@overload
def _offset_curves_in_place(
    curves: List[DataFrame], offsets: Optional[Sequence[float]] = None
):
    pass


@overload
def _offset_curves_in_place(
    curves: List[DataFrame], offsets: Optional[Sequence[Sequence[float]]] = None
):
    pass


def _offset_curves_in_place(
    curves: List[DataFrame],
    offsets: Optional[Union[Sequence[float], Sequence[Sequence[float]]]] = None,
):
    """
    Args:
        curves:
        offsets:

    Returns:

    Test:
        # Suppression Justification; Private member imported only for testing.
        >>> # noinspection PyProtectedMember
        >>> from examplecurves import _offset_curves_in_place
        >>> from pandas import DataFrame, Index
        >>> from doctestprinter import doctest_print
        >>> test_frame = DataFrame([0], columns=["y"], index=Index([0], name="x"))
        >>> sample_curves = [test_frame.copy(), test_frame.copy()]
        >>> _offset_curves_in_place(curves=sample_curves, offsets=[1.0])
        Traceback (most recent call last):
            ...
        ValueError: There must be 2 curve offsets defined. Got only 1.
        >>> _offset_curves_in_place(curves=sample_curves, offsets=[1.0, 2.0])
        >>> for item in sample_curves:
        ...     doctest_print(item)
             y
        x
        1.0  0
             y
        x
        2.0  0
        >>> sample_curves = [test_frame.copy(), test_frame.copy()]
        >>> _offset_curves_in_place(
        ...     curves=sample_curves, offsets=[(1.0, 1.0), (2.0, 2.0)]
        ... )
        >>> for item in sample_curves:
        ...     doctest_print(item)
               y
        x
        1.0  1.0
               y
        x
        2.0  2.0
    """
    no_offsets_defined_so_do_nothing = offsets is None
    if no_offsets_defined_so_do_nothing:
        return None

    count_of_sample_curves = len(curves)
    offset_count = len(offsets)
    if offset_count < count_of_sample_curves:
        raise ValueError(
            "There must be {} curve offsets defined. Got only {}."
            "".format(count_of_sample_curves, offset_count)
        )

    for index in range(len(curves)):
        curves[index] = _offset_curves(curves=curves[index], offsets=offsets[index])


def load(
    group_index: str,
    cut_curve_at: Optional[List[int]] = None,
    x_offsets: Optional[List[float]] = None,
    curve_selection: Optional[List[int]] = None,
) -> List[DataFrame]:
    """
    Loads sample curves with additional preperations.

    Args:
        group_index:
            The group index consists of 2 chars.

        cut_curve_at(Optional[List[int]]):
            An optional index at which the curve is cut. A list defines parameters
            of a slice.

        x_offsets(Optional[List[float]]):

        curve_selection(Optional[List[int]]):

    Returns:
        List[DataFrame]

    """
    if isinstance(cut_curve_at, (list, tuple)):
        curve_value_selection_slice = slice(*cut_curve_at)
    else:
        curve_value_selection_slice = slice(cut_curve_at)

    selection_pattern = "*{}?.csv".format(group_index)
    sample_curve_paths = list(_SAMPLE_CURVE_ROOT_PATH.glob(selection_pattern))
    if curve_selection is not None:
        sample_curve_paths = [sample_curve_paths[index] for index in curve_selection]
        count_of_sample_curves = len(sample_curve_paths)
    else:
        count_of_sample_curves = len(sample_curve_paths)
        curve_selection = list(range(count_of_sample_curves))

    if count_of_sample_curves == 0:
        raise ValueError(
            "No sample curves for of the group-index '{}' "
            "where found in '{}'".format(group_index, _SAMPLE_CURVE_ROOT_PATH)
        )

    used_offsets = x_offsets
    if x_offsets is not None:
        x_offset_count = len(x_offsets)
        if x_offset_count < count_of_sample_curves:
            raise ValueError(
                "There must be {} curve offsets defined. Got only {}."
                "".format(count_of_sample_curves, x_offset_count)
            )
        if x_offset_count > count_of_sample_curves:
            maximum_selected_index = max(curve_selection)
            if maximum_selected_index > x_offset_count:
                raise ValueError(
                    "The given offsets doesn't fit to the curve selection. "
                    "Either supply the same amount of offsets as the selection of {} "
                    "or a list with {} items."
                    "".format(count_of_sample_curves, x_offset_count)
                )
            used_offsets = [x_offsets[index] for index in curve_selection]

    add_offset_to_curves = used_offsets is not None

    sample_curves = []
    for index, curve_filepath in enumerate(sample_curve_paths):
        curve = pandas.read_csv(curve_filepath, index_col="x")
        curve = curve.iloc[curve_value_selection_slice]
        if add_offset_to_curves:
            curve = _offset_curves(curve, offsets=used_offsets[index])
        sample_curves.append(curve)

    return sample_curves


_GROUP10_SPLINE_ARGS = numpy.array(
    list(zip([0.0, 0.2, 0.8, 1.0], [0.0, 0.3, 0.9, 1.0]))
)
_GROUP10_TARGET_X = numpy.arange(0.0, 1.1, 0.1)


CurveCreationParameters = namedtuple(
    "CurveCreationParameters", "creation_function curve_key_arguments offsets"
)


class CreatesCurves(object):
    @staticmethod
    def make(**kwargs):
        raise NotImplementedError(
            "This method needs to implement "
            "the creation of a curve sample upon keyword arguments."
        )

    @classmethod
    def get_curve_creation_parameters(cls) -> List[Dict]:
        raise NotImplementedError(
            "This method needs to return the requested creation parameters "
            "of each curve defined within this class."
        )

    @classmethod
    def iter_curve_creation_parameters(
        cls, selection_indexes: Optional[List[int]] = None
    ) -> Generator[Dict, None, None]:
        all_parameters = cls.get_curve_creation_parameters()
        if selection_indexes is not None:
            selected_creation_parameters = [
                copy.deepcopy(parameters)
                for index, parameters in enumerate(all_parameters)
                if index in selection_indexes
            ]
        else:
            selected_creation_parameters = copy.deepcopy(all_parameters)
        return selected_creation_parameters

    @classmethod
    def get_offsets(cls, offset_index: int):
        raise NotImplementedError(
            "This method needs to return the predefined offset "
            "for the requested offset index."
        )

    @classmethod
    def get_offsets(cls, offset_index: int):
        raise NotImplementedError(
            "This method needs to return the predefined offset "
            "for the requested offset index."
        )

    @classmethod
    def get_offset_count(cls):
        raise NotImplementedError(
            "This method needs to return the count of predefined offsets."
        )


class NonLinear0(CreatesCurves):
    """
    5 non linear curves with a light curvature. Each curve has 11 points.

    Examples:
        >>> import examplecurves
        >>> non_linear_curves_no_0 = examplecurves.create("nonlinear0")
        >>> from doctestprinter import doctest_print
        >>> doctest_print(non_linear_curves_no_0[1])
                   y
        x
        0.0   0.0000
        0.1   1.5625
        0.2   3.0000
        0.3   4.3125
        0.4   5.5000
        0.5   6.5625
        0.6   7.5000
        0.7   8.3125
        0.8   9.0000
        0.9   9.5625
        1.0  10.0000

    .. plot::

        from examplecurves import make_family_overview_plots
        make_family_overview_plots("nonlinear0")

    """

    SPLINE_ARGS = numpy.array([(0.0, 0.0), (0.2, 0.3), (0.8, 0.9), (1.0, 1.0)])
    TARGET_X = numpy.arange(0.0, 1.1, 0.1)

    CURVE_CREATION_PARAMETERS = [
        {"base_points": SPLINE_ARGS * [1.15, 9.0], "target_x": TARGET_X * 1.15,},
        {"base_points": SPLINE_ARGS * [1.0, 10.0], "target_x": TARGET_X,},
        {"base_points": SPLINE_ARGS * [1.1, 10.2], "target_x": TARGET_X * 1.11,},
        {"base_points": SPLINE_ARGS * [0.96, 11.5], "target_x": TARGET_X * 0.96,},
        {"base_points": SPLINE_ARGS * [0.9, 11.5], "target_x": TARGET_X * 0.9,},
    ]

    OFFSETS = [
        [0.08, 0.1, 0.05, 0.01, 0.02],
        [(0.08, 0.01), (0.1, 0.05), (0.05, 0.1), (0.01, 0.08), (0.02, 0.0)],
    ]

    @staticmethod
    def make(**kwargs):
        return _calculate_curve_by_cubic_spline(**kwargs)

    @classmethod
    def get_curve_creation_parameters(cls) -> List[Dict]:
        return cls.CURVE_CREATION_PARAMETERS

    @classmethod
    def get_offsets(cls, offset_index: int):
        return copy.deepcopy(cls.OFFSETS[offset_index])

    @classmethod
    def get_offset_count(cls):
        return len(cls.OFFSETS)


SAMPLE_CURVE_CREATORS = {"nonlinear0": NonLinear0}


@overload
def _cut_curves_in_place(curves: List[DataFrame], cut_curves_at: int):
    pass


@overload
def _cut_curves_in_place(curves: List[DataFrame], cut_curves_at: List[int]):
    pass


def _cut_curves_in_place(curves: List[DataFrame], cut_curves_at: Union[int, List[int]]):
    """

    Args:
        curves:

    Returns:

    Test:
        # Suppression Justification; Private member imported only for testing.
        >>> # noinspection PyProtectedMember
        >>> from examplecurves import _cut_curves_in_place
        >>> import numpy
        >>> sample_curves = [DataFrame(numpy.arange(5))]
        >>> sample_curves[0]
           0
        0  0
        1  1
        2  2
        3  3
        4  4
        >>> _cut_curves_in_place(sample_curves, 2)
        >>> sample_curves[0]
           0
        0  0
        1  1
        >>> sample_curves = [DataFrame(numpy.arange(5))]
        >>> _cut_curves_in_place(sample_curves, [2, 4])
        >>> sample_curves[0]
           0
        2  2
        3  3
        >>> sample_curves = [DataFrame(numpy.arange(5))]
        >>> _cut_curves_in_place(sample_curves, [-4, None, 2])
        >>> sample_curves[0]
           0
        1  1
        3  3
    """
    if isinstance(cut_curves_at, (list, tuple)):
        curve_value_selection_slice = slice(*cut_curves_at)
    else:
        curve_value_selection_slice = slice(cut_curves_at)

    for index, curve_filepath in enumerate(curves):
        curves[index] = curves[index].iloc[curve_value_selection_slice]


def get_curve_creator(family_name: str) -> CreatesCurves:
    return SAMPLE_CURVE_CREATORS[family_name]


def create(
    family_name: str,
    cut_curves_at: Optional[Union[int, List[int]]] = None,
    offsets: Optional[Union[Iterable[float], Iterable[Tuple[float, float]]]] = None,
    predefined_offset: Optional[int] = None,
    curve_selection: Optional[List[int]] = None,
) -> List[DataFrame]:
    """
    Creates the family of curves requested by name.

    Args:
        family_name:
            Name of the *family of curves*.

        cut_curves_at(Optional[Union[int, List[Optional[int]]]]):
            Cuts the curves at an integer position, os slices it by 2 or 3
            entries, where 'None' is a blank. Like [None, -3] being [:-3].

        offsets(Optional[Union[Iterable[float], Iterable[Tuple[float, float]]]]):
            Offsets to apply to the group's curves. Provide either abzissa offsets
            as a 1-dimensial array or absizza and ordinate offsets as a 2-dimensional
            array.

        predefined_offset(Optional[int]):
            Index of the group's predefined offsets to use. Overrules *offsets*.

        curve_selection(Optional[List[int]]):
            Number (0 .. n-1) of the curves, which should be actually be created.

    Returns:
        List[DataFrame]

    Examples:
        >>> import examplecurves
        >>> from doctestprinter import doctest_iter_print, doctest_print
        >>> sample_curves = examplecurves.create(
        ...     family_name="nonlinear0", cut_curves_at=[2, 8, 2]
        ... )
        >>> doctest_iter_print(sample_curves)
                 y
        x
        0.23  2.70
        0.46  4.95
        0.69  6.75
               y
        x
        0.2  3.0
        0.4  5.5
        0.6  7.5
                      y
        x
        0.222  3.085479
        0.444  5.651643
        0.666  7.698492
                   y
        x
        0.192  3.450
        0.384  6.325
        0.576  8.625
                  y
        x
        0.18  3.450
        0.36  6.325
        0.54  8.625
        >>> sample_curves = examplecurves.create(
        ...     family_name="nonlinear0",
        ...     cut_curves_at=[2, 4],
        ...     predefined_offset=1,
        ...     curve_selection=[1]
        ... )
        >>> doctest_print(sample_curves[0])
                   y
        x
        0.28  3.0100
        0.38  4.3225

    """
    if family_name not in SAMPLE_CURVE_CREATORS:
        raise ValueError(
            "Example curve group '{}' could not be found.".format(family_name)
        )
    creates_curves = SAMPLE_CURVE_CREATORS[family_name]

    if predefined_offset is not None:
        try:
            offsets = creates_curves.get_offsets(predefined_offset)
        except IndexError:
            raise IndexError(
                "The group '{}' doesn't have offsets defined at the index '{}'"
                "".format(offsets)
            )

    requested_curves = []
    for creation_keyword_parameters in creates_curves.iter_curve_creation_parameters(
        selection_indexes=curve_selection
    ):
        created_curves = creates_curves.make(**creation_keyword_parameters)
        requested_curves.append(created_curves)

    count_of_sample_curves = len(requested_curves)
    if count_of_sample_curves == 0:
        raise ValueError(
            "No sample curves for of the group-index '{}' "
            "where found in '{}'".format(family_name, _SAMPLE_CURVE_ROOT_PATH)
        )

    _cut_curves_in_place(curves=requested_curves, cut_curves_at=cut_curves_at)
    _offset_curves_in_place(curves=requested_curves, offsets=offsets)
    return requested_curves


def plot_curves(curves: List[DataFrame], title: Optional[str] = None):
    """
    Plots curves within a diagram.

    Args:
        curves(List[DataFrame]):
            Curves to plot.

        title(Optional[str]):
            Optional title for the diagram.

    """
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(8, 5), dpi=96, tight_layout=True)
    gs = fig.add_gridspec(1, 10)
    axes = fig.add_subplot(gs[:, :9])
    if title:
        axes.set_title(title)
    for index, curve in enumerate(curves):
        axes.plot(curve, "-o", label=str(index))
    fig.legend(loc="upper right", bbox_to_anchor=(0.99, 0.945))
    fig.show()


def make_family_overview_plots(family_name: str):
    """
    Plots each predefined offset example of the *family of curves*.

    Args:
        family_name(str):
            Name of the exemplary family of curves.

    """
    creates_curves = get_curve_creator(family_name=family_name)
    number_of_offsets = creates_curves.get_offset_count()

    example_title = "{}'s curves".format(family_name)
    curves = create(family_name=family_name)
    plot_curves(curves, title=example_title)

    for offset_index in range(number_of_offsets):
        example_title = "{}'s curves with offsets at index {}".format(
            family_name, offset_index
        )
        curves = create(family_name=family_name, predefined_offset=offset_index)
        plot_curves(curves, title=example_title)
