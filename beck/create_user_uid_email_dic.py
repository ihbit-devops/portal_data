import json

dictionary = {}

with open('./email_and_uid.csv', 'r') as the_file:
    the_file.readline()
    lines = the_file.readlines()
    for line in lines:
        splitted_line = line.split(',')
        email = splitted_line[1].strip()
        uid = splitted_line[0].strip()

        dictionary[email] = uid
    
    with open('./uidsWithEmail.json', 'w') as f:
        f.write(json.dumps(dictionary))
