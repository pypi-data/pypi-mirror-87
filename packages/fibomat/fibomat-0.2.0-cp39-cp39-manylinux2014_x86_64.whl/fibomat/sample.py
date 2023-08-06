"""
Provides the :class:`Sample` class.
"""

from typing import Optional, List, Union, TypeVar, Type, Tuple
import collections

from fibomat import site
from fibomat import units
from fibomat import linalg
from fibomat import backend
from fibomat import utils
from fibomat import shapes
from fibomat import pattern
from fibomat.layout import LayoutBase
from fibomat import default_backends
from fibomat import describable

BackendType = TypeVar('BackendType')


class Sample(describable.Describable):
    """
    This class is the glueing between all subcomponents of the library.
    All shapes and their milling settings are added to this class and can be exported with the help of registered
    backends .

    """
    def __init__(self, description: Optional[str] = None):
        """
        Args:
            description (str, optional): Optional description of the project, default to None
        """
        super().__init__(description)

        self._sites: List[site.Site] = []
        self._annotations: [List[Tuple[shapes.Shape, bool, Optional[str]]]] = []

    def create_site(
            self,
            dim_position: linalg.DimVectorLike,
            dim_fov: Optional[linalg.DimVectorLike] = None,
            description: Optional[str] = None
    ) -> site.Site:
        """
        Creates and Site in-place (hence, the Site is automatically added to the sample). Patterns can be added to the
        returned object.

        See :class:`fibomat.site.Site.__init__` for argument description.

        Returns:
            Site
        """
        new_site: site.Site = site.Site(dim_position, dim_fov, description)
        self._sites.append(new_site)
        return new_site

    def add_site(self, site_like: site.Site) -> None:
        """
        Adds a Site to the project.
        Alternatively, the '+=' operator can be used.

        Args:
            site_like (Site): new site

        Returns:
            None
        """
        if isinstance(site_like, LayoutBase):
            for site_ in site_like.layout_elements():
                self._sites.append(site_)
        else:
            self._sites.append(site_like)

    def __iadd__(self, site_like):
        """See :meth:`~Sample.add_site`."""
        self.add_site(site_like)
        return self

    @staticmethod
    def _export(backend_class: Type[BackendType], sites: Union[site.Site, List[site.Site]], **kwargs) -> BackendType:
        exporter: Type[backend.BackendBase] = backend_class(**kwargs)

        if isinstance(sites, collections.Iterable):
            for site_ in sites:
                exporter.process_site(site_)
        else:
            exporter.process_site(sites)

        return exporter

    def plot(self, show: bool = True, filename: Optional[utils.PathLike] = None, **kwargs) -> default_backends.BokehBackend:
        """
        Plots and save the project using the :class:`~fibomat.default_backends.bokeh_backend.BokehBackend`.

        Args:
            show (bool): if true, the plot is opened in a browser automatically
            filename (PathLike, optional): if filename is given, the plot is saved in this file. The file suffix should
                                           be `*.htm` or `*.html`, default to None
            `**kwargs`: parameters for the bokeh backend. These are directly passed to the __init__ method of the
                        BokehBackend class. The title parameter is automatically set to the :attr:`Sample.description`

        Returns:
            None
        """

        plotter: default_backends.BokehBackend = self._export(
            default_backends.BokehBackend, self._sites, title=self._description, **kwargs)

        for shape, filled, color, descr in self._annotations:
            raster = default_backends.StubAreaStyle(2) if filled else default_backends.StubAreaStyle(1)

            pat = pattern.Pattern((shape, plotter._unit), None, raster, _annotation=True, _color=color, description=descr)
            plotter.process_pattern(
                pat
            )

        plotter.plot()

        if filename:
            plotter.save(filename)
        if show:
            plotter.show()

        return plotter

    # only for convenience/type hinting
    # TODO: find out why sphinx is not working correctly with this overload
    # @overload
    # def export(self, backend_name: Literal['spotlist'], **kwargs) -> SpotListBackend:
    #     return self._export(SpotListBackend, self._sites, **kwargs)

    def export(self, exp_backend: Union[str, Type[backend.BackendBase]], **kwargs) -> backend.BackendBase:
        """
        Exports the project. Note that the method returns the backend object so you will be able to save a file or show
        a plot. See backends example nd docs for details.

        .. note:: The export method does not save any files on its one. This must be done by the user manually. See docs
                  of the used backend for details.

        Args:
            exp_backend (str or Type[backend.BackendBase]):
                name of the backend or class. The backend must be registered before.
            **kwargs: optional arguments are passed to the backend's __init__ method

        Returns:
            BackendBase
        """

        if isinstance(exp_backend, str):
            exp_backend = backend.registry.get(exp_backend)

        return self._export(exp_backend, self._sites, description=self._description, **kwargs)

    def export_multi(self, exp_backend: Union[str, Type[backend.BackendBase]], **kwargs) -> List[backend.BackendBase]:
        """
        Similar to :meth:`Project.export` but for each :class:`fibomat.site.Site` an individual backend instance is
        returned.

        Returns:
            List[BackendBase]
        """
        backends: List[backend.BackendBase] = []

        if isinstance(exp_backend, str):
            exp_backend = backend.registry.get(exp_backend)

        for added_site in self._sites:
            backends.append(self._export(exp_backend, added_site, description=self._description, **kwargs))

        return backends

    def add_annotation(
        self, shape: shapes.Shape, filled: bool = False, color = None, description: Optional[str] = None
    ) -> None:
        """
        Add `shape` to a annotation layer. This layer is only used to visualize extra shapes (e.g. sample dimensions)
        and will be ignored by the exporting backend.

        Args:
            shape (shapes.Shape): shape
            description (str, optional): description, default to None

        Returns:

        """
        self._annotations.append((shape, filled, color, description))
