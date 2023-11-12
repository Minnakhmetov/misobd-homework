## Разместим на HDFS файл ~1Gb
```
dd if=/dev/zero of=one_file bs=1M count=1000
```
Получили файл размером ~1Gb

Посмотрим сколько памяти занято на нодах.
Для этого выполним на них команду:
```
df -h .
```
hadoop1:
```
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda2       295G  9.8G  273G   4% /
```
hadoop2:
```
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda2       295G  8.5G  274G   4% /
```
hadoop3:
```
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda2       295G  8.5G  274G   4% /
```
