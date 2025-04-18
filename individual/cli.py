import argparse
import pandas as pd

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



def main():
    arguments = get_parsed_arguments()
   


    df = pd.read_csv('data/MIAC_data.csv')

    print(df.dtypes)
    for event in arguments.eventName:
        

        if event in df['Event'].values:
            filtered_df = df[df['Event'] == event]
          
            sorted_df = filtered_df.sort_values(by="Time", key=lambda col: col.map(parse_time))
            
            print(event)
            for i in range(10):
                print(i+1, end=": ") 
                print(sorted_df.iloc[i]["Athlete"] + ', ' + sorted_df.iloc[i]["Time"])
                print("*******************************")
        else: 
            print(event + " is an invalid event, please check the csv to see what the properly named events are. Remember to use quotation marks, e,g '100 Meters' ")
            
            
    

if __name__ == '__main__':
    main()