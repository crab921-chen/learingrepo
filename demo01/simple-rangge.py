from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama

# 指定本地大模型
Settings.llm = Ollama(model="qwen2.5:3b", request_timeout=300)
# 中文向量模型
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-zh-v1.5")

# 读取docs文件夹所有文档
documents = SimpleDirectoryReader("./docs").load_data()
# 构建向量索引
index = VectorStoreIndex.from_documents(documents)
# 创建问答引擎
query_engine = index.as_query_engine()

# 发起提问
response = query_engine.query("RAG完整流程是什么？")
print(response)