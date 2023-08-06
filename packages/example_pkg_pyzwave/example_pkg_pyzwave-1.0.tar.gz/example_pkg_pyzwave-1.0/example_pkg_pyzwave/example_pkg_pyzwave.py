import serial
from serial import SerialException
import time
import binascii 
import datetime
import logging
from logging import handlers

# init interavate
send_bytes_intervate_list = [
     [0x23,0x05,0x00,0x49,0x47],
     [0x23,0x01,0x00],
     [0x23,0x02,0x01,0x01],
     [0x23,0x03,0x00],
     [0x23,0x13,0x01,0x00],
     [0x23,0x13,0x01,0x01],
     [0x23,0x13,0x01,0x02],
     [0x23,0x13,0x01,0x03],
     [0x23,0x13,0x01,0x08],
     [0x23,0x13,0x01,0x09],
     [0x23,0x13,0x01,0x0A],
     [0x23,0x13,0x01,0x1A],
     [0x23,0x13,0x01,0x1B],
     [0x23,0x13,0x01,0x1C],
     [0x23,0x13,0x01,0x1D],
     [0x23,0x13,0x01,0x04],
     [0x23,0x13,0x01,0x05],
     [0x23,0x13,0x01,0x06],
     [0x23,0x13,0x01,0x07],
     [0x23,0x13,0x01,0x0B],
     [0x23,0x13,0x01,0x0C],
     [0x23,0x13,0x01,0x0D],
     [0x23,0x13,0x01,0x0E],
     [0x23,0x13,0x01,0x0F],
     [0x23,0x13,0x01,0x18],
     [0x23,0x13,0x01,0x10],
     [0x23,0x13,0x01,0x11],  
]

# init set zniffer frequence
send_bytes_set_frequence_lists = [
    [[0x23,0x05,0x00,0x49,0x47],
     [0x23,0x01,0x00],
     [0x23,0x02,0x01,0x01],
     [0x23,0x03,0x00],
     [0x23,0x13,0x01,0x00],
     [0x23,0x13,0x01,0x01],
     [0x23,0x13,0x01,0x02],
     [0x23,0x13,0x01,0x03],
     [0x23,0x13,0x01,0x08],
     [0x23,0x13,0x01,0x09],
     [0x23,0x13,0x01,0x0A],
     [0x23,0x13,0x01,0x1A],
     [0x23,0x13,0x01,0x1B],
     [0x23,0x13,0x01,0x1C],
     [0x23,0x13,0x01,0x1D],
     [0x23,0x13,0x01,0x04],
     [0x23,0x13,0x01,0x05],
     [0x23,0x13,0x01,0x06],
     [0x23,0x13,0x01,0x07],
     [0x23,0x13,0x01,0x0B],
     [0x23,0x13,0x01,0x0C],
     [0x23,0x13,0x01,0x0D],
     [0x23,0x13,0x01,0x0E],
     [0x23,0x13,0x01,0x0F],
     [0x23,0x13,0x01,0x18],
     [0x23,0x13,0x01,0x10],
     [0x23,0x13,0x01,0x11]],
    [[0x23,0x05,0x00,0x49,0x47],
     [0x23,0x01,0x00],
     [0x23,0x0e,0x01,0x01],
     [0x23,0x02,0x01,0x01],
     [0x23,0x03,0x00],
     [0x23,0x13,0x01,0x00],
     [0x23,0x13,0x01,0x01],
     [0x23,0x13,0x01,0x02],
     [0x23,0x13,0x01,0x03],
     [0x23,0x13,0x01,0x08],
     [0x23,0x13,0x01,0x09],
     [0x23,0x13,0x01,0x0A],
     [0x23,0x13,0x01,0x1A],
     [0x23,0x13,0x01,0x1B],
     [0x23,0x13,0x01,0x1C],
     [0x23,0x13,0x01,0x1D],
     [0x23,0x13,0x01,0x04],
     [0x23,0x13,0x01,0x05],
     [0x23,0x13,0x01,0x06],
     [0x23,0x13,0x01,0x07],
     [0x23,0x13,0x01,0x0B],
     [0x23,0x13,0x01,0x0C],
     [0x23,0x13,0x01,0x0D],
     [0x23,0x13,0x01,0x0E],
     [0x23,0x13,0x01,0x0F],
     [0x23,0x13,0x01,0x18],
     [0x23,0x13,0x01,0x10],
     [0x23,0x13,0x01,0x11],
     [0x23,0x04,0x00]]
]


hex_num = {
    "a":10,"b":11,"c":12,"d":13,"e":14,"f":15
}

class Logger(object):
    level_relations = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'crit':logging.CRITICAL
    }#日志级别关系映射
    def __init__(self,filename,level='info',when='D',backCount=3,fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):     
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)#设置日志格式
        self.logger.setLevel(self.level_relations.get(level))#设置日志级别
#        sh = logging.StreamHandler()#往屏幕上输出
#       sh.setFormatter(format_str) #设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=filename,when=when,backupCount=backCount,encoding='utf-8')#往文件里写入#指定间隔时间自动生成文件的处理器
        #实例化TimedRotatingFileHandler
        #interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)#设置文件里写入的格式
#        self.logger.addHandler(sh) #把对象加到logger里
        self.logger.addHandler(th)


class Z_W_Data_Model(object):

    baudrate = 115200  # baudrate
    timeout = 1.5  # timeout
    bytesize = 8 # data byte size

    def __init__(self):
        self.speed = ""
        self.remain_data = "" # pack recombination
        self.home_id = None # z-wave network mark
        self.src_node_id = 0 # source node id
        self.frame_ctr = None # frame controll 
        self.frame_len = 0   # frame length
        self.des_node_id = 0  # destion node id
        self.cc_data = None # avliaed data
        self.crc = None  # checksum crc16
        self.log = Logger('zwave.log',level='debug')

    # open serial
    def open(self,porta_name):
        while True:
            try:
                self.ser = serial.Serial(port=port_name, 
                                    baudrate=Z_W_Data_Model.baudrate, 
                                    timeout=Z_W_Data_Model.timeout, 
                                    bytesize=Z_W_Data_Model.bytesize)
                if self.ser.isOpen():
                   # print("serial opened")
                    self.log.logger.info("serial opened")
                    time.sleep(0.5)
                    self.send_data()
                break
            except Exception as res:
                #print(res)
                #print("open serial failed!")
                self.log.logger.critical(res)
                self.log.logger.critical("open serial failed!")
                time.sleep(3)


    def send_data(self):   # send func
        menu = {
            1:"first",
            2:"second",
            3:"third"
        }
        z_wave_data = ""
        count = 1
        for send_bytes_intervate in send_bytes_intervate_list: # intervate send_data
            data = bytes(send_bytes_intervate)  # hex data to byte data
            self.ser.write(data)  # send data
            data = [hex(x) for x in bytes(data)]       
        self.log.logger.info("-intervate sucessful!" )
        try:
            self.ser.close()
            self.log.logger.info("serial close sucessfull")
            self.log.logger.info("wait 1s restart")
            time.sleep(0.5)
        except:
            self.log.logger.critical("serial close failed!")
        else:
            try:
                self.ser.open()
            except:
                self.log.logger.critical("serial open restart failed!")
            else:
                self.log.logger.info("serial open restart sucessful!")
                for set_frequence_list in send_bytes_set_frequence_lists:
                    count += 1
                    for send_byte_set_frequence in set_frequence_list:                    
                        data = bytes(send_byte_set_frequence)  # send hex data framat
                        self.ser.write(data)  # send serial data
                        self.log.logger.info("send init set intervate")
                        data = [hex(x) for x in bytes(data)]
                        self.log.logger.info(data)
                        replay_data = None 
                    self.log.logger.info(menu[count] + " intervate sucessful!")
        self.log.logger.info("waitting zniffer recv_data")
        self.zniffer_start()

    # zniffer start interface
    def zniffer_start(self):
        start_time = None
        while True:  
            #self.log.logger.info("---------------------->zniffer is working")
            # print("---------------------->zniffer is working")
            start_time = time.time() 
            z_wave_data = self.recv_data()
            stop_time = time.time()
            if len(z_wave_data) > 0:
                self.speed = str(int(len(z_wave_data)*4 / (stop_time - start_time))) + "kb/s"
                z_wave_data = self.remain_data + z_wave_data
                self.remain_data = ""
                self.split_data(z_wave_data)
                if self.data_flag >= 0: # error_data 
                    self.log.logger.info("nukown data,Ongoing peocessing")
                    self.error_data_save(z_wave_data[self.data_flag:]) # 
                    self.log.logger.info("error frame,insert table z_wave_error_data") 
            else:
                time.sleep(0.01)
                continue
    

    def recv_data(self):  
        time.sleep(0.05)
        # self.log.logger.info("--------->waitting replay")
        data = "" # recv_data
        while self.ser.inWaiting()>0:  # have data 
            data_byte = self.ser.read(7) # read pre 7byte
            data += str(binascii.b2a_hex(data_byte))[2:-1]
        return data

    def split_data(self,z_wave_data):
        start_index = 0 # data frame start
        complete_frame_len = 0
        complete_frame_data = ""
        #s_framelen = ""
        # must be decover frame_len
        while start_index + 36 < len(z_wave_data):
            # if z_wave_data[start_index:start_index+2] != "21":
            #     self.data_flag = 1
            #     return None
            self.frame_len = 1
            s_framelen = z_wave_data[start_index+34:start_index+36] # str frame_len
            s_src_node_id = ""
            s_des_node_id = ""
            self.frame_len = int(s_framelen[0])*16 if s_framelen[0].isdigit() else hex_num[s_framelen[0]]*16
            self.frame_len += int(s_framelen[1]) if s_framelen[1].isdigit() else hex_num[s_framelen[1]]
            if self.frame_len > 25 or self.frame_len < 10:
                self.data_flag = start_index
                return None
            complete_frame_len = 20 + self.frame_len * 2
            # least decover complete one frame
            if start_index + complete_frame_len <= len(z_wave_data):
                self.count_data += 1
                self.log.logger.info(self.count_data)
                complete_frame_data = z_wave_data[start_index:start_index+complete_frame_len]
                
                self.home_id = complete_frame_data[20:28]
                s_src_node_id = complete_frame_data[28:30]
                self.src_node_id = int(s_src_node_id[0])*16 if s_src_node_id[0].isdigit() else hex_num[s_src_node_id[0]]*16
                self.src_node_id += int(s_src_node_id[1]) if s_src_node_id[1].isdigit() else hex_num[s_src_node_id[1]]
                self.frame_ctr = complete_frame_data[30:34]
                s_des_node_id = complete_frame_data[36:38]
                self.des_node_id = int(s_des_node_id[0])*16 if s_des_node_id[0].isdigit() else hex_num[s_des_node_id[0]]*16
                self.des_node_id += int(s_des_node_id[1]) if s_des_node_id[1].isdigit() else hex_num[s_des_node_id[1]]
                if self.frame_len != 10:
                    self.cc_data = complete_frame_data[38:len(complete_frame_data)-4]
                    if self.cc_data == "":
                        self.cc_data = "06"
                    self.crc = complete_frame_data[-4:]
                else:
                    self.cc_data = complete_frame_data[-2:]
                    self.crc = ""
                yield self.speed,self.home_id,self.src_node_id,self.frame_ctr,self.frame_len,self.des_node_id,self.cc_data,self.crc
            else:
                self.remain_data += z_wave_data[start_index:]
                break
            start_index += complete_frame_len
        else:
            self.remain_data += z_wave_data[start_index:]


    def error_data_save(self,z_wave_data):
        self.log.logger.info(z_wave_data)
        yield z_wave_data
        self.data_flag = -1

if "name" == "__main__":
    pass

