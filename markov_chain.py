import argparse, random, os
from whatsapp_data import WhatsappData

class Markov_Chain():

    def __init__(self, source_file, chain_length=2):
        self.whatsapp_data = WhatsappData(source_file)
        self.chain_length = chain_length
        self.markov_chain, self.start = self._build_markov_chain(self.whatsapp_data.msg_list)

    def _build_markov_chain(self, msg_list):
        markov_chain = {}
        start = []

        for msg in msg_list:
            content = msg['content'].split()
            content.append('<eos>')

            for idx in range(len(content) - self.chain_length):
                history = tuple(content[i] for i in range(idx,idx+self.chain_length))

                if idx == 0:
                    start.append(history)

                if not history in markov_chain.keys():
                    markov_chain[history] = [content[idx + self.chain_length]]
                else:
                    markov_chain[history].append(content[idx + self.chain_length])

        return markov_chain, start

    def generate_message(self, max_length=25):
        init_words = random.choice(list(self.start))
        sentence = list(init_words)
        next = random.choice(self.markov_chain[init_words])

        while next != "<eos>" and len(sentence) < max_length:
            if self.chain_length > 1:
                words = sentence[-1*(self.chain_length-1):]
            else:
                words = []
            words.append(next)
            words = tuple(words)
            sentence.append(next)
            next = random.choice(self.markov_chain[words])

        sentence = " ".join(sentence).capitalize()
        print(sentence)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("logfile", help="File path of the Whatsapp text log relative to this script's path",
                        type=str)
    parser.add_argument("n_msgs", help="Number of messages to generate",
                        type=int)
    parser.add_argument("--n", dest="chain_len", help="N-gram size", default=2,
                        type=int)
    args = parser.parse_args()

    markov_chain = Markov_Chain(args.logfile, args.chain_len)
    for idx in range(args.n_msgs):
        markov_chain.generate_message()
