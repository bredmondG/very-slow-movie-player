#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import ffmpeg
import logging
import epd7in5
import time
from threading import Thread
from PIL import Image,ImageDraw,ImageFont
import traceback



libdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib')
if os.path.exists(libdir):
    print("path exits")
    sys.path.append(libdir)
else:
    print("path does not exist")
    
    
#creates log file to monitor progress        
logging.basicConfig(filename='../../../log.txt', filemode='w', level=logging.DEBUG)
logging.warning('hello log')



def generate_frames():

    y = 0
    #206800 is total number of frames in .m4v
    while y < 206800:
        #created a 2000 frame buffer, as it takes ffmpeg longer than 2.5 minutes to grab frames from the end of the .m4v 
        if len(os.listdir('shining_frames')) < 2000:
            os.system('ffmpeg -i THE_SHINING.m4v -vf "select=gte(n\,%d)" -vframes 1 shining_frames/out_img%d.png' %(y, y) )
            y+=1

    print("done")
    logging.info("done")
    print(y)


def display_frames():
    try:
        
        epd = epd7in5.EPD()
        logging.info("init and Clear")
        epd.init()
        epd.Clear()
        #time.sleep(1)

        frame_num = 0
        
        #opens frame and resizes to epaper dimensions, converts image to 1 bit and sleeps for 2.5 minutes 
        while frame_num < 206800:

            logging.info("frames in shining frames: %d" %len(os.listdir('shining_frames')))

            logging.info("Frame # %d" % frame_num)
            print("Frame # %d" % frame_num)
            logging.info("Total frames: 206800")
            im = Image.open(os.path.join('shining_frames/out_img%d.png' % frame_num))
            
            sized = im.resize((640,384), Image.ANTIALIAS)
            
            converted = sized.convert(mode='1')
            
            epd.display(epd.getbuffer(sized))
            
            time.sleep(150)

            os.remove('shining_frames/out_img%d.png' %(frame_num))
            
            frame_num += 1
       

        
        print("finished")
        epd.Clear()
        epd.sleep()
        

    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd7in5bc.epdconfig.module_exit()
        exit()
        
#runs generate_frames and display_frames simultaneously
if __name__ == '__main__':
        Thread(target = generate_frames).start()
        time.sleep(10)
        Thread(target = display_frames).start()
