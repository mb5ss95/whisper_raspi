
class my_conf:
    
    
    def __init__(self, path):
        self.path_config = path + "/whisper/config"
        
        
    def receiveMsg(self):
        import bluetooth as bt
        import os

        uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
        myssid=""
        mypasswd=""
        
        # RFCOMM Port communication prepare
        server_sock = bt.BluetoothSocket(bt.RFCOMM)
        server_sock.bind(('', bt.PORT_ANY))
        server_sock.listen(1)
        
        port = server_sock.getsockname()[1]
        
        # Advertise
        bt.advertise_service(server_sock, "BtChat", service_id = uuid, service_classes = [uuid, bt.SERIAL_PORT_CLASS], profiles = [bt.SERIAL_PORT_PROFILE])
        
        print("Waiting for connection : channel %d" % port)
        
        client_sock, client_info = server_sock.accept()
        print('accepted')
        while True:
            print("Accepted connection from ", client_info)
            try:
                data = client_sock.recv(1024)
                if len(data) == 0 or data.decode() == "q":
                    break
                print("received [%s]"%data)
                print("send [%s]"%data)
                a = data.split()
                myssid = a[0]
                mypasswd = a[1]
                ssid = myssid.decode('utf-8')
                passwd = mypasswd.decode('utf-8')
                filename = "/etc/wpa_supplicant/wpa_supplicant.conf"
                #filename = "/home/pi/test.conf"
                f = open(filename, mode='w', encoding='utf-8')
                f.write("ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n")
                f.write("update_config=1\n")
                f.write("country=US\n")
                
                f.write("\nnetwork={\n")
                str = '\tssid="%s"\n'%("IotZone")
                f.write(str)
                str = '\tpsk="%s"\n'%("makerspace")
                f.write(str)
                f.write('\tkey_mgmt=WPA-PSK\n')
                f.write('}\n')
                
                f.write("\nnetwork={\n")
                str = '\tssid="%s"\n'%(ssid)
                f.write(str)
                str = '\tpsk="%s"\n'%(passwd)
                f.write(str)
                f.write('\tkey_mgmt=WPA-PSK\n')
                f.write('}\n')
                f.close()
                
                print("myssid = {}".format(myssid))
                print("my password = {}".format(mypasswd))
                break
            except IOError:
                print("disconnected")
                client_sock.close()
                server_sock.close()
                print("all done")
                break
        
        print("reboot")
        #os.system('sudo reboot')



    def load_mp3_list(self, temp):
        import json

        with open(temp) as json_file:
            json_data = json.load(json_file)
        
        return json_data
        
        
    def get_mp3_list(self, name):
        dict_mp3_file = self.load_mp3_list(self.path_config + "/data_"+name+".json")
        
        for i in dict_mp3_file.items():
            file_list = i
            break
        
        return file_list
        
        
    def get_file_list(self):
        import pyrebase
        import json

        with open(self.path_config + "/config.json") as json_file:
            json_data = json.load(json_file)

        firebase_storage = pyrebase.initialize_app(json_data)
        storage = firebase_storage.storage()

        #all_files = storage.list_files()

        dict_files = dict()
        name_mp3 = dict()
        
        for file in storage.list_files():      
            name = file.name
            
            temp = name.split(".")
            
            if "txt" in temp:
                continue
            elif "jpg" in temp:
                continue
            
            temp = name.split("/")
            
            if temp[0] in dict_files:
                if temp[1] in dict_files[temp[0]]:
                    dict_files[temp[0]][temp[1]].append(temp[2])
                else:
                    dict_files[temp[0]].setdefault(temp[1], list())
            else:
                dict_files.setdefault(temp[0], dict())

        return dict_files
