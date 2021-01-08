# OTP

# Introduction

Self-contained tool in Python that can be used for secure messaging. 

The tool is able to apply a One-Time Pad cipher to a given message.

Don't forget to copy the generated files to have the copy needed to decrypt the encrypted message.

# Launch program

## Help

python3 main.py -h

## Default mode, generate mode

python3 main.py -d directory_path

python3 main.py -d directory_path -g

## Send mode

text read from terminal : python3 main.py -d directory_path -s

text read from file : python3 main.py -d directory_path -s -f filepath

text read from argument : python3 main.py -d directory_path -s -t "some text"

## Receive mode

python3 main.py -d directory_path --transmission transmission_file -r