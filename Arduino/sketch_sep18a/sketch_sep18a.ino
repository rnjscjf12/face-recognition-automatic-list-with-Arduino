#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <stdint.h>
#include <Adafruit_MLX90614.h>
 
#define OLED_RESET 4
 
Adafruit_SSD1306 display(OLED_RESET);
Adafruit_MLX90614 mlx = Adafruit_MLX90614();
 
#if (SSD1306_LCDHEIGHT != 32)
#error("Height incorrect, please fix Adafruit_SSD1306.h!");
#endif
 
void setup()  
{               
  
  Serial.begin(9600);
  mlx.begin(); 
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);  // initialize with the I2C addr 0x3C (for the 128x32)
  pinMode(3, INPUT);
}
 
 
void loop()
{
    // Clear the buffer.
  display.clearDisplay();
  display.setTextColor(WHITE);
  display.setCursor(0,5);
  // text display tests
  if(digitalRead(3)&&!Serial.available())
  {
  float temper = 0;
  display.setTextSize(2);
  display.print("MEASURING");
  display.display();
  
  delay(3000);
  display.clearDisplay();
  display.setCursor(0,5);
  display.setTextSize(3);
  temper = mlx.readObjectTempC();
  display.print(temper);
  temper *= 100;
  display.print(" C");
  display.display();
  Serial.println(int(temper));
  delay(5000);
  }
  
  else
  {
    display.setTextSize(2);
    display.print("NOT FOUND"); 
    display.display();
    if(Serial.available() <= 0){
    Serial.println(int(0));  
    }
    delay(200);
  }
}
