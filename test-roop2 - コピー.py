#coding: utf-8
import RPi.GPIO as GPIO 
from time import sleep

#ポート番号の定義
launcher_pin = 27                       
servo_pin = 0
pwm_pin = 19
led_green_pin = 9
led_blue_pin = 11
led_red_pin = 10


#GPIOの設定
#GPIOのモードを"GPIO.BCM"に設定
GPIO.setmode(GPIO.BCM)

#GPIOを入力モードに設定してプルダウン抵抗を有効にする
GPIO.setup(launcher_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(servo_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#GPIOを出力端子設定 
GPIO.setup(pwm_pin, GPIO.OUT)
GPIO.setup(led_green_pin, GPIO.OUT)
GPIO.setup(led_blue_pin, GPIO.OUT) 
GPIO.setup(led_red_pin, GPIO.OUT)

#GPIOをPWM設定、周波数は50Hz 
p = GPIO.PWM(pwm_pin, 50)


#関数の定義
#信号入力を確認
def input_judge(pin):
    while True:
        if GPIO.input(pin) == 1:
            break

#サーボモータを少しずつ閉じる
def servoclose():
    for degree in range(51):
        dc = 2.5 + (11.0-2.5)/50*(50-degree)
        p.ChangeDutyCycle(dc)
        sleep(0.2)
        p.ChangeDutyCycle(0.0)#一旦DutyCycle0%にする        

#入力信号が無くなった7秒後にサーボモータを開く
def servoopen():
    sleep(1)
    while True:
        if GPIO.input(launcher_pin) == 0:
            break
    for i in range(7):  
	    GPIO.output(led_green_pin,0)
	    GPIO.output(led_blue_pin,0)
	    sleep(0.5)
	    GPIO.output(led_green_pin,1)
	    GPIO.output(led_blue_pin,1)
	    sleep(0.5)
    #回転
    p.ChangeDutyCycle(11.0)

#ここから作った。
def roop1():
    i=0
    s = input_judge(servo_pin)
    while i == 0:
        if   s == "0":#ボタンの入力がない場合
            break
        elif s == "1":#ボタンの入力がある場合
            i = 1

    else:
        return 1

def roop2():
    i=0
    s1 = input_judge(servo_pin)    #ボタン
    s2 = input_judge(launcher_pin)    #ランチャーピンの信号　０になるか
    while   i == 0:
        if      s2 == "0":
            break
        if      s1 == "1":
            i = 1
    else :
        return 1



if __name__=="main":
    while True:
        GPIO.output(led_red_pin,1) #信号を出力
        p.start(11.0) #パルス波出力開始(duty比11%)
        print(GPIO.input(servo_pin))
    
        input_judge(servo_pin) #信号の入力を確認
        print(GPIO.input(servo_pin))
        servoclose() #サーボモータを閉じる
        GPIO.output(led_green_pin,1) #信号を出力
        
        #print("正常に作動しています。1でリセット、0で次にすすみます")


        #赤から閉めるまでのプログラム

        if roop1() == 1:
            print("reset")
            continue
            #passの代わりに次に進む

        

        print("roop2")
        
        if roop2() == 1:
            print("reset")
            continue
            #最初に戻る
            input_judge(launcher_pin) #信号の入力を確認
        GPIO.output(led_blue_pin,1) #信号を出力
        GPIO.output(led_red_pin,0) #信号を止める

        print("a")
        servoopen() #サーボモータを開く
        print("a")

        
        ledlist = [led_red_pin,led_green_pin,led_blue_pin] #LED用のピンのリストを作成
        for i in ledlist: #LED用のピンの信号をすべて止める
            GPIO.output(i,0)

        sleep(1)
        
        GPIO.cleanup() #GPIOピンをリセット