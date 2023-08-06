# from typing import Union
#
# import numpy as np
#
# from fibomat.mill import mill as mill_
# from fibomat import rasterizing as raster
# from fibomat import units
#
#
# class DoseEstimation:
#     def __init__(self):
#         pass
#
#     @property
#     def total_mean(self):
#         return None
#
#     @property
#     def local_mean(self):
#         return None
#
#     @property
#     def delta(self):
#         return None
#
#     @property
#     def delta_max(self):
#         return None
#
#     @property
#     def delta_min(self):
#         return None
#
#
# def estimate_dose(mill: mill_.Mill, shape: Union[raster.RasterizedPoints], shape_unit: units.UnitType):
#     if not mill.beam_specified:
#         raise RuntimeError('beam must be specified in mill object to calculate dose.')
#
#     beam = mill.beam
#     dwell_points = shape # shape.dwell_points.copy()
#
#     total_dose = np.sum(mill.spot_dose * dwell_points[:, 2]) / units.Q_('1 µm')
#
#     # if isinstance(shape, raster.RasterizedCurve):
#     #
#     # else:
#     #     raise NotImplementedError
#
#     return total_dose
