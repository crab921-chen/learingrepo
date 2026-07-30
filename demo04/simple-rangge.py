from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader,load_index_from_storage, StorageContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
import os
from llama_index.core import PromptTemplate
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.retrievers.bm25 import BM25Retriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import QueryFusionRetriever
from llama_index.core import get_response_synthesizer
# 指定本地大模型
Settings.llm = Ollama(model="qwen2.5:3b", request_timeout=300)
# 中文向量模型
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-zh-v1.5")

text_splitter = SentenceSplitter(
    chunk_size=512,
    chunk_overlap=80
)
Settings.node_parser = text_splitter

qa_prompt = PromptTemplate("""
【硬性强制规则，最高优先级，不可违反】
1. 你的回答只能完全来源于【上下文资料】。
2. 如果上下文资料不存在与问题相关内容，**只允许输出：【知识库未查询到相关资料】**。
3. 绝对禁止使用你预训练学到的任何外部知识，禁止猜测、拓展、编造信息。

上下文资料：
{context_str}
用户问题：{query_str}
""")
documents = SimpleDirectoryReader("./docs").load_data()

PERSIST_DIR = "./storage"

# 2. 加载或构建索引
if not os.path.exists(PERSIST_DIR):
    print("未检测到本地索引，开始加载文档并构建向量索引...")
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir=PERSIST_DIR)
    print("索引构建完成，已保存至 ./storage")
storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
index = load_index_from_storage(storage_context)

#纯向量检索
vector_retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=3
)
query_engine = RetrieverQueryEngine(
    retriever=vector_retriever
)

# 融合检索：混合稠密+稀疏检索
parser = Settings.node_parser
nodes = parser.get_nodes_from_documents(documents)
bm25_retriever = BM25Retriever.from_defaults(
    nodes=nodes,
    similarity_top_k=3
)

fusion_retriever = QueryFusionRetriever(
    retrievers=[vector_retriever, bm25_retriever],
    num_queries=1,
    use_async=False,
)
response_synthesizer = get_response_synthesizer(
    text_qa_template=qa_prompt
)
query_engine1 = RetrieverQueryEngine(
    retriever=fusion_retriever,
    response_synthesizer=response_synthesizer
)

# 发起提问
response = query_engine.query("C语言指针需要掌握哪些内容？")
print(response)

response1 = query_engine1.query("C语言指针需要掌握哪些内容？")
print(response1)