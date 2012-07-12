import re

##########
# Custom representation of geographic coordinates. Note that wherever
# latitude and longitude appear together, *longitude* comes first. This
# mirrors the convention used by PostgreSQL's earthdistance module.

class Coords:
    """A set of geographic coordinates."""

    def __init__(self, lon, lat):
        if lon < -180 or lon > 180:
            raise ValueError('Longitude out of range.')
        if lat < -90 or lat > 90:
            raise ValueError('Latitude out of range.')
        self._lon = lon
        self._lat = lat

    @property
    def lon(self):
        return self._lon

    @property
    def lat(self):
        return self._lat

    def __str__(self):
        return '({},{})'.format(lon, lat)

class CoordsField(models.Field):
    __metaclass__ = models.SubfieldBase

    description = 'A set of geographic coordinates.'
    coords_re = re.compile(r'\(\s*(?P<lon>\S+?)\s*,\s*(?P<lat>\S+?)\s*\)')

    def __init__(self, *args, **kwargs):
        super(CoordsField, self).__init__(*args, **kwargs)

    def db_type(self, connection):
        return 'geo_coords'

    def to_python(self, value):
        if isinstance(value, Coords):
            return value

        # 'value' is a '(lon, lat)' string that needs parsing
        match = coords_re.search(value)
        if not match:
            raise ValidationError('Invalid input for a Coords instance.')
        return Coords(match.group('lon'), match.group('lat'))
