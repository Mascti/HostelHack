import RPi.GPIO as gpio
import pandas
from twilio.rest import Client
from time import sleep
from RPLCD.i2c import CharLCD
import time
import smbus

account_sid = "AC1f61fb9a0f60018a7347fb12a4e6e7e"
auth_token = "a870aa3628d9fc381c9c496adecedfd"
#the above account_sid and auth_token are just an example and should be replaced by the ones provided to you by twilio
client = Client(account_sid, auth_token)

df = pandas.read_csv('hostelhack.csv')

lcd = CharLCD('PCF8574', 0x3f)
#0x3f is the address for LCD display

lcd = CharLCD(i2c_expander='PCF8574', address=0x3f, port=1,
	cols=20, rows=4, dotsize=8,
	charmap='A02',
	auto_linebreaks=True,
	backlight_enabled=True)

def display(number, initiate):
	lcd.cursor_pos = (1, initiate)
	lcd.write_string(str(number))
	return

gpio.setmode(gpio.BOARD)

Matrix = [ [1, 2, 3, 'A'],
           [4, 5, 6, 'B'],
           [7, 8, 9, 'C'],
           ['*', 0, '#', 'D']]

ROW = [7, 11, 13, 15]
COL = [12, 16, 18, 22]

for j in range(4):
    gpio.setup(COL[j], gpio.OUT)
    gpio.output(COL[j], 1)

for i in range (4):
    gpio.setup(ROW[i], gpio.IN, pull_up_down = gpio.PUD_UP)

b=1

try:
    while(True):
            for j in range(4):
                gpio.output(COL[j],0)

                for i in range(4):
                    if gpio.input(ROW[i])==0:
                        print Matrix[i][j]
                        RoomNumber=str(Matrix[i][j])
                        display(Matrix[i][j], 1)
                        while(gpio.input(ROW[i])==0):
                            pass
                        gpio.output(COL[j],1)

                        

                        while (b==1):
                            for k in range(4):
                                gpio.output(COL[k],0)

                                for g in range(4):
                                    if gpio.input(ROW[g])==0:
                                        if g==2 and k==3:
                                            b=0
                                        print Matrix[g][k]
                                        RoomNumber=RoomNumber+ str(Matrix[g][k])
                                        display(Matrix[g][k],2)
                                        while(gpio.input(ROW[g])==0):
                                            pass
                                        gpio.output(COL[k],1)



                                        while (b==1):
                                            for l in range(4):
                                                gpio.output(COL[l],0)

                                                for h in range(4):
                                                    if gpio.input(ROW[h])==0:
                                                        if h==2 and l==3:
                                                            b=0
                                                        print Matrix[h][l]
                                                        RoomNumber=RoomNumber+ str(Matrix[h][l])
                                                        display(Matrix[h][l],3)
                                                        while(gpio.input(ROW[h])==0):
                                                            pass
                                                        gpio.output(COL[l],1)



                                                        while (b==1):
                                                            for n in range(4):
                                                                gpio.output(COL[n],0)

                                                                for m in range(4):
                                                                    if gpio.input(ROW[m])==0:
                                                                        if m==2 and n==3:
                                                                            b=0
                                                                        print Matrix[m][n]
                                                                        RoomNumber=RoomNumber+ str(Matrix[m][n])
                                                                        display(Matrix[m][n],4)
                                                                        time.sleep(2)
                                                                        while(gpio.input(ROW[m])==0):
                                                                            pass
                                                                        gpio.output(COL[n],1)

                                                                        a='+91' + str(df[RoomNumber][1])
                                                                        
                                                                        message = client.api.account.messages.create(
                                                                            to = a,
                                                                            from_ = "(563) 202-7146",
                                                                            body = "Your order has arrived.")

                                                                        lcd.clear()
                                                                        str_='Your message is sent to'+ str(df[RoomNumber][0])
                                                                        display(str_)
                                                                        time.sleep(2)
                                                                        b=0

                                        
                gpio.output(COL[j],1)
                lcd.clear()
                b=1
except KeyboardInterrupt:
        gpio.cleanup()

