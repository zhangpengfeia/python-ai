# model/main.py
import asyncio
from sqlalchemy import text
from app.model.engine import get_engine
from app.model.base import Base
from app.model.category import Category   # noqa: F401
from app.model.product import Product     # noqa: F401
from app.model.sku import Sku             # noqa: F401


async def init_db():
    engine = get_engine()
    async with engine.begin() as conn: # 开启事务上下文管理
        await conn.run_sync(Base.metadata.drap_all) # 删除所有表
        await conn.run_sync(Base.metadata.create_all) # 创建所有表单，把 Base记录的所有语句执行
    print("✅ 数据库表创建完成")


async def test_connection():
    engine = get_engine()
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            value = result.scalar()
            print(f"✅ 连接成功！查询结果: {value}")
    except Exception as e:
        print(f"❌ 连接失败: {e}")


async def main():
    await init_db()
    await test_connection()


if __name__ == "__main__":
    asyncio.run(main())