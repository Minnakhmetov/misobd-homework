# ДЗ1
## Настроим кластер с одним узлом

```
$ apt update

$ apt upgrade

$ sudo iptables -I INPUT -p tcp --dport 9870 -j ACCEPT
$ sudo iptables -I INPUT -p tcp --dport 8020 -j ACCEPT
$ sudo iptables -I INPUT -p tcp --match multiport --dports 9866,9864,9867 -j ACCEPT
$ sudo apt install iptables-persistent
$ sudo netfilter-persistent save

$ sudo apt install default-jdk
$ wget https://dlcdn.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz
$ sudo mkdir /usr/local/hadoop
$ sudo tar -zxf hadoop-*.tar.gz -C /usr/local/hadoop --strip-components 1

$ sudo useradd hadoop -m 
$ sudo passwd hadoop
$ sudo chsh -s /bin/bash hadoop
$ sudo chown -R hadoop:hadoop /usr/local/hadoop

$ echo 'export HADOOP_HOME=/usr/local/hadoop
export HADOOP_HDFS_HOME=$HADOOP_HOME
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_COMMON_HOME=$HADOOP_HOME
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
export HADOOP_OPTS="$HADOOP_OPTS -Djava.library.path=$HADOOP_HOME/lib/native"
export YARN_HOME=$HADOOP_HOME
export PATH="$PATH:${HADOOP_HOME}/bin:${HADOOP_HOME}/sbin"' | sudo tee /etc/profile.d/hadoop.sh >/dev/null

$ sudo sed -i 's|# export JAVA_HOME=|export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64|' /usr/local/hadoop/etc/hadoop/hadoop-env.sh

$ sudo sed -z -i "s|<configuration>.*</configuration>||" /usr/local/hadoop/etc/hadoop/core-site.xml && echo "
<configuration> 
  <property><name>fs.defaultFS</name><value>hdfs://localhost:9000</value></property> 
</configuration>
" | sudo tee --append /usr/local/hadoop/etc/hadoop/core-site.xml &>/dev/null

$ sudo mkdir -p /hadoop/hdfs/{namenode,datanode}
$ sudo chown -R hadoop:hadoop /hadoop

$ sudo sed -z -i "s|<configuration>.*</configuration>||" /usr/local/hadoop/etc/hadoop/hdfs-site.xml && echo "
<configuration>
   <property>
      <name>dfs.replication</name>
      <value>1</value>
   </property>
   <property>
      <name>dfs.name.dir</name>
      <value>file:///hadoop/hdfs/namenode</value>
   </property>
   <property>
      <name>dfs.data.dir</name>
      <value>file:///hadoop/hdfs/datanode</value>
   </property>
</configuration>
" | sudo tee --append /usr/local/hadoop/etc/hadoop/hdfs-site.xml &>/dev/null
```

Заходим под пользователем hadoop.

```
$ su - hadoop
```

Генерируем и добавляем ssh ключ.

```
$ ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
$ cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
$ chmod 0600 ~/.ssh/authorized_keys
```

## Эксперимент 1

Из-под пользователя haddop.

Сгенирируем файл размером 64 МБ.

```
$ python3 << ANIME

import random

random.seed(42)

# 64 megabytes
n_kilobytes = 64 * 1024

with open("test_file", "wb") as f:
    for i in range(n_kilobytes):
        f.write(random.randbytes(1024))

ANIME
```

Проверяем, что нужный размер.

```
$ du -h test_file
64M	test_file
```


Запускаем чистую hdfs.

```
$ rm -rf /hadoop/hdfs/datanode/*
$ hdfs namenode -format
$ start-dfs.h
```

Смотрим сколько место занимает пустая файловая система.

```
$ du -sh /hadoop/hdfs
1.1M	/hadoop/hdfs
```

Записываем файл и смотрим размер файловой системы.

```
$ hdfs dfs -put test_file /
$ du -sh /hadoop
66M	/hadoop/hdfs
```

Вывод: файл занял столько же места, сколько занимает в локальной файловой системе. Оно и понятно: в hdfs-site.xml указывали фактор репликации 1.

## Настроим кластер с тремя узлами

Проделаем конфигурацию из первого пункта на остальных двух узлах.

Далее дописываем в /etc/hosts на всех трех узлах:

```
10.0.10.33 hadoop1
10.0.10.34 hadoop2
10.0.10.35 hadoop3
```

На всех трех узлах меняем хост, на котором запущена namenode:

```
$ sudo sed -i "s/localhost/hadoop1/" /usr/local/hadoop/etc/hadoop/core-site.xml
```

Также меняем фактор репликации:

```
$ sudo sed -z "s|<value>3</value>|<value>1</value>|" /usr/local/hadoop/etc/hadoop/hdfs-site.xml
```

Далее на hadoop1 пишем в /usr/local/hadoop/etc/hadoop/workers хосты, на которых будут хранится данные, то есть запущена datanode:

```
hadoop1
hadoop2
hadoop3
```

На мастере тоже будет запущена datanode, потому что, чтобы фактор репликации равный трем имел смысл, нужно хотя бы три узла, которые будут участвовать в репликации.

## Эксперимент 2

Заходим на hadoop1 и запускаем файловую систему, предварительно отформатировав.

```
$ rm -rf /hadoop/hdfs/datanode/*
$ hdfs namenode -format
$ start-dfs.h
```

Проверяем, что мастер видит все датаноды:

```
$ hdfs dfsadmin -report

...
Live datanodes (3):
...
```

Заходим на все узлы смотрим, сколько занимает пустая файловая система.

На hadoop1:

```
$ du -sh /hadoop/hdfs
1.1M	/hadoop/hdfs
```

На hadoop2 и hadoop3 получаем одинаковый результат:

```
$ du -sh /hadoop/hdfs
52K	/hadoop/hdfs
```

На hadoop1 чуть больше, потому что на нем запущена namenode, в котором хранятся метаданные (namenode).

Заходим на hadoop1 и загружаем файл.

```
$ hdfs dfs -put test_file /
```

Снова измерим размеры.

На hadoop1:

```
$ du -sh /hadoop
66M	/hadoop/hdfs
```

На hadoop2 и hadoop3:

```
$ du -sh /hadoop
65M	/hadoop/hdfs
```

Как и ожидали, файл хранится с фактором репликации 3.

