import csv

from gtfs_objs import Route, Agency, Calendar, Shape, Stop, StopTime, Trip


class GtfsCrud:
    def __init__(self, routes_file_handler, agency_file_handler, calendar_file_handler, shapes_file_handler,
                 stops_file_handler, stop_times_file_handler, trips_file_handler):
        self.routes_file_handler = routes_file_handler
        self.agency_file_handler = agency_file_handler
        self.calendar_file_handler = calendar_file_handler
        self.shapes_file_handler = shapes_file_handler
        self.stops_file_handler = stops_file_handler
        self.stop_times_file_handler = stop_times_file_handler
        self.trips_file_handler = trips_file_handler

    @staticmethod
    def _create_generator(gen, callable_mapper):
        for itm in gen:
            yield callable_mapper(*itm)

    def get_routes(self):
        return GtfsCrud._create_generator(self.routes_file_handler.read(), Route)

    def get_agency(self):
        return GtfsCrud._create_generator(self.agency_file_handler.read(), Agency)

    def get_calendar(self):
        return GtfsCrud._create_generator(self.calendar_file_handler.read(), Calendar)

    def get_shapes(self):
        return GtfsCrud._create_generator(self.shapes_file_handler.read(), Shape)

    def get_stops(self):
        return GtfsCrud._create_generator(self.stops_file_handler.read(), Stop)

    def get_stop_times(self):
        return GtfsCrud._create_generator(self.stop_times_file_handler.read(), StopTime)

    def get_trips(self):
        return GtfsCrud._create_generator(self.trips_file_handler.read(), Trip)


class FileHandler:
    def __init__(self, path):
        self.path = path

    def read(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            next(f)
            for row in csv.reader(f):
                yield row


class GtfsManager:
    def __init__(self, gtfs_crud: GtfsCrud):
        self.gtfs_crud = gtfs_crud

    