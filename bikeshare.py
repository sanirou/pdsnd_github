

import time
import pandas as pd  # >=0.24.0 , nlargest Parameter keep set to 'all'
import numpy as np
import json


# Let's define here Some global variables ---

# Three cities names, with their corresponding csv data files
city_data = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# Full month names as we would like to get them from user inputs
months = {
      1 : "January",2 : "February",3 : "March",
      4 : "April",5 : "May", 6 : "June",
      7 : "July", 8 : "August", 9 : "September",
      10 : "October",11 : "November",12 : "December"
    }

# Full week days names as we would like to get them from user inputs
days = {7 : 'Sunday', 1 : 'Monday', 2 : 'Tuesday',3 : 'Wednesday',4 : 'Thursday',5 : 'Friday',6 : 'Saturday'}


#-------------------------------------


def overview(city, month, day, df):
    """
    Recalls and displays the city name and time filters specified by user, as well as 
    the total number of rows in the DataFrame containing the city data.
    
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        (DataFrame) df - Pandas DataFrame containing city data, if applicable filtered by month and/or day
        
    Returns:
        None
    """
    
    # Tests on already formatted values of month name and week day name ('all' = no filter)
    if month == 'all' and day == 'all':
        filter_str = '{0} -- NO TIME FILTER'.format(city.upper())
    elif month != 'all' and day != 'all':
        filter_str = '{0} -- MONTH : {1}, DAY : {2}'.format(city.upper(),month, day)
    elif month != 'all' and day == 'all':
        filter_str = '{0} -- MONTH : {1}'.format(city.upper(),month)
    elif month == 'all' and day != 'all':
        filter_str = '{0} -- DAY : {1}'.format(city.upper(),day)
            
    print()
    print(filter_str)
    print('Total trips : {0}'.format(df.shape[0]))
    print('-'*40)
    

#-------------------------------------


def get_city():
    """
    Prompts user to enter the name of the city to analyse.
    
    Args:
        None
        
    Returns:
        (str) city - well formated name of the city to analyse              
    """
    
    # capture some understandable user inputs for New York, Chicago or Washington
    while True:
        city = input('Would you like to see data for New York, Chicago or Washington? \ncity> ').strip()
        if city.lower() in {'chicago','chicago, il', 'chicago, il.','ch'}:
            city = 'chicago'
            break
        elif city.lower() in {'new york city','new york','ny','nyc','n.y.c'}:
            city = 'new york city'
            break
        elif city.lower() in {'washington','wash','wash.','wa'}:
            city = 'washington'
            break
        else:
            print('\n« {0} » is not a valid city name, try again please!\n'.format(city))
            continue
    
    print("City : {0}\n".format(city.title()))
    
    return city


#-------------------------------------
    

def get_month():
    """
    Prompts user (who wants to filter data by month) to enter a month name or month number.
    
    Args:
        None

    Returns:
        (str) month - well formated name of the month to filter by, or "all" to apply no month filter   
    """

    # inputs we usually get from users for month name or month number. 
    # each understandable user input is matched with the corresponding correct 
    # value expected extracted from 'months' global variable
    month_input_set = {
      "1" : months[1], "01" : months[1], "jan" : months[1], "jan." : months[1], "january" : months[1],
      "2" : months[2], "02" : months[2], "feb" : months[2], "feb." : months[2], "february" : months[2],
      "3" : months[3], "03" : months[3], "mar" : months[3], "mar." : months[3], "march" : months[3],
      "4" : months[4], "04" : months[4], "apr" : months[4], "apr." : months[4], "april" : months[4],
      "5" : months[5], "05" : months[5], "may" : months[5],
      "6" : months[6], "06" : months[6], "jun" : months[6], "jun." : months[6], "june" : months[6]
    }

    # capture some understandable user inputs for month name or month number
    print('')
    while(True):
        try:
            month = input('Which month? Type a month name or month number between January/01 and June/06? \nmonth> ').strip()
            month = month_input_set[month.lower()]
            print('Month : {0}\n'.format(month.title()))
            break
        except KeyError:
            print('\n« {0} » is not an understandable month name or month number between January/01 and June/06, try again please!\n'.format(month))
    return month


#-------------------------------------


def get_day():
    """
    Prompts the user (who wants to filter data by day) to enter a weekday name or weekday number.
    
    Args:
        None

    Returns:
        (str) day - : well formarted name of the day of week to filter by, or "all" to apply no day filter
    """
    
    # inputs we usually get from users for weekday name or weekday number.
    # each understandable user input is matched with the corresponding correct 
    # value expected extracted from 'days' global variable
    day_input_set = {
      '7' : days[7], '07' : days[7],'sunday' : days[7],'sun' : days[7],'sun.' : days[7],
      '1' : days[1], '01' : days[1],'monday' : days[1],'mon' : days[1],'mon.' : days[1],
      '2' : days[2], '02' : days[2],'tuesday' : days[2],'tue' : days[2],'tue.' : days[2],
      '3' : days[3], '03' : days[3],'wednesday' : days[3],'wed' : days[3],'wed.' : days[3],
      '4' : days[4], '04' : days[4],'thursday' : days[4],'thu' : days[4],'thu.' : days[4],
      '5' : days[5], '05' : days[5],'friday' : days[5],'fri' : days[5],'fri.' : days[5],
      '6' : days[6], '06' : days[6],'saturday' : days[6],'sat' : days[6],'sat.' : days[6],
    }
    
    # capture some understandable user inputs for weekday name or weekday number
    print('')
    while(True):
        try:
            day = input('Which day? Type a weekday name or weekday number(1=Monday, ..., 7=Sunday)?\nday> ')
            day = day_input_set[day.lower()]
            print('Day : {0}\n'.format(day.title()))
            break
        except KeyError:
            print('\n« {0} » is not an understandable weekday name or weekday number, try again please!\n'.format(day))
    return day


#-------------------------------------
    

def common_station(df,station_type):
    """
    Displays the most commonly used station(s), 'Start Station' or 'End Station' depending on station_type.
    
    Args:
        (DataFrame) df - Pandas DataFrame containing city data
        'str) station_type - station type ('Start Station' or 'End Station') 
    
    Returns:
        None  
    """
    
    # there could be more than 1 most commonly used stations
    common_station = (
      df[df[station_type].isin(df[station_type].mode().values)]
      .groupby(station_type)
      .agg({'trip_id' : 'count'})
      .reset_index()
      .rename(columns={'trip_id': 'trip_count'}))
    
    print('Most commonly used {0}(s):'.format(station_type.lower()))
    for i in range(common_station.shape[0]):
        print(' > {0} : {1} trips, {2}% of total trips\n'.format(common_station.iloc[i,0], common_station.iloc[i,1], round(common_station.iloc[i,1]*100/df.shape[0],1)))


#-------------------------------------
        

def format_hour(hour):
    """
    Converts an int hour in 24-hour clock format to a string hour in 12-hour clock format format.
    
    Args:
        (int) hour - hour in 24-hour clock format
        
    Returns:
        (str) str_hour - hour in 12-hour clock format    
    """
    
    if hour == 0:
        str_hour = '12 AM'
    elif hour >= 1 and hour <= 11:
        str_hour = '{0} AM'.format(hour)
    elif hour == 12:
        str_hour = '12 PM'
    else:
        str_hour = '{0} PM'.format(hour - 12)
        
    return str_hour


#-------------------------------------


def common_period(df, period):
    """
    Calculates the most frequent month, day or start hour of travel.
    
    Args:
        (DataFrame) df - Pandas DataFrame containing city data
        (str) period - period of travel ('month','day_of_week' or 'hour') 
    
    Returns:
        (str) result - most common month, day or start hour of travel  
    """
    
    # there could be more than 1 most popular month, day or start hour
    common = df[period].mode()
    for i in range(common.shape[0]):
        if i == 0:
            if period == 'month':
                # get well formated month name from 'months' global variable
                result = months[common[i]]
            elif period == 'day_of_week':
                result = common[i]
            elif period == 'hour':
                result = format_hour(common[i])
        else:
            if period == 'month':
                result = '{0}, {1}'.format(result, months[common[i]])
            elif period == 'day_of_week':
                result = '{0}, {1}'.format(result, common[i])
            elif period == 'hour':
                result = '{0}, {1}'.format(result, format_hour(common[i]))
    return result


#-------------------------------------
    

def format_duration(duration_seconds):
    """
    Convert a time duration to a human-readable string.
    
    Args:
        (int) duration_seconds - time duration in seconds
        
    Returns:
        (str) duration_str - time duration as a human-readable string   
    """
    
    # calculate week, day, hour, minute and second parts of the time duration
    minutes, seconds = divmod(duration_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)
    
    # format duration as human-readable string 
    duration_str = ''    
    if weeks > 0:
        duration_str += '{0} week(s)'.format(weeks)
        
    if days > 0:
        if weeks > 0:
            duration_str += ', {0} day(s)'.format(days)
        else:
            duration_str += '{0} day(s)'.format(days)
            
    if hours > 0:
        if weeks > 0 or days > 0:
            duration_str += ', {0} hour(s)'.format(hours)
        else:
            duration_str += '{0} hour(s)'.format(hours)
            
    if minutes > 0:
        if weeks > 0 or days > 0 or hours > 0:
            duration_str += ', {0} min(s)'.format(minutes)
        else:
            duration_str += '{0} min(s)'.format(minutes)
            
    if seconds > 0:
        if weeks > 0 or days > 0 or hours > 0 or minutes > 0:
            duration_str += ', {0} sec(s)'.format(seconds)
        else:
            duration_str += '{0} sec(s)'.format(seconds)
            
    return duration_str


#-------------------------------------
    

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    
    Args:
        None

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    print('\nHello! Let\'s explore some US bikeshare data!\n')    

    # TO DO: get user input for city (chicago, new york city, washington)
    city = get_city()

    # TO DO: get user input for month  and/or day of week 
    while(True):
        time_filter = input('Would you like to filter the data by month, day, both or not at all? Type «month», «day», «both» or «none» \ntime filter> ').strip().lower()
        if time_filter == 'none':
            month = 'all'
            day = 'all'
            break
        elif time_filter == "both":
            month = get_month()
            day = get_day()
            break
        elif time_filter in {'month','m'}:
            month = get_month()
            day = 'all'
            break
        elif time_filter in {'day','d','wd','wdn'}:
            month = 'all'
            day = get_day()
            break
        else:
            print('\n« {0} » is not a understandable answer, try again please!\n'.format(time_filter))
            continue


    print('-'*40)
    return city, month, day


#-------------------------------------
    

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        
    Returns:
        df - Pandas DataFrame containing city data, if applicable filtered by month and/or day
    """

    # get csv file name from the 'city_data' global variable
    # load data into a dataframe
    # rename the unnamed first column 
    # format datetime columns
    # add 'month', 'day_of_week' and 'hour' columns to the DataFrame
    df = (
      pd.read_csv(city_data[city],parse_dates=['Start Time','End Time'])
        .rename(columns = {'Unnamed: 0' : 'trip_id'})
        .assign(month = lambda x : x['Start Time'].dt.month,
                day_of_week = lambda x : x['Start Time'].dt.strftime('%A'),
                hour = lambda x : x['Start Time'].dt.hour))

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        six_first_months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = six_first_months.index(month.lower()) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]


    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


#-------------------------------------


def time_stats(df):
    """
    Displays statistics on the most frequent month, day or start hour of travel.
    
    Arg:
        (DataFrame) df - Pandas DataFrame containing city data
    
    Returns:
        None    
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print('Most common month(s) for start time: {0}'.format(common_period(df = df, period = 'month')))

    # TO DO: display the most common day of week
    print('Most common day(s) of week for start time: {0}'.format(common_period(df = df, period = 'day_of_week')))

    # TO DO: display the most common start hour
    print('Most common hours(s) of the day for start time: {0}'.format(common_period(df = df, period = 'hour')))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


#-------------------------------------
    

def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
    
    Args:
        (DataFrame) df - Pandas DataFrame containing city data

    Returns:
        None
    """

    print('\nCalculating The Most Popular Stations and Trip(s)...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_station(df = df, station_type = 'Start Station')


    # TO DO: display most commonly used end station
    common_station(df = df, station_type = 'End Station')


    # TO DO: display most frequent combination of start station and end station trip
    # there could be more than 1 most popular trip
    common_trip = (
      df[['Start Station','End Station']]
      .groupby(['Start Station','End Station'])
      .size()
      .nlargest(keep = 'all', n = 1)
      .reset_index()
      .rename(columns = {0:'trip_count'})
      .assign(trip = lambda x : '«' + x['Start Station'] + '»   to   «' + x['End Station'] + '»'))
    
    print('Most popular trip(s), from start to end:')
    for i in range(common_trip.shape[0]):
        print(' > {0} : {1} trips, {2}% of total trips'.format(common_trip.iloc[i,3], common_trip.iloc[i,2], round(common_trip.iloc[i,2]*100/df.shape[0],1)))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


#-------------------------------------


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.
    
    Args:
        (DataFrame) df - Pandas DataFrame containing city data
    
    Returns:
        None     
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_duration_sec = int(round(df['Trip Duration'].sum(),0))
    print('Total trip duration: {0}'.format(format_duration(total_duration_sec)))  
    

    # TO DO: display mean travel time
    average_duration_sec = int(round(df['Trip Duration'].mean(),0))
    print('Average trip duration: {0}'.format(format_duration(average_duration_sec)))   


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


#-------------------------------------


def user_stats(df):
    """
    Displays statistics on bikeshare users.
    
    Args:
        (DataFrame) df - Pandas DataFrame containing city data
    
    Returns:
        None 
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    # we would like to see stats on undefined 'User Type'
    df['User Type'].fillna('Undefined',inplace = True)
    user_types = df['User Type'].value_counts()
    print('What is the breakdown of users? ')
    for i in range(user_types.shape[0]):
        print('{0:<12}: {1:<10}{2}%'.format(user_types.index[i], user_types[i], round(user_types[i]*100/df.shape[0],1)))
    print('')


    # TO DO: Display counts of gender
    # if 'Gender" information is avaiblable
    if 'Gender' in df.columns:        
        gender = df.replace({"Gender" : np.nan},"Undefined")['Gender'].value_counts()
        print('What is the breakdown of gender? ')
        for i in range(gender.shape[0]):
            print('{0:<10}: {1:<10}{2}%'.format(gender.index[i], gender[i], round(gender[i]*100/df.shape[0],1)))
        print('')


    # TO DO: Display earliest, most recent, and most common year of birth
    # we would like to see stats on undefined 'Birth Year'
    # if 'Birth Year" information is avaiblable
    if 'Birth Year' in df.columns:
        print('Birth year')
        
        print('{0:<12}: {1:<20}'.format('Eartliest', int(df['Birth Year'].min())))
        
        print('{0:<12}: {1:<20}'.format('Most recent', int(df['Birth Year'].max())))
        
        # We should think about a list since there could be more than 1 most common birth years
        tmp_common_birth_year = df['Birth Year'].mode()
        for i in range(tmp_common_birth_year.shape[0]):
            if i == 0:
                common_birth_year = '{0}'.format(int(tmp_common_birth_year[i]))
            else:
                common_birth_year = '{0}, {1}'.format(common_birth_year, int(tmp_common_birth_year[i]))
        print('{0:<12}: {1:<20}'.format('Most common', common_birth_year))
        print('')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


#-------------------------------------
    

def raw_data_chunker(df, chunk_size = 5):
    """
    Generator function, that takes in a DataFrame and yields a chunk of a specified size at a time.
    
    Args:
        (DataFrame) df - Pandas DataFrame containing city data
        (int) chunk_size - size of the chunk to display at a time
    
    Returns:
        None   
    """
    for i in range(0, df.shape[0], chunk_size):
        yield df[i:i + chunk_size]


#-------------------------------------
        

def print_raw_data(df):
    """
    Print raw data that's have been analyszed.
    
    Args:
        (DataFrame) df - Pandas DataFrame containing city data

    Returns:
        None   
    """  
    
    print_raw_data = input('\nWould you like to see raw data?\nyes/no> ').strip().lower()
    if print_raw_data in {'yes','y'}:            
        page = 1
        # drop some columns we dont want to display
        df.drop(['month','hour','day_of_week'],axis = 1, inplace=True)
        # display chunc as json
        for chunk in raw_data_chunker(df = df):
            parsed = chunk.to_json(orient='records', date_format = "iso")
            parsed = json.loads(parsed)
            print('\n+' + '-'*20 + ' page ' + str(page) + '\n')
            print(json.dumps(parsed, indent=2))
            print('')
            
            while True:
                print_more = input('Would you like to see more data?\nyes/no> ').strip().lower()    
                if print_more in {'yes','y','no','n'}:
                    break
                else:
                    continue
            
            if print_more in {'yes','y'}:
                page += 1
                continue
            elif print_more in {'no','n'}:
                print('\n+' + '-'*40 + '\n')
                break
    else:
        print('Well, you do not want to display raw data.')
   


#-------------------------------------
        

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)        
        overview(df = df, city = city, month = month, day = day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        print_raw_data(df = df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

#-------------------------------------
            
if __name__ == "__main__":
	main()
    #pass



#-------------------------------------