from abc import ABC, abstractmethod
from typing import Any, Callable
from langchain_core.prompts import ChatPromptTemplate
from biochatter.llm_connect import Conversation
from pydantic import BaseModel


class BaseQueryBuilder(ABC):
    """
    An abstract base class for query builders.
    """

    @property
    def structured_output_prompt(self) -> ChatPromptTemplate:
        """
        Defines a structured output prompt template. This provides a default
        implementation for an API agent that can be overridden by subclasses to
        return a ChatPromptTemplate-compatible object.
        """
        return ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a world class algorithm for extracting information in structured formats.",
                ),
                (
                    "human",
                    "Use the given format to extract information from the following input: {input}",
                ),
                ("human", "Tip: Make sure to answer in the correct format"),
            ]
        )

    @abstractmethod
    def create_runnable(
        self,
        api_fields: "BaseModel",
        conversation: "Conversation",
    ) -> Callable:
        """
        Creates a runnable object for executing queries. Must be implemented by
        subclasses. Should use the LangChain `create_structured_output_runnable`
        method to generate the callable.

        Args:
            api_fields: A Pydantic data model that specifies the fields of the
                API that should be queried.

            conversation: A BioChatter conversation object.

        Returns:
            A callable object that can execute the query.
        """
        pass

    @abstractmethod
    def generate_query(
        self,
        question: str,
        conversation: "Conversation",
    ) -> BaseModel:
        """
        Generates a query object (a parameterised Pydantic model with the fields
        of the API) based on the given question using a BioChatter conversation
        instance. Must be implemented by subclasses.

        Args:
            question (str): The question to be answered.

            conversation: The BioChatter conversation object containing the LLM
                that should parameterise the query.

        Returns:
            A parameterised instance of the query object (Pydantic BaseModel)
        """
        pass


class BaseFetcher(ABC):
    """
    Abstract base class for fetchers. A fetcher is responsible for submitting
    queries (in systems where submission and fetching are separate) and fetching
    and saving results of queries.
    """

    @abstractmethod
    def submit_query(self, request_data):
        """
        Submits a query and retrieves an identifier.
        """
        pass

    @abstractmethod
    def fetch_and_save_results(
        self,
        question_uuid,
        query_return,
        save_path,
        max_attempts=10000,
    ):
        """
        Fetches and saves the results of a query.
        """
        pass


class BaseInterpreter(ABC):
    """
    Abstract base class for result interpreters. The interpreter is aware of the
    nature and structure of the results and can extract and summarise
    information from them.
    """

    @abstractmethod
    def summarise_answer(
        self,
        question: str,
        conversation_factory: Callable,
        file_path: str,
        n_lines: int,
    ) -> str:
        """
        Summarises an answer based on the given parameters.

        Args:
            question (str): The question that was asked.

            conversation_factory (Callable): A function that creates a
                BioChatter conversation.

            file_path (str): The path to the file containing the query results.

            n_lines (int): The number of lines to include from the result file.

        Returns:
            A summary of the answer.

        Todo:
            Genericise (remove file path and n_lines parameters, and use a
            generic way to get the results). The child classes should manage the
            specifics of the results.
        """
        pass
