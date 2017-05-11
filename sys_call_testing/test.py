import sys
import re


def main():
    flag = int(sys.argv[1])
    if flag == 1:
        datafile = open(sys.argv[2], "r")
        syscount_process(datafile)
    elif flag == 2:
        datafile = open(sys.argv[2], "r")
        strace_process(datafile)
    elif flag == 3:
        combine_sets(sys.argv[2:])
    else:
        print("Please use a proper flag value of 1, 2, or 3")

def syscount_process(datafile):
    call_list, total = syscount_array(datafile)
    call_list = list(reversed(call_list))
    print_sorted_list(call_list, total)

def strace_process(datafile):
    call_map, total = strace_to_hash(datafile)
    call_list = hash_to_sorted_list(call_map)
    print_sorted_list(call_list, total)

def combine_sets(args):
    call_map, total = extract_calls(args)
    call_list = hash_to_sorted_list(call_map)
    print_sorted_list(call_list, total)

def extract_calls(file_names):
    call_map = {}
    total = 0
    for x in file_names:
        f = open(x, "r")
        for i in xrange(2):
            f.next()
        for line in f:
            call, count = extract_line_information(line)
            if call != None:
                total = total + count
                if call in call_map:
                    call_map[call] += count
                else:
                    call_map[call] = count
            else:
                next
    return call_map, total

def syscount_array(datafile):
    call_list = []
    total = 0
    for i in xrange(2):
        datafile.next()
    for line in datafile:
        try:
            call, count = extract_line_information(line)
            total = total + count
            print(call + " " + count)
            call_list.append((call, count)) if call != None else next
        except:
            print("Error processing: %s" % (line))
    return call_list, total

def extract_line_information(line):
    result = re.sub(' +',' ', line).strip()
    call = result.split(" ")[0]
    try:
        count = int(result.split(" ")[1])
    except:
        return None, None
    return call, count

def strace_to_hash(datafile):
    call_map = {}
    total = 0
    for line in datafile:
        call = line.split("(")[0]
        total = total + 1

        if line.find('SIGCHLD')!= -1:
            call = 'signal'

        if call not in call_map:
            call_map[call] = 1
        else:
            call_map[call] = call_map[call] + 1
    return call_map, total


def hash_to_sorted_list(call_map):
    call_list = []
    for key in call_map:
        call_list.append((key, call_map[key]))
    return sorted(call_list, key=lambda tup: tup[1], reverse=True)

def print_sorted_list(call_list, total):
    formatted_line = '{:>20}  {:>20}  {:>20}'.format("Call", "Number of calls made", "Percentage of total calls")
    print formatted_line
    for call, value in call_list:
        percentage = (value/float(total)) * 100
        formatted_line = '{:>20}  {:>20}  {:>20}'.format(call, value, percentage)
        print formatted_line

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Shutting Down')
        sys.exit(0)
