from dotenv import load_dotenv
import os
import asyncio

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings

load_dotenv()


#Getting all Env variables
document_folder_path = os.getenv("DOCUMENT_FOLDER")
embedding_model = os.getenv("EMBEDDING_MODEL")

vector_database_type = os.getenv("VECTOR_DB")
vector_store_path = os.getenv("VECTOR_STORE_PATH")

chunk_limits = int(os.getenv("MAX_CONTEXT_CHUNKS"))
chunk_size = int(os.getenv("CHUNK_SIZE"))
chunk_overlap = int(os.getenv("CHUNK_OVERLAP"))

openai_api_key = os.getenv("OPENAI_API_KEY")
openai_base_url = os.getenv("OPENAI_BASE_URL")


class IngestDocument:
    
    def __init__(self,document_folder_path : str):
        self.document_folder_path = document_folder_path
        self.splitted_document = None
        self.document_content = None
    
    async def load_document_split_document_content(self):
    
        self.document_content = await PyPDFDirectoryLoader(path=self.document_folder_path).aload()

        if not self.document_content:
            raise ValueError("No documents found in the document folder")

        print(f"Loaded {len(self.document_content)} documents")


        self.splitted_document = await RecursiveCharacterTextSplitter(chunk_size = chunk_size,chunk_overlap=chunk_overlap).atransform_documents(documents=self.document_content)
    
        return self.splitted_document
    
    async def embed_document_vectorstore(self):

        print("Preparing documents for embedding...")

        # Remove invalid or empty chunks
        self.clean_documents = []

        for doc in self.splitted_document:
            if isinstance(doc.page_content, str):
                text = doc.page_content.strip()
                doc.page_content = text
                self.clean_documents.append(doc)


        embedding_service = NVIDIAEmbeddings(base_url=openai_base_url,
                                             api_key=openai_api_key,
                                             model=embedding_model)
        
        if vector_database_type.lower() == "faiss":
            vectorstore = await FAISS.afrom_documents(self.clean_documents,embedding=embedding_service)

        else:
            raise NotImplementedError("Other VectorStores Features Coming Soon...")
        
        os.makedirs(vector_store_path, exist_ok=True)


        vectorstore.save_local(vector_store_path)

        print(f"Vector store saved to {vector_store_path}")

        

async def main():

    print("Starting document ingestion pipeline...")

    ingestor = IngestDocument(document_folder_path)

    await ingestor.load_document_split_document_content()

    print("Documents Loaded & Splitted Succesfully...")

    await ingestor.embed_document_vectorstore()

    print("Document ingestion completed successfully!")



if __name__ == "__main__":
    asyncio.run(main())

    

    

    
    

