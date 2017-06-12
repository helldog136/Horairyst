#!/bin/bash
kill -SIGKILL $(lsof -ti tcp:4242) || true;
sleep 2;
/usr/local/sbin/daemonize -a -o /var/log/horairyst_backend.log -e /var/log/horairyst_backend.log -c /horairyst/Horairyst/ /horairyst/Horairyst/main.py;
