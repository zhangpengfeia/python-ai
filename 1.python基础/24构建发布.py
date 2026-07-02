"""
库的开发： 源代码-》构建-》wheel包-》发布-》仓库 -》安装
构建前端：uv,Poetry,PDM
构建后端：hatchling, setuptools, PDM-backend

python -m build -》 读 pyprojects.toml
"""
[project] # 工程描述
name = 'xxx' # 发行名字
version = '1.2.3' # 版本

[tool.hatch.build.targets.wheel] # 配置 wheel包，本质就是zip文件
packages = ["src/xxx"] # 配置 wheel 包目录

# 发布