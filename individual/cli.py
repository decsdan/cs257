import argparse
import csv
import pprint
#cli.py, Daniel Scheider, 4/17/2025 - 
# NAME: cli.py
# SYNOPSIS: python3 cli.py topAthletes byEvent
# DESCRIPTION: Shows a list of the top 10 athletes by event chosen.


 
 
def get_parsed_arguments():
    parser = argparse.ArgumentParser(prog = 'cli.py ',
                                     
                                     description='NAME: cli.py - command-line interface exercise SYNOPSIS: list the events you want to see the top 10 athletes and their times',
    epilog="DESCRIPTION: Shows a list of the top 10 times and athletes for the events chosen. Some athletes have multiple top 10 times.",
    
    )
    
    parser.add_argument('eventName', metavar='event', nargs='+', help='one or more events you want to see the top 10 runners of')
    
    parsed_arguments = parser.parse_args() 
    
    return parsed_arguments



def parse_time(t):  
    if ':' in t:
     
        minutes, seconds = t.split(':')
        return int(minutes) * 60 + float(seconds)
    else:
        
        return float(t)



def read_csv_file(file_path):
   
    data = []
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data.append(row)
    return data




def main():
    arguments = get_parsed_arguments()
   

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
    
    
    
    del(dictData[0]) #deletes column name row

    
    for event in arguments.eventName: #checks to see if an event is valid
        if event in events:
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
                
                print(i+1, end=": ") 
                print(athletes[i] + ', ' + times[i])
                print("*******************************")
        else: 
            print(event + " is an invalid event, please check the csv to see what the properly named events are. Remember to use quotation marks, e,g '100 Meters' ")
       
  
    
if __name__ == '__main__':
    main()