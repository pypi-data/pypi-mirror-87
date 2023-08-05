# 机器人工厂引擎
>>>

## 目录
* [安装方式](#安装方式)
* [使用方式](#使用方式)
---
提供的功能有:
* 创建BOT
* 问答管理
* 知识图谱
* 任务引擎
---

## 安装方式
pip安装
```shell
pip install -U bfengine
```
如果比较慢，可以使用清华的pip源：-i https://pypi.tuna.tsinghua.edu.cn/simple

## 使用方式
1.加载BF引擎
```python
import bf_engine

result = bf_engine.init() #加载BF引擎
```

2.使用BF引擎
```python
import bf_engine

# 机器人创建
bot    = bf_engine.create_bot()

# 训练问答语料
bot.qa.train(question_path='data/问答上传模板.xlsx',corpus_path='data/语料上传模板.xlsx')
# 问答语料测试
print('qa出话: ' + bot.qa.query('你好').text)

# 训练知识图谱语料
bot.kg.train(path='data/kg-test.xlsx')
# 知识图谱测试
print('kg出话: ' + bot.kg.query('竹间的年龄').text)

# 加载任务
bot.te.load(path='data/taskengine.json')
# 任务出话
print('te出话: ' + bot.te.query('我要买火车票').text)
print('te出话: ' + bot.te.query('北京').text)
print('te出话: ' + bot.te.query('是的').text)

```
