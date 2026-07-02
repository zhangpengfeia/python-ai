# """
# python
# """
# # 创建虚拟环境（Python 3.3+）
# python -m venv .venv
#
# # 激活虚拟环境
# # macOS / Linux
# source .venv/bin/activate
#
# # Windows
# .venv\Scripts\activate
#
# # 激活后，pip 安装的包只在该环境中生效
# pip install requests
#
# # 退出虚拟环境
# deactivate
#
# # 使用 venv 管理项目依赖
# # 1. 创建并激活虚拟环境
# python -m venv .venv
# source .venv/bin/activate
# # 2. 安装项目依赖
# pip install -r requirements.txt
# # 3. 开发完成后冻结依赖
# pip freeze > requirements.txt
# # 4. 退出虚拟环境
# deactivate