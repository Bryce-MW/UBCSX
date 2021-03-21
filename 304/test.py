#! /usr/bin/python3
import os
print("Content-type: text/plain\n")  # DO NOT REMOVE, MUST BE DONE FIRST


print("Hello, World!\n")
print("Welcome! Your CWL username is: " + os.environ["REMOTE_USER"] + "\n")
print("Here are the environment variables which are available in this script:")

for key, value in os.environ.items():
    print(f"    {key}: {value}")
