#!/usr/bin/python
import smbus
from time import sleep

class LM75():
    """ 
    LM75: I2C based Temperature Sensor
    
    LM75 is a 2-wire Serial Temperature Sensor and Monitor.
    It works on the I2C Protocol. The following class helps integrating 
    the LM75 sensor with python based embedded systems. The class object 
    encapsulates all main features of the sensor, abstracting the 
    operations for easy usage.
    
    Usage: 
            sensorObj = LM75(<address>,[I2C Bus(optional)])
            currentTemperature  = sensorObj.getTemp()
    
    """
    bus = smbus.SMBus(1)
    address = 0x48 
    __TEMP = 0x00
    _CONFIG = 0x01
    _THYST = 0x02
    _TSET = 0x03
    
    
    def __init__(self,add,bus=1):
        """
        Initialize the sensor
        """
        self.bus = smbus.SMBus(bus)
        self.address = add
        self.setConf(0x00)
        self.setThys(0x004B)
        self.setTset(0x0050)
        #self.setConf(0x00)
        return
        
    def setFaultQueue(self, value):
        """
        Sets the Fault Queue value of the sensor
        """
        if(value not in [0,1,2,3]):
            print ("Error: Invalid fault queue value. Must be  0,1,2 or 3")
            return False
        cfgVal = self.getConf()
        cfgVal = cfgVal | (value<<3)
        self.setConf(cfgVal)
        return True
        
    def getTemp(self):
        """
            Gets the current temperature value of the sensor
        """
        temp = self.bus.read_word_data(self.address,0x00)
        dec = (temp&0x8000)>>15
        temsign = temp & 0x0080
        temp = temp&0x007F
        temp = ((-1)**temsign)*( temp +(0.5*dec))
        return temp
        
    def setPolarity(self,polarity):
        """ 
        Sets the polarity of the INT/CMP sensor 
            1: ACTIVE HIGH
            0: ACTIVE LOW
        """
        cfgVal = self.getConf()
        if(polarity == 1):
            cfgVal = cfgVal | 0x04
        else:
            cfgVal = cfgVal & ~(0x04)
        self.setConf(cfgVal)
        return
       
    def comparator_mode(self):
        """ 
        Puts the sensor into comparator mode 
        """
        cfgVal = self.getConf()
        cfgVal = cfgVal & 0xFD
        self.setConf(cfgVal)
        return True
        
    def interrupt_mode(self):
        """ 
        Puts the sensor into interrupt mode 
        """
        cfgVal = self.getConf()
        cfgVal = cfgVal | 0x02
        self.setConf(cfgVal)
        return True
        
    # Operation Mode control
    def wakeup(self):
        """
        Puts the sensor into normal mode 
        """
        cfgVal = self.getConf()
        cfgVal = cfgVal & 0xFE
        self.setConf(cfgVal)
        return True
        
    def shutdown(self):
        """ 
        Puts the sensor into shutdown mode 
        """
        cfgVal = self.getConf()
        cfgVal = (cfgVal) | 0x01
        self.setConf(cfgVal)
        return True
        
    #System Register Reads    
    def getThys(self):
        """
        Get the current Thyst value from the sensor 
        """
        thys = self.bus.read_word_data(self.address,self._THYST)
        dec = (thys&0x8000)>>15
        thyssign = thys & 0x0080
        thys = thys&0x007F
        thys = ((-1)**thyssign)*( thys +(0.5*dec))              
        return thys
    
    def getTset(self):
        """ 
        Get the current Tset value from the sensor 
        """
        tos = self.bus.read_word_data(self.address,self._TSET)
        dec = (tos&0x8000)>>15
        tossign = tos & 0x0080
        tos = tos&0x007F
        tos = ((-1)**tossign)*( tos +(0.5*dec))
        return tos
    
    def getConf(self):
        """ 
        Get the current configuration of the sensor 
        """
        conf  = self.bus.read_byte_data(self.address,self._CONFIG)
        return (conf)	
        
    #System Register Writes    
    def setConf(self,conf):
        """ 
        Set configuration value of the sensor 
        """
        self.bus.write_byte_data(self.address,self._CONFIG,conf)
        return
        
    def setThys(self,thys):
        """ 
        Set the Thyst value of the sensor 
        """
        self.bus.write_word_data(self.address,self._THYST,thys)
        return
    def setTset(self,tos):
        """ 
        Set the Tset value of the sensor
        """
        self.bus.write_word_data(self.address,self._TSET,tos)
        return
    	
def testSensor():
    sensor = LM75(0x48)
    print ("Accessing LM75 at address ")
    print ("Temperature: " + str(sensor.getTemp()))
    print ("Thys: " + str(sensor.getThys()))
    print ("Tset: " + str(sensor.getTset()))
    sleep(1)
    print ("Shutting down sensor")
    sensor.shutdown()
    for i in range(0,20):
        sleep(1)
        print ("Temperature while Shutdown: " + str(sensor.getTemp()))
    
    print("Waking up sensor now")
    sensor.wakeup()
    for i in range(0,20):
        sleep(1)
        print("Temperature while wakeup: " + str(sensor.getTemp()))
    
    
    

if __name__ == '__main__':
    testSensor()