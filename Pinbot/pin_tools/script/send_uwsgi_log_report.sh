#!/bin/bash

cd /data/pinbot/uwsgi_report/

file_suffix_list="  .1 .2 .3 .4 .5"
data_dictory="/data/pinbot/log/supervisord/pinbot_web.log"

for i in $file_suffix_list; do
    if [ -f $data_dictory$i ]; then
        cat $data_dictory$i > log_tmp
    fi
done

source ~/Pinbot/pin_venv/bin/activate
uwsgi-sloth analyze -f log_tmp --output=report.html
curl http://api.submail.cn/mail/send.json \
    -F appid=11145 \
    -F to=developer\<developer@hopperclouds.com\> \
    -F subject="本周uwsgi访问日志慢请求分析报表" \
    -F text="本周uwgi访问日志分析" \
    --form-string html="<strong>请查看附件</strong>" \
    -F from=pinbot@smail.pinbot.me \
    -F from_name=uwsgi_log_report \
    -F attachments[]=@./report.html \
    -F signature=19fdcf9f37008c63ba1125a74b2db86e
