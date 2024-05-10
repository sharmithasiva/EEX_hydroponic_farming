from machine import ADC, Pin
import utime
import network
import BlynkLib
 
soil = ADC(Pin(26)) 

min_moisture=19200
max_moisture=49300
 
readDelay = 2 
 
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("jeeva","jeeva2020")
 

BLYNK_AUTH = "F7t-EN2bGRQIZWoTAPwZAd5sZU0EEXeG"
 
      
wait = 10
while wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    wait -= 1
    print('waiting for connection...')
    time.sleep(1)
 

if wlan.status() != 3:
    raise RuntimeError('wifi connection failed')
else:
    print('connected')
    ip=wlan.ifconfig()[0]
    print('IP: ', ip)
 

blynk = BlynkLib.Blynk(BLYNK_AUTH)
 

while True:
   
    moisture = (max_moisture-soil.read_u16())*100/(max_moisture-min_moisture) 
  
    print("moisture: " + "%.2f" % moisture +"% (adc: "+str(soil.read_u16())+")")
 
 
    blynk.virtual_write(0, moisture)  
 
 
    blynk.run()
    
relay_pin = Pin(15, Pin.OUT)
moisture_level = moisture(round,2)
if moisture_level < 60:  
        relay_pin.value(1) 
else:
        relay_pin.value(0)
 
    utime.sleep(readDelay)
    