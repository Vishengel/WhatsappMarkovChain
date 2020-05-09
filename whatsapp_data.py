import datetime, re, string
from collections import Counter

class WhatsappData():

    def __init__(self, source_file):
        self.ignore_list = ['media weggelaten', '']
        self.msg_list = self.read_from_history(source_file)

    def datetime_from_timestamp(self, timestamp):
        day = int(timestamp[:2])
        month = int(timestamp[3:5])
        year = int("20" + timestamp[6:8])
        hour = int(timestamp[9:11])
        min = int(timestamp[12:14])

        return datetime.datetime(year, month, day, hour, min)


    def read_from_history(self, source_file):
        msg_list = []
        re_datetime = "([\d]{2}[-]){2}[\d]{2}[\s][\d]{2}[:][\d]{2}"
        re_sender = "[:][\s]"

        with open(source_file, encoding='utf-8') as f:
            for line in f:
                if not re.search(re_datetime, line):
                    msg_list[1]['content'] += line.lower().strip('\n')
                    continue

                msg = {}

                msg['timestamp'] = self.datetime_from_timestamp(line[:14])
                remainder = line[17:]

                split = re.split(re_sender, remainder)

                if len(split) == 1:
                    continue

                msg['sender'] = split[0].lower()
                msg['content'] = split[1].lower().strip('\n').translate(str.maketrans('', '', string.punctuation))

                if not msg['content'] in self.ignore_list:
                    msg_list.append(msg)

        return msg_list

    def get_att_frequency(self, att_name):
        return Counter([x[att_name] for x in self.msg_list])

    def get_bow(self):
        all_msgs = [x['content'] for x in self.msg_list]
        words = []
        for msg in all_msgs:
            words.extend(msg.split(" "))

        return Counter(words)