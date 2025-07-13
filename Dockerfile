FROM python:3.10.5

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN python -c "from langchain_huggingface.embeddings import HuggingFaceEmbeddings; \
            embedding_function: HuggingFaceEmbeddings = HuggingFaceEmbeddings(\
            model_name='sentence-transformers/all-mpnet-base-v2', \
            model_kwargs={'device': 'cpu'}, \
            encode_kwargs={'normalize_embeddings': False}\
            )"
