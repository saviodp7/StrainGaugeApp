#include "HX711.h"
#include <math.h>

void ScalesCalibration(HX711 & scale, double & offset, double & calib_factor){

  //Avvio Calibrazione e setting
  scale.set_scale(calib_factor);
  delay(100);

  //Setto offset
  scale.tare();
  offset = scale.get_offset();
  delay(100);
  
  
  //Aspetto peso di calibrazione
  while (!Serial.available());
  delay(100);
  
  double calib_weight = Serial.readString().toDouble();

  // Calibrazione
  boolean done = false;
  int flipDirCount = 0; // Contatore flip di incremento
  int direction = 1;    // Direzione di incremento
  int dirScale = 100;   // Fattore di incremento
  double data = abs(scale.get_units());
  double prevData = data;
  while (!done)
  {
      data = abs(scale.get_units());
      // if not match
      if (abs(data - calib_weight) >= 0.01) // calcolo errore
      {
          // Confronto l'errore col precedente per controllare direzione di incremento
          // ed eventuali cambi di segni
          if (abs(data - calib_weight) < abs(prevData - calib_weight) && direction != 1 && data < calib_weight)
          {
              direction = 1;
              flipDirCount++;
          }
          else if (abs(data - calib_weight) >= abs(prevData - calib_weight) && direction != -1 && data > calib_weight)
          {
              direction = -1;
              flipDirCount++;
          }
          // Se flippo due volte l'errore riduco il fattore di incremento
          if (flipDirCount > 2)
          {
              if (dirScale != 1)
              {
                  dirScale = dirScale / 10;
                  flipDirCount = 0;
              }
          }
          // Aggiornamento fattore calibrazione 
          calib_factor += direction * dirScale;
          scale.set_scale(calib_factor);
          // Attendo aggiornamento
          delay(5);
          // Salvo dati precedenti 
          prevData = data;
      }
      // Termino se l'errore � minimo
      else
      {
          done = true;
      }
  } // Fine calibrazione
  scale.set_offset(offset);
  Serial.println("calib_done," + String(offset) + "," + String(calib_factor));
}
