#!/usr/bin/env python

#Een programma dat op een LCD je de datum tijd en ip address van u rpi ziet
            
# Imports

from subprocess import Popen, PIPE
from time import sleep
from datetime import datetime
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd


__author__ = "Jasper Withofs"
__email__ = "jasper.withofs@student.kdg.be"
__version__ = "1.0.2"
__status__ = "Development"


#pas dit aan naargelang de grote van de lcd
lcd_columns = 16
lcd_rows = 2

#IO / LCD Initialiseren
lcd_rs = digitalio.DigitalInOut(board.D22)
lcd_en = digitalio.DigitalInOut(board.D17)
lcd_d4 = digitalio.DigitalInOut(board.D25)
lcd_d5 = digitalio.DigitalInOut(board.D24)
lcd_d6 = digitalio.DigitalInOut(board.D23)
lcd_d7 = digitalio.DigitalInOut(board.D18)

lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6,
                                      lcd_d7, lcd_columns, lcd_rows)

#ethernet/wifi device zoeken
def find_interface():
    find_device = "ip addr show"
    interface_parse = run_cmd(find_device)
    for line in interface_parse.splitlines():
        if "state UP" in line:
            dev_name = line.split(':')[1]
    return dev_name

#IP zoeken
def parse_ip():
    find_ip = "ip addr show %s" % interface
    find_ip = "ip addr show %s" % interface
    ip_parse = run_cmd(find_ip)
    for line in ip_parse.splitlines():
        if "inet " in line:
            ip = line.split(' ')[5]
            ip = ip.split('/')[0]
    return ip

#shell command dat ASCII teruggeeft
def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output.decode('ascii')


lcd.clear()

#detecteren van actieve network devices
sleep(2)
interface = find_interface()
ip_address = parse_ip()

while True:
    #Datum & tijd
    lcd_line_1 = datetime.now().strftime('%b %d  %H:%M:%S\n')
    #IP Adress
    lcd_line_2 = "IP " + ip_address
    #2 lijnen samenvoegen
    lcd.message = lcd_line_1 + lcd_line_2

    sleep(2)