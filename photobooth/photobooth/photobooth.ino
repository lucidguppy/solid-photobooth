//Matthew Karas - starting out using the neopixel example

#include<Wire.h>
#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

#define PIN 6
constexpr uint8_t buttonPin = 3;

// Parameter 1 = number of pixels in strip
// Parameter 2 = Arduino pin number (most are valid)
// Parameter 3 = pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_KHZ400  400 KHz (classic 'v1' (not v2) FLORA pixels, WS2811 drivers)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_RGB     Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)
constexpr int NUM_PIXELS {64};
constexpr int rows {8};
constexpr int CHAR_BIT {8};
Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUM_PIXELS, PIN, NEO_GRB + NEO_KHZ800);


void set_bit_map(Adafruit_NeoPixel& strip, uint8_t* bm, const size_t& rows, const uint8_t& red, const uint8_t& green, const uint8_t& blue) {
  for(int ii = 0; ii < rows; ++ii) {
    for(int jj = 0; jj < CHAR_BIT; ++jj) {
      auto pixel = ii * CHAR_BIT + jj;
      auto pixelOn = ((bm[ii]) >> (CHAR_BIT - jj - 1)) & 1;
      if(pixelOn) {
        strip.setPixelColor(pixel, strip.Color(red,green,blue));    
      } else {
        strip.setPixelColor(pixel, strip.Color(0,0,0));    
      }
    }
  }
  strip.show();
}

void setup() {
  // This is for Trinket 5V 16MHz, you can remove these three lines if you are not using a Trinket
  #if defined (__AVR_ATtiny85__)
    if (F_CPU == 16000000) clock_prescale_set(clock_div_1);
  #endif
  // End of trinket special code


  strip.begin();
  strip.show(); // Initialize all pixels to 'off'

  Wire.begin(8);
  Wire.onReceive(receiveEvent);

}

void receiveEvent(int howMany) {
  constexpr uint8_t dataLength = 1 + 8 + 3;
  uint8_t data[dataLength]; 
  auto bytesRead = 0;
  while(Wire.available() > 0) {
    if(bytesRead > dataLength) {
      return;  // don't have enough space
    } else {
      data[bytesRead] = Wire.read();
    }
    ++bytesRead;
  }
  auto dataIdx = 0;
  if(data[dataIdx] == 'a'){
    if (bytesRead != 2) {
      return; // incorrect size
    }
    ++dataIdx;
    uint8_t bright = data[dataIdx];
    analogWrite(buttonPin, bright);
  } else if (data[dataIdx] == 'b') {
    if (bytesRead != dataLength) {
      return; // incorrect size
    }
    uint8_t bm[8];
    for(int ii = 0; ii < rows; ++ii) {
      ++dataIdx;
      bm[ii] = data[dataIdx];
    }
    ++dataIdx;
    uint8_t r = data[dataIdx];
    ++dataIdx;
    uint8_t g = data[dataIdx];
    ++dataIdx;
    uint8_t b = data[dataIdx];
    set_bit_map(strip, &bm[0], rows, r,g,b);
  }
}

void colorWipe(uint32_t c) {
  for(uint16_t i=0; i<strip.numPixels(); i++) {
    strip.setPixelColor(i, c);
  }
  strip.show();
}

void loop() {
}

