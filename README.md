# CS307-Project2

Spring 2024.

## 使用指南:
### 本地配置
按照`Requirement.txt`中的版本安装 `Flask` `Flask_Migrate` `flask_sqlalchemy` `SQLAlchemy`
`cd backend`切换到backend目录下后运行`flask run`即可开启后端口

### 常用操作(默认本地路径:http://127.0.0.1:5000)
#### 线路操作

##### 获取所有线路或创建线路

- 请求路径：`/lines`
- 请求方法：`GET`, `POST`
- 描述：获取所有线路的列表或创建新的线路。对于POST方法，需要在Body字段中按照字典的格式添加每一个字段所对应的信息。(`start_time` `end_time` `intro` `mileage` `color` `first_opening` `url`)

##### 获取、更新或删除指定线路

- 请求路径：`/lines/<line_id>`
- 请求方法：`GET`, `PUT`, `DELETE`
- 描述：获取、更新或删除指定ID的线路。对于PUT方法，需要在Body字段中按照字典的格式添加每一个字段更新后所对应的信息。(`start_time` `end_time` `intro` `mileage` `color` `first_opening` `url`)

#### 车站操作

##### 获取所有车站或创建车站

- 请求路径：`/stations`
- 请求方法：`GET`, `POST`
- 描述：获取所有车站的列表或创建新的车站。对于POST方法，需要在Body字段中按照字典的格式添加每一个字段所对应的信息。(`English_name` `Chinese_name` `District` `Introduction`)

##### 获取、更新或删除指定车站

- 请求路径：`/stations/<station_id>`
- 请求方法：`GET`, `PUT`, `DELETE`
- 描述：获取、更新或删除指定ID的车站。对于PUT方法，需要在Body字段中按照字典的格式添加每一个字段更新后所对应的信息。(`English_name` `Chinese_name` `District` `Introduction`)

#### 线路和车站操作

##### 获取线路上的所有车站

- 请求路径：`/lines/<line_id>/stations`
- 请求方法：`GET`
- 描述：获取指定线路上的所有车站。

##### 获取、添加或删除线路上的指定车站

- 请求路径：`/lines/<line_id>/stations/<station_id>`
- 请求方法：`GET`, `POST`, `DELETE`
- 描述：获取、添加或删除线路上的指定车站。在POST方法中,需要在Body字段中按照字典的格式添加每一个字段所对应的信息(`line_num`)。

##### 获取线路上指定车站的前后n个车站

- 请求路径：`/lines/<line_id>/stations/<station_id>/n/<n>`
- 请求方法：`GET`
- 描述：获取线路上指定车站的前后n个车站。

注意：在以上的路径中，`<line_id>`、`<station_id>`和`<n>`需要替换为实际的线路ID、车站ID和车站数量。
