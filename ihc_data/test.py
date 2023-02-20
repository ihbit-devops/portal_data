


with open('./ihc_trade.csv', 'r') as the_file:
    print(the_file.readline())
    lines = the_file.readlines()
    unique_lists = set()
    for line in lines:
        uid = line.split(',')[0].strip()
        unique_lists.add(uid)

    with open('./uids_to.csv', 'a') as the_file:
        for uid in unique_lists:
            the_file.write(f'{uid}\n')
    
