# 简单RAG  Demo04
## 简单介绍
基于前面的学习，了解稀疏检索和稠密检索，实现基础的混合检索，对比稠密检索和混合检索的特点。
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
- 调用模型bge-small-zh-v1.5构建索引并持久化索引
- 用户问题转化为向量，
- 向量检索：召回top3
- 混合检索：融合向量检索和BM25关键词检索
- 大模型给出回答
## 项目目录结构
demo04/
├── docs/                   
├── storage/                
├── venv/                    
├── simple-rangge.py         
├── requirements.txt         
├── .gitignore               
└── README.md  
## 遇到的问题
1. 新版本的LlamaIndex将BM25等拆出去独立分发，需要额外安装llama-index-retrievers-bm25  
2. get_all_nodes()已经废弃，使用get_nodes() 需要强制传入 node_ids，无法一次性读取全部节点
方案：提前加载 documents，通过切片器重新生成 nodes
> parser = Settings.node_parser
nodes = parser.get_nodes_from_documents(documents)

3.index.as_query_engine()和 RetrieverQueryEngine()
-    index.as_query_engine()：进行了封装，只需要传入基础参数，允许直接传 text_qa_template
> query_engine = index.as_query_engine (text_qa_template=qa_prompt)

-  RetrieverQueryEngine()：底层原生组件，无封装，还是可以对Prompt进行处理，只是没有提供对应的接口，需要进行绑定后才可以传入
> response_synthesizer = get_response_synthesizer(
    text_qa_template=qa_prompt
)
> query_engine = RetrieverQueryEngine(
    retriever=fusion_retriever,
    response_synthesizer=response_synthesizer
)

- 二者完成的都是同一个事情（召回处理融合生成答案），第一个是简单的封装，第二个则是可以进行调整