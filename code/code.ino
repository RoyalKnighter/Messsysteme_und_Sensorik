/* ---------------------------------------------------
* Piezo-Vibrationssensor – Endgültiger Frequenz-Sketch
* (LM393-Rechteck → D4, Taster → D2, LCD 0x27)
* Outlier-Filter: Mode-Bin (0,5 Hz Raster) im Band 55…100 Hz
* --------------------------------------------------*/
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
/* ---------- Hardware ---------- */
const uint8_t PIN_SIG = 4; // LM393-Ausgang
const uint8_t PIN_BTN = 2; // Starttaster (LOW)
LiquidCrystal_I2C lcd(0x27, 16, 2);
/* ---------- Mess-Parameter ---------- */
const uint32_t MEASURE_MS = 30000UL; // 30 s
const uint16_t MAX_SAMPLES = 300; // Puffergröße
const uint32_t TIMEOUT_US = 500000; // pulseIn-Timeout
/* Akzeptiertes Frequenzfenster */
const float F_MIN = 55.0; // Hz
const float F_MAX = 100.0; // Hz
/* Histogramm (0,5-Hz-Raster von 50…110 Hz → 120 Bins) */
const float BIN_W = 0.5; // Binbreite
const uint8_t N_BINS= uint8_t((110-50)/BIN_W)+1;
uint16_t hist[N_BINS] = {0};
/* Puffer für Einzelmessungen */
float samples[MAX_SAMPLES];
uint16_t nSamp = 0;

/* ---------- Hilfsfunktion: eine Rechteckperiode lesen ---------- */
bool readPeriod(float &fOut)
{

  unsigned long tH = pulseIn(PIN_SIG, HIGH, TIMEOUT_US);
  unsigned long tL = pulseIn(PIN_SIG, LOW , TIMEOUT_US);


  Serial.println(tH + " " + tL);

  if (tH == 0 || tL == 0) return false;
  float T = float(tH + tL); // µs
  float f = 1e6 / T; // Hz
  if (f < F_MIN || f > F_MAX) return false;
  fOut = f;

  return true;
}

/* ---------- Setup ---------- */
void setup()
{
  Serial.begin(115200);
  pinMode(PIN_SIG, INPUT);
  pinMode(PIN_BTN, INPUT_PULLUP);
  lcd.init(); lcd.backlight();
  lcd.print(F("Piezo bereit"));
  delay(1500);
}

/* ---------- loop ---------- */
void loop()
{
/* --- Warten auf Taster --- */
  lcd.clear(); lcd.print(F("Taster druecken"));
  while (digitalRead(PIN_BTN) == HIGH);
  while (digitalRead(PIN_BTN) == LOW); // entprellen
  lcd.clear();
  lcd.print(F("Messung laeuft"));
  Serial.println(F("\n--- START ---"));
  
  /* Variablen zurücksetzen */
  memset(hist, 0, sizeof(hist));
  nSamp = 0;
  uint32_t tStart = millis();
  uint32_t nextLCD = millis() + 1000;

  /* ---------- Messphase ---------- */
  while (millis() - tStart < MEASURE_MS && nSamp < MAX_SAMPLES)
  {
    float f;
    if (!readPeriod(f)) continue; // ungültig → weiter

      /* <<< NEU: Live-Ausgabe der Frequenz */
      Serial.print("t=");
      Serial.print(millis() - tStart);
      Serial.print(" ms  f=");
      Serial.print(f, 2);
      Serial.println(" Hz");


      /* Puffer & Histogramm */
    samples[nSamp++] = f;
    uint8_t idx = uint8_t((f - 50) / BIN_W); // 50 Hz Start
    if (idx < N_BINS) hist[idx]++;
    /* einmal/Sekunde Live-Anzeige */
    if (millis() >= nextLCD) {
      lcd.setCursor(0,1);
      lcd.print(F("f="));
      lcd.print(f, 1); 

      lcd.print(F(" Hz "));
      nextLCD += 1000;
    }
  }

  // --- NEU: Alle Samples ausgeben ---
  Serial.println(F("Samples (roh):"));
  for (uint16_t i = 0; i < nSamp; i++) {
    Serial.print(i);
    Serial.print(": ");
    Serial.println(samples[i], 4);  // 4 Nachkommastellen
  }
  Serial.println();

  
  /* ---------- Auswertung: Mode-Bin mitteln ---------- */
  uint8_t bestBin = 0;
  uint16_t bestCnt = 0;
  for (uint8_t i=0;i<N_BINS;i++) {
    if (hist[i] > bestCnt) { bestCnt = hist[i]; bestBin = i; }
  }
  float fSum = 0; uint16_t nSel = 0;
  float binLo = 50 + bestBin*BIN_W - BIN_W; // Nachbar-Bins einschließen
  float binHi = 50 + bestBin*BIN_W + 2*BIN_W;
  for (uint16_t i=0;i<nSamp;i++) {
    if (samples[i] >= binLo && samples[i] < binHi) {
      fSum += samples[i]; nSel++;
    }
  }
  float fResult = (nSel>0) ? fSum / nSel : 0;
  /* ---------- Ausgabe ---------- */
  lcd.clear();
  if (fResult > 0) {
    lcd.print(F("Ergebnis:"));
    lcd.setCursor(0,1);
    lcd.print(fResult,2); lcd.print(F(" Hz "));
  } else {
    lcd.print(F("Messung fehlgeschlagen"));
  }
  Serial.print(F("Samples=")); Serial.print(nSamp);
  Serial.print(F(" ModeBin=")); Serial.print(bestBin);
  Serial.print(F(" f=")); Serial.println(fResult,2);
  delay(10000); // Ergebnis 10 s stehen lassen
}