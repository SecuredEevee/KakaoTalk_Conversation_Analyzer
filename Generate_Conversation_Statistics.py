import pickle
import os
from pprint import pprint

with open('data.pk', 'rb') as f:
    data = pickle.load(f)

data.reset_index(inplace=True, drop=True)
user_list = set(data['name'])
authors = data.groupby('name')
# pprint(authors.groups)
# print(type(authors.groups))
authors_list = {}

for user, index in authors.groups.items():
    user = user.replace('/',' ').split(' ')[1] # parse nick_name from full_name
    if user is '':
        continue
   # print(user)
    # authors_list[user.split('/')[0].replace(' ','')] = list(index)
    authors_list[user]=list(index)

# print(authors_list)

content_count = {}
existed_user = []
if os.path.exists('user.txt'):
    with open('user.txt', 'r', encoding='utf-8') as fp: # open and read previus user
        while True:
            user = fp.readline()
            if not user: break
            existed_user.append(user.replace('\n',''))

for user in authors_list.keys():
    # if user in deleted_user or user is '':
    if user is '':
        continue
    else:
        content_count[user] = len(authors_list[user])

res = sorted(content_count.items(), key=(lambda x:x[1]), reverse=True)
last = 0
last_rank = 0
last_cnt = 0
joint_rank_cnt = 0
for i, content in enumerate(res):
    content = list(content)
    if content[1] == last_cnt:
        print(str(last_rank) +'위', content[0], str(content[1]) + '회')
        joint_rank_cnt+=1
    else:
        last_rank+=joint_rank_cnt+1
        joint_rank_cnt = 0
        last_cnt = content[1]
        print(str(last_rank) +'위 ', content[0], str(content[1])+'회')

    last = last_rank
for user in existed_user:
    if user not in authors_list.keys(): # If there's someone who didn't say a word
        print(str(last+1+joint_rank_cnt)+'위 ', user, '0회')
# print(data['name'][5202])

with open('user.txt','w',encoding='utf-8') as fp: # save user_list to user.txt
    for user in authors_list.keys():
        fp.write(user+'\n')
    for user in existed_user:
        if user not in authors_list.keys():
            fp.write(user+'\n')

