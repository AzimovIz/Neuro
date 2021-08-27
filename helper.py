import os
import re
import emoji

from bs4 import BeautifulSoup

#clean = lambda x: x.split('<div>')[1].replace('<div class="kludges">', '').replace('<br/>', ' ')
def clean(x):
    try:
        pre = x.split('<div>')[1].replace('<div class="kludges">', '').replace('<br/>', ' ')
    except:
        print(f'exc: {x}')
        pre = '' #\U0001f914
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E6-\U0001F1FF"  # flags
                               u"\U0001F600-\U0001F64F"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U0001F1F2"
                               u"\U0001F1F4"
                               u"\U0001F620"
                               u"\u200d"
                               u"\u2640-\u2642"
                               u"\xbe"
                               u"\u0301"
                               "]+", flags=re.UNICODE)
    pre = emoji_pattern.sub(r'', pre)
    pre = re.sub(emoji.get_emoji_regexp(), r"", pre)
    pre = pre.encode().decode('utf-8')
    if ('div' in pre) or ('http' in pre):
        return ''
    else:
        return pre

def f():
    for dir in os.listdir('message/'):
        print(f'{dir}-------------------------------------')
        for file in os.listdir(f'message/{dir}'):
            print(f'\n\n\n\n{file}')
            file_ = open(f'message/{dir}/{file}', 'r')
            soup = BeautifulSoup(file_, features="lxml")
            item = soup.find_all('div', {'class': 'message'})
            #print(str(item).split('</div></div>\n</div>')[1])
            ms = str(item).split('</div></div>\n</div>')
            i = 0
            mss = ''
            for j in range(len(ms)-1):
                #print('\n')
                #print(f'i+2={i+2}   len(ms)-1:{len(ms)-1}')
                if i+2 > len(ms)-1:
                    break
                if 'href' in ms[i]:
                    mss = mss + '\nP1 ' + clean(ms[i])
                    #print('P1: ')
                    #print(clean(ms[i]))
                    while 'href' in ms[i+1]:
                        mss = mss + ' ' + clean(ms[i+1])
                        #print(clean(ms[i+1]))
                        #print(i)
                        i += 1
                        if i + 2 > len(ms) - 1:
                            break
                else:
                    mss = mss + '\nP0 ' + clean(ms[i])
                    #print('P0: ')
                    #print(clean(ms[i]))
                    try:
                        while 'href' not in ms[i + 1]:
                            mss = mss + ' ' + clean(ms[i + 1])
                            #print(f'i={i}   len(ms):{len(ms)}')
                            #print(clean(ms[i+1]))
                            #print(i)
                            i += 1
                            if i + 2 > len(ms) - 1:
                                break
                    except:
                        print(f'err! i+1:{i+1}  len(ms):{len(ms)}')
                        return
                i +=1
            print(mss)
            with open(f'messages/{dir}.txt', 'w') as fil:
                fil.write(mss)


f()