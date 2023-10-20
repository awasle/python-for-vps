import paramiko

servers = [

    {"name": "美国", "hostname": "1.1.1.1", "port": 22, "username": "root", "password": "123456", "domain": "yuming.com"},   
    {"name": "不丹", "hostname": "1.1.1.1", "port": 22, "username": "root", "password": "123456", "domain": "yuming.com"},   
    {"name": "毛里求斯", "hostname": "1.1.1.1", "port": 22, "username": "root", "password": "123456", "domain": "yuming.com"},   
    # 添加更多服务器

]

# 定义更新操作
def update_server(name, hostname, port, username, password, domain):
    try:

        # 连接服务器
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, port=port, username=username, password=password)


        print(f" {name} 更新")
        stdin, stdout, stderr = client.exec_command("apt update -y && apt install -y curl wget sudo socat")
        
        print(f"正在更新:")
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode(), end="")

        # 检查执行状态
        if stderr.channel.recv_exit_status() == 0:
            print(f"更新成功")
        else:
            print(f"更新失败")
        
        print()

        print(f"{name} 安装 Docker")
        stdin, stdout, stderr = client.exec_command("curl -fsSL https://get.docker.com | sh")

        print(f"正在安装 Docker:")
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode(), end="")

        # 检查执行状态
        if stderr.channel.recv_exit_status() == 0:
            print(f"安装 Docker 成功")
        else:
            print(f"安装 Docker 失败")

        print()

        print(f"{name} 安装 Docker Compose")
        stdin, stdout, stderr = client.exec_command('curl -L "https://github.com/docker/compose/releases/download/v2.18.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose')

        print(f"正在安装 Docker Compose:")
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode(), end="")

        # 检查执行状态
        if stderr.channel.recv_exit_status() == 0:
            print(f"安装 Docker Compose 成功")
        else:
            print(f"安装 Docker Compose 失败")

        print()


        print(f"{name} 创建web目录")
        stdin, stdout, stderr = client.exec_command("cd /home && mkdir -p web/html web/mysql web/certs web/redis && touch web/nginx.conf web/docker-compose.yml")

        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode(), end="")

        # 检查执行状态
        if stderr.channel.recv_exit_status() == 0:
            print(f"创建目录成功")
        else:
            print(f"创建目录失败")

        print()

        print(f"{name} 申请证书")
        stdin, stdout, stderr = client.exec_command("curl https://get.acme.sh | sh && ~/.acme.sh/acme.sh --register-account -m xxxx@gmail.com && ~/.acme.sh/acme.sh --issue -d {} --standalone".format(domain))
        print(f"正在申请中:")
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode(), end="")

        # 检查执行状态
        if stderr.channel.recv_exit_status() == 0:
            print(f"申请成功")
        else:
            print(f"申请失败")

        print()

        print(f"{name} 下载证书")
        stdin, stdout, stderr = client.exec_command("~/.acme.sh/acme.sh --installcert -d {} --key-file /home/web/certs/key.pem --fullchain-file /home/web/certs/cert.pem".format(domain))
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode(), end="")

        # 检查执行状态
        if stderr.channel.recv_exit_status() == 0:
            print(f"下载证书成功")
        else:
            print(f"下载证书失败")

        print()        

        print(f"{name} 配置nginx")
        stdin, stdout, stderr = client.exec_command('wget -O /home/web/nginx.conf https://raw.githubusercontent.com/awasle/nginx/main/nginx7.conf && sed -i "s/yuming.com/' + domain + '/g" /home/web/nginx.conf')
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode(), end="")

        # 检查执行状态
        if stderr.channel.recv_exit_status() == 0:
            print(f"配置成功")
        else:
            print(f"配置失败")

        print()

        print(f"{name} 配置docker-compose.yml")
        stdin, stdout, stderr = client.exec_command('wget -O /home/web/docker-compose.yml https://raw.githubusercontent.com/awasle/docker/main/LNMP-docker-compose-2.yml')
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode(), end="")

        # 检查执行状态
        if stderr.channel.recv_exit_status() == 0:
            print(f"配置成功")
        else:
            print(f"配置失败")

        print()

        print(f"{name} 下载网站源码-发卡网站")
        stdin, stdout, stderr = client.exec_command('cd /home/web/html && wget https://github.com/assimon/dujiaoka/releases/download/2.0.6/2.0.6-antibody.tar.gz && apt install -y tar && tar -zxvf 2.0.6-antibody.tar.gz && rm 2.0.6-antibody.tar.gz')
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode(), end="")

        # 检查执行状态
        if stderr.channel.recv_exit_status() == 0:
            print(f"配置成功")
        else:
            print(f"配置失败")


        print()

        print(f"{name} 启动环境")
        stdin, stdout, stderr = client.exec_command('cd /home/web && docker-compose up -d')
        print(f"启动中:")
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode(), end="")

        # 检查执行状态
        if stderr.channel.recv_exit_status() == 0:
            print(f"启动成功")
        else:
            print(f"启动失败")

        print()


        print(f"{name} 赋予文件权限")
        stdin, stdout, stderr = client.exec_command('docker exec nginx chmod -R 777 /var/www/html && docker exec php chmod -R 777 /var/www/html')
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode(), end="")

        # 检查执行状态
        if stderr.channel.recv_exit_status() == 0:
            print(f"赋予成功")
        else:
            print(f"赋予失败")

        print()

        print(f"{name} 安装PHP依赖")
        stdin, stdout, stderr = client.exec_command('docker exec php apt update && docker exec php apt install -y libmariadb-dev-compat libmariadb-dev libzip-dev')
        print(f"安装中:")
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode(), end="")

        # 检查执行状态
        if stderr.channel.recv_exit_status() == 0:
            print(f"安装成功")
        else:
            print(f"安装失败")

        print()

        print(f"{name} 安装PHP扩展")
        stdin, stdout, stderr = client.exec_command('docker exec php docker-php-ext-install pdo_mysql zip bcmath && docker exec php pecl install redis && docker exec php sh -c \'echo "extension=redis.so" > /usr/local/etc/php/conf.d/docker-php-ext-redis.ini\' && docker restart php')
        print(f"安装中:")
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode(), end="")

        # 检查执行状态
        if stderr.channel.recv_exit_status() == 0:
            print(f"安装成功")
        else:
            print(f"安装失败")

        print()




        print(f"搭建完成\nhttps://{domain}")
        print()
        print()


        print()
        print()

        # 关闭 SSH 连接
        client.close()


    except Exception as e:
        print(f"连接 {name} 失败")


# 遍历服务器列表，逐一更新
for server in servers:
    name = server["name"]
    hostname = server["hostname"]
    port = server["port"]
    username = server["username"]
    password = server["password"]
    domain = server["domain"]
    update_server(name, hostname, port, username, password, domain)

# 等待用户按下任意键后关闭窗口
input("按任意键关闭窗口...")


