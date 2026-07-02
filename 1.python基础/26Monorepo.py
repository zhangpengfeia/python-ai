"""
单工程多包结构：构建发布问题，依赖边界问题，所有依赖都在一个 pyproject.toml 里
Multirepo：多工程，各个项目独立，包独立，但是协作繁琐，适合各团队独立，版本节奏不一致的开发，代码需要发布才能共享，流水线单独配置
monorepo：单工程，子包模式，一个git仓库管理，统一风格管理，统一框架管理，统一CI
"""
# pyproject.toml
[tool.uv.workspace]
members = [
    "packages/*", # 一般放独立的包
    "app/*", # 一般放应用程序，服务，前端
    "docs/*" # 文档
]
# uv init --lib packages/agents # 初始化包, --lib表示库格式，自动加后端构建能力，会把main放到src里

# 子包导入另一个子包依赖：
[project]
dependencies = [
    "agents",
]
[tool.uv.source]
agents = { workspace = true } # 从本地包中找
