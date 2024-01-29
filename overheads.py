from pathlib import Path
import csv

# read the csv file
def readFile():
    fp = Path.cwd()/"csv_reports/Overheads.csv"

    # read the csv file.
    with fp.open(mode="r", encoding="UTF-8", newline="") as file:
        reader = csv.reader(file)
        next(reader) # skip header
        
        oh=[] 

        # append record into the list
        for row in reader:
            # all columns
            oh.append([row[0],row[1]]) 
    return oh

def find_highest(records):
    highest = records[0][-1]
    cat = records[0][0]
    for i in range(1, len(records)):
        if records[i][-1] > highest:
            highest = records[i][-1]
            cat = records[i][0]
    return cat, highest

def output_overhead(cat, highest):
    output = f'[HIGHEST OVERHEAD] {cat.upper()}: {highest}%\n'
    return output


def overhead_function():
    records = readFile()
    cat, highest = find_highest(records)
    output = output_overhead(cat, highest)

    # overwrite the file
    with open('Summary_report.txt', 'w') as f:
        f.write(output)