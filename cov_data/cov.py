import time
import requests
import sys

filename = "out.csv"

if len(sys.argv):
    filename = sys.argv[1]

outfile = open(filename, "w")

i = 0

start = time.time()
while True:
    try:
        r = requests.get('http://localhost:80')
        r_split = r.text.split('tr')

        for t in r_split:
            if 'cover' in t:
                t = t.replace('<', '>')
                coverage_rep = t.split('>')[9]
                if int(coverage_rep) != 0:
                    if i == 0:
                        start = time.time()
                    outfile.write(str(int(time.time() - start)) + "\t" + coverage_rep)
                    outfile.write("\n")
                    outfile.flush()
                    print str(i) + ":", coverage_rep
                    i += 1
                break
        time.sleep(1)
    except:
        exit(0)
