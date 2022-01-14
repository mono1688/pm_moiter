# 1.在每台机器上安装相对应的node监控
docker run -itd --name=node-exporter  -p 9100:9100 --restart=always -v "/proc:/host/proc:ro" -v "/sys:/host/sys:ro" -v "/:/rootfs:ro" --net="host" prom/node-exporter

# 2.安装mysql-exporter
①mysql本机授权<br/><br/>
create user 'exporter'@'127.0.0.1' IDENTIFIED BY '密码'<br/>
GRANT REPLICATION CLIENT, PROCESS ON *.* TO 'exporter'@'127.0.0.1'  ;<br/>
GRANT GRANT SELECT ON performance_schema.* TO 'exporter'@'127.0.0.1'  ;<br/>
ALTER USER 'exporter'@'127.0.0.1' IDENTIFIED WITH mysql_native_password BY '密码';<br/>
flush privileges； <br/>

②安装mysql-exporter<br/>
一。下载mysql-exporter 地址：<br/>
https://github.com/prometheus/mysqld_exporter/releases/download/v0.13.0/mysqld_exporter-0.13.0.linux-amd64.tar.gz<br/>

解压到/opt/mysql-export目录下<br/>

二。在/opt/mysql-export创建.my.cnf文件<br/>
内容如下：<br/>
[client]<br/>
host=127.0.0.1<br/>
port=3306<br/>
user=exporter<br/>
password=密码<br/>

三。加入到systemctl环境下运行<br/>
vim /usr/lib/systemd/system/mysql_exporter.service<br/>

[Unit]<br/>
Description=mysql_exporter<br/>
After=network.target<br/>
Documentation= https://github.com/prometheus/mysqld_exporter<br/>
[Service]<br/>
Type=simple<br/>
ExecStart=/opt/mysqld_exporter/mysqld_exporter --config.my-cnf=/opt/mysqld_exporter/.my.cnf<br/>
Restart=on-failure<br/>
[Install]<br/>
WantedBy=multi-user.target<br/>

# 3.安装redis-exporter
1.下载redis-exporter 地址：<br/>
https://github.com/oliver006/redis_exporter/releases/download/v1.32.0/redis_exporter-v1.32.0.linux-amd64.tar.gz<br/>
2.解压到/opt/redis-export目录下<br/>
3.加入到系统systemctl下面<br/>

vim /usr/lib/systemd/system/redis_exporter.service<br/>
<br/>
[Unit]<br/>
Description=redis_exporter<br/>
After=network.target<br/>
Documentation= https://github.com/oliver006/redis_exporter<br/>
[Service]<br/>
Type=simple<br/>
ExecStart=/opt/redis_exporter/redis_exporter -redis.addr 127.0.0.1:6379<br/> 
Restart=on-failure<br/>
[Install]<br/>
WantedBy=multi-user.target<br/>

# 4.安装mongodb-exporter

1.下载mongodb-exporter 地址：<br/>
https://github.com/percona/mongodb_exporter/releases/download/v0.11.2/mongodb_exporter-0.11.2.linux-amd64.tar.gz<br/>
2.解压到/opt/mongodb-exporter目录下<br/>
3.加入到系统systemctl下面<br/>

vim /usr/lib/systemd/system/mongodb-exporter.service<br/>
<br/>
[Unit]<br/>
Description=mongodb-exporter<br/>
After=network.target<br/>
Documentation= https://github.com/percona/mongodb_exporter<br/>
[Service]<br/>
Type=simple<br/>
ExecStart=/opt/mongodb_exporter/mongodb_exporter --mongodb.uri=mongodb://172.17.0.1:27017<br/>
Restart=on-failure<br/>
[Install]<br/>
WantedBy=multi-user.target<br/>


# 5.安装kafka-exporter

1.下载kafka-exporter 地址：<br/>
https://github.com/danielqsj/kafka_exporter/releases/download/v1.2.0/kafka_exporter-1.2.0.linux-amd64.tar.gz<br/>
2.解压到/opt/kafka-exporter目录下<br/>
3.加入到系统systemctl下面<br/>

vim /usr/lib/systemd/system/kafka-exporter.service<br/>
<br/>
[Unit]<br/>
Description=kafka-exporter<br/>
After=network.target<br/>
Documentation= https://github.com/danielqsj/kafka_exporter<br/>
[Service]<br/>
Type=simple<br/>
ExecStart=/opt/kafka-exporter/kafka_exporter  --kafka.server=172.31.43.176:9092 --kafka.version=1.1.0 --log.level=info<br/>
Restart=on-failure<br/>
[Install]<br/>
WantedBy=multi-user.target<br/>



# 6.安装prometheus

1.新建相对于的文件夹和对应文件拷贝<br/>
mkdir -p /opt/prometheus<br/>

把rules文件夹复制到/opt/prometheus下<br/>
把prometheus.yml文件复制到/opt/prometheus下<br/>

# # # # 重要点运行prometheus之前请修改prometheus.yml对应的ip地址<br/>

docker run  -itd --net=host --restart=always --name=prometheus -p 9090:9090 -v /opt/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml  -v /opt/prometheus/rules:/etc/prometheus/rules prom/prometheus  --web.enable-lifecycle --config.file=/etc/prometheus/prometheus.yml
<br/>运行之后浏览器打开：http://xx.xx.xx.xx:9090 查看target,看状态如果全绿为正常状态，如果不正常请检查ip是否通的

![image](https://user-images.githubusercontent.com/97171025/149499269-fbf94676-4b29-4792-a286-e31eb37a89af.png)




