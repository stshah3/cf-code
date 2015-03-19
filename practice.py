"""
file = open("newfile.txt", "w")

a = 50.0034534
b = "Hello world"

if (a>50):
	for x in range (0,4):
		file.write("test number"+str(x)+":\n")
		file.write("Samyak is "+str(a)+" years old and says "+str(b)+"\n")
			
"""



"""
class Student(object):
    name = ""
    age = 0
    major = ""
    print ("Student:"+str(student.name)+","+str(student.ago)+","+str(student.major))

    # The class "constructor" - It's actually an initializer 
    def __init__(self, name, age, major):
        self.name = name
        self.age = age
        self.major = major

def make_student(name, age, major):
    student = Student(Samyak, 20, AE)
    return student
 
"""
"""
import logging
logger = logging.getLogger('test')
hdlr = logging.FileHandler('test.txt')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.WARNING)
#We can use this logger object now to write entries to the log file:

logger.error('We have a problem')
logger.info('While this is just chatty')
"""
"""

import logging
logging.basicConfig(
    level = logging.DEBUG,
    format = '%(asctime)s %(levelname)s %(message)s',
    filename = 'test.txt',
    filemode = 'w'
)
logger = logging.getLogger(__name__)

logger.info('Start reading database')
# read database here

records = {'john': 55, 'tom': 66}
logger.debug('Records: %s', records)
logger.info('Updating records ...')
# update records here

logger.info('Finish updating records')
"""

"""
# This program compares two strings.

# Get a password from the user.
password = raw_input('Enter the password: ')

# Determine whether the correct password
# was entered.

if password == 'hello':
    print'Password Accepted'
elif password == 'bye':
    print 'wtf?'
else:
    print'Sorry, that is the wrong password.'
"""

"""

import sys

num = int(raw_input('Enter a number: '))

if num>5:
    print( str(num)+" is greater than 5")
elif num<5:
         print( str(num)+" is less than 5")
else: 
    sys.exit()
"""
string_1 = "Camelot"
string_2 = "place"

print "Let's not go to %s. 'Tis a silly %s." % (string_1, string_2)
