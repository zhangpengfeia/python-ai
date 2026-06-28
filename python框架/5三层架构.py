"""
1.经典三层
api -> model 接口层
 ↓
service -> model  业务逻辑层
 ↓
dao -> model  数据存储层（data access object） 针对每个模型，原子操作

2.模型分化
DTO ← api
BO ← service
model(po) ← dao


"""