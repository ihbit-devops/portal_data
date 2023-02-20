import json

doa_v2 = json.load(open('./x-meta-dao_v2.json'))
old = doa_v2['users']

tier_change = []
new_nft = []


with open('./sell_order_balance.csv', 'r') as the_file:
    lines = the_file.readlines()

    for line in lines:
        is_repated = False
        splitted_line = line.split(',')
        email = splitted_line[0].strip()
        balance = float(splitted_line[1].strip())
        
        tier = None

        score = {
            'gold': 1,
            'platinum': 2,
            'purple_gold': 3
        }

        if balance >= 5000000.0:
            tier = 'gold'
            if balance >= 10000000.0:
                tier = 'platinum'
                if balance >= 50000000.0:
                    tier = 'purple_gold'
        

        for old_item in old:
            if old_item['email'] == email:
                is_repated = True
                if score[old_item['tier']] < score[tier]:
                    print(f'Change TIER: {old_item["tier"]} : {tier}')
                    tmp_old = old_item
                    tmp_old['tier'] = tier
                    tmp_old['new-balance'] = balance

                    del tmp_old['new-balance']
                    del tmp_old['balance']

                    tier_change.append(tmp_old)
                else:
                    print(f'NOTHING: {old_item["tier"]} : {tier}')
        

        if not is_repated:
            new_nft.append({
                "address":"",
                "email": email,
                "type":"email",
                "tier": tier
                # "balance": balance
            })



# with open('./x-meta-dao-new-request.json', 'a') as f:
#     f.write(json.dumps({"users": new_nft}))
# print(len(new_nft))

with open('./x-meta-dao-new-tier-change.json', 'a') as f:
    f.write(json.dumps({"users": tier_change}))


# with open('./new_request.csv', 'a') as f:
#     f.write('email,tier,balance\n')

#     for user in new_nft:
#         f.write(f'{user["email"]},{user["tier"]},{user["balance"]}\n')

# with open('./tier_change_request.csv', 'a') as f:
#     f.write('email,tier,balance,new-balance\n')

#     for user in tier_change:
#         print(user)
#         f.write(f'{user["email"]},{user["tier"]},{user["balance"]},{user["new-balance"]}\n')
