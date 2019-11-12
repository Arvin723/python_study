import tkinter as tk
from tkinter import *
import tkinter.messagebox
import json
import os

window = tk.Tk()
window.title('OpenSSH')
et_ssh = tk.Entry(bd=3, width=40)
et_txt = tk.Entry(bd=3, width=40)
MAXNUM = 10

'''
config data
'''
with open("cfg.json") as ff:
    data = json.load(ff)
with open("cfg_old.json", "w") as f:
    json.dump(data, f)
gitPath = data["gitPath"]
addrs = data["addrs"]

'''
global
'''
sshStr = ''
buttonTexts = []

def writeScript():
    fw = open("sshOpen.bat", "w")
    fw.write("start " + gitPath + " sshCmd.bat")
    fw.close()
    fw = open("sshCmd.bat", "w")
    fw.write("ssh " + sshStr)
    fw.close()

def readScript():
    pass

def openScript():
    global sshStr
    sshStr = et_ssh.get()
    if len(sshStr) == 0:
        tk.messagebox.showinfo('打开失败', '地址不能为空')
        return
    writeScript()
    if os.system('sshOpen.bat') != 0:
        tk.messagebox.showinfo('警告', '打开失败')

def saveScript():
    i = len(addrs)
    if i == MAXNUM:
        tk.messagebox.showinfo('添加失败', '数量已达最大,\n请保存至既存条目')
        return
    elif et_txt.get() in addrs:
        tk.messagebox.showinfo('添加失败', '该名称已存在,\n请尝试更改名称')
        return
    elif len(et_ssh.get()) == 0:
        tk.messagebox.showinfo('添加失败', 'ssh地址不能为空')
        return

    var = StringVar()
    var.set(et_txt.get())
    buttonTexts.append(var)
    bt_a = tk.Button(window, textvariable=var, width=40, command=SSHCtrl(i).openSSH)
    bt_b = tk.Button(window, text='保存到此', width=7, command=SSHCtrl(i).saveSSH)
    bt_c = tk.Button(window, text='读取', width=7, command=SSHCtrl(i).loadSSH)
    bt_a.grid(row=i + 3, column=1), bt_b.grid(row=i + 3, column=2), bt_c.grid(row=i + 3, column=3)

    addrs[et_txt.get()] = et_ssh.get()
    with open("cfg.json", "w") as f:
        json.dump(data, f)


class SSHCtrl:
    def __init__(self, index):
        self.index = index

    def openSSH(self):
        global sshStr
        sshStr = addrs[buttonTexts[self.index].get()]
        print(sshStr)
        writeScript()
        if os.system('sshOpen.bat') != 0:
            tk.messagebox.showinfo('警告', '打开失败')

    def saveSSH(self):
        if len(et_ssh.get()) == 0:
            tk.messagebox.showinfo('添加失败', 'ssh地址不能为空')
            return
        if et_txt.get() in addrs:
            tk.messagebox.showinfo('添加失败', '该名称已存在,\n请尝试更改名称')
            return

        oldTxt = buttonTexts[self.index].get()
        buttonTexts[self.index].set(et_txt.get())
        addrs.pop(oldTxt)
        addrs[et_txt.get()] = et_ssh.get()

        with open("cfg.json", "w") as f:
            json.dump(data, f)
        print(addrs)
        print('save: ' + et_txt.get())
        pass

    def loadSSH(self):
        et_txt.delete(0, END)
        et_ssh.delete(0, END)
        et_txt.insert(0, buttonTexts[self.index].get())
        et_ssh.insert(0, addrs[buttonTexts[self.index].get()])


def buju():
    global et_ssh, et_txt
    bt_et = tk.Button(window, text='打开', width=7, command=openScript)
    bt_et2 = tk.Button(window, text='保存', width=7, command=saveScript)
    et_ssh.grid(row=1, column = 1), bt_et.grid(row=1, column = 2), bt_et2.grid(row=1, column = 3)
    et_txt.grid(row=2, column=1)

    i = 0
    for key in addrs:
        if i >= MAXNUM:
            return
        var = StringVar()
        var.set(key)
        buttonTexts.append(var)
        bt_a = tk.Button(window, textvariable=var, width=40, command=SSHCtrl(i).openSSH)
        bt_b = tk.Button(window, text='保存到此', width=7, command=SSHCtrl(i).saveSSH)
        bt_c = tk.Button(window, text='读取', width=7, command=SSHCtrl(i).loadSSH)

        bt_a.grid(row=i+3, column = 1), bt_b.grid(row=i+3, column = 2), bt_c.grid(row=i+3, column = 3)

        i += 1

'''
main pro
'''
buju()
window.mainloop()
