import datetime
import tempfile
import unittest
import os
from collections import OrderedDict

from gtfscrud import FileHandler, GtfsCrud, Trip, Route, Agency, Calendar, Shape, Stop, StopTime


class FileHandlerTests(unittest.TestCase):
    def test_get_generator(self):
        # Arrange
        expected = ['val1', 'vla2']  # OrderedDict([('title1', 'val1'), (' title2', 'vla2')])

        file_content = "title1, title2\nval1,vla2"
        with TmpFile(file_content) as f:

            file_handler = FileHandler(f.path)

            for _ in range(2):
                # Act
                actual = next(file_handler.read())

                # Assert
                self.assertEqual(expected, actual)


class GtfsCrudTests(unittest.TestCase):
    def test_get_routes(self):
        # Expect
        expected = Route(route_id='1', agency_id='25', route_short_name='1',
                         route_long_name='ת. רכבת יבנה מערב-יבנה<->ת. רכבת יבנה מזרח-יבנה-1#', route_desc='67001-1-#',
                         route_type='3', route_color='')

        # Arrange
        file_content = "route_id,agency_id,route_short_name,route_long_name,route_desc,route_type,route_color\n" \
                       "1,25,1,ת. רכבת יבנה מערב-יבנה<->ת. רכבת יבנה מזרח-יבנה-1#,67001-1-#,3,"
        with TmpFile(file_content) as f:
            routes_file_handler = FileHandler(f.path)

            gtfs = GtfsCrud(routes_file_handler=routes_file_handler,
                            agency_file_handler=None, calendar_file_handler=None, shapes_file_handler=None,
                            stops_file_handler=None, stop_times_file_handler=None, trips_file_handler=None)

            # Act
            actual = next(gtfs.get_routes())

            # Assert
            self.assertEqual(expected.route_type, actual.route_type)
            self.assertEqual(expected.route_short_name, actual.route_short_name)
            self.assertEqual(expected.route_long_name, actual.route_long_name)
            self.assertEqual(expected.route_id, actual.route_id)
            self.assertEqual(expected.route_desc, actual.route_desc)
            self.assertEqual(expected.route_color, actual.route_color)
            self.assertEqual(expected.agency_id, actual.agency_id)

    def test_get_agency(self):

        expected = Agency(agency_id='2', agency_name='רכבת ישראל', agency_url='http://www.rail.co.il',
                          agency_timezone='Asia/Jerusalem', agency_lang='he', agency_phone='', agency_fare_url='')

        file_content = "agency_id,agency_name,agency_url,agency_timezone,agency_lang,agency_phone,agency_fare_url\n" \
                       "2,רכבת ישראל,http://www.rail.co.il,Asia/Jerusalem,he,,"

        with TmpFile(file_content) as a:
            gtfs = GtfsCrud(agency_file_handler=FileHandler(a.path),
                            routes_file_handler=None, calendar_file_handler=None, shapes_file_handler=None,
                            stops_file_handler=None, stop_times_file_handler=None, trips_file_handler=None)

            # Act
            actual = next(gtfs.get_agency())

        self.assertEqual(expected.agency_id, actual.agency_id)
        self.assertEqual(expected.agency_fare_url, actual.agency_fare_url)
        self.assertEqual(expected.agency_lang, actual.agency_lang)
        self.assertEqual(expected.agency_name, actual.agency_name)
        self.assertEqual(expected.agency_phone, actual.agency_phone)
        self.assertEqual(expected.agency_timezone, actual.agency_timezone)
        self.assertEqual(expected.agency_url, actual.agency_url)

    def test_get_calendar(self):
        file_content = "service_id,sunday,monday,tuesday,wednesday,thursday,friday,saturday,start_date,end_date\n" \
                       "1,1,1,1,1,1,0,0,20181231,20190301"
        with TmpFile(file_content) as a:

            gtfs = GtfsCrud(stops_file_handler=None, routes_file_handler=None, agency_file_handler=None,
                            shapes_file_handler=None, calendar_file_handler=FileHandler(a.path),
                            stop_times_file_handler=None, trips_file_handler=None)
            actual = next(gtfs.get_calendar())

            self.assertEqual(1, actual.service_id)
            self.assertEqual(True, actual.sunday)
            self.assertEqual(True, actual.monday)
            self.assertEqual(True, actual.tuesday)
            self.assertEqual(True, actual.wednesday)
            self.assertEqual(True, actual.thursday)
            self.assertEqual(False, actual.friday)
            self.assertEqual(False, actual.saturday)
            self.assertEqual(20181231, actual.start_date)
            self.assertEqual(20190301, actual.end_date)

    def test_get_shapes(self):
        file_content = "shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence\n44505,31.753486,34.988064,1"

        with TmpFile(file_content) as a:

            gtfs = GtfsCrud(routes_file_handler=None, agency_file_handler=None, calendar_file_handler=None,
                            shapes_file_handler=FileHandler(a.path), stops_file_handler=None,
                            stop_times_file_handler=None, trips_file_handler=None)
            actual = next(gtfs.get_shapes())

            self.assertEqual(44505, actual.shape_id)
            self.assertEqual(31.753486, actual.shape_pt_lat)
            self.assertEqual(34.988064, actual.shape_pt_lon)
            self.assertEqual(1, actual.shape_pt_sequence)

    def test_get_stops(self):
        file_content = "stop_id,stop_code,stop_name,stop_desc,stop_lat,stop_lon,location_type,parent_station,zone_id" \
                       "\n1,38831,בי''ס בר לב/בן יהודה, רחוב:בן יהודה 76 עיר: כפר סבא רציף:   קומה:  " \
                       ",32.183939,34.917812,0,,6900"

        with TmpFile(file_content) as a:

            gtfs = GtfsCrud(routes_file_handler=None, agency_file_handler=None, calendar_file_handler=None,
                            shapes_file_handler=None, stops_file_handler=FileHandler(a.path),
                            stop_times_file_handler=None, trips_file_handler=None)
            actual = next(gtfs.get_stops())

            self.assertEqual(1, actual.stop_id)
            self.assertEqual(38831, actual.stop_code)
            self.assertEqual("בי''ס בר לב/בן יהודה", actual.stop_name)
            self.assertEqual(32.183939, actual.stop_lat)
            self.assertEqual(34.917812, actual.stop_lon)
            self.assertEqual(0, actual.location_type)
            self.assertEqual('', actual.parent_station)
            self.assertEqual(6900, actual.zone_id)

    def test_get_stop_times(self):
        file_content = "trip_id,arrival_time,departure_time,stop_id,stop_sequence,pickup_type,drop_off_type," \
                       "shape_dist_traveled\n10021427_020119,00:00:00,00:00:00,36133,1,0,1,0"

        with TmpFile(file_content) as a:

            gtfs = GtfsCrud(routes_file_handler=None, agency_file_handler=None, calendar_file_handler=None,
                            shapes_file_handler=None, stops_file_handler=None,
                            stop_times_file_handler=FileHandler(a.path), trips_file_handler=None)
            actual = next(gtfs.get_stop_times())

            self.assertEqual(36133, actual.stop_id)
            self.assertEqual('00:00:00', actual.arrival_time)
            self.assertEqual('00:00:00', actual.departure_time)
            self.assertEqual(36133, actual.stop_id)
            self.assertEqual(1, actual.stop_sequence)
            self.assertEqual(0, actual.pickup_type)
            self.assertEqual(1, actual.drop_off_type)
            self.assertEqual(0, actual.shape_dist_traveled)

    def test_get_trips(self):
        file_content = "route_id,service_id,trip_id,trip_headsign,direction_id,shape_id" \
                       "\n1,1,30900053_311218,רכבת מזרח/שוק,0,97105"

        with TmpFile(file_content) as a:
            gtfs = GtfsCrud(routes_file_handler=None, agency_file_handler=None, calendar_file_handler=None,
                            shapes_file_handler=None, stops_file_handler=None,
                            stop_times_file_handler=None, trips_file_handler=FileHandler(a.path))
            actual = next(gtfs.get_trips())

            self.assertEqual(1, actual.route_id)
            self.assertEqual(1, actual.service_id)
            self.assertEqual('30900053_311218', actual.trip_id)
            self.assertEqual('רכבת מזרח/שוק', actual.trip_headsign)
            self.assertEqual(0, actual.direction_id)
            self.assertEqual(97105, actual.shape_id)


class ShapeTests(unittest.TestCase):
    def test__csv_header(self):
        expected = 'shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence'
        self.assertEqual(expected, Shape._csv_header)


class StopTests(unittest.TestCase):
    def test__csv_header(self):
        expected = 'stop_id,stop_code,stop_name,stop_desc,stop_lat,stop_lon,location_type,parent_station,zone_id'
        self.assertEqual(expected, Stop._csv_header)


class StopTimeTests(unittest.TestCase):
    def test__csv_header(self):
        expected = "trip_id,arrival_time,departure_time,stop_id,stop_sequence,pickup_type,drop_off_type," \
                   "shape_dist_traveled"
        self.assertEqual(expected, StopTime._csv_header)


class TripTests(unittest.TestCase):
    def test__csv_header(self):
        expected = "route_id,service_id,trip_id,trip_headsign,direction_id,shape_id"
        self.assertEqual(expected, Trip._csv_header)


class RouteTests(unittest.TestCase):
    def test_eq(self):
        my_route = Route(route_id=3, agency_id=4, route_short_name=None, route_long_name=None, route_desc=None,
                         route_type=6, route_color=None)
        same_route = Route(route_id=3, agency_id=5, route_short_name=None, route_long_name=None, route_desc=None,
                           route_type=5, route_color=None)
        diff_route = Route(route_id=5, agency_id=6, route_short_name=None, route_long_name=None, route_desc=None,
                           route_type=4, route_color=None)

        self.assertEqual(my_route, same_route)
        self.assertNotEqual(my_route, diff_route)

    def test__csv_header(self):
        expected = 'route_id,agency_id,route_short_name,route_long_name,route_desc,route_type,route_color'
        self.assertEqual(expected, Route._csv_header)


class AgencyTests(unittest.TestCase):
    def test__csv_header(self):
        expected = 'agency_id,agency_name,agency_url,agency_timezone,agency_lang,agency_phone,agency_fare_url'
        self.assertEqual(expected, Agency._csv_header)


class CalendarTests(unittest.TestCase):
    def test__convert_int_to_date(self):
        actual = Calendar._convert_int_to_date(20000225)

        expected = datetime.datetime(2000, 2, 25, 0, 0)

        self.assertEqual(expected, actual)

    def test__csv_header(self):
        expected = 'service_id,sunday,monday,tuesday,wednesday,thursday,friday,saturday,start_date,end_date'
        self.assertEqual(expected, Calendar._csv_header)

    def test_get_start_date(self):

        calendar = Calendar(service_id=1, start_date=20000225, end_date=20000225)
        actual = calendar.get_start_date()
        expected = datetime.datetime(2000, 2, 25, 0, 0)
        self.assertEqual(expected, actual)

    def test_get_end_date(self):
        calendar = Calendar(service_id=1, start_date=20000225, end_date=20000225)
        actual = calendar.get_end_date()
        expected = datetime.datetime(2000, 2, 25, 0, 0)
        self.assertEqual(expected, actual)


class TmpFile:
    def __init__(self, content):

        self.path = tempfile.NamedTemporaryFile(delete=False).name

        with open(self.path, 'w') as f:
            f.write(content)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.remove(self.path)


if __name__ == '__main__':
    unittest.main()
