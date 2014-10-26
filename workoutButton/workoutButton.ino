/*
  LiquidCrystal Library - Hello World
 
 Demonstrates the use a 16x2 LCD display.  The LiquidCrystal
 library works with all LCD displays that are compatible with the 
 Hitachi HD44780 driver. There are many of them out there, and you
 can usually tell them by the 16-pin interface.
 
 This sketch prints "Hello World!" to the LCD
 and shows the time.
 
  The circuit:
 * LCD RS pin to digital pin 12
 * LCD Enable pin to digital pin 11
 * LCD D4 pin to digital pin 5
 * LCD D5 pin to digital pin 4
 * LCD D6 pin to digital pin 3
 * LCD D7 pin to digital pin 2
 * LCD R/W pin to ground
 * 10K resistor:
 * ends to +5V and ground
 * wiper to LCD VO pin (pin 3)
 
 Library originally added 18 Apr 2008
 by David A. Mellis
 library modified 5 Jul 2009
 by Limor Fried (http://www.ladyada.net)
 example added 9 Jul 2009
 by Tom Igoe
 modified 22 Nov 2010
 by Tom Igoe
 
 This example code is in the public domain.

 http://www.arduino.cc/en/Tutorial/LiquidCrystal
 */

// include the library code:
#include <LiquidCrystal.h>
#include <string.h>

int buttonPin = 2;
int buttonOutPin = 4;
// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(7, 8, 9, 10, 11, 12);
int buttonState = 0;
int lastButtonState = LOW;   // the previous reading from the input pin

// the following variables are long's because the time, measured in miliseconds,
// will quickly become a bigger number than can be stored in an int.
long lastDebounceTime = 0;  // the last time the output pin was toggled
long debounceDelay = 20;    // the debounce time; increase if the output flickers

// Read a workout if it is available
char topText[16];    // Allocate space for second line
char bottomText[16]; 
char inChar = '-1';
byte index = 0;
boolean inProgress = false;
boolean released = false;
String inData = "";
String top = "default";
String bot = "default";
long startTime = millis();

void setup() {
  Serial.begin(9600);
  // set up the LCD's number of columns and rows: 
  lcd.begin(16, 2);
  // Print a message to the LCD.
  lcd.noCursor();
  pinMode(buttonOutPin, OUTPUT);
  digitalWrite(buttonOutPin, HIGH);
  pinMode(buttonPin, INPUT);
}


void loop() {
  released = false;
  // ------------HANDLE BUTTON BOUNCE--------------
  // read the state of the switch into a local variable:
  int reading = digitalRead(buttonPin);

  // check to see if you just pressed the button 
  // (i.e. the input went from LOW to HIGH),  and you've waited 
  // long enough since the last press to ignore any noise:  

  // If the switch changed, due to noise or pressing:
  if (reading != lastButtonState) {
    // reset the debouncing timer
    lastDebounceTime = millis();
  } 
  
  if ((millis() - lastDebounceTime) > debounceDelay) {
    // whatever the reading is at, it's been there for longer
    // than the debounce delay, so take it as the actual current state:

    // if the button state has changed:
    if (reading != buttonState) {
      buttonState = reading;
      if(reading){
        released = true;
      }else{released = false;}
    }
  }

  // save the reading.  Next time through the loop,
  // it'll be the lastButtonState:
  lastButtonState = reading;
  // -------------END BUTTON BOUNCE---------------
  
  // ---------------Handle Workout Inputs------------
  // Read both sections and display them
  if(Serial.available() > 0)
  {
    inData = Serial.readString();
    top  = inData.substring(0, 16);
    bot = inData.substring(16);
    inProgress = true;
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print(top);
    lcd.setCursor(0,1);
    lcd.print(bot);
    lcd.noCursor();
    digitalWrite(buttonOutPin, HIGH);
    delay(1000);
    digitalWrite(buttonOutPin, LOW);
    startTime = millis();
  }
  
  // -------------Handle Button Events--------------
  if(released){
    lcd.clear();
    if(inProgress) {
      inProgress = false;
      Serial.write('e');
    }else{
      startTime = millis();
      Serial.write('n');
    }
  }
  
  if(buttonState){
    digitalWrite(buttonOutPin, HIGH);
  }else{
    digitalWrite(buttonOutPin, LOW);
  }
  
  // Display the current time
  if ((millis() - startTime > 500)&inProgress) {
    int secs = (millis() - startTime)/1000;
    if(secs < 10) {lcd.setCursor(14, 1);}
    else if(secs < 100) {lcd.setCursor(13, 1);}
    else if(secs < 1000) {lcd.setCursor(12, 1);}
    lcd.print(secs);
  }
  
  delay(1);
}



