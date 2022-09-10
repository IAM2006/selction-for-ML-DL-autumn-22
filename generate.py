import pickle
import argparse
from random import choice
import os

class Model:
    def __init__(self) -> None:
        self.data1 = {}
        self.data2 = {}
        self.keys = []

    def fit(self, text):
        dt1 = {}
        dt2 = {}
        parsed_text = []
        keys1 = set()
        keys2 = set()
        for ln in text:
            ln1 = ln.split()
            for word in ln1:
                new_word = ""
                for i in word:
                    if i.isalpha(): 
                        new_word += i
                if len(new_word) != 0: 
                    new_word = new_word.lower()
                    dt1[new_word] = set()
                    self.data1[new_word] = []
                    if (len(parsed_text) != 0) :
                        self.data2[(parsed_text[-1], new_word)] = []
                        dt2[(parsed_text[-1], new_word)] = set()
                        keys2.add((parsed_text[-1], new_word))
                    parsed_text.append(new_word)
                    keys1.add(new_word)
        for i in range(len(parsed_text) - 1):
            dt1[parsed_text[i]].add(parsed_text[i + 1])
            if (i > 0) :
                dt2[(parsed_text[i - 1], parsed_text[i])].add(parsed_text[i + 1])
        for i in keys1:
            self.keys.append(i)
            for j in dt1[i]:
                self.data1[i].append(j)
        for i in keys2:
            for j in dt2[i]:
                self.data2[i].append(j)

    def generate(self, prefix, ln):
        ans = prefix
        for i in range(ln - len(prefix)):
            try:
                ans.append(choice(self.data2[(ans[-2], ans[-1])]))
            except:
                try:
                    ans.append(choice(self.data1[ans[-1]]))
                except:
                    ans.append(choice(self.keys))
        print(*ans)

if __name__ == "__main__" :
    pr = argparse.ArgumentParser(description="Text generator")
    pr.add_argument('--len', type=int, required=True)
    pr.add_argument('--prefix', nargs='+', type=str)
    group = pr.add_mutually_exclusive_group()
    group.add_argument('--model', action='store_true')
    args = pr.parse_args()
    pref = args.prefix
    pref1 = []
    for word in pref:
        new_word = ""
        for i in word:
            if i.isalpha(): 
                new_word += i
        if new_word != 0: 
            pref1.append(new_word.lower())
    with open("model.pkl", "rb") as f:
        md = pickle.load(f)
    md.generate(pref1, args.len)
    if args.model:
        print(os.path.abspath("model.plk"))
    