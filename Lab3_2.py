from math import radians, cos, sin, asin, sqrt
from collections import defaultdict
import csv
import sys
import unittest

def Distance(lon1, lat1, lon2, lat2): #This function calculates the distance using the Haversine formula
   dlon = lon2 - lon1 ;dlat = lat2 - lat1 
   a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
   c = 2 * asin(sqrt(a))* 6371 #In Kilometers
   return c;

def LocationFinder():
    with open('GeoLiteCity-Location.csv', 'r') as csvfile: #Reading file in read mode
        reader = csv.DictReader(csvfile)    # read the file as a dictionary for each row ({header : value})
        name1 =[]; #For storing the names of all nearby cities and ensuring we do not get duplicate results for distance(several duplicate entries in csv file) 
        lon1=0;lat1=0; mapStore = defaultdict(list); name = []
        Limit = 0; #For keeping a limit on how many cities in the vicinity of our city are printed
        count = 0; #A temp variable for keeping track of iterations and ensuring they are less than the limit
        reader.fieldnames = 'locId', 'country', 'region', 'city', 'postalCode', 'latitude', 'longitude', 'metroCode', 'areaCode' #Adding filednames to distinguish columns
        for row in reader:
            if(row['city']!="" and row['city']!= 'None' and row['city']!= 'city'):
                if not mapStore[row['city']]:
                    name.append(row['city']); 
                    mapStore[row['city']].append(row['latitude']); mapStore[row['city']].append(row['longitude']) #Each map has a city name as its key 
        choice = int(raw_input('Enter 1 for searching by latitude/longitude; Enter 2 for searching by name: '))

        if(choice !=1 and choice !=2): #To exit the program if user enters illegal option
               print "Illegal value entered, exiting!"

        if(choice == 1): #Search by entering Latitude and Longitude
            city = 'city'
            lat1 = float(raw_input('Enter latitude: ')) #Taking input in float
            lon1 = float(raw_input('Enter longitude: '))
            lon1,lat1 = map(radians, [lon1, lat1])#The latitudes and longitudes are converted to radians here
        
        if(choice == 2):
           city = raw_input('Enter the name of the city you wish to search: ')#Takes user input of the city name
           if mapStore[city]: #Here we check if the city exists and then store its latitude and longitude in a variable 
               lat1 = float(mapStore[city][0])
               lon1 = float(mapStore[city][1])
               lon1,lat1 = map(radians, [lon1, lat1])#The latitudes and longitudes are converted to radians here
         
        if(choice == 1 or choice == 2):
           Limit = int(raw_input('Enter a limit on the number of nearby cities you wish to see: '))#Takes user input of the city name
           for i in name:
               if mapStore[i] and mapStore[i] != city and mapStore[i][0]: #To ensure we do not compute the great circle distance for the city itself as well
                   lat2 = float(mapStore[i][0]);lon2 = float(mapStore[i][1])
                   lon2, lat2 = map(radians, [lon2, lat2])
                   c = Distance(lon1, lat1, lon2, lat2) #In Kilometers
                   if(c < 1000 and (row['city'] not in name1) and count < Limit): #Limit on nearby cities shown is 4
                       count+=1
                       name1.append(i) #To keep track of all entries already covered
                       print "Distance from ",i," is: ", c



class cityTester(unittest.TestCase):

    def testOne(self): #TestOne checks if the function that computes Haversine formula is working correctly
       x = Distance(-1.28427085948,0.794124809657, -1.24354709205,0.816814089933) #Here we are sending the distances in Radians to the concerned function
       lon1= -1.28427085948;lat1=0.794124809657; lon2 = -1.24354709205; lat2 = 0.816814089933;
       dlon = lon2 - lon1 ;dlat = lat2 - lat1 
       a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
       c = 2 * asin(sqrt(a))* 6371 #In Kilometers
       self.assertEqual(x,c) #Here we check whether the result we calculated at the unit test and the result from the distance function match

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(cityTester)#Code to automatically execute a unit test at startup
    unittest.TextTestRunner(verbosity=2).run(suite)
    LocationFinder()
                 
        
