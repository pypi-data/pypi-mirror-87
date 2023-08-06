def dset_version(latest_vers, version):
    if version is None:
        vers = latest_vers
    else:
        if isinstance(version, str):
            assert int(version)>0, "Version number must be positive"
            vers_length = 3
            vers = version.zfill(vers_length)
        else:
            raise TypeError("Please enter the version number as a string")

        if int(vers) < int(latest_vers):
            warnings.filterwarnings("always")
            warnings.warn("You are using an old version of this dataset")
    
    return vers


#DevGoal: I suspect these classes need to be cleaned up a bit and methodized to make testing easier (too many if statements now)
class spatial():
    def __init__(self, spatial_extent):
        pass

    def __main__(spatial_extent):
        if isinstance(spatial_extent, list):
            #bounding box
            if len(spatial_extent)==4 and all(type(i) in [int, float] for i in spatial_extent):
                assert -90 <= spatial_extent[1] <= 90, "Invalid latitude value"
                assert -90 <= spatial_extent[3] <= 90, "Invalid latitude value"
                assert -180 <= spatial_extent[0] <= 360, "Invalid longitude value" #tighten these ranges depending on actual allowed inputs
                assert -180 <= spatial_extent[2] <= 360, "Invalid longitude value"
                assert spatial_extent[0] <= spatial_extent[2], "Invalid bounding box longitudes"
                assert spatial_extent[1] <= spatial_extent[3], "Invalid bounding box latitudes"
                self._spat_extent = spatial_extent
                self.extent_type = 'bounding_box'
            
            #user-entered polygon as list of lon, lat coordinate pairs
            elif all(type(i) in [list, tuple] for i in spatial_extent):
                assert len(spatial_extent)>=4, "Your spatial extent polygon has too few vertices"
                assert spatial_extent[0][0] == spatial_extent[-1][0], "Starting longitude doesn't match ending longitude"
                assert spatial_extent[0][1] == spatial_extent[-1][1], "Starting latitude doesn't match ending latitude"
                polygon = (','.join([str(c) for xy in spatial_extent for c in xy])).split(",")
                polygon = [float(i) for i in polygon]
                self._spat_extent = polygon
                self.extent_type = 'polygon'
                #DevGoal: properly format this input type (and any polygon type) so that it is clockwise (and only contains 1 pole)!!
                warnings.warn("this type of input is not yet well handled and you may not be able to find data")

            #user-entered polygon as a single list of lon and lat coordinates
            elif all(type(i) in [int, float] for i in spatial_extent):
                assert len(spatial_extent)>=8, "Your spatial extent polygon has too few vertices"
                assert len(spatial_extent)%2 == 0, "Your spatial extent polygon list should have an even number of entries"
                assert spatial_extent[0] == spatial_extent[-2], "Starting longitude doesn't match ending longitude"
                assert spatial_extent[1] == spatial_extent[-1], "Starting latitude doesn't match ending latitude"
                polygon = [float(i) for i in spatial_extent]
                self._spat_extent = polygon
                self.extent_type = 'polygon'

            else:
                raise ValueError('Your spatial extent does not meet minimum input criteria')
            
            #DevGoal: write a test for this
            #make sure there is nothing set to self._geom_filepath since its existence determines later steps
            if hasattr(self,'_geom_filepath'):
                del self._geom_filepath

        elif isinstance(spatial_extent, str):
            assert os.path.exists(spatial_extent), "Check that the path and filename of your geometry file are correct"
            #DevGoal: more robust polygon inputting (see Bruce's code): correct for clockwise/counterclockwise coordinates, deal with simplification, etc.
            if spatial_extent.split('.')[-1] in ['kml','shp','gpkg']:
                self.extent_type = 'polygon'
                self._spat_extent = apifmt._format_polygon(spatial_extent)
                self._geom_filepath = spatial_extent

            else:
                raise TypeError('Input spatial extent file must be a kml, shp, or gpkg')

        if not hasattr(self, '_geom_filepath'): self._geom_filepath = None
        return self.extent_type, self._spat_extent, self._geom_filepath

class temporal():

    def __main__(date_range, start_time, end_time):
        if isinstance(date_range, list):
            if len(date_range)==2:
                self._start = dt.datetime.strptime(date_range[0], '%Y-%m-%d')
                self._end = dt.datetime.strptime(date_range[1], '%Y-%m-%d')
                assert self._start.date() <= self._end.date(), "Your date range is invalid"

            else:
                raise ValueError("Your date range list is the wrong length. It should have start and end dates only.")

#DevGoal: accept more date/time input formats
#         elif isinstance(date_range, date-time object):
#             print('it is a date-time object')
#         elif isinstance(date_range, dict):
#             print('it is a dictionary. now check the keys for start and end dates')


        if start_time is None:
            self._start = self._start.combine(self._start.date(),dt.datetime.strptime('00:00:00', '%H:%M:%S').time())
        else:
            if isinstance(start_time, str):
                self._start = self._start.combine(self._start.date(),dt.datetime.strptime(start_time, '%H:%M:%S').time())
            else:
                raise TypeError("Please enter your start time as a string")

        if end_time is None:
            self._end = self._start.combine(self._end.date(),dt.datetime.strptime('23:59:59', '%H:%M:%S').time())
        else:
            if isinstance(end_time, str):
                self._end = self._start.combine(self._end.date(),dt.datetime.strptime(end_time, '%H:%M:%S').time())
            else:
                raise TypeError("Please enter your end time as a string")
        
        return self._start, self._end
