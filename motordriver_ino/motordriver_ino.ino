


void setup() {

   Serial.begin(115200); 
  pinMode(4, INPUT);
  pinMode(8 , INPUT);  
  analogWrite(3,0);  // full duty cycle pwm pulse
  analogWrite(5,0);  // full duty cycle pwm pulse
  digitalWrite(4,HIGH);
  digitalWrite(8,HIGH);
}
void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    int n = data.indexOf('#');
    int m = data.lastIndexOf('#');
    int leftMtr = data.substring(0, n).toInt();
    int rightMtr = data.substring(n+1, m).toInt();
    //Serial.print(data1);
    //Serial.print(data2);
    Serial.print('R');  
  
  analogWrite(3,leftMtr);  // full duty cycle pwm pulse
  analogWrite(5,rightMtr);  
  }
  
}
