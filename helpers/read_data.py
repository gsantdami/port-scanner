import csv 

def read_csv(filepath):
    ports = []
    with open(filepath, newline='', encoding='utf-8' ) as csvfile:
        reader = csv.reader(csvfile)
        
        for row in reader:
            ports.extend([int(port) for port in row])
            
    return ports