# 简单RAG  Demo
## 项目介绍
一个基于 LlamaIndex 框架，通过读取本地文档，依托本地模型完成问答的小程序。适合理解检索增强生成完整链路
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
- 调用模型bge-small-zh-v1.5构建索引，若索引存在则直接加载索引
- 用户问题转化为向量，检索得到的上下文一并传给大模型
- 大模型给出回答
## 项目目录结构
demo01/
├── docs/                
├── venv/                
├── simple-rangge.py        
├── requirements.txt     
└── .gitignore 
## 与Demo01的区别
- Deno01缺乏索引持久化，导致重启程序都需要进行索引构建，耗费时间
-  Demo02改进
1. 导入所需库函数
> from llama_index.core import load_index_from_storage, StorageContext
> import os

2. 构建或加载索引
> if not os.path.exists(PERSIST_DIR):
    documents = SimpleDirectoryReader("./docs").load_data()
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir=PERSIST_DIR)
else:
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)

3.每一次启动程序大模型的总结都不同，但是内容都大差不差 
- 设置回答的格式
> qa_prompt = PromptTemplate(
    """
请根据下面提供的上下文信息，用连贯完整的段落总结回答问题，不要分点罗列。
上下文信息：
{context_str}
问题：{query_str}
回答：
"""
)
query_engine = index.as_query_engine(text_qa_template=qa_prompt)
-  初始化Ollama模型时，设置温度为0，减少波动(回答基本没有改变)
>  Settings.llm = Ollama(model="qwen2.5:3b", request_timeout=300, temperature=0.1)








