# ddns-dnspod
腾讯云ddns脚本


1. 运行环境：

- python3

- 安装 python3 库

pip3 install -i https://mirrors.tencent.com/pypi/simple/ --upgrade tencentcloud-sdk-python

pip3 install -i https://mirrors.tencent.com/pypi/simple/ --upgrade tencentcloud-sdk-python-dnspod

- 自建 nginx ，获取本机公网 ip
公网服务器的 nginx 加入下面的配置：
'''bash
location /getip {
default_type  text/plain;
return        200 $remote_addr;
}
'''
使用脚本或浏览器访问 http://server/getip ，就可以返回本机的公网地址


2. 使用方法：

在脚本中填入自己腾讯云账户的SecretId、SecretKey、域名以及需要解析的子域名列表，
运行python3 ddns-api30.py即可

建议使用screen维持后台运行：

screen -S ddns

python3 ddns-api30.py

或者加入定时任务

crontab -e

*/5 * * * * python3 ddns-api30.py>>/tmp/ddns.log
