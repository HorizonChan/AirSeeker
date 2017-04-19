# AirSeeker
A device based on RaspberryPi and PMS5003 to monitor the air quality in room


基于树莓派和攀藤PMS5003的一个设备，可以用来检测室内空气质量，如PM2.5等。
这个代码每执行一次读取串口的数据一次，然后上传到Yeelink，在Yeelink中设置好微博内容，能够形成以下效果 请访问http://weibo.com/airseeker

将AirSeeker.py中的api key改成你自己的yeelink api，然后将设备的ID也改为你自己的。利用Crontab定时运行即可。

2017年4月19日
