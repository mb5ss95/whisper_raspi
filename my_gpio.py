from RPi import GPIO as gpio
#import threading as th
import threading
#from threading import Thread as th

class my_gpio(threading.Thread):
    
    
    __state_num = -1
    
    __cnt = 3
    __last_num = list()
    __last_val = list()
    
    __evt = threading.Event()
    
        
    def __init__(self, gpio_list, media_player, q):
        threading.Thread.__init__(self)
        
        self.__gpio_list = gpio_list[0]
        self.__pin_vibe = 17
        self.__pin_ledd = 23
        self.__pin_roty = gpio_list[2]
        self.__pin_rclk = gpio_list[3]
        self.__mp = media_player
        self.__q = q
       
       
    def gpio_get_val(self):
        import time
        
        time.sleep(0.1)
        
        check = True
        gpio_num = 0
        summ = 0
    
        print((25, 8, 7, 1, 12, 16, 6 ,26), end=" : ")
        
        for i in (25, 8, 7, 1, 12, 16, 6 ,26):
            val = gpio.input(i)
            if val:
                summ = summ + 1
                if check:
                    gpio_num = i
                    check = False
            else:
                pass
            print(val, end="")
        
        print(" -> sum, num : ", summ, ", ", gpio_num)
        
        return summ, gpio_num
        
        
    def run(self):       
        self.__q.put(self.__evt)
        
        print("gpio reader start!!")
        
        while(1):
            try:
                summ, pin_num = self.gpio_get_val()

                if summ == 1 and self.__mp.is_playing():
                    continue
                elif pin_num == 0 and self.__mp.is_playing():
                    self.__mp.stop()
                elif summ > 1:
                    self.__mp.stop()
                elif summ == 1:
                    self.__last_num.append(pin_num)
                    if self.__last_num.count(pin_num) > 7:
                        self.__last_num.clear()
                        print("lets go ---> ", pin_num)
                        self.__state_num = self.__gpio_list.index(pin_num)
                        self.__q.put((self.__state_num))
                        self.__evt.set()
                        
            except IOError:
                gpio.cleanup()
                break
        
            except KeyboardInterrupt:
                gpio.cleanup()
                break

                
        
    def rotary_handler(self, ch):
        temp_val = []
        
        
        val_left = gpio.input(14)
        val_right = gpio.input(15)
        
        
        if not self.__mp.is_playing() :
            return
        
    
        if val_left == 0 and val_right == 1:
            if self.__last_val.count(14) > 3:
                temp = self.__mp.audio_get_volume() - 15
                print(temp)
                self.__mp.audio_set_volume(temp)
                self.__last_val.clear()
            else:
                self.__last_val.append(14)
        
        elif val_left == 1 and val_right == 0:
            if self.__last_val.count(15) > 3:
                if self.__mp.audio_get_volume() <= 130:
                    temp = self.__mp.audio_get_volume() + 15
                    print(temp)
                    self.__mp.audio_set_volume(temp)
                self.__last_val.clear()
            else:
                self.__last_val.append(15)


    def rotary_switch(self, ch):
        if self.cnt >= 5:
            self.state_num = -2
            self.cnt = 0
            return
        
        self.cnt = self.cnt + 1
        print(self.cnt)


    
    def vibe(self, long):
        import time
        
        gpio.output(self.__pin_vibe, 1)
        time.sleep(long)
        gpio.output(self.__pin_vibe, 0)
            
            
    def gpio_setup(self):
        gpio.setmode(gpio.BCM)
        gpio.setwarnings(False)
        print("gpio setup")
    
        for i in self.__gpio_list:
            gpio.setup(i, gpio.IN,  pull_up_down = gpio.PUD_UP)
        
        for i in [self.__pin_vibe, self.__pin_ledd]:
            gpio.setup(i, gpio.OUT)
            
        for i in self.__pin_roty:
            gpio.setup(i, gpio.IN)
            gpio.add_event_detect(i, gpio.BOTH, callback=self.rotary_handler, bouncetime=100)
    
        gpio.setup(self.__pin_rclk, gpio.IN)
        gpio.add_event_detect(self.__pin_rclk, gpio.BOTH, callback=self.rotary_switch, bouncetime=100)
        
        gpio.output(self.__pin_vibe, 0)
        gpio.output(self.__pin_ledd, 1)
        print("gpio setup done")
        
     
     
if __name__ == "__main__":
    pass
