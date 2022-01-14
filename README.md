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

# # # # 重要点运行prometheus之前请修改prometheus.yml对应的ip地址,并且注释掉alertmanager以及rules<br/>

docker run  -itd --net=host --restart=always --name=prometheus -p 9090:9090 -v /opt/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml  -v /opt/prometheus/rules:/etc/prometheus/rules prom/prometheus  --web.enable-lifecycle --config.file=/etc/prometheus/prometheus.yml
<br/>运行之后浏览器打开：http://xx.xx.xx.xx:9090 查看target,看状态如果全绿为正常状态，如果不正常请检查ip是否通的

![image](https://user-images.githubusercontent.com/97171025/149499269-fbf94676-4b29-4792-a286-e31eb37a89af.png)

<br/>


# 7.安装grafana
新建grafana目录<br/>
mkdir -p /opt/grafana <br/>
运行：
docker run -itd --restart=always --name=grafana -p 3000:3000 -v /opt/grafana:/var/lib/grafana grafana/grafana<br/>

浏览器打开：http://xx.xx.xx.xx:3000 默认账号密码为admin/admin<br/>
![image](https://user-images.githubusercontent.com/97171025/149500781-9844475c-1bcc-433c-ab23-26176bc6d77d.png)<br/>

添加prometheus数据源：<br/>
![image](https://user-images.githubusercontent.com/97171025/149501900-a00f319a-3910-4c56-816f-053564e36c57.png)
![image](https://user-images.githubusercontent.com/97171025/149502053-2b3f6aa8-d708-4f1e-b7b3-824283a04a26.png)
![image](https://user-images.githubusercontent.com/97171025/149502231-bbc354b9-276a-4203-a567-7e64a4dacd4f.png)


导入模板：<br/>
![image](https://user-images.githubusercontent.com/97171025/149501144-33619182-1611-4ad7-b615-a714676b2e8d.png)
![image](https://user-images.githubusercontent.com/97171025/149501306-1dc3fff2-ecfb-4218-8581-d30a3c8685c7.png)

<br/>
模板id对应：
node:9276    mysql:11323   redis:763  mongo:2583 kafka:12460 <br/>
导入之后出现对应的图像<br/>

# 8.安装alertmanager

1.新建相对于的文件夹和对应文件拷贝<br/>
mkdir -p /opt/alertmanager<br/>

把alertmanager.yaml文件复制到/opt/alertmanager下<br/>
运行：<br/>
docker run -itd -p 9093:9093 -v /opt/alertmanager/:/etc/alertmanager/ prom/alertmanager --config.file=/etc/alertmanager/alertmanager.yaml

运行之后打开prometheus的alertmanager注释：<br/>
alerting:<br/>
  alertmanagers:<br/>
  - static_configs:<br/>
      - targets: ['172.31.43.176:9093']<br/>
rule_files:<br/>
  - "rules/*.yml"<br/>

<br/>
修改之后reload prometheus:<br/>
curl -X POST "http://localhost:9090/-/reload"<br/>

然后查看对应的页面alert:<br/>
![image](https://user-images.githubusercontent.com/97171025/149502980-0ea354f7-28d0-48a7-bd4a-414a938fc1de.png)<br/>

# 9.创建telegram机器人<br/>
①首先找到tg官方系统机器人：@BotFather<br/>
点击开始<br/>
之后创建一个机器人,选择newbot选项：<br/>
![image](https://user-images.githubusercontent.com/97171025/149503438-016ccc8d-f5df-418c-913f-52d360619186.png)<br/>
输入bot的名字:注意机器人的名字必须是bot结尾，比如test_ddddd_bot/newyyyy_bot<br/>

之后出现token页：<br/>
![image](https://user-images.githubusercontent.com/97171025/149503490-66fb1832-1744-4340-b22e-a9bf8733d914.png)<br/>
把token复制下来备用<br/>

②.建一个tg群组把新建的机器人拉进去,比如新建的机器人名字test_xxx_bot ，@test_xxx_bot为机器人的名称<br/>

③.把@RawDataBot机器人拉到群组获取chatid信息，拉进去之后出现<br/>
![image](https://user-images.githubusercontent.com/97171025/149503566-06eb26b8-dff6-48f6-a8d6-b81d36e494a3.png)<br/>

把chatid 复制下来备用<br/>
④.保存好token和chatid 把rawdata剔除群组<br/>


# 10.编译运行telegram报警程序：<br/>
打包程序,程序位置：altermanager_hook<br/>
①修改dockerfile的<br/>
CHATID 和 TOKEN的环境变量，在以上获取得到的<br/>

②打包成镜像：
docker  build -t telegram_warn .<br/>

③.运行docker程序
docker run -itd --name=telegram_warn -p 9119:9119   --restart=always telegram_warn <br/>

④测试接口：
运行curl 127.0.0.1:9119 返回success正常 <br/>


# 11。测试telegram报警程序：<br/>
6.修改Prometheus的rule规则host.yml 某一项变小<br/>
比如：
expr: (1 - (node_memory_MemAvailable_bytes{} / (node_memory_MemTotal_bytes{})))* 100 > 80<br/>

改成：<br/>
expr: (1 - (node_memory_MemAvailable_bytes{} / (node_memory_MemTotal_bytes{})))* 100 > 1<br/>

reloa Prometheus: curl -X POST "http://localhost:9090/-/reload"<br/>
查看界面为报警状态：<br/>

![image](https://user-images.githubusercontent.com/97171025/149504002-7df5eebc-1a85-4bd4-9b5e-a28032866c5b.png)<br/>

过一会出现报警：<br/>
![image](https://user-images.githubusercontent.com/97171025/149504233-9c7e3d1e-cb68-4c75-9f21-998b06afccfc.png)<br/>

# 12.把报警规则调回到80%，然后reload prometheus:  curl -X POST "http://localhost:9090/-/reload"<br/>
正常状态<br/>
![image](https://user-images.githubusercontent.com/97171025/149504579-e91af18b-c15d-4618-ae74-badc24a99e65.png)



