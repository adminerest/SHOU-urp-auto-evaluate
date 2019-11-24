# 上海海洋大学urp自动评教程序
摆脱手动评教的苦海   

## 依赖的库
* *tkinter* in Python 3+
* beautifulsoup4==4.8.1
* certifi==2019.9.11
* chardet==3.0.4
* idna==2.8
* Pillow==6.2.1
* requests==2.22.0
* soupsieve==1.9.5
* urllib3==1.25.7
 
## 原理
* 模拟登陆获取cookie
* 获取评价列表
* 模拟POST评价信息

## 注意事项
由于urp评教后端强制限定了30秒后才能提交，所有评教过程会有点慢。。。
本程序默认全部最高评价，主观评价是：老师非常好

## 使用教程
```shell script
# Only for  Windows Platform because of the VPN

# 0. recommended
pip install -r requirement.txt

# unrecommened
python setup.py install

# 1. open your vpn in your PC and connect
cd 'C:\Program Files (x86)\Sangfor\SSL\SangforCSClient'

# 2. run
python main.py
```

## 已知问题
暂时不知道会有啥bug，可能有一个bug就是未连接vpn的时候可能没啥反映。。。

部分错误还未进行测试，等教务关掉评教通道以及验证码无法访问的时候再测试

欢迎隔壁提issue  

## finger
adminerest: 1F8F 6972 9033 0BE7 5D82  7A35 81BE 3986 7E8B 1F22

## 贡献代码

**_Fork_** and open **_pull request_** to [here](https://github.com/adminerest/SHOU-urp-auto-evaluate) .