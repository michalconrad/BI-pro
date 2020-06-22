# coding: utf-8

# import needed library
import pandas as pd


df1 = pd.read_csv('table_A_conversions.csv')
df2 = pd.read_csv('table_B_attribution.csv')

# table join
# method: full outer join to better see all data and analyse solutions
df = pd.merge(df1, df2, on='Conv_ID', how='outer')


# convert the 'Date' column into datetime
df['Conv_Date'] = pd.to_datetime(df['Conv_Date'])

def date_to_weekday(date_value):
    return date_value.weekday()

# add each day of week
df['DayOfTheWeek'] = df['Conv_Date'].apply(date_to_weekday)

# Monday=0, (...), Sunday=6
df['DayOfTheWeek'] = df['DayOfTheWeek'].map({0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'})

# check the num of rows
if df.shape[0] == df.DayOfTheWeek.count():
    print('Goes on!')
else:
    pass

# add each month
list_months = []
for i in range(df.shape[0]):
    list_months.append(df['Conv_Date'][i].month)

df['Month'] = list_months
df['Month'] = df['Month'].map({1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June', 7:'July', 8:'August', 9:'September', 10:'October', 11:'November',12:'December'})

# re-order the columns in df
df = df[['User_ID', 'Revenue', 'Conv_ID', 'Conv_Date', 'Channel',
       'IHC_Conv', 'DayOfTheWeek', 'Month']]


# Top 10 revenues
top_10 = df.sort_values(by=['Revenue'], ascending=False).head(10)

# number of orders for each day
top_week_day = df['DayOfTheWeek'].value_counts()

# number of orders for each month
top_month = df['Month'].value_counts()

# number of orders for each channel
top_channel = df['Channel'].value_counts()

# number of orders for each client
orders_by_client = df.groupby('User_ID')['Conv_ID'].count().sort_values(ascending=False)

# number of orders for each channel for each day of the week
days = df.DayOfTheWeek.unique()

def sort_by_day(day):
    for i in days:
        return df[df.DayOfTheWeek == i]

# for example Monday
day = sort_by_day('Monday')
day['Channel'].value_counts()

# number of orders for each channel for each month of the year
months = df.Month.unique()

def sort_by_month(month):
    for i in months:
        return df[df.Month == i]

# for example February
month = sort_by_month('February')
month['Channel'].value_counts()

# average revenue
average = df.Revenue.sum() / df.Revenue.count()

# orders larger than average
channel = df[df.Revenue > average].sort_values(by=['Revenue'], ascending=False)

# for particular channel
channel['Channel'].value_counts()

# show each row where 'User_ID' is NaN
nan = df.loc[df['User_ID'].isnull()]

# number of NaN's for each channel
nan['Channel'].value_counts()

# drop all NaN rows for 'User_ID'
drop = df.dropna(subset = ['User_ID'])

# number of orders for each day
top_week_day_nan = df['DayOfTheWeek'].value_counts()

# number of orders for each month
top_month_nan = df['Month'].value_counts()

# number of orders for each channel
top_channel_nan = df['Channel'].value_counts()

# particular channel for each user
uni = df.groupby('User_ID')['Channel'].unique()