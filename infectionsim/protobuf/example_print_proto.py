#!/usr/local/bin/python3

import example_pb2
import sys

def ListPeople(population):
    for person in population.people:
        print("Person ID: " + person.id)
        print("Person state: " + person.state)

test = example_pb2.Population()

# Read the existing test proto
f = open("./infectionsim/protobuf/test.file", "rb")
test.ParseFromString(f.read())
f.close()

ListPeople(test)
