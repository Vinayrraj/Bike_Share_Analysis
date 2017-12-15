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

print("-"*30)

def type_of_user(datum, city):
    """
    Takes as input a dictionary containing info about a single trip (datum) and
    its origin city (city) and returns the type of system user that made the
    trip.

    Remember that Washington has different category names compared to Chicago
    and NYC.
    """

    # YOUR CODE HERE
    user_type = None
    if city == "NYC" or city == "Chicago":
        user_type = datum['usertype']
    elif city == "Washington":
        user_type = datum['Member Type']
        if user_type == "Registered":
            user_type = "Subscriber"
        else:
             user_type = "Customer"

    return user_type


# Some tests to check that your code works. There should be no output if all of
# the assertions pass. The `example_trips` dictionary was obtained from when
# you printed the first trip from each of the original data files.
tests = {'NYC': 'Customer',
         'Chicago': 'Subscriber',
         'Washington': 'Subscriber'}

for city in tests:
    assert type_of_user(example_trips[city], city) == tests[city]


print("-"*30)

def condense_data(in_file, out_file, city):
    """
    This function takes full data from the specified input file
    and writes the condensed data to a specified output file. The city
    argument determines how the input file will be parsed.

    HINT: See the cell below to see how the arguments are structured!
    """

    with open(out_file, 'w') as f_out, open(in_file, 'r') as f_in:
        # set up csv DictWriter object - writer requires column names for the
        # first row as the "fieldnames" argument
        out_colnames = ['duration', 'month', 'hour', 'day_of_week', 'user_type']
        trip_writer = csv.DictWriter(f_out, fieldnames = out_colnames)
        trip_writer.writeheader()

        ## TODO: set up csv DictReader object ##
        trip_reader = csv.DictReader(f_in)

        # collect data from and process each row
        for row in trip_reader:
            # set up a dictionary to hold the values for the cleaned and trimmed
            # data point
            new_point = {}

            ## TODO: use the helper functions to get the cleaned data from  ##
            ## the original data dictionaries.                              ##
            ## Note that the keys for the new_point dictionary should match ##
            ## the column names set in the DictWriter object above.         ##
            new_point['duration'] = duration_in_mins(row, city)
            new_point['month'], new_point['hour'], new_point['day_of_week'] = time_of_trip(row, city)
            new_point['user_type'] = type_of_user(row, city)


            ## TODO: write the processed information to the output file.     ##
            ## see https://docs.python.org/3/library/csv.html#writer-objects ##
            trip_writer.writerow(new_point)


print("-"*30)

# Run this cell to check your work
city_info = {'Washington': {'in_file': '/Users/Singh/Documents/PythonWorkspace/Machine Learning/Bike_Share_Analysis/data/Washington-CapitalBikeshare-2016.csv',
                            'out_file': '/Users/Singh/Documents/PythonWorkspace/Machine Learning/Bike_Share_Analysis/data/Washington-2016-Summary.csv'},
             'Chicago': {'in_file': '/Users/Singh/Documents/PythonWorkspace/Machine Learning/Bike_Share_Analysis/data/Chicago-Divvy-2016.csv',
                         'out_file': '/Users/Singh/Documents/PythonWorkspace/Machine Learning/Bike_Share_Analysis/data/Chicago-2016-Summary.csv'},
             'NYC': {'in_file': '/Users/Singh/Documents/PythonWorkspace/Machine Learning/Bike_Share_Analysis/data/NYC-CitiBike-2016.csv',
                     'out_file': '/Users/Singh/Documents/PythonWorkspace/Machine Learning/Bike_Share_Analysis/data/NYC-2016-Summary.csv'}}

for city, filenames in city_info.items():
    condense_data(filenames['in_file'], filenames['out_file'], city)
    print_first_point(filenames['out_file'])
