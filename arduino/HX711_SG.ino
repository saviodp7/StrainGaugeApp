#include "HX711.h"

HX711 sns;

// 1. HX711 circuit wiring
#define SNS_DOUT_PIN 4
#define SNS_SCK_PIN 5

// 2. Settings
long SNS_SCALE = 0;
const float SG_gain = 2.11;
const int smp_time = 50;
String command = "";

// 3. Variables
double V_0, V_a, dR_R, strain;
unsigned long currentMillis, previousMillis;

void setup(){
  Serial.begin(9600);

  // Inizializzazione
  sns.begin(SNS_DOUT_PIN, SNS_SCK_PIN);
  sns.set_scale();
  sns.tare();

  // Calibrazione
//  SNS_SCALE = sns.get_value(10);
//  sns.set_scale(SNS_SCALE/KNOWN_STRAIN);
//  Serial.println("Calibrazione effettuata");

  delay(50);
}

void loop(){
  currentMillis = millis();

  if(currentMillis - previousMillis >= smp_time){
    previousMillis = currentMillis;
  
    if(Serial.available()){
      command = Serial.readString();
      if(command == "tara")
        sns.tare();
    }
        
    V_0 = sns.get_value()*40/(pow(2,24));      // conversione in mV : V_0 = lettura*V_max-V_min/2^24(bit)
    //V_a = double(analogRead(A0))/1024*5*1000;  // V_a tensione di alimentazione in mV
    //dR_R = 4*V_0/V_a;                          // Ricavo dR/R
    //strain = dR_R/SG_gain*1000;                // Ricavo lo strain \epsilon=dR/(R*k)
    Serial.println(V_0);                    // valore in mStrain
  }
}
