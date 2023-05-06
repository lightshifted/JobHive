import chromadb
from langchain.document_loaders import PyMuPDFLoader
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.llms import PromptLayerOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains.question_answering import load_qa_chain
from dotenv import load_dotenv

class DocSummarizer:
    def __init__(self, db_dir="../client_data/chroma",
                 file_path="../client_data/documents/doc.pdf"):
        self.db_dir = db_dir
        self.file_path = file_path
        load_dotenv()

    def get_documents(self):
        loader = PyMuPDFLoader(self.file_path)
        docs = loader.load()
        text_splitter = CharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=0
        )
        return text_splitter.split_documents(docs)

    def init_chromadb(self):
        client_settings = chromadb.config.Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory=self.db_dir,
        anonymized_telemetry=False
        )

        embeddings=OpenAIEmbeddings()

        vectorstore = Chroma(
        collection_name="langchain_store",
        embedding_function=embeddings,
        client_settings=client_settings,
        persist_directory=self.db_dir,
        )

        vectorstore.add_documents(documents=self.get_documents(), embedding=embeddings)
        vectorstore.persist()


    def query_chromadb(self, query: str):
        client_settings = chromadb.config.Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=self.db_dir,
            anonymized_telemetry=False
        )

        embeddings=OpenAIEmbeddings()

        vectorstore = Chroma(
            collection_name="langchain_store",
            embedding_function=embeddings,
            client_settings=client_settings,
            persist_directory=self.db_dir,
        )
        result = vectorstore.similarity_search_with_score(query=query, k=2)
        return result

    def run(self, query: str):
        self.init_chromadb()
        docs = self.query_chromadb(query=query)

        docs_list = [docs[i][0] for i in range(len(docs))]

        template = """You are a chatbot having a conversation with a job seeker.

        You are a chatbot specializing in job hunting. Given the following information about the job seeker's background, skills, and preferences, as well as a question, provide a helpful and relevant response.

        {context}

        {chat_history}
        Human: {human_input}
        Chatbot:"""

        prompt = PromptTemplate(
            input_variables=["chat_history", "human_input", "context"],
            template=template,
        )

        memory = ConversationBufferMemory(
            memory_key="chat_history", input_key="human_input"
        )

        chain = load_qa_chain(
            PromptLayerOpenAI(
                temperature=0,
                pl_tags=["jobSearch"],
            ),
            chain_type="stuff",
            memory=memory,
            prompt=prompt,
        )
        return chain(
            {"input_documents": docs_list, "human_input": query}, return_only_outputs=True
        )

if __name__ == "__main__":
    DS = DocSummarizer()
    query = "Analyze my resume and provide a well-written summary that highlights my key skills and professional experience. Refer to me by name in your response."
    response = DS.run(query=query)
    print(response)



