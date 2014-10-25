import serial # Serial connection
import time # time sleep
import mysql.connector # database connection
from random import randint # random numbers
from multiprocessing import Process # threading
from csaudio import* # audio playing



# connect to local database
cnx = mysql.connector.connect(user = 'root')
cursor = cnx.cursor()

# connect to Serial port
ser = serial.Serial("/dev/tty.AdafruitEZ-Link48a4-SPP",9600);

# database details
SCHEMA = "workoutbutton"
TABLE  = "workouts"
workoutFreq = 1200

# get number of total workouts
cursor.execute("SELECT COUNT(*) FROM " + SCHEMA + "." +  TABLE +  ";")
for (count) in cursor:
    numWorkouts = count[0] # cursor result comes in as tuple, so we only want first element of tuple


def getRandWorkout():
    """
    Gets a random workout from MySQL database.
    :return: N/A
    """

    # Construct SQL Query
    query = "SELECT NameTop, NameBot, Reps FROM " + SCHEMA + "." + TABLE + " "
    workoutId = randint(1,numWorkouts)
    query += "WHERE ID=" + str(workoutId)

    cursor.execute(query);

    # Get Query results
    for (nameTop, nameBot, Reps) in cursor:
        message = nameTop.ljust(14) + str(Reps) + nameBot.ljust(16) # pad string to 16 characters
        return message


def timeWorkout():
    """
    Function for timed workout thread. Gets a random workout at some time interval and writes to the Serial to send to
    Arduino.
    Time interval set with variable 'workoutFreq'
    :return: N/A
    """
    while True:
        time.sleep(workoutFreq)
        message = getRandWorkout()
        print message
        ser.write(message.encode())
        play( "Survivor_EyeOfTheTiger.mp3" )

def buttonPressWorkout():
    """
    Function for button push workout thread. Gets a random workout when the button is pressed. Reads a serial write from
    Arduino
    :return: N/A
    """
    # time.sleep(5)
    # print "Hi"
    while True:
        size = ser.inWaiting()
        if ( size > 0 ):
            pushed = ser.read(size)
            if (pushed == "n"):
                message = getRandWorkout()
                print message
                ser.write(message.encode())
                play( "Survivor_EyeOfTheTiger.mp3" )


if __name__ == "__main__":
    timeProcess = Process(target=timeWorkout, args=())
    buttonProcess = Process(target=buttonPressWorkout, args=())
    timeProcess.start()
    buttonProcess.start()


