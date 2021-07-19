#!usr/bin/env python3
# -*- coding:utf-8-*-

'''
Description: Guardkey
Date: 2021-05-01 09:33:13
LastEditTime: 2021-05-28 20:42:20
FilePath: /keycode/key_monitor.py
Author: Vanchrn
LastEditors: Do not edit
copyright: Copyright (C) 2021 Dumplings. All rights reserved.
'''
from pynput import keyboard
from time import time
import csv 
import numpy as np
from G_container import keytable,container,G4,G110,G111,G112,G113
from keyworld import keyword
import joblib
from verification_code import mail
import os
#from kb_client import Keyboard
import threading

#kb = Keyboard
SEuid = list(range(22))     # time list
SDuid = []
Kuid = list(range(11))  # keyword_list
# Tuid2 = []
# Tuid = list(range(1))
Euid = []   #long text list
long_id = 0
s_id = 0

def on_press(key):
    # on_press
    start_time = int(1000*time())   # time stamp
    try:
        Kuid.append(str(key.char))
        SEuid.append(start_time)
        Kuid.pop(0)
        SEuid.pop(0)
        Euid.append(['keyDown',str(key.char),start_time])
        Euid2Duidb(Euid)
    except AttributeError:
        if str(key)[4:] == 'backspace':
            Kuid.pop()
            SEuid.pop()
            Kuid.insert(0,0)
        else:
            SEuid.append(start_time)
            Kuid.append(str(key)[4:])
            Kuid.pop(0)
            SEuid.pop(0)
        # SEuid.append(start_time)
        # Kuid.append(str(key)[4:])
        # Kuid.pop(0)
        # SEuid.pop(0)
        Euid.append(['keyDown',str(key)[4:],start_time])
        Euid2Duidb(Euid)
    if key == keyboard.Key.esc:
        return False
    

def on_release(key):
    # on_release
    end_time = int(1000*time())
    try:
        Euid.append(['keyUp',str(key.char),end_time])
        SEuid.append(end_time)
        SEuid.pop(0)
        Euid2Duidb(Euid)
    except AttributeError:
        if str(key)[4:] == 'backspace':
            SEuid.pop(-1)
            SEuid.insert(0,0)
            SEuid.insert(0,0)
        else:
            SEuid.append(end_time)
            SEuid.pop(0)
        Euid.append(['keyUp',str(key)[4:],end_time])
        Euid2Duidb(Euid) 
    verify_keyword(Kuid)
        
    # if key == keyboard.Key.esc:
    #     Tuid[0] = (int(time()))
    #     print(Tuid)
    #     if 10<Tuid[0] - Tuid2[0] <30 :
    #         order = input()
    #         if order == '1':
    #             collect_data.write_keyword()
    #             print('录入密码')
    #         elif order == '2':
    #             verify_keyword(Kuid)
    #             print('训练短文本')
    #         elif order == '3':
    #             print('训练长文本')
    #             collect_data.collect_events()
            
    #         elif order == 'l':
    #             system_stop()
            
        # Stop listener

    # Tuid2.clear()

# Collect events until released
def collect_events():
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()

def justify_len(ls):
    if len(ls) == 100:
        # longtext_justify(cal_vector(),"admin4.csv")
        F2csv(cal_vector(),"admin10.csv")
        ls.clear()
    else:
        pass

def cal_vector():
    # calculate vector
    F = []
    for G_i in container:
        if len(G_i) > 0:
            f = np.std(np.array(G_i))
            F.append(f)
        else:
            F.append(0)
        #print(F)
    return F

def F2csv(v,path):
    # store data
    global long_id
    long_id += 1
    with open(path, "a", newline='', encoding='utf-8') as file:
        writer = csv.writer(file ,delimiter=',')
        writer.writerow(v)

def verify_keyword(ls,if_collect = 0):
    # justify keyword
    if ls[0] in keyword:
        print("ok")
        for item in keyword[ls[0]]:
            # print(Kuid[:len(item)],item)
            if Kuid == item:
                RSEuid = SEuid[:2*len(item)]
                print("okklkk:",RSEuid)
                SEuid2SDuid(RSEuid,keyword[ls[0]],if_collect = if_collect)
            else:
                pass

def Euid2Duid(Euid):
    for uid in range(len(Euid)-1):
        try:
            if Euid[uid][1] == Euid[uid+1][1]:
                key = Euid[uid][1]
                try:
                    for index in keytable[key]:
                        container[index-1].append(Euid[uid+1][2]-Euid[uid][2])
                        justify_len(container[index-1])

                except KeyError:
                    G4.append(Euid[uid+1][2]-Euid[uid][2])
                    justify_len(G4)
        
            else:
                G110.append(Euid[uid+1][2]-Euid[uid][2])
                key_a,key_b = Euid[uid][1],Euid[uid+1][1]
                if len(key_a) == 1 and len(key_b) == 1:
                    G112.append(Euid[uid+1][2]-Euid[uid][2])
                    justify_len(G112)
                    #print(G112)
                elif len(key_a) != 1 and len(key_b) != 1:
                    G111.append(Euid[uid+1][2]-Euid[uid][2])
                    justify_len(G111)
                else:
                    G113.append(Euid[uid+1][2]-Euid[uid][2])
                    justify_len(G113)
                    #print(G113)
                del Euid[uid]
        except IndexError:
            pass

def Euid2Duidb(Euid):
    if len(Euid) >=100:
        for uid in range(0,2*len(Euid)-1,2):
            try:
                if Euid[uid][0] == 'keyDown':
                    key = Euid[uid][1]
                    if (Euid[uid][1] == Euid[uid+1][1] and Euid[uid+1][0] == 'keyUp'):
                        try:
                            for index in keytable[key]:
                                container[index-1].append(Euid[uid+1][2]-Euid[uid][2])
                                justify_len(container[index-1])
                                # print('G{0}:'.format(index-1),container[index-1])
                        except KeyError:
                            G4.append(Euid[uid+1][2]-Euid[uid][2])
                            justify_len(G4)
                            # print('G4:',G4)
                    elif Euid[uid+1][1] == 'keyDown':
                        G110.append(Euid[uid+1][2]-Euid[uid][2])
                        # print('G110:',G110)
                        key_a,key_b = Euid[uid][1],Euid[uid+1][1]
                        if len(key_a) == 1 and len(key_b) == 1:
                            G112.append(Euid[uid+1][2]-Euid[uid][2])
                            justify_len(G112)
                            # print('G112:',G112)
                        elif len(key_a) != 1 and len(key_b) != 1:
                            G111.append(Euid[uid+1][2]-Euid[uid][2])
                            justify_len(G111)
                            # print('G111:',G111)
                        else:
                            G113.append(Euid[uid+1][2]-Euid[uid][2])
                            justify_len(G113)
                            # print('G:',G113)
            except IndexError:
                pass
        Euid.clear()
    else:
        pass
       

def SEuid2SDuid(Xuid,key,if_collect = 0):
    for uid in range(len(Xuid)-1):
        try:
            if uid % 2 == 0:
                SDuid.append(Xuid[uid+1]-Xuid[uid])
                SDuid.append(Xuid[uid+2]-Xuid[uid])
            else:
                SDuid.append(Xuid[uid+1]-Xuid[uid])
        except IndexError:
                pass
    if if_collect == 0:
        password_justify(SDuid)
    else:
        F2csv(SDuid,'t_user.csv')
        SDuid.clear()

def longtext_justify(X,path):
    X_test = np.array(X).reshape(1,-1)
    if len(set(X)) > 20:
        # clf = joblib.load("voting_model.m")
        # k_ls = clf.predict_proba(X_test)
        # print(k_ls)
        # k = k_ls[0,-1]
        # if k > 0.8:
        #     F2csv(X,path)
        # else:
        #     system_stop()
        F2csv(X,path)
    else:
        pass
    
def password_justify(X):
    # clf = joblib.load("/Users/chenyao/Documents/keycode/password_model.m")
    # k_ls = clf.predict(np.array(X).reshape(1,-1))
    # k = k_ls[0]
    # if k == 1:
    #     print("开始")
    #     F2csv(SDuid,'t1_user.csv')
    #     print('okkkkkkk')
    # else:
    #     system_stop()
    F2csv(SDuid,'/Users/chenyao/Documents/keycode/t2_user.csv')

    SDuid.clear()
def system_stop():
    #kb.send_winlock()
    os.system('killall kb_client.py')
    code = mail()
    input_code = input()
    for i in range(3):
        input_code = input()
        if input_code == str(code):
            # threads.pop(0)
            # threads[0] = threading.Thread(target = system_initial)
            # threads[0].start()
            for G_i in container:
                G_i.clear()
            print('HYUU')
            break #更改
        else:
            print('入侵停止')
def system_initial():
    os.system('tmux')
    os.system('tmux kill-session')
    os.system('sh setup.sh')
    os.system('sh boot.sh')
    #kb.event_loop()
def system_build():
    print("Setting up keyboard")
    print("starting event loop")
    #kb.event_loop()
threads = []
threads.append(threading.Thread(target=collect_events()))
if __name__ == '__main__':
    threads[0].start()