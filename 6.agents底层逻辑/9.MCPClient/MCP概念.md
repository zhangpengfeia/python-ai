# MCP 协议

MCP 定义了 **Agent** 和 **外部工具** 的 **通信标准** 

https://modelcontextprotocol.io/

## 协议内核

标准中包含：

- 通信角色

  - 客户端 MCP Client：通常是 Agent
  - 服务端 MCP Server：工具提供者

- 通信方式

  - stdio：通过 stdin、stdout 在本地进程间通信
  - http：通过 http 协议通信

- 通信格式：JSON‑RPC 2.0

  ```json
  // json-rpc 示例
  {
    "jsonrpc": "2.0",
    "id": "req-123",
    "method": "tools/call",
    "params": { ... }
  }
  ```

## 客户端

任何匹配 MCP 协议的程序都可以作为 MCP Client

本节课使用 `@modelcontextprotocol/inspector` 充当 MCP Client 客户端，它通常用于调试 MCP Server，可以清楚的看到通信内容

```shell
npx -y @modelcontextprotocol/inspector@1.0.0
```

## 服务端

MCP 聚合站包含了海量 MCP 服务器，常见聚合站：

- [awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers)
- [mcp.so](https://mcp.so/zh)
- [smithery.ai](https://smithery.ai/servers)
- [glama.ai](https://glama.ai/)
- ...

建议:

- 官方的测试服务器 [time](https://github.com/modelcontextprotocol/servers/tree/main/src/time)

  `uvx mcp-server-time`

- 微软官方文档 `Microsoft Learn`

  `https://learn.microsoft.com/api/mcp`

## 通信内容

| 内容       | 备注         |
| ---------- | ------------ |
| initialize | 初始化       |
| tools/list | 发现工具列表 |
| tools/call | 调用工具     |


# 实现MCP服务器

# https://github.com/modelcontextprotocol/python-sdk/tree/v1.28.1
!uv add mcp==1.28.1

```python
from mcp.server.fastmcp import FastMCP
mcp = FastMCP(
    "Weather Service",
    json_response=True,
)

# 工具函数
# https://www.juhe.cn/ 聚合数据有一些免费API接口，有兴趣的同学自行使用
@mcp.tool()
async def get_weather(city: str = "成都") -> dict[str, str]:
    """Get weather data for a city"""
    return {
        "city": city,
        "temperature": "22",
        "condition": "多云",
        "humidity": "65%",
    }
  
# 运行服务
# mcp库底层使用 starlette + uvicorn 启动 http 服务
mcp.run(transport="streamable-http")
# for jupyter
import threading
def run():
    """在独立线程中运行服务器"""
    mcp.run(transport="streamable-http")

t = threading.Thread(target=run)
t.start()


# MCP 测试
!npx -y @modelcontextprotocol/inspector@1.0.0
```