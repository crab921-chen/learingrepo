from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader,load_index_from_storage, StorageContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
import os
from llama_index.core import PromptTemplate
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import QueryFusionRetriever
# 指定本地大模型
Settings.llm = Ollama(model="qwen2.5:3b", request_timeout=300)
# 中文向量模型
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-zh-v1.5")

text_splitter = SentenceSplitter(
    chunk_size=512,
    chunk_overlap=260
)
Settings.node_parser = text_splitter

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

class FilteredRetriever(VectorIndexRetriever):
    def _retrieve(self, query_bundle):
        nodes = super()._retrieve(query_bundle)
        threshold = 0.5
        filter_nodes = [n for n in nodes if n.score >= threshold]
        print(f"\n过滤前召回数量：{len(nodes)}，阈值{threshold}，过滤后剩余：{len(filter_nodes)}")
        return filter_nodes

filtered_retriever = FilteredRetriever(index=index, similarity_top_k=3)

# 组装查询引擎
query_engine = RetrieverQueryEngine(
    retriever=filtered_retriever,
)

# 发起提问
response = query_engine.query("简述RAG完整执行流程")

print(response)
print("\n===== 最终送入LLM的文本片段 =====")
for idx, node in enumerate(response.source_nodes):
    print(f"【片段{idx+1}】相似度分数：{node.score:.4f}")
    print(node.text)
    print("-" * 60)