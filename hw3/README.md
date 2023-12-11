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
Реализовали приложение MapReduce для подсчёта каждой партии — [mapper](/mapper.py) и [reducer](/reducer.py).

## Скорость работы без Hadoop

## Скорость работы c Hadoop Standalone

## Скорость работы с кластером Hadoop
