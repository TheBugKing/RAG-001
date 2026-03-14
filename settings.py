import os

###-----------------------------------------------------------###
### Environment Variables
###-----------------------------------------------------------###
# using local path for now
UPLOAD_FOLDER = "./data/files"

# OpenAI Embedding Model
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"

# Chunk Size
CHUNK_SIZE = 1000

# Chunk Overlap
CHUNK_OVERLAP = 100

# Vector Store Name
VECTOR_STORE_COLLECTION = "rag_vector_001"

# Embedding concurrency: number of chunks per batch; multiple batches run in parallel
EMBEDDING_BATCH_SIZE = 50