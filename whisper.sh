#load date
date=$(date +%y/%m/%d-%H:%M:%S)

#해당되는 프로세스 ID 읽어오기 (read process id with file name 'takeOriginImage.php').
pid=`ps -ef | grep "main.py" | grep -v 'grep' | awk '{print $2}'`

#프로세스ID가 있을 경우, 즉 실행 중일 경우, 메시지를 출력하고 종료.
#If the process ID - that means if it is running, a message and exit.
if [ -z $pid ]
then
python3 /home/pi/whisper/main.py
else
echo $data "can not dual exec process!!!\r\n";
fi
