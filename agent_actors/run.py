import ray
from typing import List
from dotenv import load_dotenv
from faiss import IndexFlatL2
from langchain.agents import Tool
from langchain.callbacks import BaseCallbackManager
from langchain.chat_models import ChatOpenAI
from langchain.chat_models.base import BaseChatModel
from langchain.docstore import InMemoryDocstore
from langchain.embeddings import OpenAIEmbeddings
from langchain.retrievers import TimeWeightedVectorStoreRetriever
from langchain.schema import BaseRetriever
from langchain.vectorstores import FAISS

from agent_actors.callback_manager import ConsolePrettyPrintManager
from agent_actors.child import ChildAgent
from agent_actors.parent import ParentAgent
from agent_actors.toolkit import default_toolkit
from agent_actors.generate_summary import DocSummarizer

class JobHive:
    llm: BaseChatModel
    long_term_memory: BaseRetriever
    callback_manager: BaseCallbackManager
    tools: List[Tool] = []

    def __init__(self):
        load_dotenv()
        self.setup_class()

    def setup_class(self):
        self.callback_manager = ConsolePrettyPrintManager([])
        self.llm = ChatOpenAI(
            temperature=0.25,
            model_name="gpt-3.5-turbo",
            callback_manager=self.callback_manager,
            max_tokens=1024,
            streaming=True
        )
        self.tools = default_toolkit()
        self.long_term_memory = TimeWeightedVectorStoreRetriever(
            vectorstore=FAISS(
                embedding_function=OpenAIEmbeddings().embed_query,
                index=IndexFlatL2(1536),
                docstore=InMemoryDocstore({}),
                index_to_docstore_id={},
            )
        )
        ray.init()

    def create_child(
        self, name: str, traits: List[str], max_iterations=5
    ) -> ChildAgent:
        return ChildAgent(
            name=name,
            traits=traits,
            max_iterations=max_iterations,
            llm=self.llm,
            long_term_memory=self.long_term_memory,
            tools=self.tools,
            callback_manager=self.callback_manager,
        )

    def create_parent(
        self, name: str, traits: List[str], max_iterations=1, **kwargs
    ) -> ParentAgent:
        return ParentAgent(
            **kwargs,
            name=name,
            traits=traits,
            max_iterations=max_iterations,
            llm=self.llm,
            # tools=self.tools,
            long_term_memory=self.long_term_memory,
            callback_manager=self.callback_manager,
        )

    def run(self):
        resume_summarizer = DocSummarizer(
            db_dir="./client_data/chroma",
            file_path="./client_data/documents/doc.pdf",
        )
        task = "User needs a list of 5 urls to job postings that would be a good fit for the person described below: \
            {summary}"
        query = """
        Analyze my resume and provide a well-written summary that highlights
        my key skills and professional experience. Refer to me by name in your response.
        """
        summary = resume_summarizer.run(query)
        task_with_custom_summary = task.format(summary=summary['output_text'])

        jiang = self.create_child(
            name="Jiang",
            traits=["job-search-strategist", "market-savvy", "analytical", "communicative",
                    "detail-oriented", "empathetic"],
        )

        siobhan = self.create_child(
            name="Siobhan",
            traits=["career-coach", "empathetic", "insightful", "motivating", "supportive", "communicative"],
        )

        llamar = self.create_child(
            name="Llamar",
            traits=["resume-writer", "detailed-oriented", "creative", "persuasive", "customizing", "articulate"],
        )

        kendall = self.create_child(
            name="Kendall",
            traits=["interview-coach", "observant", "constructive", "encouraging", "patient", "knowledgeable"],
        )

        roman = self.create_child(
            name="Roman",
            traits=["networker", "sociable", "connector", "initiator", "persuasive"],
        )

        logan = self.create_parent(
            name="Logan",
            traits=["project-manager", "organized", "decisive", "communicative", "proactive"],
            max_iterations=3,
            children={0: jiang, 1: siobhan, 2: llamar, 3: kendall, 4: roman},
        )

        logan.run(
            task=task_with_custom_summary
        )

if __name__ == "__main__":
    jobhive = JobHive()
    jobhive.run()
