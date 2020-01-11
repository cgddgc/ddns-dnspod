# ddns-dnspod
腾讯云ddns脚本


运行环境：

在python3.6、3.7环境测试通过，但在3.5有几率报错（身份验证失败），一直没找到原因，希望知道的能提个issue

使用方法：

在脚本中填入自己腾讯云账户的SecretId、SecretKey、域名以及需要解析的子域名列表，
运行python3 ddns-dnspod.py即可

建议加入计划任务：

crontab -e

*/5 * * * *  nohup python3 ddns-dnspod.py >> ddns.log 2>&1 &

