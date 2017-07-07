


# drone
all inputs to pi and esc / motors via arduino

### run
python3 -m drone 

### web-socket for debugging

connect to  `ws://rpihost:8765`

**sample recieved data:**

```json
{
"long": 43.8, "lat": 64.1,"altitude": 0.56, 
"pitch": -21.51,"yaw":34.07, "roll": 22.92,
"m4": 36, "m2": 34, "m3": 36, "m1": 35
}
```

**instructions:**

format:
  instruction followed by comma seperated arguments
  
- **stop**
    to stop HeliCarrier
  
- **start**
    to start HeliCarrier
    
- **yaw,direction,step**
    to change yaw. direction = cw/aw
    
- **pitch,direction,step**
    to change pitch. direction = up/down
    
- **roll,direction,step**
    to change roll. direction = left/right
    
- **altitude,direction,step**
    to change altitude. direction = ascend/descend
  
- **mannual,s1,s2,s3,s4**
    mannually change trust of each motor. s1-s4 are pwm values.