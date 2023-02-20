import json

new_nft = json.load(open('./X-META-NEW-REQUEST-UPDATED.json'))

users = []

# for data in new:
#     is_repeated = False
#     for d2 in old:
#         if data['email'] == d2['email']:
#             is_repeated = True
#             print(f'{data} - {d2}')
    
#     if not is_repeated:
#         users.append(data)

# print(len(users))

# with open('./X-META-NEW.json', 'a') as f:
#     f.write(json.dumps(users))

# users = []
# unique_list = set()

# for data in new_nft:
#     unique_list.add(data['email'])


# for data in new_nft:
#     is_there = False
#     for d1 in users:
#         if data['email'] == d1['email']:
#             is_there = True
    
#     if not is_there:
#         users.append(data)

# print(len(unique_list))
# print(len(users))


# for data in new_nft:
#     if data['tier'] == 'gold':
#         data['tier'] = 'platinum'
    
#     users.append(data)

# print(len(new_nft))

# with open('./X-META-NEW-REQUEST-FINAL.json', 'a') as f:
#     f.write(json.dumps(users))




# platinum - 168
# gold - 121
# purple gold - 13
