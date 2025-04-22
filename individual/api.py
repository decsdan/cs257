#Homework Assignment for Simple Flask Endpoint Design and Implementation
#the structure of this code was copied from flask_sample from Jeff Ondich, for the use in Software Design Spring 2025

import sys
import argparse
import flask
import json
import csv


eventCheck = ['110 Hurdles', '3000 Steeplechase', '55 Hurdles', '55 Meters', 'Weight Throw', '60 Hurdles', '400 Hurdles', 'Pole Vault', '4 x 200 Relay', '4 x 400 Relay', '500 Meters', '60 Meters', 'Decathlon', '600 Meters', 'Event', '3000 Meters', 'Javelin', '1500 Meters', 'Long Jump', '4 x 100 Relay', 'Triple Jump', '10,000 Meters', 'Sprint Medley Relay', 'Shot Put', 'Pentathlon', '400 Meters', 'Distance Medley Relay', 'Hammer', 'Mile', '800 Meters', '5000 Meters', '1000 Meters', '4 x 800 Relay', '200 Meters', 'Heptathlon', 'Shuttle Hurdle Relay', 'High Jump', '100 Meters', '100 Hurdles', '300 Meters', 'Discus']
  
app = flask.Flask(__name__)

def read_csv_file(file_path):
   
    data = []
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data.append(row)
    return data

def parse_time(t):  
    if ':' in t:
     
        minutes, seconds = t.split(':')
        return int(minutes) * 60 + float(seconds)
    else:
        
        return float(t)

data = read_csv_file('data/MIAC_data.csv')

events = set()
dictData = []
for row in data: # adds all stored events to a set for uniqueness, and creates a list of dictionaries where athlete info is stored.
    events.add(row[8])
    tempDict = { 'Year' : row[1], 
                'Meet Date' : row[2],
                'Place' : row[3],
                'Time' : row[4],
                'Meet' : row[5],
                'Wind' : row[6],
                'Athlete' : row[7],
                'Event' : row[8],
                'Athletes' : row[9],
                'Mark' : row[10],
                'Conv' : row[11],
                'School' : row[12],
                'Category' : row[13],
                'Points' : row[14]
        
    }
    dictData.append(tempDict)


@app.route('/')
def hello():
    return flask.render_template('homePage.html')

@app.route('/help')
def get_help():
    return flask.render_template('help.html')

@app.route('/top10/<event_names>')
def getTop10(event_names):
    returnList = []
    

    event_list = event_names.split(',') if event_names else []
    print
    for index, event in enumerate(event_list):
        event = event.replace("_", " ")
        event_list[index] = event
        print(event_list)
    
    for event in event_list: #checks to see if an event is valid
        currList = []
        if event in eventCheck:
            currList.append(event)
            filtered_data = []
            for item in dictData:
                if(item.get("Event") == event):
                    filtered_data.append(item)
            
            filtered_data = sorted(filtered_data, key = lambda x: parse_time(x['Time']))
            athletes = []
            times = []
            for i in range(len(filtered_data)):
                currAth = filtered_data[i].get("Athlete") 
                currTime = filtered_data[i].get("Time")
                if currAth not in athletes: #makes sure that each athlete/time is unique, so multiple PR's from the same person dont countd
                    athletes.append(currAth)
                    times.append(currTime)
                
                
                if len(athletes) > 10:
                    break
            print("Event: " + event)
            for i in range(10):
                n = i + 1
                currList.append(str(n) + ": " + athletes[i] + ', ' + times[i])
                
              

            returnList.append(currList)
        else: 
           
            currList.append(event + " is an invalid event, please check the help to see what the properly named events are. Remember to use an underscore for spaces, e.g 100_Meters' ")
            returnList.append(currList)
            
    
    return returnList   
    



if __name__ == '__main__':
    parser = argparse.ArgumentParser('A sample Flask application/API')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)
