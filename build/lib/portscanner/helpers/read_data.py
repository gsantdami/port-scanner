import csv 
import os

def read_csv(ports_number=None):
    ports = []
    fp = 'data/top10k.csv'
    filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), fp)
    
    with open(filepath, newline='', encoding='utf-8' ) as csvfile:
        reader = csv.reader(csvfile)
        
        if ports_number > 10000:
            return -1
        
        for row in reader:
            ports.extend([int(port) for port in row])
            if ports_number and len(ports) >= ports_number:
                break
            
    return ports[:ports_number] if ports_number else ports