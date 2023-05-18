#!/bin/bash
# Задаём переменные (Specify variables)
MYSQL_USER="pbxuser"                              # Имя пользователя MySQL (MySQL username)
MYSQL="/usr/bin/mysql"                            # Расположение MySQL (whereis mysql)
MYSQLCHECK="/usr/bin/mysqlcheck"                  # Расположение MySQLcheck (whereis mysqlcheck)
MYSQL_PASSWORD="Ntvysqktc1723" 			# Пароль пользователя MySQL (MySQL password)
EMAIL="rcuur.18@gmail.com"                      # Почтовый адрес для уведомлений (Email address for notification)
TYPE="month"                                      # Интервал времени (SECOND,MINUTE,HOUR,DAY,MONTH,YEAR)
NUMBER="3"                                        # Количество (3 месяца) (the number 3 months)
LOG="/var/log/cdr-temp.log"                       # Лог файл перезаписываемый и отсылаемый на почту(A temporary log file is sent on email as a report)
LOG1="/var/log/cdr-clean.log"                     # Лог файл постоянный (The log file permanent)
data="`date`"

# Чистим лог от старых записей (Clean old log records from)
echo > $LOG

# Делаем запись даты в лог (The date recorded in the log)
echo >> $LOG1
echo "---------=$data=---------" >> $LOG1
echo >> $LOG1

# Чистим asteriskcdrdb.cdr (clean asterisksdrdb.cdr)
if $MYSQL -u$MYSQL_USER -p$MYSQL_PASSWORD -e "delete from asteriskcdrdb.cdr where calldate < DATE_SUB(NOW(), interval $NUMBER $TYPE);"; then
echo >> $LOG1
echo Старые записи из asteriskcdrdb.cdr успешно удалены >> $LOG1
echo >> $LOG1
else
echo Не удалось удалить старые записи из asteriskcdrdb.cdr >> $LOG1
echo >> $LOG1
exit 0
fi

# Чистим asteriskcdrdb.cel (clean asteriskcdrdb.cel)
if $MYSQL -u$MYSQL_USER -p$MYSQL_PASSWORD -e "delete from asteriskcdrdb.cel where eventtime < DATE_SUB(NOW(), interval $NUMBER $TYPE);"; then
echo Старые записи из asteriskcdrdb.cel успешно удалены >> $LOG1
echo >> $LOG1
else
echo Не удалось удалить старые записи из asteriskcdrdb.cel >> $LOG1
echo >> $LOG1
exit 0
fi

# Оптимизируем asteriskcdrdb (optimaze asteriskcdrdb table)
if $MYSQLCHECK -u$MYSQL_USER -p$MYSQL_PASSWORD --optimize asteriskcdrdb; then
echo asteriskcdrdb успешно оптимизирована >> $LOG1
echo >> $LOG1
else
echo Не удалось оптимизировать базу asteriskcdrdb >> $LOG1
echo >> $LOG1
exit 0
fi

echo >> $LOG1
echo "----------Были удалены следующие файлы и папки----------" >> $LOG1

# Чистим папки от файлов записи (Recording you want to delete, and empty folders)
find /var/spool/asterisk/monitor/ -name "*.*" -type f -mtime +91 -print -delete >> $LOG1
find /var/spool/asterisk/monitor/ -type d -empty -print -delete >> $LOG1

# Выводим последние 10 000 записей из временного лога и копируем их в постоянный (Get the last 100,000 records from the temporary log file and copy it to permanent)
grep -A 10000 "$data" $LOG1 >> $LOG

# Отсылаем письмо с логами чистки в теле письма (Send email with progress report)
echo "Отчёт об отчистке старых записей" | mail -s PBX-CDR-CLEANER $EMAIL < $LOG
