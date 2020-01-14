# ddns-dnspod
腾讯云ddns脚本


运行环境：

python3，无需额外安装模块

使用方法：

在脚本中填入自己腾讯云账户的SecretId、SecretKey、域名以及需要解析的子域名列表，
运行python3 ddns-dnspod.py即可

建议使用screen维持后台运行：

screen -S ddns

python3 ddns_dnspod.py

或者加入定时任务

crontab -e

*/5 * * * * python3 ddns_dnspod_noc.py>>/tmp/ddns.log


