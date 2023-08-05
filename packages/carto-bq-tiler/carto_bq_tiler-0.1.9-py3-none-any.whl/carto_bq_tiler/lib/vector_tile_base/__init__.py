# Package not in PyPI, source: https://github.com/mapbox/vector-tile-base

from . import engine

VectorTile = engine.VectorTile
Layer = engine.Layer
PointFeature = engine.PointFeature
LineStringFeature = engine.LineStringFeature
PolygonFeature = engine.PolygonFeature
SplineFeature = engine.SplineFeature
FeatureAttributes = engine.FeatureAttributes
Float = engine.Float
FloatList = engine.FloatList
UInt = engine.UInt
scaling_calculation = engine.scaling_calculation

__version__ = "1.0"
