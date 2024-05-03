# CS307 Project2
#### 小组成员：陈明志 12211414，邱天润 12210829

> 源码托管于 GitHub，将在项目 ddl 结束后基于 **MIT License** 协议开源，访问链接：
>
> https://github.com/RoderickQiu/CS307-Project2

------

### 成员分工及贡献百分比

陈明志：

- Backend Flask的实现
- 通过 Sqlalchemy 实现`connection pool` `trigger`以及用户权限的配置

邱天润：

- 

贡献百分比**相同，均为 50%**。

### 项目源码文件夹结构：

```shell
├─ backend
│  ├─ __init__.py
│  ├─ config.py
│  ├─ controllers.py
│  ├─ models.py
│  └─ urls.py
├── frontend
├── Data_process
│   └─ Process.py
```

- [\_\_init\_\_.py](backend/__init__.py): 使得该文件夹被识别为一个Python包。
- [app.py](backend/app.py): 包含应用程序的主要运行逻辑
- [config.py](backend/config.py): 包含应用程序的配置信息，如数据库连接字符串、密钥等
- [controllers.py](backend/controllers.py): 包含处理请求和响应的控制器函数
- [models.py](backend/models.py): 定义应用程序的数据模型，与数据库表格对应
- [urls.py](backend/urls.py): 定义应用程序的URL路由访问规则
- [Process.py](Data_process/Process.py): 处理或转换数据的脚本，将票价.xlsx转换为csv文件后再转换为可直接用的数据

## 使用指南:
### 本地配置
按照`Requirement.txt`中的版本安装 `Flask` `Flask_Migrate` `flask_sqlalchemy` `SQLAlchemy`
`cd backend`切换到backend目录下后运行`flask run`即可开启后端口

### 基础部分(默认本地路径:http://127.0.0.1:5000)
#### 线路操作

##### 获取所有线路或创建线路

- 请求路径：`/lines`
- 请求方法：`GET`, `POST`
- 描述：获取所有线路的列表或创建新的线路。对于POST方法，需要在Body字段中按照字典的格式添加每一个字段所对应的信息。(`line_name` `business_carriage` `start_time` `end_time` `intro` `mileage` `color` `first_opening` `url`)

##### 获取、更新或删除指定线路

- 请求路径：`/lines/<line_id>`
- 请求方法：`GET`, `PUT`, `DELETE`
- 描述：获取、更新或删除指定ID的线路。对于PUT方法，需要在Body字段中按照字典的格式添加每一个字段更新后所对应的信息。(`line_name` `business_carriage` `start_time` `end_time` `intro` `mileage` `color` `first_opening` `url`)

#### 车站操作

##### 获取所有车站或创建车站

- 请求路径：`/stations`
- 请求方法：`GET`, `POST`
- 描述：获取所有车站的列表或创建新的车站。
  - 对于POST方法，需要在Body字段中按照字典的格式添加每一个字段所对应的信息, Status字段包括三个状态`opening` `closed` `under`。(`English_name` `Chinese_name` `District` `Status` `Introduction`)
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
- 描述：获取、更新或删除指定ID的车站。对于PUT方法，需要在Body字段中按照字典的格式添加每一个字段更新后所对应的信息。, Status字段包括三个状态`opening` `closed` `under`。(`English_name` `Chinese_name` `District` `Status` `Introduction`)

#### 线路和车站操作

##### 获取线路上的所有车站

- 请求路径：`/lines/<line_id>/stations`
- 请求方法：`GET`
- 描述：获取指定线路上的所有车站。

##### 获取、添加或删除线路上的指定车站

- 请求路径：`/lines/<line_id>/stations/<station_id>`
- 请求方法：`GET`, `POST`, `DELETE`
- 描述：
  - 获取、添加或删除线路上的指定车站。在POST方法中，需要在Body字段中按照字典的格式添加每一个字段所对应的信息(`line_num`)。
  - 另外，对于POST方法，我们可以指定station_id为一个数组，如`[1,2,3]`，表示在在line_num位置先后添加station_id为1，2，3的三个车站。

##### 获取线路上指定车站的前后n个车站

- 请求路径：`/lines/<line_id>/stations/<station_id>/n/<n>`
- 请求方法：`GET`
- 描述：获取线路上指定车站的前后n个车站。

注意：在以上的路径中，`<line_id>`、`<station_id>`和`<n>`需要替换为实际的线路ID、车站ID和车站数量。

#### 用户操作

##### 获取所有用户或创建用户

- 请求路径：`/users`
- 请求方法：`GET`, `POST`
- 描述：
  - 获取所有用户的列表或创建新的用户。对于POST方法，需要在Body字段中按照字典的格式添加每一个字段所对应的信息。(`user_id_number` `name` `phone` `gender` `district`)
  - 对于GET方法，我们进行分页，在GET参数中添加`page`和`elem_per_page`字段，表示当前的页数和每页长度；返回值为这样的形式：
      ```
      {
        "page": "1",
        "total": "2000",
        "result": { RESPONSE }
      }
      ```

#### 卡操作

##### 获取所有卡或创建卡

- 请求路径：`/cards`
- 请求方法：`GET`, `POST`
- 描述：
  - 获取所有卡的列表或创建新的卡。对于POST方法，需要在Body字段中按照字典的格式添加每一个字段所对应的信息(`card_number` `money` `create_time`)
  - 对于GET方法，我们进行分页，在GET参数中添加`page`和`elem_per_page`字段，表示当前的页数和每页长度；返回值为这样的形式：
      ```
      {
        "page": "1",
        "total": "2000",
        "result": { RESPONSE }
      }
      ```

#### 卡行程操作

##### 获取所有卡行程或创建卡行程

- 请求路径：`/card_rides`
- 请求方法：`GET`, `POST`
- 描述：获取所有卡行程的列表或创建新的卡行程。对于POST方法(上车)，需要在Body字段中按照字典的格式添加每一个字段所对应的信息。(`card_id` `from_station` `start_time` `business_carriage`)

##### 获取、更新或删除指定卡行程

- 请求路径：`/card_rides/<ride_id>`
- 请求方法：`GET`, `PUT`, `DELETE`
- 描述：获取、更新或删除指定ID的卡行程。对于PUT方法（下车），需要在Body字段中按照字典的格式添加每一个字段更新后所对应的信息。(`to_station` `end_time`)
- 
##### 获取指定卡的所有行程

- 请求路径：`/card_rides/card/<card_id>`
- 请求方法：`GET`
- 描述：获取指定卡的所有行程。

#### 用户行程操作

##### 获取所有用户行程或创建用户行程

- 请求路径：`/user_rides`
- 请求方法：`GET`, `POST`
- 描述：获取所有用户行程的列表或创建新的用户行程。对于POST方法(上车)，需要在Body字段中按照字典的格式添加每一个字段所对应的信息。(`user_id` `from_station` `start_time` `business_carriage`)

##### 获取指定用户的所有行程

- 请求路径：`/user_rides/user/<user_id>`
- 请求方法：`GET`
- 描述：获取指定用户的所有行程。

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
