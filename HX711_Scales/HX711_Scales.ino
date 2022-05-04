#include "HX711.h"
#include "calib.h"

HX711 sns;
// 1. HX711 circuit wiring
const int SNS_DOUT_PIN = 2;
const int SNS_SCK_PIN = 3;

// 2. Settings
const float SG_gain = 2.11;
const int smp_time = 500;
double offset = 0;
double calib_factor = -7500;

// 3. Variabili
double V_a; // tensione alimentazione
double V_0; // differenza di potenziale ponte Wheatstone
double dR_R;
double strain;
double calib_weight; 
unsigned long currentMillis, previousMillis;
long sns_scale = 0;
String lettura, flag = "non sono entrato";

void setup(){
  Serial.begin(9600);
  // Inizializzazione
  sns.begin(SNS_DOUT_PIN, SNS_SCK_PIN);
  sns.set_scale();
  sns.tare();
  pinMode(13, OUTPUT);

  delay(50);
}

void loop(){
  currentMillis = millis();

  if(currentMillis - previousMillis >= smp_time){
    previousMillis = currentMillis;
    if(Serial.available()){
      lettura = Serial.readString();
      // Taratura
      if(lettura == "tara")
        sns.tare();
      // Calibrazione
      if (lettura == "calib")
        ScalesCalibration(sns, offset, calib_factor);
    // Ricezione dati
      if (lettura == "load"){
        while(!Serial.available());
        delay(100);
        offset = Serial.readString().toDouble();
        while(!Serial.available());
        delay(100);
        calib_factor = Serial.readString().toDouble();
        Serial.println("loaded");
        sns.set_offset(offset);
        sns.set_scale(calib_factor);
      }
    }
    Serial.println(sns.get_value()/10000);
  }
}
