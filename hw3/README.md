# ДЗ3

## Получить датасет с Kaggle
Взяли датасет Chess Games: https://www.kaggle.com/datasets/arevel/chess-games.

Размер датасета: ~4.38 GB.

В первой колонке (```Event```) содержится вид, сыгранной шахматной партии:
* ```Blitz```;
* ```Blitz tournament```;
* ```Bullet```;
* ```Bullet tournament```;
* ```Classical```;
* ```Classical tournament```;
* ```Correspondence```.

Хотим посчитать кол-во сыгранных партий каждого вида. 

## Реализовать MapReduce приложение
Реализовали приложение MapReduce для подсчёта каждой партии — [mapper](./mapper.py) и [reducer](./reducer.py).

## Скорость работы без Hadoop 

## Скорость работы c Hadoop Standalone
С помощью следующей команды положим .csv файл на кластер hadoop:

```hdfs dfs -copyFromLocal /chess_games.csv /chess_games.csv```

Запускаем yarn:

```start-yarn.sh```

## Скорость работы с кластером Hadoop
С помощью следующей команды запустим MapReduce а кластере из трёх нод:
```
    hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
    -files mapper.py,reducer.py \
    -mapper "python3 mapper.py" \
    -reducer "python3 reducer.py" \
    -input /chess_games.csv \
    -output /output
```
<details>
   <summary><b>MapReduce job</b></summary>
   <pre>
2023-12-14 19:10:35,558 INFO mapreduce.Job: Running job: job_1702580996266_0001
2023-12-14 19:10:42,676 INFO mapreduce.Job: Job job_1702580996266_0001 running in uber mode : false
2023-12-14 19:10:42,677 INFO mapreduce.Job:  map 0% reduce 0%
2023-12-14 19:10:59,802 INFO mapreduce.Job:  map 3% reduce 0%
2023-12-14 19:11:01,826 INFO mapreduce.Job:  map 4% reduce 0%
2023-12-14 19:11:02,830 INFO mapreduce.Job:  map 9% reduce 0%
2023-12-14 19:11:08,873 INFO mapreduce.Job:  map 12% reduce 0%
2023-12-14 19:11:11,891 INFO mapreduce.Job:  map 18% reduce 0%
2023-12-14 19:11:31,791 INFO mapreduce.Job:  map 25% reduce 0%
2023-12-14 19:11:38,022 INFO mapreduce.Job:  map 28% reduce 0%
2023-12-14 19:11:39,027 INFO mapreduce.Job:  map 29% reduce 0%
2023-12-14 19:11:42,071 INFO mapreduce.Job:  map 35% reduce 0%
2023-12-14 19:11:43,146 INFO mapreduce.Job:  map 36% reduce 0%
2023-12-14 19:12:01,267 INFO mapreduce.Job:  map 38% reduce 12%
2023-12-14 19:12:02,466 INFO mapreduce.Job:  map 43% reduce 12%
2023-12-14 19:12:07,485 INFO mapreduce.Job:  map 45% reduce 12%
2023-12-14 19:12:08,493 INFO mapreduce.Job:  map 48% reduce 12%
2023-12-14 19:12:09,505 INFO mapreduce.Job:  map 52% reduce 12%
2023-12-14 19:12:13,520 INFO mapreduce.Job:  map 52% reduce 17%
2023-12-14 19:12:22,711 INFO mapreduce.Job:  map 55% reduce 17%
2023-12-14 19:12:25,729 INFO mapreduce.Job:  map 55% reduce 18%
2023-12-14 19:12:27,737 INFO mapreduce.Job:  map 59% reduce 18%
2023-12-14 19:12:28,741 INFO mapreduce.Job:  map 60% reduce 18%
2023-12-14 19:12:31,751 INFO mapreduce.Job:  map 61% reduce 18%
2023-12-14 19:12:33,758 INFO mapreduce.Job:  map 67% reduce 18%
2023-12-14 19:12:35,765 INFO mapreduce.Job:  map 70% reduce 18%
2023-12-14 19:12:37,771 INFO mapreduce.Job:  map 70% reduce 23%
2023-12-14 19:12:38,784 INFO mapreduce.Job:  map 73% reduce 23%
2023-12-14 19:12:41,958 INFO mapreduce.Job:  map 76% reduce 23%
2023-12-14 19:12:44,152 INFO mapreduce.Job:  map 76% reduce 25%
2023-12-14 19:12:52,187 INFO mapreduce.Job:  map 78% reduce 25%
2023-12-14 19:12:53,193 INFO mapreduce.Job:  map 79% reduce 25%
2023-12-14 19:12:54,197 INFO mapreduce.Job:  map 82% reduce 25%
2023-12-14 19:12:56,210 INFO mapreduce.Job:  map 85% reduce 26%
2023-12-14 19:12:57,213 INFO mapreduce.Job:  map 86% reduce 26%
2023-12-14 19:12:58,216 INFO mapreduce.Job:  map 88% reduce 26%
2023-12-14 19:12:59,221 INFO mapreduce.Job:  map 91% reduce 26%
2023-12-14 19:13:02,231 INFO mapreduce.Job:  map 91% reduce 30%
2023-12-14 19:13:08,253 INFO mapreduce.Job:  map 94% reduce 30%
2023-12-14 19:13:09,258 INFO mapreduce.Job:  map 100% reduce 30%
2023-12-14 19:13:14,279 INFO mapreduce.Job:  map 100% reduce 85%
2023-12-14 19:13:15,284 INFO mapreduce.Job:  map 100% reduce 100%
2023-12-14 19:13:16,295 INFO mapreduce.Job: Job job_1702580996266_0001 completed successfully
   </pre>
</details>

<details>
   <summary><b>Все статистики</b></summary>
   <pre>
2023-12-14 19:13:16,382 INFO mapreduce.Job: Counters: 55
	File System Counters
		FILE: Number of bytes read=96762834
		FILE: Number of bytes written=203040626
		FILE: Number of read operations=0
		FILE: Number of large read operations=0
		FILE: Number of write operations=0
		HDFS: Number of bytes read=4379029100
		HDFS: Number of bytes written=159
		HDFS: Number of read operations=104
		HDFS: Number of large read operations=0
		HDFS: Number of write operations=2
		HDFS: Number of bytes read erasure-coded=0
	Job Counters 
		Killed map tasks=1
		Launched map tasks=33
		Launched reduce tasks=1
		Data-local map tasks=33
		Total time spent by all maps in occupied slots (ms)=730673
		Total time spent by all reduces in occupied slots (ms)=92715
		Total time spent by all map tasks (ms)=730673
		Total time spent by all reduce tasks (ms)=92715
		Total vcore-milliseconds taken by all map tasks=730673
		Total vcore-milliseconds taken by all reduce tasks=92715
		Total megabyte-milliseconds taken by all map tasks=748209152
		Total megabyte-milliseconds taken by all reduce tasks=94940160
	Map-Reduce Framework
		Map input records=6256185
		Map output records=6256184
		Map output bytes=84250460
		Map output materialized bytes=96763026
		Input split bytes=2871
		Combine input records=0
		Combine output records=0
		Reduce input groups=7
		Reduce shuffle bytes=96763026
		Reduce input records=6256184
		Reduce output records=7
		Spilled Records=12512368
		Shuffled Maps =33
		Failed Shuffles=0
		Merged Map outputs=33
		GC time elapsed (ms)=1376
		CPU time spent (ms)=102800
		Physical memory (bytes) snapshot=10399490048
		Virtual memory (bytes) snapshot=92861599744
		Total committed heap usage (bytes)=8144289792
		Peak Map Physical memory (bytes)=337944576
		Peak Map Virtual memory (bytes)=2760204288
		Peak Reduce Physical memory (bytes)=250695680
		Peak Reduce Virtual memory (bytes)=2746531840
	Shuffle Errors
		BAD_ID=0
		CONNECTION=0
		IO_ERROR=0
		WRONG_LENGTH=0
		WRONG_MAP=0
		WRONG_REDUCE=0
	File Input Format Counters 
		Bytes Read=4379026229
	File Output Format Counters 
		Bytes Written=159
   </pre>
</details>

Избранные статистики:
```
GC time elapsed (ms)=1376
CPU time spent (ms)=102800
Physical memory (bytes) snapshot=10399490048
Virtual memory (bytes) snapshot=92861599744
```

Соответственно ответ можно посмотреть в папке ```/output``` на hdfs:
```
hdfs dfs -ls /output/
>> -rw-r--r--   3 hadoop supergroup        159 2023-12-14 19:13 /output/part-00000
```
```
hdfs dfs -cat /output/part-00000
>> Blitz  2339574	
>> Blitz tournament  472262	
>> Bullet  1198185	
>> Bullet tournament  546777	
>> Classical  1510811	
>> Classical tournament  165635	
>> Correspondence  22940	
```
