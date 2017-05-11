# mod_syzkaller

Written by Scott, Jacob and Zach

## About
This repository is the compilation two tools and a copy of the syzkaller code base. The two tools were used to collect results to be used in measuring and improving syzkaller, a linux kernel fuzzer. The code for syzkaller can be found here: https://github.com/google/syzkaller. This is also were you can find proper credit for the tools creation and it's license.

## cov_data
In this directory is the tool we used for collecting coverage data of our fuzzer. The way it works is it hits localhost address, where the syzkaller coverage data is available, every second, parsing the coverage data and saving it. At the end of data collection the results are saved to CSV. The results from our experiment are saved in the results folder embedded in this one. These results can easily be uploaded to any program for processing and graphing.

The program to collect data is called cov.py, it must be run in parallel with syzkaller.

## sys_call_testing
test.py is a program with three functions:

First, it can parse output from syscount. syscount is an opensource tool available here: https://github.com/brendangregg/perf-tools/blob/master/syscount as part of perf-tools, it runs as a background process on a linux machine collecting the system calls made. The output of syscount is processed by our program, which takes the system calls made and ranks them based on how many times they were called and also adds in the percentage of times a call was made out of all the system calls made. usage: `python test.py 1 syscount_output.txt`, tou can pipe the results to file like `python test.py 1 syscount_output.txt > output.txt`

Second, it parses output from strace. Strace is a linux program that can be used to log the system calls made by a single program. For our experiments we ran `strace -o output.txt <program_name>`. The logs from strace can be parsed by the `test.py` program and counts of system calls and their percentage of time called relative to other system calls are calculated. Usage: `python test.py 2 strace_output.txt` and you can pipe output like `python test.py 2 strace_output.txt > output-with percentages.txt`

Note, the result from running `test.py` on strace or syscount output is the same structured system call information. e.g.
`System call  |  Times Called  |  Percentage of times called`

Third, it can be used to combine the piped output from the first and second process described above. Usage: `python test.py 2 output1.txt output2.txt`

General Usage:
`python test.py <flag_num> <file_name>`

Note for `flag=3` you can supply multiple files

Result Files:
The `result` folder contains results from different trials, each subdirectory within this directory is descriptive of what was used for testing, e.g. the bash folder has results from seeing what system calls were made during a bash session. For the syscount folder we used the syscount program, and the data was collected in respective scenarios as described in the file names. Any file with total in it is the conglomeration of totals for that type of test using the third process described above. Also files with `percentage` in the total are the result of running the logs through our `test.py` program, any file without `percentage` in the filename is a log file. Note for the server test we used a simple flask server, the code for which can be found here: http://flask.pocoo.org/docs/0.12/quickstart/

## syzkaller
In this folder is syzkaller along with our modifications. Our modifications allow for direct changes in the priorities of system calls, through the config file.

The changes we made can be found in the following locations:

https://github.com/zwanthor/mod_syzkaller/blob/master/syzkaller/config/config.go#L72
we added `Weight_Syscalls` and `Weight`

https://github.com/zwanthor/mod_syzkaller/blob/master/syzkaller/prog/prio.go#L29
https://github.com/zwanthor/mod_syzkaller/blob/master/syzkaller/prog/prio.go#L40
The changes we made to the calculate prioties functions to take in the variables for system calls and their change in priority values are found at the above location

https://github.com/zwanthor/mod_syzkaller/blob/master/syzkaller/prog/prio.go#L45
At this location is where we added a loop to adjust the weight/priorities for the specified system calls in the config.

https://github.com/zwanthor/mod_syzkaller/blob/master/syzkaller/syz-manager/manager.go#L700
This is where we supply the priorities specified in the config to the priotities functions used during the fuzzing process.

### Example
Check out `my.cfg` to see an example of supplying modified priorities to specific system calls. Checkout specifically
https://github.com/zwanthor/mod_syzkaller/blob/master/syzkaller/my.cfg#L19 to the end of the file. The config values to modify are `weight_syscalls` and `weight`. The format is as follows:

"weight_syscalls": <array_of_system_calls>,
"weight": <system_call_priority_multiplier>,
