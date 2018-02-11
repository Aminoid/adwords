import os, sys, math
import csv, random
from collections import defaultdict

random.seed(0)

def greedy(data, max_bid, queries):
    final = 0.0
    for q in queries:
        q1 = q.strip()

        if len(data[q1]):
            temp = {}
            for k, v in data[q1]:
                #print max_bid[k],
                if max_bid[k] >= v:
                    temp[k] = v
            if len(temp):
                mk = max(temp, key=temp.get)
                #print max_bid[mk], temp[mk],
                max_bid[mk] -= temp[mk]
                final += temp[mk]

    return final

def mssv(data, max_bid, queries):
    final = 0.0
    main = max_bid[:]

    for q in queries:
        q = q.strip()

        if len(data[q]):
            temp = {}
            temp_score = {}
            for k, v in data[q]:
                if max_bid[k] >= v:
                     temp[k] = v
                     temp_score[k] = v * (1 - math.exp(-1 * float(max_bid[k]/main[k])))

            if len(temp):
                mk = max(temp_score, key=temp_score.get)
                max_bid[mk] -= temp[mk]
                final += temp[mk]

    return final

def balance(data, max_bid, queries):            
    final = 0.0

    for q in queries:
        q = q.strip()

        if len(data[q]):
            temp = {}
            temp_score = {}
            for k, v in data[q]:
                if max_bid[k] >= v:
                    temp[k] = v
                    temp_score[k] = max_bid[k]

            if len(temp):
                mk = max(temp_score, key=temp_score.get)
                max_bid[mk] -= temp[mk]
                final += temp[mk]

    return final

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: python adwords.py <greedy|mssv|balance>"
        sys.exit(0)
    
    arg = sys.argv[1]
    total = 0.0

    # Get bidder data

    data = defaultdict(list)
    max_bid = [0]*100
    csvfile = open("bidder_dataset.csv", 'rb')
    dialect = csv.Sniffer().has_header(csvfile.read(1024))
    csvfile.seek(0)
    reader = csv.reader(csvfile, dialect)

    for index, row in enumerate(reader):
        if index != 0:
            if row[3] != '':
                max_bid[int(row[0])] = float(row[3])
            data[row[1]].append((int(row[0]), float(row[2])))

    q = open("queries.txt" , "rb")
    queries = q.readlines()
    if arg == 'greedy':
        for i in range(100):
            temp = max_bid[:]
            total += greedy(data, temp, queries)
            random.shuffle(queries)
        print total/100, total/(100*sum(max_bid))
              
    elif arg == 'mssv':
        for i in range(100):
            temp = max_bid[:]
            total += mssv(data, temp, queries)
            random.shuffle(queries)

        print total/100, total/(100*sum(max_bid))
     
    elif arg == 'balance':
        for i in range(100):
            temp = max_bid[:]
            total += balance(data, temp, queries)
            random.shuffle(queries)

        print total/100, total/(100*sum(max_bid))

    else:
        print "Usage: python adwords.py <greedy|mssv|balance>"
        sys.exit(1)
