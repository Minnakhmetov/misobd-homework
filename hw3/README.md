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

## Скорость работы с кластером Hadoop
С помощью следующей команды запустим MapReduce а кластере из трёх нод:

```hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
    -files mapper.py,reducer.py \
    -mapper "python3 mapper.py" \
    -reducer "python3 reducer.py" \
    -input /chess_games.csv \
    -output /output
```


