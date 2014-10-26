import serial # Serial connection
import mysql.connector # database connection
from random import randint # random numbers
from multiprocessing import Process # threading
from csaudio import* # audio playing
import time



# connect to local database
cnx = mysql.connector.connect(user = 'root')
cursor = cnx.cursor()

# connect to Serial port
ser = serial.Serial("/dev/tty.AdafruitEZ-Link48a4-SPP",9600);

# database details
SCHEMA = "workoutbutton"
TABLE  = "workouts"
workoutFreq = 2400

# get number of total workouts
cursor.execute("SELECT COUNT(*) FROM " + SCHEMA + "." +  TABLE +  ";")
for (count) in cursor:
    numWorkouts = count[0] # cursor result comes in as tuple, so we only want first element of tuple

# thread for song playing so it doesn't interupt other things
def playSong():
     play( "Survivor_EyeOfTheTiger.mp3" )

# data members for workout time tracking
start = 0
end = 0
curWorkoutID = 0
curWorkoutBestTime = 0


def getRandWorkout():
    """
    Gets a random workout from MySQL database.
    :return: N/A
    """
    global curWorkoutBestTime
    global curWorkoutID

    # Construct SQL Query
    query = "SELECT ID, NameTop, NameBot, Reps, BestTime FROM " + SCHEMA + "." + TABLE + " "
    workoutId = randint(1,numWorkouts)
    query += "WHERE ID=" + str(workoutId)

    cursor.execute(query);

    # Get Query results
    for (id, nameTop, nameBot, reps, bestTime) in cursor:
        message = nameTop.ljust(14) + str(reps) + nameBot.ljust(16) # pad string to 16 characters
        curWorkoutBestTime = bestTime
        curWorkoutID = id
        return message

def sendToSerial(message):
    global start

    print message
    ser.write(message.encode())
    start = time.time()

def updateTime(newTime):
    global curWorkoutID

    query = "UPDATE " + SCHEMA + "." + TABLE + " SET BestTime=" + str(int(newTime))
    query += " WHERE ID=" + str(curWorkoutID)
    print query
    cursor.execute(query)
    cnx.commit()

def timeWorkout():
    """
    Function for timed workout thread. Gets a random workout at some time interval and writes to the Serial to send to
    Arduino.
    Time interval set with variable 'workoutFreq'
    :return: N/A
    """
    global curWorkoutID
    global curWorkoutBestTime
    global start
    global end

    while True:
        songProcess = Process(target=playSong, args=())
        time.sleep(workoutFreq)
        message = getRandWorkout()
        sendToSerial(message)
        songProcess.start()


def buttonPressWorkout():
    """
    Function for button push workout thread. Gets a random workout when the button is pressed. Reads a serial write from
    Arduino
    :return: N/A
    """
    # time.sleep(5)
    # print "Hi"
    global start
    global end
    global curWorkoutBestTime
    global curWorkoutID


    while True:
        songProcess = Process(target=playSong, args=())
        size = ser.inWaiting()
        if ( size > 0 ):
            pushed = ser.read(size)

            if (pushed == "n"):
                message = getRandWorkout()
                sendToSerial(message)
                songProcess.start()

            elif (pushed == "e"):
                end = time.time()
                workoutTime = end - start
                print workoutTime
                print curWorkoutBestTime

                if (workoutTime < curWorkoutBestTime):
                    updateTime(workoutTime)
                    curWorkoutBestTime = 0
                    curWorkoutID = 0
                    start = 0
                    end = 0

if __name__ == "__main__":
    timeProcess = Process(target=timeWorkout, args=())
    buttonProcess = Process(target=buttonPressWorkout, args=())
    timeProcess.start()
    buttonProcess.start()


