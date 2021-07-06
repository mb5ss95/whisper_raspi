from my_gpio import my_gpio as gpio
from my_conf import my_conf as conf
from queue import Queue

import time
import vlc

gpio_list = ((26, 6, 16, 12, 1, 7, 8, 25), (23, 17), (14, 15), 18) #page, led&vibe, rotary

def mp3_player(name):
    global media_player
    
    if media_player.is_playing():
        media_player.stop()
    path = "/home/pi/whisper/mp3" + name
    print("Start Music : ", path)
    media_player.set_media(vlc.Media(path))
    media_player.play()
    '''
    time.sleep(1)
    media_player.pause()
    time.sleep(1.5)
    media_player.play()
    '''
  



    
if __name__ == "__main__":
    print("Main Started!!!")
    last_index = -1

    media_player = vlc.MediaPlayer()
    
    q = Queue()
    gpio = gpio(gpio_list, media_player, q)
    gpio.gpio_setup()
    gpio.vibe(2)
    
    conf = conf("/home/pi")
    file_list = conf.get_mp3_list("mp3")
    print(file_list)
    
    gpio.start()
    evt = q.get()
    
    while(1):
        evt.wait()
        mp3_index = q.get()
        if mp3_index != last_index:
            mp3_player("/" + file_list[0] + "/" + file_list[1][mp3_index])
            gpio.vibe(1)
            last_index = mp3_index
            evt.clear()
        time.sleep(0.2)
