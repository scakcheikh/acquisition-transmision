/**
 *
 * Program allowing to fetch GPS coordinates and RSSI signal from the FONA_3G via arduino, 
 * whenever arduino receives the input 'g' from the serial connection
 */

#include "Adafruit_FONA.h"

// standard pins for the shield, adjust as necessary
#define FONA_RX 2
#define FONA_TX 3
#define FONA_RST 4

#include <SoftwareSerial.h>
SoftwareSerial fonaSS = SoftwareSerial(FONA_TX, FONA_RX);
SoftwareSerial *fonaSerial = &fonaSS;

// FONA 3G object type 
Adafruit_FONA_3G fona = Adafruit_FONA_3G(FONA_RST);

void setup() {

  while (! Serial);
  Serial.begin(115200);
  Serial.println(F("Adafruit FONA 3G GPS module"));
  Serial.println(F("Initializing FONA... (May take a few seconds)"));

  fonaSerial->begin(4800);
  if (!fona.begin(*fonaSerial)) {
    Serial.println(F("Couldn't find FONA"));
    while(1);
  }
  Serial.println(F("FONA Ready !"));
  Serial.println(F("Enabling GPS..."));
  fona.enableGPS(true);
}

void loop() {

  float latitude, longitude, speed_kph, heading, speed_mph, altitude;
  while(1){
    Serial.println("\nlistening...");
    while(!Serial.available());
    char cmd = Serial.read();
    flushSerial();
    Serial.print("> Data Received ! --> ");
    Serial.println(cmd);
  
    if(cmd == 'g'){
      // if you ask for an altitude reading, getGPS will return false if there isn't a 3D fix
      boolean gps_success = fona.getGPS(&latitude, &longitude, &speed_kph, &heading, &altitude);
      if (gps_success) {
        Serial.print("lat:");
        Serial.print(latitude, 6);
        Serial.print(",long:");
        Serial.print(longitude, 6);
        Serial.print(",speed_KPH:");
        Serial.print(speed_kph);
        Serial.print(",heading:");
        Serial.print(heading);
        Serial.print(",alti:");
        Serial.println(altitude);
      } else {
        Serial.println("Waiting for FONA GPS 3D fix...");
      }
      // read the RSSI
        uint8_t n = fona.getRSSI();
        int8_t r;

        // Serial.print(n); Serial.print(": ");
        if (n == 0) r = -115;
        if (n == 1) r = -111;
        if (n == 31) r = -52;
        if ((n >= 2) && (n <= 30)) {
          r = map(n, 2, 30, -110, -54);
        }
        Serial.print(F("RSSI:"));Serial.print(r); 
        //Serial.println(F(" dBm"));
    }else{
        Serial.println("No support!");
    }
  }  
}

void flushSerial() {
  while (Serial.available())
    Serial.read();
}

