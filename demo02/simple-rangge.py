from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader,load_index_from_storage, StorageContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
import os
from llama_index.core import PromptTemplate

# 指定本地大模型
Settings.llm = Ollama(model="qwen2.5:3b", request_timeout=300, temperature=0.1)
# 中文向量模型
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-zh-v1.5")

PERSIST_DIR = "./storage"

# 2. 加载或构建索引
if not os.path.exists(PERSIST_DIR):
    
    print("未检测到本地索引，开始加载文档并构建向量索引...")
    documents = SimpleDirectoryReader("./docs").load_data()
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir=PERSIST_DIR)
    print("索引构建完成，已保存至 ./storage")
else:
    print("检测到本地持久化索引，直接加载...")
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)
# 创建问答引擎
query_engine = index.as_query_engine()

# 发起提问
response = query_engine.query("RAG完整流程是什么？")
print(response)