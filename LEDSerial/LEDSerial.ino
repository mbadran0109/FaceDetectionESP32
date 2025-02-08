#include <Servo.h>

// Pin assignments
int greenLED = 6; // Green LED pin
int redLED = 7;   // Red LED pin
Servo servoMotor;  // Servo object

void setup() {
    Serial.begin(9600);
    pinMode(greenLED, OUTPUT);
    pinMode(redLED, OUTPUT);
    servoMotor.attach(9); // Servo connected to pin 9
    servoMotor.write(0);  // Start servo at 0 degrees
}

void loop() {
    if (Serial.available() > 0) {
        char received = Serial.read();
        
        if (received == '1') {
            digitalWrite(greenLED, HIGH); // Turn Green LED ON
            digitalWrite(redLED, LOW);   // Ensure Red LED is OFF
        } 
        else if (received == '2') {
            digitalWrite(greenLED, LOW);  // Ensure Green LED is OFF
            digitalWrite(redLED, HIGH);  // Turn Red LED ON
        } 
        else if (received == '3') {
           digitalWrite(greenLED, HIGH);
            servoMotor.write(90);        // Open Servo to 90 degrees
            delay(2000);                 // Wait 2 seconds
            servoMotor.write(0);         // Reset Servo to 0 degrees
        } 
        else {
            digitalWrite(greenLED, LOW);
            digitalWrite(redLED, LOW);
        }
    }
}
