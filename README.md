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
- 描述：获取所有线路的列表或创建新的线路。对于POST方法，需要在Body字段中按照字典的格式添加每一个字段所对应的信息。(`line_name` `start_time` `end_time` `intro` `mileage` `color` `first_opening` `url`)

##### 获取、更新或删除指定线路

- 请求路径：`/lines/<line_id>`
- 请求方法：`GET`, `PUT`, `DELETE`
- 描述：获取、更新或删除指定ID的线路。对于PUT方法，需要在Body字段中按照字典的格式添加每一个字段更新后所对应的信息。(`line_name` `start_time` `end_time` `intro` `mileage` `color` `first_opening` `url`)

#### 车站操作

##### 获取所有车站或创建车站

- 请求路径：`/stations`
- 请求方法：`GET`, `POST`
- 描述：获取所有车站的列表或创建新的车站。
  - 对于POST方法，需要在Body字段中按照字典的格式添加每一个字段所对应的信息。(`English_name` `Chinese_name` `District` `Introduction`)
  - 对于GET方法，我们进行分页，在GET参数中添加`page`和`elem_per_page`字段，表示当前的页数和每页长度；返回值为这样的形式：
      ```
      {
        "page": "1",
        "total": "2000",
        "result": { RESPONSE }
      }
      ```

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

#### 用户操作

##### 获取所有用户或创建用户

- 请求路径：`/users`
- 请求方法：`GET`, `POST`
- 描述：获取所有用户的列表或创建新的用户。对于POST方法，需要在Body字段中按照字典的格式添加每一个字段所对应的信息。(`user_id_number` `name` `phone` `gender` `district`)

#### 卡操作

##### 获取所有卡或创建卡

- 请求路径：`/cards`
- 请求方法：`GET`, `POST`
- 描述：获取所有卡的列表或创建新的卡。对于POST方法，需要在Body字段中按照字典的格式添加每一个字段所对应的信息(`card_number` `money` `create_time`)

#### 卡行程操作

##### 获取所有卡行程或创建卡行程

- 请求路径：`/card_rides`
- 请求方法：`GET`, `POST`
- 描述：获取所有卡行程的列表或创建新的卡行程。对于POST方法(上车)，需要在Body字段中按照字典的格式添加每一个字段所对应的信息。(`card_id` `from_station` `start_time`)

##### 获取、更新或删除指定卡行程

- 请求路径：`/card_rides/<ride_id>`
- 请求方法：`GET`, `PUT`, `DELETE`
- 描述：获取、更新或删除指定ID的卡行程。对于PUT方法（下车），需要在Body字段中按照字典的格式添加每一个字段更新后所对应的信息。(`to_station` `end_time`)

#### 用户行程操作

##### 获取所有用户行程或创建用户行程

- 请求路径：`/user_rides`
- 请求方法：`GET`, `POST`
- 描述：获取所有用户行程的列表或创建新的用户行程。对于POST方法(上车)，需要在Body字段中按照字典的格式添加每一个字段所对应的信息。(`user_id` `from_station` `start_time`)

##### 获取、更新或删除指定用户行程

- 请求路径：`/user_rides/<ride_id>`
- 请求方法：`GET`, `PUT`, `DELETE`
- 描述：获取、更新或删除指定ID的用户行程。对于PUT方法（下车），需要在Body字段中按照字典的格式添加每一个字段更新后所对应的信息。(`to_station` `end_time`)

注意：在以上的路径中，`<ride_id>`需要替换为实际的行程ID。

#### 在线人数操作

##### 获取在线人数

- 请求路径：`/online`
- 请求方法：`GET`
- 描述：获取当前地铁线上还未下车的人数以及其具体信息。
