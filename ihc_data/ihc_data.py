import json

dictionary = {}
users = []

with open('./ihc_balance_25.csv', 'r') as the_file:
    lines = the_file.readlines()

    for line in lines:
        is_repeated = False
        splitted_line = line.split(',')
        email = splitted_line[0].strip()
        balance = float(splitted_line[1].strip())

        tier = None

        score = {
            'gold': 1,
            'platinum': 2,
            'purple_gold': 3
        }

        if balance >= 2000000.0:
            tier = 'gold'
            if balance >= 10000000.0:
                tier = 'platinum'
                if balance >= 50000000.0:
                    tier = 'purple_gold'

        if tier is not None:
            
            for index, user in enumerate(users):
                if user['email'] == email:
                    is_repeated = True
                    if score[user['tier']] > score[tier]:
                        print(f'REPEAT: {user["tier"]} : {tier}')
                        user['tier'] = tier
                    else:
                        print(f'No Change: {user["tier"]} : {tier}')
            
            if not is_repeated:
                users.append({
                    "address":"",
                    "email": email,
                    "type":"email",
                    "tier": tier,
                    "balance": balance
                })
        else:
            print('WHAT???---')
            break


with open('./x-meta-dao.json', 'a') as f:
    f.write(json.dumps({"users": users}))


print(len(users))

with open('./sheet_data_2.csv', 'a') as f:
    f.write('email,tier,balance\n')

    for user in users:
        f.write(f'{user["email"]},{user["tier"]},{user["balance"]}\n')
