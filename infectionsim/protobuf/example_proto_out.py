#!/usr/local/bin/python3

import test_pb2
import sys

# Function for inputting dummy data
def input_person_data(person):
    person.id = "John"
    person.state = "infected"


test = test_pb2.Population()
try:
    f = open("./infectionsim/protobuf/test.file", "rb")
    test.ParseFromString(f.read())
    f.close()
except:
    print("./test.file" + ": Could not open file. Creating a new one.")

input_person_data(test.people.add())

# Write the new person out to disk
f = open("./infectionsim/protobuf/test.file", "wb")
f.write(test.SerializeToString())
f.close
