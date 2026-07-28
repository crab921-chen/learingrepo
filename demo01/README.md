
# 简单RAG  Demo
## 项目介绍
一个基于 LlamaIndex 框架，通过读取本地文档，依托本地模型完成问答的小程序。适合理解检索增强生成完整链路。
## 技术栈
- 核心框架：LlamaIndex
- 本地大模型：ollama 和qwen2.5:3b
- 中文向量模型：BAAI/bge-small-zh-v1.5
- 运行环境：python 3.10+
## 前置准备
1. 安装ollama客户端：国内下载网速比较慢，甚至可能无法下载，可以复制对应链接到迅雷进行下载
2. 提前设置好环境变量，以便于自定义模型存储路径，避免占用c盘
3. 通过终端输入命令进行拉取对应的模型（模型会自动存放在你设置好的路径中）
## 项目启动
1. 创建并激活虚拟环境
> python -m venv venv
> .\venv\Scripts\Activate.ps1

2. 安装项目所需的依赖
> pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

3. 准备知识库
建立docs文件夹，存放对应的txt文档

4. 启动程序

## 底层执行流程
- SimpleDirectorReader读取文档,文本自动分块
- 调用模型bge-small-zh-v1.5构建索引
- 用户问题转化为向量，检索得到的上下文一并传给大模型
- 大模型给出回答
## 项目目录结构
demo01/
├── docs/                
├── venv/                
├── simple-rangge.py        
├── requirements.txt     
└── .gitignore 
## 不足
每次启动会重复向量化，无法支持向量索引本地持久化


