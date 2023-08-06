"""Provide rasterization routines."""
from typing import List, Tuple, Optional, Dict, Any, Union

import numpy as np

from fibomat.shapes.arc import Arc
from fibomat.shapes.line import Line
from fibomat.shapes.rasterizedpoints import RasterizedPoints
from fibomat.shapes.shape import Shape
from fibomat.shapes.arc_spline import ArcSplineCompatible, ArcSpline
from fibomat.linalg import Vector, translate, rotate
from fibomat.curve_tools.intersections import curve_intersections
from fibomat.linalg.boundingbox import BoundingBox
from fibomat.shapes._line_non_continuous import LineNonContinuous


def _rasterize_arc_spline_non_continuous_curve(
    curve: Union[ArcSpline, LineNonContinuous], pitch: float
) -> RasterizedPoints:
    # pylint: disable=invalid-name,too-many-locals

    pitch = float(pitch)
    # n_points = int(curve.length / pitch) + 1

    points = []

    i_points = 0
    offset = 0.
    for segment in curve.segments:
        if isinstance(segment, Arc):
            arc: Arc = segment

            offset_angle = offset / arc.radius
            pitch_angle = pitch / arc.radius

            if offset_angle <= arc.theta:
                points_on_arc = int((arc.theta - offset_angle) / pitch_angle) + 1

                if np.isclose((arc.theta - offset_angle) / pitch_angle - points_on_arc - 1, 0.):
                    points_on_arc += 1

                if not arc.sweep_dir:
                    pitch_angle *= -1.
                    arc_start_angle = arc.start_angle - offset_angle
                else:
                    arc_start_angle = arc.start_angle + offset_angle

                center = np.array(arc.center)
                theta = pitch_angle*np.arange(points_on_arc)

                points.append(
                    center + arc.radius * np.column_stack(
                        (np.cos(theta + arc_start_angle), np.sin(theta + arc_start_angle))
                    )
                )

                i_points += points_on_arc
                offset = pitch - (arc.length - offset - (len(theta)-1) * pitch)
            else:
                offset -= arc.length

        elif isinstance(segment, Line):
            line: Line = segment
            if offset <= line.length:
                direction = (line.end - line.start).normalized()

                start = line.start + direction * offset

                points_on_line = int((line.length-offset) / pitch) + 1

                direction = np.array(direction)
                start = np.array(start)

                t = pitch * np.arange(points_on_line)
                # points[i_points:i_points+points_on_line, :2] = start + np.repeat(t[None, :], 2, axis=0).T * direction
                points.append(start + np.repeat(t[None, :], 2, axis=0).T * direction)
                # points[i_points:i_points+points_on_line, 2] = 1.

                i_points += points_on_line
                offset = pitch - (line.length - t[-1] - offset)
            else:
                offset -= line.length
        else:
            raise RuntimeError(f'Cannot rasterize segment type {segment.__class__.__name__}')

    # assert i_points == n_points
    dwell_points = np.ones(shape=(i_points, 3))
    dwell_points[:, :2] = np.concatenate(points)

    return RasterizedPoints(dwell_points, curve.is_closed)


def rasterize(curve: Shape, pitch: float) -> RasterizedPoints:
    """Rasterize the outline of a Shape with a given pitch uniformly.

    For this, the shape must be convertible to an ArcSpline or must have a `rasterize` method expecting the pitch as
    input.

    Args:
        curve (Shape): curve
        pitch (float): pitch (spacing of points)

    Returns:
        RasterizedPoints

    Raises:
        ValueError: Raised if curve is no ArcSpline, ArcSplineCompatible or not have a `rasterize` method.
    """
    if isinstance(curve, ArcSpline) or isinstance(curve, LineNonContinuous):
        return _rasterize_arc_spline_non_continuous_curve(curve, pitch)

    if raster_method := getattr(curve, 'rasterize', None):
        return raster_method(curve, pitch)

    if isinstance(curve, ArcSplineCompatible):
        return _rasterize_arc_spline_non_continuous_curve(curve.to_arc_spline(), pitch)

    raise ValueError(f'Cannot rasterize the passed object of type {curve.__class__}.')


def _make_line(
    curve: ArcSpline, intersection_interval: Tuple[Dict[str, Any], Dict[str, Any]], holes: List[ArcSpline]
) -> Optional[Line]:
    start = Vector(intersection_interval[0]['pos'])
    end = Vector(intersection_interval[1]['pos'])

    assert np.isclose(start.y, end.y)
    assert end.x > start.x

    midpoint = Vector((start.x + end.x) / 2, start.y)

    if curve.contains(midpoint):
        for hole in holes:
            if hole.contains(midpoint):
                return
        return Line(start, end)


def fill_with_lines(
    curve: ArcSpline, pitch: float, alpha: float, invert: bool, holes: Optional[List[ArcSpline]] = None
) -> List[List[Line]]:
    """Fill a closed shape with lines which are rotated by `alpha`-

    Args:
        curve (ArcSpline): closed curve to be filled.
        pitch (float): distance between lines.
        alpha (float): rotation angle of lines with respect to x-axis.

    Returns:
        List[ArcSpline]

    Raises:
        ValueError: Raised if angle < 0 or angle > pi.
        NotImplementedError: Raised if some kind of singularities occur. This can be fixed (probably) if the shape is
                             rotated.
    """
    # pylint: disable=invalid-name,too-many-locals

    # TODO: cache spatial tree for intersection calculations

    if not curve.is_closed:
        raise ValueError('ArcSpline is not closed.')

    if not (-np.pi/2 <= alpha <= np.pi/2):
        raise ValueError('alpha < -pi/2 or alpha > pi/2')

    holes = holes or []

    # for hole in holes:
    #     if not hole.is_closed:
    #         raise ValueError('hole is not closed')
    #
    #     if hole.bounding_box not in curve.bounding_box:
    #         raise ValueError('Hole not contained in curve.')

    center = curve.center

    curve = curve.transformed(
        translate(-center) | rotate(-alpha)
    )

    holes = list(map(lambda hole: hole.transformed(translate(-center) | rotate(-alpha)), holes))

    extend = 2.1 * pitch

    bbox_curve = curve.bounding_box

    bbox = BoundingBox(bbox_curve.lower_left - (extend, extend), bbox_curve.upper_right + (extend, extend))

    bbox_left = bbox.lower_left.x
    bbox_right = bbox.upper_right.x
    bbox_top = bbox.upper_right.y
    bbox_bottom = bbox.center.y - bbox.height / 2

    y = np.arange(-bbox.height / 2, bbox.height / 2, pitch)

    ny = len(y)

    if invert:
        intersection_line = ArcSpline([(bbox_left, bbox_bottom, 0), (bbox_right, bbox_bottom, 0)], False)
        pitch = -pitch
    else:
        intersection_line = ArcSpline([(bbox_left, bbox_top, 0), (bbox_right, bbox_top, 0)], False)

    fill_lines: List[List[Line]] = []

    for _ in range(ny):
        intersections = curve_intersections(curve, intersection_line)['intersections']

        # ignore coincidences for now
        # # TODO: handle case, if cl_inter contains coincidence
        # assert len(cl_intersections['coincidences']) == 0

        if len(intersections) > 1:
            for hole in holes:
                intersections.extend(curve_intersections(hole, intersection_line)['intersections'])

            intersections_sorted = sorted(
                intersections,
                key=lambda intersection: intersection['pos'][0]
            )

            fill_line = []

            for intersection_interval in zip(intersections_sorted, intersections_sorted[1:]):
                if part_fill_line := _make_line(curve, intersection_interval, holes):
                    fill_line.append(
                        part_fill_line.transformed(
                            translate(center) | rotate(alpha, origin=center)
                        )
                    )

            if fill_line:
                fill_lines.append(fill_line)

        intersection_line = intersection_line.translated((0, -pitch))

    return fill_lines
