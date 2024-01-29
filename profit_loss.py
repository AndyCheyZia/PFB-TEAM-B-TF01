from pathlib import Path
import csv

# read the csv file
def readFile():
    fp = Path.cwd()/"csv_reports/Profit & Loss.csv"

    # read the csv file.
    with fp.open(mode="r", encoding="UTF-8", newline="") as file:
        reader = csv.reader(file)
        next(reader) # skip header
        
        p_l=[] 

        # append record into the list
        for row in reader:
            # all columns
            p_l.append([row[0],row[1], row[2], row[3], row[4]]) 
    return p_l

# find profit difference
def find_difference(records):
    for index in range(len(records)):
        # first record, difference is 0
        if index == 0:
            records[index].append(0)
        else:
            # get current an dprevious row using indexing
            previous_row = records[index-1]
            current_row = records[index]
            # find the difference between cureent row and previous row
            difference = int(current_row[4]) - int(previous_row[4])
            current_row.append(difference)
    return records

# check if increasing, decreasing or fluctuates
def check_trend(records):
    # skip the first day
    profit_difference = []
    for row in records:
        # get profit difference only
        profit_difference.append(row[-1])

    # check if all profit difference is positive
    if all(p > 0 for p in profit_difference):
        state = 'increasing'
    # check if all profit difference is negative
    elif all(p < 0 for p in profit_difference):
        state = 'decreasing'
    # if none of the above condition, profit difference fluctuates
    else:
        state = 'fluctuate'
    
    return state

# for increasing scenario -------------------------------------------------------------------
def highest_increament(records):
    # first row last column, first day profit difference
    highest = records[0][-1]
    # get first day
    day = records[0][0]

    # loop through to find highest profit difference
    for row in records:
        # if this row profit is higher then the current highest one
        if row[-1] > highest:
            # replace current one
            day = row[0]
            highest = row[-1]
    return day, highest

def output_increasing_scenario(records):
    day, highest = highest_decreament(records)
    output = f'\
    [NET PROFIT SURPLUS] NET PROFIT ON EACH DAY IS HIGHER THAN PREVIOUS DAY\n\
    [HIGHEST NET PROFIT SURPLUS] DAY: {day}, AMOUNT: USD{highest}'
    return output


# for decreasing scenario -------------------------------------------------------------------
def highest_decreament(records):
    # first row last column, first day profit difference
    lowest = records[0][-1]

    # loop through to find highest profit difference
    for row in records:
        # if this row profit is higher then the current lowest one
        if row[-1] > lowest:
            # replace current one
            day = row[0]
            lowest = row[-1]
    return day, lowest

def output_decreaing_scenario(records):
    day, lowest = highest_decreament(records)
     # *-1 to remove negative sign
    output = f'\
    [NET PROFIT DEFICIT] NET PROFIT ON EACH DAY IS LOWER THAN PREVIOUS DAY\n\
    [HIGHEST NET PROFIT DEFICIT] DAY {day}, AMOUNT:{lowest*-1}'
    return output

# for fluctuating scenario -------------------------------------------------------------------
def find_deficit(records):
    days = []
    amount = []

    for row in records:
        # if this row profit is higher then the current lowest one
        if row[-1] < 0:
            # replace current one
            days.append(row[0])
            amount.append(row[-1])
    return days, amount

def top3_deficit(days, amount):
    # get sorted index using list comprehension
    amount_index = [amount.index(x) for x in sorted(amount)]
    # and get the top 3 days and amount using the sorted index and list comprehension
    top3_day = [days[i] for i in amount_index[:3]]
    top3_amount = [amount[i] for i in amount_index[:3]]
    return top3_day, top3_amount

def output_fluctuate_scenario(records):
    output = ''
    days, amount = find_deficit(records)
    top3_days, top3_amount = top3_deficit(days, amount)
    for i in range(len(days)):
        output += f'[NET PROFIT DEFICIT] DAY: {days[i]}, AMOUNT: USD{amount[i]*-1}\n'

    if len(days) >= 3:
        number = 3
    else: 
        number = len(days)
    for i in range(number):
        if i == 0:
            order = 'HIGHEST'
        elif i == 1:
            order = '2ND'
        elif i == 2:
            order = '3RD'

         # *-1 to remove negative sign
        output += f'[{order} NET PROFIT DEFICIT] DAY: {top3_days[i]}, AMOUNT: USD{top3_amount[i]*-1}\n'
    return output



# compile -------------------------------------------------------------------------------------
def profitloss_function():
    csv_records = readFile()
    records_with_profit_diff = find_difference(csv_records)
    state = check_trend(records_with_profit_diff)
    if state == 'increasing':
        output = output_increasing_scenario(records_with_profit_diff)
    elif state == 'decreasing':
        output = output_decreaing_scenario(records_with_profit_diff)
    else:
        output = output_fluctuate_scenario(records_with_profit_diff)

    # continue writing on the file
    with open('Summary_report.txt', 'a') as f:
        f.write(output)





