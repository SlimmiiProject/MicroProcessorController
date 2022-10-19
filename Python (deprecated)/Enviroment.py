class __Enviroment:
    @property
    def PUBLIC_FOLDER(self):
        return "public"
        
    @property
    def POWER_LED_PIN(self):
        return -1
    
    @property
    def WIFI_LED_PIN(self):
        return -2
    
    @property
    def ADHOC_LED_PIN(self):
        return -3
    
    @property
    def DEBUG_MODE(self):
        return True
    
    @property
    def CAMERA_INTERVAL(self):
        mins = 15
        ms = (mins)*60*1000
        sec = (ms / 1000)
        
        return int(sec)
    
Enviroment = __Enviroment()
