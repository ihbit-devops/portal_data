import json

dictionary = {}
users = []

with open('./data.csv', 'r') as the_file:
    lines = the_file.readlines()

    with open('./ihc_2mil.csv', 'a') as the_file_1:
        for line in lines:
            if '@' in line:
                split_line = line.split(',')
                print(line)
                email = split_line[0]
                balance = float(split_line[1])

                if balance >= 2000000.0 and balance < 5000000.0:
                    the_file_1.write(f'{email},{balance},0,0,0\n')

