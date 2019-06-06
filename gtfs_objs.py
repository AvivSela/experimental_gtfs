import datetime
from typing import List


class GtfsItm:

    csv_header = ""

    def get_csv_fields(self):
        raise Exception("Not Implemented Exception")


class Agency(GtfsItm):
    csv_header = 'agency_id,agency_name,agency_url,agency_timezone,agency_lang,agency_phone,agency_fare_url'

    def __init__(self, agency_id, agency_name, agency_url, agency_timezone, agency_lang, agency_phone, agency_fare_url):
        self.agency_id = agency_id
        self.agency_name = agency_name
        self.agency_url = agency_url
        self.agency_timezone = agency_timezone
        self.agency_lang = agency_lang
        self.agency_phone = agency_phone
        self.agency_fare_url = agency_fare_url

    def get_csv_fields(self):

        return [self.agency_id, self.agency_name, self.agency_url, self.agency_timezone, self.agency_lang,
                self.agency_phone, self.agency_fare_url]


class Calendar(GtfsItm):
    csv_header = 'service_id,sunday,monday,tuesday,wednesday,thursday,friday,saturday,start_date,end_date'

    def __init__(self, service_id, sunday=False, monday=False, tuesday=False, wednesday=False,
                 thursday=False, friday=False, saturday=False, start_date=None, end_date=None):
        self.service_id = int(service_id)
        true_values = ('1', True)
        self.sunday = sunday in true_values
        self.monday = monday in true_values
        self.tuesday = tuesday in true_values
        self.wednesday = wednesday in true_values
        self.thursday = thursday in true_values
        self.friday = friday in true_values
        self.saturday = saturday in true_values
        self.start_date = int(start_date)
        self.end_date = int(end_date)

    @staticmethod
    def _convert_int_to_date(int_date):
        return datetime.datetime.strptime(str(int_date), '%Y%m%d')

    def get_start_date(self):
        return Calendar._convert_int_to_date(self.start_date)

    def get_end_date(self):
        return Calendar._convert_int_to_date(self.end_date)


class Route(GtfsItm):
    csv_header = 'route_id,agency_id,route_short_name,route_long_name,route_desc,route_type,route_color'

    def __init__(self, route_id, agency_id, route_short_name, route_long_name, route_desc, route_type, route_color):
        self.route_id = int(route_id)
        self.agency_id = int(agency_id)
        self.route_short_name = route_short_name
        self.route_long_name = route_long_name
        self.route_desc = route_desc
        self.route_type = int(route_type)
        self.route_color = route_color

    def __eq__(self, other):
        return self.route_id == other.route_id

    def __repr__(self):
        return "Route: [route_short_name: {}, route_long_name: {}, route_desc: {}]".format(self.route_short_name,
                                                                                           self.route_long_name,
                                                                                           self.route_desc)


class Shape(GtfsItm):
    csv_header = 'shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence'

    def __init__(self, shape_id, shape_pt_lat, shape_pt_lon, shape_pt_sequence):
        self.shape_id = int(shape_id)
        self.shape_pt_lat = float(shape_pt_lat)
        self.shape_pt_lon = float(shape_pt_lon)
        self.shape_pt_sequence = int(shape_pt_sequence)


class Stop(GtfsItm):
    csv_header = 'stop_id,stop_code,stop_name,stop_desc,stop_lat,stop_lon,location_type,parent_station,zone_id'
    def __init__(self, stop_id, stop_code, stop_name, stop_desc, stop_lat, stop_lon, location_type, parent_station,
                 zone_id):

        self.stop_id = int(stop_id)
        self.stop_code = int(stop_code)
        self.stop_name = stop_name
        self.stop_desc = stop_desc
        self.stop_lat = float(stop_lat)
        self.stop_lon = float(stop_lon)
        self.location_type = int(location_type)
        self.parent_station = parent_station
        self.zone_id = int(zone_id)


class StopTime(GtfsItm):
    csv_header = "trip_id,arrival_time,departure_time,stop_id,stop_sequence,pickup_type,drop_off_type," \
                   "shape_dist_traveled"

    def __init__(self, trip_id, arrival_time, departure_time, stop_id, stop_sequence, pickup_type, drop_off_type,
                 shape_dist_traveled):

        self.trip_id = int(trip_id)
        self.arrival_time = arrival_time
        self.departure_time = departure_time
        self.stop_id = int(stop_id)
        self.stop_sequence = int(stop_sequence)
        self.pickup_type = int(pickup_type)
        self.drop_off_type = int(drop_off_type)
        self.shape_dist_traveled = int(shape_dist_traveled)


class Trip(GtfsItm):
    csv_header = 'route_id,service_id,trip_id,trip_headsign,direction_id,shape_id'

    def __init__(self, route_id, service_id, trip_id, trip_headsign, direction_id, shape_id):
        self.route_id = int(route_id)
        self.service_id = int(service_id)
        self.trip_id = trip_id
        self.trip_headsign = trip_headsign
        self.direction_id = int(direction_id)
        self.shape_id = int(shape_id)


def gtfs_to_csv_file(itms: List[GtfsItm], f):
    import csv
    if len(itms) == 0:
        return
    writer = csv.writer(f)

    itm = next(itms)
    writer.writerow(itm.csv_header)
    writer.writerow(itm.get_csv_fields())

    for itm in itms:
        writer.writerow(itm.get_csv_fields())
