import sys
import math
import os
import pygame
from pygame import locals
import time

import RPi.GPIO as GPIO

# GPIO set
GPIO.setmode(GPIO.BCM)

GPIO.setup(4, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)


GPIO.setup(22, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)

GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)


pwm1 = GPIO.PWM(4,50)
pwm2 = GPIO.PWM(22,50)
pwm3 = GPIO.PWM(13,50)


x1 = 0
y1 = 0

x2 = 0
y2 = 0

r1 = 0
r2 = 0

s1 = 0
s2 = 0

dc1 = 0
dc2 = 0
dc3 = 0


pwm1.start(dc1)
pwm2.start(dc2)
pwm3.start(dc3)


# 初期化
pygame.init()
pygame.joystick.init()

try:
        # ゲームパッドを認識しているか？
        if pygame.joystick.get_count() == 0:
                print "ゲームパッドがありません。"
                sys.exit("終了")
        else:
                print "ゲームパッドが" + str(pygame.joystick.get_count()) + "個見つかりました。"

        # 最初の一個だけ初期化
        joystick = pygame.joystick.Joystick(0)
        joystick.init()

        # ゲームパッドは６軸１１ボタン
        n_ax = joystick.get_numaxes()
        n_bu = joystick.get_numbuttons()
        n_ha = joystick.get_numhats()

        # 800x600のウインドウを用意する
        size = width, height = 600, 400
        black = 0, 0, 0
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("gamepad demo")
        os.environ['SDL_VIDEO_WINDOW_POS'] = str(0) + "," + str(0)

        # フォント
        font = pygame.font.Font(None, 30)

        # 状態データの保管場所
        axis   = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        button = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        hat    = [0, 0]

        # 軸は左親指の左右、上下、左中指、右親指の左右、上下、右中指
        axispos   = [ ( 10,150), ( 90,150), (170,150), (250,150), (330,150), (410,150)]

        # ボタンは順に、A, B, X, Y, LB, RB, Back, Start, xboxガイドボタン、
        # 右スティック押し込み、左スティック押し込み
        buttonpos = [ ( 30,200), ( 50,200), ( 70,200), ( 90,200), (110,200),
                          (130,200), (150,200), (170,200), (190,200), (210,200),
                          (230,200) ]

        # ハットスイッチ
        # いわゆる十字ボタンのこと。左右、上下で二つデータがある。
        # 左または下が押されると-1、右または上が押されると1になる。
        # 上下が不自然な仕様になっている。
        hatpos    = [ ( 30, 250), ( 50, 250) ]

        # ここから無限ループ
        while 1:
                # ゲームパッドのイベントを確認する
                event = False
                for e in pygame.event.get():
                        event = True
                        if e.type == pygame.locals.JOYAXISMOTION:
                                # 軸
                                for a in range(6):
                                        axis[a] = joystick.get_axis(a)
                        elif e.type == pygame.locals.JOYBUTTONDOWN or e.type == pygame.locals.JOYBUTTONUP:
                                # ボタン
                                for b in range(11):
                                        button[b] = joystick.get_button(b)
                        elif e.type == pygame.locals.JOYHATMOTION:
                                # ハットスイッチ（十字ボタン）
                                hat[0], hat[1] = joystick.get_hat(0)

                if event == False:
                        # 100分の1秒だけスリープする。CPUの利用率がこれでかなり下がる。
                        time.sleep(0.01)
                        continue

                # 画面更新の準備。まずは真っ暗なスクリーンを用意。
                screen.fill(black)

                # 軸の情報を表示
                for a in range(6):
                        label = font.render("%+5.3f" % ( axis[a] ), 1, (225,225,225))
                        screen.blit(label, axispos[a])
        
                # ボタンの情報を表示
                for b in range(11):
                        if button[b] == 0:
                                label = "-"
                                
                        else:
                                label = "*"
                                
                                
                        label = font.render(label, 1, (225,225,225))
                        screen.blit(label, buttonpos[b])

                # ハットスイッチの情報を表示
                for h in range(2):
                        label = font.render("%d" % ( hat[h] ), 1, (225, 225, 225))
                        screen.blit(label, hatpos[h])
                
                # 描画を切り替える
                pygame.display.flip()




                s1 = s2 = 0

                x1 = axis[0]
                y1 = axis[1]

                if ((x1 >= -0.05 and x1 <= 0.05) and (y1 >= -0.05 and y1 <= 0.05)):
                        s1 =0
                else:
                        s1 = (180/math.pi) * math.atan(y1/(x1+0.0000000000001))
                x2 = axis[3]
                y2 = axis[4]
                                                           
                if ((x2 >= -0.05 and x2 <= 0.05) and (y2 >= -0.05 and y2 <= 0.05)):
                        s2 =0
                else:
                        s2 = (180/math.pi) * math.atan(y2/(x2+0.0000000000001))

                s1 = abs(s1)
                s2 = abs(s2)
                
                if x1<0 and y1<0:
                        s1 = 90 + (90-s1)
                elif x1<0 and y1 >0:
                        s1 += 180
                elif x1>0 and y1>0:
                        s1 = 270 + (90-s1)

                s1 = math.floor(s1)
                s2 = math.floor(s2)
                

                if s1 > 87 and s1 < 93:
                        s1 = 90
                if s1 > 177 and s1 < 183:
                        s1 = 180

                if s1 > 57 and s1 < 63:
                        s1 = 60

                if s1 > 117 and s1 < 123:
                        s1 = 120
                if s1 > 327 and s1 < 333:
                        s1 = 330

                
                
                dc1 = math.sin((s1 - 60)) * 60
                dc2 = math.sin((s1 - 300)) * 60
                dc3 = math.sin((s1 - 180)) * 60

                
                dc1 = math.floor(dc1)
                dc2 = math.floor(dc2)
                dc3 = math.floor(dc3)

                go = 60
                ri1 = 15
                ri2 = 55
                ri3 = 60
                le1 = 55
                le2 = 15
                le3 = 60
                
                
                if dc1 < 0:
                        dc1 *= -1
                        i1 = -1

                if dc1 > 100:
                        dc1 = 100
                        
                if dc2 < 0:
                        dc2 *= -1
                        i2 = -1
                        
                if dc2 > 100:
                        dc2 = 100

                if dc3 < 0:
                        dc3 *= -1
                        i3 = -1
                        
                if dc3 > 100:
                        dc3 = 100

                if button[0] == 1:
                        dc1 += 40
                        dc2 += 40
                        dc3 += 40
                        go += 30
                        ri1 += 20
                        ri2 += 30
                        ri3 += 30
                        le1 += 30
                        le2 += 20
                        le3 += 30
                        print "TURBO!!!"

                if  hat[1] == 1:
                        
                        pwm1.ChangeDutyCycle(go)
                        GPIO.output(17,1)
                        GPIO.output(27,0)
                
                        pwm2.ChangeDutyCycle(go)
                        GPIO.output(5,0)
                        GPIO.output(6,1)
                
                        pwm3.ChangeDutyCycle(0)
                        GPIO.output(19,0)
                        GPIO.output(26,0)
                        print "GO!"

                elif hat[1] == -1:
                        pwm1.ChangeDutyCycle(go)
                        GPIO.output(17,0)
                        GPIO.output(27,1)
                
                        pwm2.ChangeDutyCycle(go)
                        GPIO.output(5,1)
                        GPIO.output(6,0)
                
                        pwm3.ChangeDutyCycle(0)
                        GPIO.output(19,0)
                        GPIO.output(26,0)

                        print "Back!"


                elif hat[0] == 1:
                        pwm1.ChangeDutyCycle(ri1)
                        GPIO.output(17,0)
                        GPIO.output(27,1)
                
                        pwm2.ChangeDutyCycle(ri2)
                        GPIO.output(5,0)
                        GPIO.output(6,1)
                
                        pwm3.ChangeDutyCycle(ri3)
                        GPIO.output(19,1)
                        GPIO.output(26,0)

                        print "Right!"

                elif hat[0] == -1:
                        pwm1.ChangeDutyCycle(le1)
                        GPIO.output(17,1)
                        GPIO.output(27,0)
                
                        pwm2.ChangeDutyCycle(le2)
                        GPIO.output(5,1)
                        GPIO.output(6,0)
                
                        pwm3.ChangeDutyCycle(le3)
                        GPIO.output(19,0)
                        GPIO.output(26,1)

                        
                        print "Left!"

                else :
                        pwm1.ChangeDutyCycle(0)
                        GPIO.output(17,0)
                        GPIO.output(27,0)
                        
                        pwm2.ChangeDutyCycle(0)
                        GPIO.output(5,0)
                        GPIO.output(6,0)
                        
                        pwm3.ChangeDutyCycle(0)
                        GPIO.output(19,0)
                        GPIO.output(26,0)

                        if x1>0 and y1<0:
                                pwm1.ChangeDutyCycle(dc1)
                                GPIO.output(17,1)
                                GPIO.output(27,0)
                        
                                pwm2.ChangeDutyCycle(dc2)
                                GPIO.output(5,0)
                                GPIO.output(6,1)
                        
                                pwm3.ChangeDutyCycle(dc3)
                                GPIO.output(19,1)
                                GPIO.output(26,0)

                                print "No1"

                        if x1>0 and y1>0:
                                pwm1.ChangeDutyCycle(dc1)
                                GPIO.output(17,0)
                                GPIO.output(27,1)
                        
                                pwm2.ChangeDutyCycle(dc2)
                                GPIO.output(5,1)
                                GPIO.output(6,0)
                        
                                pwm3.ChangeDutyCycle(dc3)
                                GPIO.output(19,1)
                                GPIO.output(26,0)

                                print "No2"

                        if x1<0 and y1>0:
                                pwm1.ChangeDutyCycle(dc1)
                                GPIO.output(17,1)
                                GPIO.output(27,0)
                        
                                pwm2.ChangeDutyCycle(dc2)
                                GPIO.output(5,1)
                                GPIO.output(6,0)
                        
                                pwm3.ChangeDutyCycle(dc3)
                                GPIO.output(19,0)
                                GPIO.output(26,1)

                                print "No3"

                        if x1<0 and y1<0:
                                pwm1.ChangeDutyCycle(dc1)
                                GPIO.output(17,1)
                                GPIO.output(27,0)
                        
                                pwm2.ChangeDutyCycle(dc2)
                                GPIO.output(5,0)
                                GPIO.output(6,1)
                        
                                pwm3.ChangeDutyCycle(dc3 )
                                GPIO.output(19,0)
                                GPIO.output(26,1)

                                print "No4"

                        if  x1<0.1 and x1>-0.98 and y1<-0.88 and s1==90:
                                pwm1.ChangeDutyCycle(go)
                                GPIO.output(17,1)
                                GPIO.output(27,0)
                        
                                pwm2.ChangeDutyCycle(go)
                                GPIO.output(5,0)
                                GPIO.output(6,1)
                        
                                pwm3.ChangeDutyCycle(0)
                                GPIO.output(19,0)
                                GPIO.output(26,0)
                                print "GO!"
                                
                        if x1<0.1 and x1 > -0.98 and y1>0.88 and s1==90:
                                pwm1.ChangeDutyCycle(go)
                                GPIO.output(17,0)
                                GPIO.output(27,1)
                        
                                pwm2.ChangeDutyCycle(go)
                                GPIO.output(5,1)
                                GPIO.output(6,0)
                        
                                pwm3.ChangeDutyCycle(0)
                                GPIO.output(19,0)
                                GPIO.output(26,0)
                                print "Back!"

                        if x1>0.88 and y1>-0.97 and y1<0.1 and s1==0:
                                pwm1.ChangeDutyCycle(ri1)
                                GPIO.output(17,0)
                                GPIO.output(27,1)
                        
                                pwm2.ChangeDutyCycle(ri2)
                                GPIO.output(5,0)
                                GPIO.output(6,1)
                        
                                pwm3.ChangeDutyCycle(ri3)
                                GPIO.output(19,1)
                                GPIO.output(26,0)

                                print "Right!"

                        if x1<-0.88 and y1>-0.97 and y1<0.1 and s1==0:
                                pwm1.ChangeDutyCycle(le1)
                                GPIO.output(17,1)
                                GPIO.output(27,0)
                        
                                pwm2.ChangeDutyCycle(le2)
                                GPIO.output(5,1)
                                GPIO.output(6,0)
                        
                                pwm3.ChangeDutyCycle(le3)
                                GPIO.output(19,0)
                                GPIO.output(26,1)
                                print "Left!"

                print s1
                time.sleep(0.01)

except KeyboardInterrupt:
        pass


pwm1.stop()
pwm2.stop()
pwm3.stop()

GPIO.cleanup()
