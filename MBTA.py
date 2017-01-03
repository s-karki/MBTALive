import urllib.request
import json
import csv

class MBTALive:

    url_red = "http://developer.mbta.com/Data/Red.json"
    url_orange = "http://developer.mbta.com/Data/Orange.json"
    url_blue = "http://developer.mbta.com/Data/Orange.json"

    def __init__(self):
        ''' Each dictionary is a live feed of trains running
            in the corresponding line
        '''

        self.red_dict = self.process(self.url_red)
        self.orange_dict = self.process(self.url_orange)
        self.blue_dict = self.process(self.url_blue)


    def process(self, url):
        request = urllib.request.urlopen(url)
        response = request.read().decode("utf-8")
        return json.loads(response)

    def next_trains(self, station):

        #generate whole list of trains (and) that pass through station
        line_dict_list = []
        for line in station.lines:
            if line == "Red":
                line_dict_list.extend(self.red_dict)
            elif line == "Blue":
                line_dict_list.extend(self.blue_dict)
            elif line == "Orange":
                line_dict_list.extend(self.orange_dict)

        next_train_list = []

        for platform in station.platforms:
            for train in line_dict_list:
                if train["PlatformKey"] == platform:
                    next_train_list.append([train["Line"],
                                            train["PlatformKey"][len(train["PlatformKey"]) - 1],
                                            train["InformationType"], # train is predicted, arriving, or has arrived
                                            train["Time"],
                                            train["TimeRemaining"]
                                            ])

        return next_train_list
    

class Station:
    def __init__(self, station_name):
        with open("RealTimeHeavyRailKeys.csv", mode="r") as infile:
            read_file = csv.reader(infile)
            self.station_keys = list(read_file)  # station keys correspond to a specific station


        try:
            self.station_name = station_name.upper()
            found_station = False

            for station in self.station_keys:
                if station[3] == self.station_name:
                    found_station = True

            if found_station == False:
                raise ValueError
        except ValueError:
            print("Error: Station Name not part of Red, Blue, or Orange Lines in MBTA System")

        self.is_line_start = self.check_param(self.station_name, 6)
        self.platforms = self.check_param(self.station_name, 1)
        self.lines = self.get_lines(self.platforms)
        self.full_name = self.check_param(self.station_name, 11)

        latitude = self.check_param(self.station_name, 13)
        longitude = self.check_param(self.station_name, 14)
        self.location = [latitude, longitude]

    # Retrieves a parameter from the HeavyKeys CSV file with a column number
    def check_param(self, station_name, index):
        station_code_list = []

        for station in self.station_keys:
            if station[3] == station_name:
                if (index != 1):
                    return station[index]
                else:
                    station_code_list.append(station[index])

        '''the direction of the trains stopping at a station are
            referred to in the station code's last letter.
            Code RHARN refers to the red-line (R), Harvard station,
            and Northbound trains (see next_trains func in class MBTALive.

        '''
        return station_code_list

    def get_lines(self, station_codes):
        lines = []
        for code in station_codes:
            if code[0] == "R":
                this_line = "Red"
            elif code[0] == "B":
                this_line = "Blue"
            else:
                this_line = "Orange"

            if this_line not in lines:
                lines.append(this_line)
        return lines



















