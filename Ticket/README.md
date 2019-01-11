#### 12306 购票小助手

- python版本支持
  - 2.7.10 - 2.7.15
- 依赖库
  - 依赖若快 若快注册地址：http://www.ruokuai.com/client/index?6726 推荐用若快，打码兔平台已经关闭
  - 项目依赖包 requirements.txt


- 项目使用说明
  - 需要配置邮箱，可以配置可以不配置，配置邮箱的格式在yaml里面可以看到ex
  - 提交订单验证码哪里依赖打码兔，所以如果是订票遇到验证码的时候，没有打码兔是过不了的，不推荐手动，手动太慢
  - 配置yaml文件的时候，需注意空格和遵循yaml语法格式

- 项目开始
  - 服务器启动:
      - 修改config/ticket_config.yaml文件，按照提示更改自己想要的信息
      - 运行根目录sudo python run.py，即可开始
        - 由于新增对时功能，请务必用sudo，sudo，sudo 执行，否则会报权限错误，windows打开ide或者cmd请用管理员身份执行python run.py，不需要加sudo
  - 如果你的服务器安装了docker与docker-compose, 那么就可以通过`docker-compose`进行启动,`docker.sh`脚本对此进行了封装，可以通过如下命令进行启动
      - 1、`sudo ./docker.sh run` #创建一个镜像并启动容器，如果镜像已经创建过了会直接启动容器。
      - 2、`sudo ./docker.sh reload` #修改配置文件后，通过此名命令可重新加载容器运行
      - 3、`sudo ./docker.sh rm` #删除容器
      - 4、`sudo ./docker.sh drun` #后台运行容器
      - 5、`sudo ./docker.sh logs` #在后台运行时，通过此命令查看运行的内容
      - 注: 若只有docker没有docker-compose. 可通过`pip install docker-compose`进行下载
  - ~~如果你的服务器安装了docker，那么就可以docker启动~~
      - 1、~~docker build -t dockerticket .~~
      - 2、~~docker run dockerticket  python run.py &~~
      - 3、~~本来是可以直接Dockerfile启动的，不知道为毛启动不了，如果有大佬看到问题所在，欢迎提出~~
      - 4、~~docker run -d --name 12306-ticket dockerticket~~

	

- 目录对应说明
  - agency - cdn代理
  - config - 项目配置
  - damatuCode - 打码兔接口
  - init - 项目主运行目录
  - myException - 异常
  - myUrllib - urllib库
