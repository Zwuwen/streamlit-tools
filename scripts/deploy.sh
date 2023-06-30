#!/bin/bash
# 重启streamlit
cd /home/zxf/workstation/web/github/streamlit/streamlit-tools
source env/bin/activate
pid=$(ps -aux | grep streamlit | grep -v grep | awk '{print $2}')
if [ -n "${pid}" ]; then
    echo "streamlit is running, pid is ${pid}"
    kill  -9  ${pid}
else
    echo "streamlit is not running"
fi
nohup streamlit run memory_show.py >/dev/null 2>&1 &
echo "Restarted streamlit !"