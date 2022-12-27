import re
import pandas as pd


def prepare(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s[am\s|pm\s]*-\s'
    messages = re.split(pattern, data)[1:]
    date = re.findall(pattern, data)
    df = pd.DataFrame({'msg': messages, 'dates': date})
    if re.findall('\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s([am\s|pm\s]*)-\s', date[0])[0] == '':
        tfhour = True
    else:
        tfhour = False
    if tfhour == False:
        df["dates"] = pd.to_datetime(df['dates'], format='%d/%m/%Y, %I:%M %p - ')
    else:
        df["dates"] = pd.to_datetime(df['dates'], format='%d/%m/%Y, %H:%M - ')
    users = []
    messages = []
    pat = '([\W\w]+?):\s'
    for message in df['msg']:
        splitted = re.split(pat, message)
        if splitted[
           1:]:  # in case if regex matches, then item at 0th index is empty, item at index 1 is username,the matched string since we used parenthesis and item at index 2 is the message. Also because of the usage of parenthesis in the pattern, we get the matched string in the output of re.split
            users.append(splitted[1])
            messages.append(splitted[2])
        else:  # in case regex doesn't match, then item at 0th index is the message itself.
            users.append('notification')
            messages.append(splitted)

    df['users'] = users
    df['messages'] = messages
    df.drop(columns='msg', inplace=True)

    return df
