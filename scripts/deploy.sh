#!/bin/bash
# 重启streamlit
source env/bin/activate
pid=$(ps -aux | grep streamlit | grep -v grep | awk '{print $2}')
if [ -n "${pid}" ]; then
    echo "streamlit is running, pid is ${pid}"
    kill  -9  ${pid}
    echo $?
else
    echo "streamlit is not running"
fi

sleep 1
nohup streamlit run memory_show.py >/dev/null 2>&1 &
echo "Restarted streamlit !"