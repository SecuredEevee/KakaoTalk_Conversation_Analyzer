import pandas as pd
data = pd.read_csv('conversation', sep='\t', engine='python', encoding='utf-8')

def parse_user_name(nick_name):
    user_name = nick_name
    if nick_name.find('/') != -1:
        user_name = nick_name.split('/')[0].replace(' ','')
    elif nick_name.find(' ') != -1:
        user_name = nick_name.split(' ')[0]
    return user_name

content_all = []
out_member_list = []
for i in data:
    for j in data[i]:
        # print(j)

        if j[0]!= '2' or j[1] != '0' or j[2] != '2': # skip if not conversation
            continue
        else:
            out_member=''
            if j.find('님') != -1:
                out_member = ' '+j.split('님')[0].split(': ')[1] + ' '
                # out_member = parse_user_name(out_member)
            if j.find('님이 나갔습니다.') != -1 or j.find('님을 내보냈습니다.') != -1:
                # print(j)
                out_member_list.append(out_member)
                continue

            elif j.find('님이 들어왔습니다.') != -1: # if user reenter, remove user from out_member_list
                out_member_list.remove(out_member)
                continue

        content = j.split(',', 2) # ['2020. 11. 30. 19:51', ' ㅎㅇ : 사진']
        try:
            content2 = content[1].split(':', 2) # content2 = [' ㅎㅇ : 사진']
            # content2[0] = parse_user_name(content2[0])
            content_all.append(content[0] + ',' + content2[0] + ',' + content2[1]) # date , name, content

        except Exception as e:

            # print(e, cnt, content,  content2)
            continue

_name = []
_date = []
_content = []
print(out_member_list)
for ii in content_all:
    iii = ii.split(',', 3)
    if iii[1] in out_member_list: # if user not existed, continue
        continue
    _date.append(iii[0])
    _name.append(iii[1])
    _content.append(iii[2])

content_df = pd.DataFrame(data=_date, columns=['data'])
content_df['name'] = _name
content_df['content'] = _content
import pickle
with open("data.pk", "wb") as f:
    pickle.dump(content_df, f)
