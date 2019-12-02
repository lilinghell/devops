# devops-console

## Project setup
### 安装pipenv创建一个virtualenv来隔离我们本地的包依赖关系
```
pip install pipenv
```
### 创建虚拟环境
```
cd apps  
pipenv shell
```
### 导入依赖包
```
pipenv install Pipfile
```
### 创建数据库
```
python manage.py makemigrations  
python manage.py migrate
```
### 启动
```
python manage.py runserver
```
### 查看API列表
```
http://127.0.0.1:8000/docs/
```

## 初始话超级管理员用户
### 同样进入虚拟环境
```
pipenv shell
```
### 启用虚拟环境下的Python
```
python manage.py shell
```
### 导入User
```
用户名和密码：admin/admin  
from users.models import User  
User.initial
```
