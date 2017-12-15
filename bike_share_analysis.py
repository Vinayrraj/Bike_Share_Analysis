## import all necessary packages and functions.
import csv # read and write csv files
from datetime import datetime # operations to parse dates
import pprint # use to print data structures like dictionaries in
                          # a nicer way than the base print function.

def print_first_point(filename):
    """
    This function prints and returns the first data point (second row) from
    a csv file that includes a header row.
    """
    # print city name for reference
    city = filename.split('-')[0].split('/')[-1]
    print('\nCity: {}'.format(city))

    with open(filename, 'r') as f_in:
        ## TODO: Use the csv library to set up a DictReader object. ##
        ## see https://docs.python.org/3/library/csv.html           ##
        trip_reader = csv.DictReader(f_in)

        ## TODO: Use a function on the DictReader object to read the     ##
        ## first trip from the data file and store it in a variable.     ##
        ## see https://docs.python.org/3/library/csv.html#reader-objects ##
        first_trip = next(trip_reader)

        ## TODO: Use the pprint library to print the first trip. ##
        ## see https://docs.python.org/3/library/pprint.html     ##
        pp = pprint.PrettyPrinter()
        pp.pprint(first_trip)

    # output city name and first trip for later testing
    return (city, first_trip)

# list of files for each city
data_files = ['/Users/Singh/Documents/PythonWorkspace/Machine Learning/Bike_Share_Analysis/data/NYC-CitiBike-2016.csv',
              '/Users/Singh/Documents/PythonWorkspace/Machine Learning/Bike_Share_Analysis/data/Chicago-Divvy-2016.csv',
              '/Users/Singh/Documents/PythonWorkspace/Machine Learning/Bike_Share_Analysis/data/Washington-CapitalBikeshare-2016.csv',]


# print the first trip from each file, store in dictionary
example_trips = {}
for data_file in data_files:
    city, first_trip = print_first_point(data_file)
    example_trips[city] = first_trip

print("-"*30)

def duration_in_mins(datum, city):
    """
    Takes as input a dictionary containing info about a single trip (datum) and
    its origin city (city) and returns the trip duration in units of minutes.

    Remember that Washington is in terms of milliseconds while Chicago and NYC
    are in terms of seconds.

    HINT: The csv module reads in all of the data as strings, including numeric
    values. You will need a function to convert the strings into an appropriate
    numeric type when making your transformations.
    see https://docs.python.org/3/library/functions.html
    """

    # YOUR CODE HERE
    duration = 0
    if city == "NYC" or city == "Chicago":
        duration = int(datum['tripduration'])/60
    elif city == "Washington":
        duration = int(datum['Duration (ms)'])/(60*1000)
    print(duration)
    return duration


# Some tests to check that your code works. There should be no output if all of
# the assertions pass. The `example_trips` dictionary was obtained from when
# you printed the first trip from each of the original data files.
tests = {'NYC': 13.9833,
         'Chicago': 15.4333,
         'Washington': 7.1231}

for city in tests:
    assert abs(duration_in_mins(example_trips[city], city) - tests[city]) < .001

print("-"*30)

from datetime import datetime
#time.strftime(fmt, d.timetuple())
def time_of_trip(datum, city):
    """
    Takes as input a dictionary containing info about a single trip (datum) and
    its origin city (city) and returns the month, hour, and day of the week in
    which the trip was made.

    Remember that NYC includes seconds, while Washington and Chicago do not.

    HINT: You should use the datetime module to parse the original date
    strings into a format that is useful for extracting the desired information.
    see https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
    """

    # YOUR CODE HERE
    dt = None

    if city == "NYC":
        dt = datetime.strptime(datum['starttime'], "%m/%d/%Y %H:%M:%S")
    elif city == "Chicago":
        dt = datetime.strptime(datum['starttime'], "%m/%d/%Y %H:%M")
    elif city == "Washington":
        dt = datetime.strptime(datum['Start date'], "%m/%d/%Y %H:%M")

    month = dt.strftime("%m")
    hour = dt.strftime("%H")
    day_of_week = dt.strftime("%A")

    return (int(month), int(hour), day_of_week)


# Some tests to check that your code works. There should be no output if all of
# the assertions pass. The `example_trips` dictionary was obtained from when
# you printed the first trip from each of the original data files.
tests = {'NYC': (1, 0, 'Friday'),
         'Chicago': (3, 23, 'Thursday'),
         'Washington': (3, 22, 'Thursday')}

for city in tests:
    #print(time_of_trip(example_trips[city], city))
    #print(tests[city])
    assert time_of_trip(example_trips[city], city) == tests[city]
