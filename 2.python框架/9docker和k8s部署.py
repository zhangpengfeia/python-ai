"""
为了保证服务器多应用部署，互不干扰，需要docker解决隔离问题
docker部署：
    1.创建预构建docker脚本
        FROM python:3.14-slim as builder # 轻量级python镜像
        WORKDIR /app # 设置工作目录，不设置自动创建
        RUN pip install uv -i https://mirrors.aliyun.com/pypi/simple/ # 安装uv包
        RUN UV_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/ # 配置uv镜像
        COPY .. # 复制项目代码到容器
        RUN --mount=type=cache,target=/root/.uv cache \
            uv aync --frozen --no-dev --no-editable # 去除虚拟路径
        WORKDIR /app # 创建新的构建系统
        COPY --from=builder /app/.venv /app/.venv # 复制打包后的 .venv 到新的构建系统中
        ENV PATH="/app/.venv/bin:$PATH" # 配置环境变量到目录
        EXPOSE 8080 # 描述信息，没有任何作用
    2.构建镜像
        一个配置文件，就会产生一个镜像
        docker build -t fast-api .
    3.运行容器
        docker run -p 8080:8080 -d \ -name my-app \ -e environment=production \ -restart unless-stopped \ --memory=128m 
        # 运行容器，映射端口，指定容器名称，环境变量，重启策略，内存限制，镜像名称

sll证书指纹：Z2eIJGAW	F0972F5B47C14D4E4298F85D89F843B3C9D8737F
vcp地域：北京 ， id: vpc-6c9jwicq, 
交换机：
    北京二区b: b2 subnet-pi35yi0p , b subnet-6jb4ys59, c subnet-6qyg2i7l, c2 subnet-j5eohxkj
对象存储： 创建测试，生成通，权限读写管理，权限策略管理
    python-ai-1301349525.cos.ap-beijing.myqcloud.com
    python-ai-1301349525  
    python-ai-test-1301349525

ACr：
账号：zhangpengfei_999
公网：crpi-d63mghmzlhoz1myh.cn-beijing.personal.cr.aliyuncs.com/python-ai/zhangpf
专有：crpi-d63mghmzlhoz1myh-vpc.cn-beijing.personal.cr.aliyuncs.com/python-ai/zhangpf


重新打版本号0.1，推送docker镜像到ACR，RDS收费，k8s收费

k8s: 实现高可用，自动部署，扩缩和管理容器化应用程序
运行容器：
    服务器1，服务器2，服务器3...


公网流量 http请求
 ⬇
ingress公网：可以做负载均衡，访问不同的service
 ⬇
service：包含多个pod，service之间内网互通，tcp协议，ser1: 登录，ser2: 订单系统，ser3:ai服务...，访问时访问ser，由ser做负载均衡
 ⬇
pod: 分组，每个pod提供一个服务，可以包含多个容器，一般是一个pod一个容器


"""