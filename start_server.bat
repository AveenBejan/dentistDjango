@ECHO OFF
FOR /F "delims=: tokens=2" %%a in ('ipconfig ^| find "IPv4"') do set _IPAddress=%%a
cd /d %~dp0 & "E:\projects\dentistsite\virtual\Scripts\activate" & python manage.py runserver %_IPAddress%:8080
cmd /k



