import datetime
import geocoder
import requests
import matplotlib.pyplot as plt

ax = plt.gca()

#Get latitude and longitude of user
g = geocoder.ip('me')
location = str(g.lat).strip("[]")+","+str(g.lng).strip("[]") #gets lat and lng then formats them to be how the api expects
print("Location used: "+ str(location)) 


def get_hourlyURL():
    url = "https://api.weather.gov/points/"+location

    try:
        response = requests.get(url)

        if response.status_code == 200:
            posts = response.json()
            properties = posts["properties"] #gets the properties section from posts
            forecastHourlyURL = properties["forecastHourly"] # gets api url for hourly forecast from properties
            return forecastHourlyURL # returns api url to get hourly forecast
        else:
            print('Error:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None

#returns list of hourly tempetures for about the next week
def get_hourly_temps():
    url = get_hourlyURL() #calls the function above this one

    try:
        response = requests.get(url)

        if response.status_code == 200:
            forecast = response.json()
            #print(forecast)
            properties = forecast["properties"]
            periods = properties["periods"]
            periods_len = len(periods)

            temps = [] #init variable to store the
            for key in periods:
                #print(f"Key: {key}") # for debug
                #print(key["temperature"]) #for debug
                temps.append(key["temperature"])                

            return temps 
        else:
            print('Error:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None
    
def get_hourly_humidity():
    url = get_hourlyURL() #calls the function above this one

    try:
        response = requests.get(url)

        if response.status_code == 200:
            forecast = response.json()
            #print(forecast)
            properties = forecast["properties"]
            periods = properties["periods"]
            periods_len = len(periods)

            humidity = [] #init variable to store the
            for key in periods:
                fullData = key["relativeHumidity"]
                humidity.append(fullData["value"])                
            return humidity 
        else:
            print('Error:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None

def get_hourly_rain_chance():
    url = get_hourlyURL() #calls the function above this one

    try:
        response = requests.get(url)

        if response.status_code == 200:
            forecast = response.json()
            #print(forecast)
            properties = forecast["properties"]
            periods = properties["periods"]

            rain_chance = [] #init variable to store the
            for key in periods:
                fullData = key["probabilityOfPrecipitation"]
                rain_chance.append(fullData["value"])                
            return rain_chance 
        else:
            print('Error:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None
    
def get_hourly_wind():
    url = get_hourlyURL() #calls the function above this one

    try:
        response = requests.get(url)

        if response.status_code == 200:
            forecast = response.json()
            #print(forecast)
            properties = forecast["properties"]
            periods = properties["periods"]
            periods_len = len(periods)

            wind_speed = [] #init variable to store the
            for key in periods:
                wind_speed.append(key["windSpeed"])                
            return wind_speed 
        else:
            print('Error:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None

def get_date():
    url = get_hourlyURL() #calls the function above this one

    try:
        response = requests.get(url)

        if response.status_code == 200:
            forecast = response.json()

            properties = forecast["properties"]
            periods = properties["periods"]

            date = [] #init variable to store the
            for key in periods:
                date.append(key["startTime"])                
            return date 
        else:
            print('Error:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None

def get_days():
    url = get_hourlyURL() #calls the function above this one

    try:
        response = requests.get(url)

        if response.status_code == 200:
            forecast = response.json()
            # print(forecast)
            properties = forecast["properties"]
            periods = properties["periods"]
            # periods = properties["periods"]
            # periods_len = len(periods)

            days = [] #init variable to store the
            for key in periods:
                # day_only = datetime.datetime.strptime('2024-09-30T12:00:00-05:00', '%Y, %m, %-d, %H:%M:%S,%H:%M').strftime('%A')
                # day_only = datetime.datetime.strptime(key["startTime"], '%Y-%m-%-dT%-H:%M:%S-%H:%M')
                days.append(key["startTime"])         
            return days 
        else:
            print('Error:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None

#def main():

#actually graph the data
str_day_list = ['Monday','Tuesday','Wendsday','Thursday','Friday','Saturday','Sunday']
# plt.xticks(range(0,12))

#X ticks generation
count = 0
label_count = 0
hourly_temps = get_hourly_temps()
ticks = []
labels = []
for i in hourly_temps:
    count = count + 1
    label_count = label_count + 1
    total = len(hourly_temps)
    # ticks.append(count)
    if label_count <= 24:
        labels.append(label_count)
        ticks.append(count)
    elif label_count > 24:
        label_count = 1
        labels.append(label_count)
        ticks.append(count)

plt.tick_params(axis="x", bottom=True, top=True, labelbottom=True, labeltop=True) # Set ticks on both sides of X axes on

# # [1::2] means start from the second element in the list and get every other element
# for tick in ax.xaxis.get_major_ticks()[1::2]:
#     tick.set_pad(15)

#generate tick hourly marks and labels

count = 0
for tick in ax.xaxis.get_major_ticks(len(hourly_temps)):
    count = count + 1
    if (count % 2) == 0:
        tick.set_pad(20)

plt.xticks(ticks,labels,minor=False,rotation=45,ha='right',fontsize=8,) #draw ticks
# plt.tick_params(axis='x', which='major', labelsize=9)


#idk how this works but it does, Thanks internet :D
N = 250
plt.gca().margins(x=0)
plt.gcf().canvas.draw()
tl = plt.gca().get_xticklabels()
maxsize = max([t.get_window_extent().width for t in tl])
m = 0.2 # inch margin
s = maxsize/plt.gcf().dpi*N+2*m
margin = m/plt.gcf().get_size_inches()[0]

plt.gcf().subplots_adjust(left=margin, right=1.-margin)
plt.gcf().set_size_inches(s, plt.gcf().get_size_inches()[1])

# get_date()

#setup some styling things
plt.style.use('dark_background') #plot style to use

plt.grid(True,'major','both') #add grid to plot

plt.xlabel('Hour of week (working on getting days here too)') #X label

#setup lines
templine = plt.plot(get_hourly_temps(), '#0e4ce8', marker='o') #line for tempeture
humidline = plt.plot(get_hourly_humidity(), '#eb0927', marker='o') #line for humidity
rainline = plt.plot(get_hourly_rain_chance(), '#c509eb', marker='o') # line for chance of rain
#windline = plt.plot(get_hourly_wind(), '#58eb09')
plt.legend(["Temperature (F⁰)", "Humidity (%)", "Chance of Rain (%)", "Average wind speed (mph)"]) # labels for the lines above
plt.show() #open window and show all lines
    

# if __name__ == '__main__':
#     main()
