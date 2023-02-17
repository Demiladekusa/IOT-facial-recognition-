
#include <Servo.h>

Servo servo;
#define led1 13




int data, flag = 2;

void setup()
{

  servo.attach(8);
  servo.write(0);
  pinMode(led1, OUTPUT);

  Serial.begin(9600);
  digitalWrite(led1, LOW);
 
}

void loop()
{
  while( Serial.available() )
  {
    data = Serial.read();

    if (data == '1')
    {
      flag = 1;
    }
    else if(data == '0')
    {
      flag = 0;
    }
  }
  if(flag == 1)
    {
      servo.write(90);
      delay(3000);
      servo.write(0);
      digitalWrite(led1, LOW);
      
    }
     else if (flag == 0)
    {
      servo.write(0);
      digitalWrite(led1, HIGH);
      
      
  

    }
}
