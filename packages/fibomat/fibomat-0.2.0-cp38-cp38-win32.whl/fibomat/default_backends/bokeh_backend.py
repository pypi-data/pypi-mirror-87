from typing import List, Optional, Dict, Any
import itertools
import pathlib
import tempfile

import bokeh.models as bm
import bokeh.plotting as bp
from bokeh.embed import file_html
from bokeh.resources import INLINE


from fibomat.backend import BackendBase
from fibomat.default_backends._bokeh_site import BokehSite, ShapeType
from fibomat import shapes
from fibomat.linalg import Vector
from fibomat.site import Site
from fibomat.pattern import Pattern
from fibomat.utils import PathLike
from fibomat.shapes.rasterizedpoints import RasterizedPoints
from fibomat.raster_styles.rasterstyle import RasterStyle
from fibomat.units import LengthUnit, TimeUnit, LengthQuantity, U_, Q_
from fibomat.dimensioned_object import DimObjLike
from fibomat.shapes import Shape
from fibomat.mill import Mill
from fibomat.default_backends.measuretool import MeasureTool


from bokeh.resources import JSResources
from bokeh.core.templates import JS_RESOURCES


_old_js_raw = getattr(JSResources, 'js_raw')

here = pathlib.Path(__file__).parent.resolve()
with open(here / 'bokeh-measuretool.min.js') as fp_js:
    _custom_ext_js = fp_js.read()

def _js_raw_patched(self):
    raw = _old_js_raw.fget(self)
    raw.append(_custom_ext_js)
    return raw


setattr(JSResources, 'js_raw', property(_js_raw_patched))


class StubAreaStyle(RasterStyle):
    def __init__(self, dimension: int):
        self._dimension = dimension

    @property
    def dimension(self) -> int:
        return self._dimension

    def rasterize(
        self,
        dim_shape: DimObjLike[Shape, LengthUnit],
        mill: Mill,
        out_length_unit: LengthUnit,
        out_time_unit: TimeUnit
    ) -> RasterizedPoints:
        pass


class BokehBackend(BackendBase):
    """
    The default backend for plotting projects, based on the bokeh library.
    All shapes defined in fibomat library are supported.

    .. note:: :class:`~fibomat.shapes.arc.shapes.Arc` and :class:`~fibomat.shapes.curve.shapes.Curve` are rasterized during plotting
              due to lack of supported of the HoverTool for this shapes in the bokeh library. The pitch can be defined
              via the `rasterize_pitch` parameter.
    """
    name = 'bokeh'

    def __init__(
            self, *,
            unit: Optional[LengthUnit] = None,
            title: Optional[str] = None,
            hide_sites: bool = False,
            rasterize_pitch: Optional[LengthQuantity] = None,
            fullscreen: bool = True,
            legend: bool = True,
            cycle_colors: bool = True,
            **kwargs
    ):
        """
        Args:
            unit (units.UnitType, optional): used unit for plotting, default to units.U_('µm')
            title (str, optional): title of plot, default to ''
            hide_sites (bool, optional): if true, sides' outlines are not shown, default to false
            rasterize_pitch (units.QuantityType. optional): curve_tools.rasterize pitch for shapes.Arc, ... and shapes.Curve, default to units.Q_('0.01 µm')
            fullscreen (bool, optional): if true, plot will be take the whole page, default to True
            cycle_colors (bool): if True, different sites get different colors.
        """
        super().__init__(**kwargs)

        if unit:
            if unit.dimensionality != '[length]':
                raise ValueError('unit\'s dimension must by [length].')
            self._unit = unit
        else:
            self._unit = U_('µm')

        if title:
            self._title = str(title)
        else:
            self._title = ''

        self._hide_sites = bool(hide_sites)

        if rasterize_pitch:
            if rasterize_pitch.dimensionality != '[length]':
                raise ValueError('rasterize_pitch\'s dimension must by [length].')
            self._rasterize_pitch = rasterize_pitch
        else:
            self._rasterize_pitch = Q_('0.01 µm')

        self._fullscreen = bool(fullscreen)
        self._legend = bool(legend)

        self._cycle_colors = cycle_colors

        self._bokeh_sites: List[BokehSite] = []
        self._annotation_site = BokehSite(
            site_index=-1,
            plot_unit=self._unit,
            dim_center=(Vector(0, 0), self._unit),
            rasterize_pitch=self._rasterize_pitch,
            description='Annotations'
        )
        self.fig: Optional[bp.Figure] = None

    def process_site(self, site: Site):
        self._bokeh_sites.append(
            BokehSite(
                site_index=len(self._bokeh_sites),
                plot_unit=self._unit,
                dim_center=site.center,
                rasterize_pitch=self._rasterize_pitch,
                cycle_colors=self._cycle_colors,
                dim_fov=site.fov,
                description=site.description
            )
        )
        super().process_site(site)

    def process_pattern(self, ptn: Pattern) -> None:
        super().process_pattern(ptn)

    def process_unknown(self, ptn: Pattern) -> None:
        bbox = ptn.dim_shape[0].bounding_box
        bbox_ptn = Pattern(
            dim_shape=(shapes.Rect(bbox.width, bbox.height, 0, bbox.center), ptn.dim_shape[1]),
            mill=ptn.shape_mill,
            raster_style=ptn.raster_style,
            **ptn.kwargs  # True if 'annotation' in ptn.kwargs else False
        )
        self._filled_curve(bbox_ptn)

    def _collect_plot_data(self, shape_type: ShapeType) -> Dict[str, Any]:
        # https://stackoverflow.com/a/40826547
        keys = BokehSite.plot_data_keys
        data_dicts = [site.plot_data[shape_type] for site in self._bokeh_sites]
        data_dicts.append(self._annotation_site.plot_data[shape_type])
        return {key: list(itertools.chain(*[data_dict[key] for data_dict in data_dicts])) for key in keys}

    def plot(self):
        tooltips = [
            # ('type', 'shape'),
            ('shape', '@shape_prop'),
            # ('collection_index', '@collection_index'),
            ('mill', '@mill'),
            ('raster style', '@raster_styles'),
            ('site', '@site_id'),
            ('description', '@description')
            # ('mill_settings', '@mill_settings'),
        ]

        site_tooltips = [
            # ('site', '@site'),
            ('description', '@description')
        ]

        fig = bp.figure(
            title=self._title,
            x_axis_label=f'x / {self._unit:~P}', y_axis_label=f'y / {self._unit:~P}',
            match_aspect=True,
            sizing_mode='stretch_both' if self._fullscreen else 'stretch_width',
            tools="pan,wheel_zoom,reset,save"
        )

        fig.add_tools(
            MeasureTool(
                measure_unit=f'{self._unit:~P}',  # line_color=bc.groups.red.Crimson, line_width=3  # bpal.all_palettes['Colorblind'][4][3]
            )
        )

        fig.add_tools(bm.BoxZoomTool(match_aspect=True))

        spot_glyphs = fig.circle_x(
            x='x', y='y',
            fill_color='color', line_color='color', fill_alpha=.25,
            legend_group='site_id',
            size=10,
            source=bm.ColumnDataSource(self._collect_plot_data(ShapeType.SPOT))
        )

        non_filled_curve_glyphs = fig.multi_line(
            xs='x', ys='y',
            line_color='color', line_width=2,
            legend_group='site_id',
            source=bm.ColumnDataSource(self._collect_plot_data(ShapeType.NON_FILLED_CURVE))
        )

        filled_curve_glyphs = fig.multi_polygons(
            xs='x', ys='y',
            line_width=2,
            fill_color='color', line_color='color', fill_alpha='fill_alpha',
            hatch_pattern='hatch_pattern',
            legend_group='site_id',
            source=bm.ColumnDataSource(self._collect_plot_data(ShapeType.FILLED_CURVE))
        )

        # layers
        # https://github.com/bokeh/bokeh/issues/9087
        if not self._hide_sites:
            site_glyphs = fig.multi_polygons(
                xs='x', ys='y',
                line_width=2,
                fill_color='color', line_color='color', fill_alpha='fill_alpha', line_alpha='fill_alpha',
                legend_group='site_id',
                source=bm.ColumnDataSource(self._collect_plot_data(ShapeType.SITE))
            )

            site_glyphs_hover = bm.HoverTool(
              renderers=[site_glyphs],
              tooltips=site_tooltips,
              point_policy='follow_mouse'
            )
            fig.add_tools(site_glyphs_hover)

        # hover tool for shapes
        # add shape hover tool after site hovertool so it is rendered on top of the site tooltip
        shape_glyphs_hover = bm.HoverTool(
            renderers=[
                spot_glyphs, non_filled_curve_glyphs,  filled_curve_glyphs
            ],
            tooltips=tooltips, point_policy='follow_mouse'
        )
        fig.add_tools(shape_glyphs_hover)

        def sorter(item):
            value = item.label['value']
            if value == 'Annotations':
                return -1
            else:
                return int(value.split(',')[0].split(' ')[1])

        legend_tmp = {x.label['value']: x for x in fig.legend.items}.values()
        fig.legend.items.clear()
        fig.legend.items.extend(sorted(
            legend_tmp,
            key=sorter
        ))

        fig.legend.visible = self._legend

        self.fig = fig

    def _save(self, fp):
        here = pathlib.Path(__file__).parent.resolve()
        with open(here / 'bokeh-measuretool.min.js') as fp_js:
            custom_js = fp_js.read()

        template = """
            {{% block inner_body %}}
                {{{{ super() }}}}
                <script type="text/javascript">
            {}
                </script>
            {{% endblock %}}
        """.format(custom_js)

        fp.write(file_html(self.fig, resources=INLINE, template=template))
        fp.flush()

    def show(self):
        # def custom_show(filename, browser=None, new="tab"):
        #     from bokeh.util.browser import NEW_PARAM, get_browser_controller
        #     import pathlib
        #     controller = get_browser_controller(browser=browser)
        #
        #     controller.open(str("file://" / pathlib.Path(filename).absolute()), new=NEW_PARAM[new])
        #
        # fp = tempfile.NamedTemporaryFile('w', suffix='.html', delete=False)
        #
        # self._save(fp)
        # custom_show(fp.name)

        bp.show(self.fig)

    def save(self, filename: PathLike):
        bp.output_file(filename)
        bp.save(self.fig)
        # with open(filename, 'w') as fp:
        #     self._save(fp)

    def spot(self, ptn: Pattern[shapes.Spot]) -> None:
        if '_annotation' in ptn.kwargs:
            self._annotation_site.spot(ptn)
        else:
            self._bokeh_sites[-1].spot(ptn)

    def _non_filled_curve(self, ptn):
        if '_annotation' in ptn.kwargs:
            self._annotation_site.non_filled_curve(ptn)
        else:
            self._bokeh_sites[-1].non_filled_curve(ptn)

    def _filled_curve(self, ptn):
        if '_annotation' in ptn.kwargs:
            self._annotation_site.filled_curve(ptn)
        else:
            self._bokeh_sites[-1].filled_curve(ptn)

    def _dispatch_pattern(self, ptn):
        if not ptn.dim_shape.obj.is_closed:
            self._non_filled_curve(ptn)
        elif ptn.raster_style.dimension < 2:
            self._non_filled_curve(ptn)
        else:
            self._filled_curve(ptn)

    def line(self, ptn: Pattern[shapes.Line]) -> None:
        self._dispatch_pattern(ptn)

    def polyline(self, ptn: Pattern[shapes.Polyline]) -> None:
        self._dispatch_pattern(ptn)

    def arc(self, ptn: Pattern[shapes.Arc]) -> None:
        self._dispatch_pattern(ptn)

    def arc_spline(self, ptn: Pattern[shapes.ArcSpline]) -> None:
        self._dispatch_pattern(ptn)

    def polygon(self, ptn: Pattern[shapes.Polygon]) -> None:
        self._dispatch_pattern(ptn)

    def rect(self, ptn: Pattern[shapes.Rect]) -> None:
        self._dispatch_pattern(ptn)

    def ellipse(self, ptn: Pattern[shapes.Ellipse]) -> None:
        self._dispatch_pattern(ptn)

    def circle(self, ptn: Pattern[shapes.Circle]) -> None:
        self._dispatch_pattern(ptn)

    def rasterized_points(self, ptn: Pattern[shapes.RasterizedPoints]):
        rect = shapes.Rect.from_bounding_box(ptn.dim_shape.obj.bounding_box)

        new_pattern = Pattern(
            dim_shape=(rect, ptn.dim_shape.unit),
            mill=ptn.mill,
            raster_style=ptn.raster_style,
            description=ptn.description,
            **ptn.kwargs
        )

        if '_annotation' in ptn.kwargs:
            self._annotation_site.filled_curve(new_pattern, hatch_pattern='/')
        else:
            self._bokeh_sites[-1].filled_curve(new_pattern, hatch_pattern='/')
