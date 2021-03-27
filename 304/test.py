#! /usr/bin/python3
import os
import sys
import urllib.parse
sys.stderr = sys.stdout
print("Content-type: text/plain\n")  # DO NOT REMOVE, MUST BE DONE FIRST


print("Hello, World!\n")
print("Welcome! Your CWL username is: " + os.environ["REMOTE_USER"] + "\n")
print("Here are the environment variables which are available in this script:")

for key, value in os.environ.items():
    print(f"    {key}: {value}")


if os.environ["REQUEST_METHOD"] == "POST":
    print("\nHere is the post data:")
    for line in sys.stdin:
        post = urllib.parse.parse_qs(line, keep_blank_values=True)
        for key, value in post.items():
            print(f"    {key}: {value}")