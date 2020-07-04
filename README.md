# prerequiste_checks
A python program which parses student transcript data to determine eligibility

Prerequisite checks are based on the studio prerequisite requirements at the New Jersey Institute of Technology. 
In order to run this code, the advisor must have a set of roster files in csv format with columns containing student id, student name, student email as well as transcript data in csv format for all students on the rosters.
When collecting transcript data, the VBA can be included on the roster file to highlight the individual cell to keep track of location in list.

The code in the checks.py file will parse each transcript line by line to check whether a student has met all the prerequisites for the course in question and return a list of students who are missing prerequisites.
The advisor should check this list to make sure that the student was not given special permission to continue before removing them from the course.
