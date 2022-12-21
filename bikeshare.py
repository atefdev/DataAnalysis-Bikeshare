import time
import pandas as pd
import numpy as np
import calendar as calendar

# explore US bikeshare data for three Cities (Chicago, New York, washington)


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

cities = ['chicago', 'new york city', 'washington']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("print one of the following Cities to analyze \n(chicago, new york city, washington): ").lower()
        if city in cities:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("which month would you search for ? only available from january to june: ").lower()
        if month in months:
            break
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("print the name of the day to start analyze: ").lower()
    while day not in days:
        day = input("please write the name of day correctly: ")


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Convert the start time colum to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extact month days and hours from start time
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by moth if applicable
    if month != 'all':
        # use the index of the moths list to get the related into
        month = months.index(month) + 1

        # filter by month to create a new dataFrame
        df = df[df['month'] == month]
    # filter by day if applicable
    if day != 'all':
        # filter by day to create a new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    popular_month_name = calendar.month_name[popular_month]

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]

    # display the most common start hour
    popular_start_hour = df['hour'].mode()[0]

    print("the most common month is: ", popular_month_name)
    print("the most common day is: ", popular_day)
    print("the most common hour is: ", popular_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))

    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('most commonly used start station is: {}'.format(popular_start_station))

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("most commonly used end station is: {}".format(popular_end_station))

    # display most frequent combination of start station and end station trip
    comb_station = df['Start Station'] + ' to ' + df['End Station']
    popular_comb_station = comb_station.mode()[0]
    print("the most common trip from start to end station is: ", popular_comb_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time

    travel_time = df['Trip Duration'].sum()
    print("Total travel time: {} seconds".format(travel_time))

    # display mean travel time
    trip_average = df['Trip Duration'].mean()
    print(" mean travel time is {} seconds".format(trip_average))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    type_counts = df['User Type'].value_counts()
    print("\ncounts of user types is: \n",type_counts)

    # Display counts of gender
    try:
        gender_counts = df['Gender'].value_counts()
        print("\ncounts of gender is: \n", gender_counts)
    except:
        print("sorry, no gender data available for this city")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        # for the oldest birth year
        earliest_year = int(df['Birth Year'].min())
        # for the youngest birth year
        most_recent_year = int(df['Birth Year'].max())
        # for common birth Year
        common_year = int(df["Birth Year"].mode())
        print("the earliest year of birth: {}".format(earliest_year))
        print("the most recent year: {}".format(most_recent_year))
        print("the most common year of birth: {}".format(common_year))
    else:
        print("sorry there is no year data available for this city")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def data_preview(df):
    """here the data preview function to show 5 lines for the user"""
    
    # Asking user if he want to preview five lines of raw data
    raw_data = input("\nwould you like to preview 5 rows of trip data? please type 'yes' or 'no'.\n").lower()
    start_line = 0
    while raw_data == 'yes':
        print(df.iloc[start_line:start_line + 5])
        start_line += 5
        raw_data = input("\nwould you like to preview 5 more rows of trip data? please type 'yes' or 'no'\n").lower()
        if raw_data == 'no':
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        data_preview(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
