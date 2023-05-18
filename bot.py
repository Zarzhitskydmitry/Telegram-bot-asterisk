#!/usr/bin/python
import config 
import telegram
import os
import subprocess
import sys
import shlex
import datetime
from subprocess import Popen, PIPE
from telegram.ext import CommandHandler, Updater
from importlib import reload
from logging import basicConfig, getLogger, INFO

bot = telegram.Bot(token = config.token)
#Проверка бота
#print(bot.getMe())
updater = Updater(token=config.token, use_context=True)
dispatcher = updater.dispatcher

basicConfig(level=INFO)
log = getLogger()

def run_command(command):
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    global textoutput
    textoutput = ''
    while True:
        global output
        output = process.stdout.readline()
        output = output.decode('utf8')
        if output == '' and process.poll() is not None:
            break
        if output:
            print (output.strip())
        textoutput = textoutput + '\n' + output.strip()
    rc = process.poll()
    return rc


def start(update, context):
    bot.sendMessage(chat_id=update.message.chat_id, text="Привет, жду команды")


def help(update, context):
    reload(config)
    bot.sendMessage(chat_id=update.message.chat_id, text='''список доступных команд:
    /start - startuem
    /id - id пользователя
    /ifconfig - сетевые настройки
    /df - информация о дисковом пространстве (df -h)
    /astertrunk - status
    /sip_reload - перерегистрация SIP'ов
    /sip_show_registry - статус регистрации SIP'ов
    /core_restart_gracefully - "мягкая" перезагрузка Астера
    /core_restart_now - немедленная перезагрузка Asterisk
    /apachestatus - нагрузка на сервере
    /dialplan_reload - перечитывание dialplan'a Астером
    /free - информация о памяти
    /mpstat - информация о нагрузке на процессор
    /dir1 - объем папки''' + config.dir1 + '''
    /dirbackup - размер файла бэкапа за текущий день в папке ''' + config.dir_backup + '''

    ''')

#Функция команды dialplan_reload
def dialplan_r(update, context):
    reload(config)
    user = str(update.message.from_user.id)
    if user in config.admin: #если пользовательский id в списке admin то команда выполняется
        run_command("botdialplanr")
        bot.sendMessage(chat_id=update.message.chat_id, text=textoutput)

def astertrunk(update, context):
    reload(config)
    user = str(update.message.from_user.id)
    if user in config.admin: #если пользовательский id в списке admin то команда выполняется
        run_command("astertrunk")
        bot.sendMessage(chat_id=update.message.chat_id, text=textoutput)


#Функция команды sip_reload
def sip_r(update, context):
    reload(config)
    user = str(update.message.from_user.id)
    if user in config.admin: #если пользовательский id в списке admin то команда выполняется
        run_command("sip_r")
        bot.sendMessage(chat_id=update.message.chat_id, text=textoutput)

#Функция команды core_restart_gracefully
def core_r_g(update, context):
    reload(config)
    user = str(update.message.from_user.id)
    if user in config.admin: #если пользовательский id в списке admin то команда выполняется
        run_command("botcorerg")
        bot.sendMessage(chat_id=update.message.chat_id, text=textoutput)

#Функция команды core_restart_now
def core_r_n(update, context):
    reload(config)
    user = str(update.message.from_user.id)
    if user in config.admin: #если пользовательский id в списке admin то команда выполняется
        run_command("botcorern")
        bot.sendMessage(chat_id=update.message.chat_id, text=textoutput)

#Функция команды sip_show_registry
def sip_s_r(update, context):
    reload(config)
    user = str(update.message.from_user.id)
    if user in config.admin: #если пользовательский id в списке admin то команда выполняется
        run_command("botsipsr")
        bot.sendMessage(chat_id=update.message.chat_id, text=textoutput)

#функция команады id
def myid(update, context):
    userid = update.message.from_user.id
    bot.sendMessage(chat_id=update.message.chat_id, text=userid)

#функция команады ifconfig
def ifconfig(update, context):
    reload(config)
    user = str(update.message.from_user.id)
    if user in config.admin: #если пользовательский id в списке admin то команда выполняется
        run_command("ifconfig")
        bot.sendMessage(chat_id=update.message.chat_id, text=textoutput)

#функция команады df
def df(update, context):
    reload(config)
    user = str(update.message.from_user.id)
    if user in config.admin: #если пользовательский id в списке admin то команда выполняется
        run_command("df -h")
        bot.sendMessage(chat_id=update.message.chat_id, text=textoutput)

#функция команады free
def free(update, context):
    reload(config)
    user = str(update.message.from_user.id)
    if user in config.admin: #если пользовательский id в списке admin то команда выполняется
        run_command("free -m")
        bot.sendMessage(chat_id=update.message.chat_id, text=textoutput)

#функция команады mpstat
def mpstat(update, context):
    reload(config)
    user = str(update.message.from_user.id)
    if user in config.admin: #если пользовательский id в списке admin то команда выполняется
        run_command("mpstat")
        bot.sendMessage(chat_id=update.message.chat_id, text=textoutput)

#функция команады top
def apachestatus(update, context):
    reload(config)
    user = str(update.message.from_user.id)
    if user in config.admin: #если пользовательский id в списке admin то команда выполняется
        run_command("apachestatus")
        bot.sendMessage(chat_id=update.message.chat_id, text=textoutput)

#функция команады dir1
def dir1(update, context):
    reload(config)
    user = str(update.message.from_user.id)
    if user in config.admin: #если пользовательский id в списке admin то команда выполняется
        dir1_command = "du -sh "+ config.dir1
        run_command(dir1_command)
        bot.sendMessage(chat_id=update.message.chat_id, text=textoutput)

#функция команады dirbackup - проверяет наличие файла по дате
def dirbackup(update, context):
    reload(config)
    user = str(update.message.from_user.id)
    if user in config.admin: #если пользовательский id в списке admin то команда выполняется
        now_date = datetime.date.today() # Текущая дата
        cur_year = str(now_date.year) # Год текущий
        cur_month = now_date.month # Месяц текущий
        if cur_month < 10:
            cur_month = str(now_date.month)
            cur_month = '0'+ cur_month
        else:
            cur_month = str(now_date.month)
        cur_day = str(now_date.day) # День текущий
        filebackup = config.dir_backup + cur_year + '-' + cur_month + '-' + cur_day + '.03.00.co.tar.gz'  #формируем имя файла для поиска
        print (filebackup)
        filebackup_command = "ls -lh "+ filebackup
        run_command(filebackup_command)
        bot.sendMessage(chat_id=update.message.chat_id, text=textoutput)




dialplan_r_handler = CommandHandler("dialplan_reload", dialplan_r)
dispatcher.add_handler(dialplan_r_handler)

astertrunk_handler = CommandHandler("astertrunk", astertrunk)
dispatcher.add_handler(astertrunk_handler)

sip_r_handler = CommandHandler("sip_reload", sip_r)
dispatcher.add_handler(sip_r_handler)

core_r_g_handler = CommandHandler("core_restart_gracefully", core_r_g)
dispatcher.add_handler(core_r_g_handler)

core_r_n_handler = CommandHandler("core_restart_now", core_r_n)
dispatcher.add_handler(core_r_n_handler)

sip_s_r_handler = CommandHandler("sip_show_registry", sip_s_r)
dispatcher.add_handler(sip_s_r_handler)

start_handler = CommandHandler("start", start)
dispatcher.add_handler(start_handler)

ifconfig_handler = CommandHandler("ifconfig", ifconfig)
dispatcher.add_handler(ifconfig_handler)

df_handler = CommandHandler("df", df)
dispatcher.add_handler(df_handler)

free_handler = CommandHandler("free", free)
dispatcher.add_handler(free_handler)

mpstat_handler = CommandHandler("mpstat", mpstat)
dispatcher.add_handler(mpstat_handler)

apachestatus_handler = CommandHandler("apachestatus", apachestatus)
dispatcher.add_handler(apachestatus_handler)

dir1_handler = CommandHandler("dir1", dir1)
dispatcher.add_handler(dir1_handler)

dirbackup_handler = CommandHandler("dirbackup", dirbackup)
dispatcher.add_handler(dirbackup_handler)

myid_handler = CommandHandler("id", myid)
dispatcher.add_handler(myid_handler)

help_handler = CommandHandler("help", help)
dispatcher.add_handler(help_handler)


updater.start_polling()