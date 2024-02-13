#!/bin/bash
yum update -y
yum -y install httpd
chkconfig httpd on
systemctl enable httpd
systemctl start httpd
echo '<h1>Hello From Your Web Server!</h1>' > /var/www/html/index.html
