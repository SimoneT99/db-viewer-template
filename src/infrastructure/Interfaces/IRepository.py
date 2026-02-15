from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional
from sqlmodel import SQLModel

T = TypeVar("T", bound=SQLModel)
ID = TypeVar("ID")


class IRepository(ABC, Generic[T, ID]):
    """
        Generic repository interface for CRUD operations on SQLModel entities.
        Exception handling is included in the method definitions. 
        NOTE: The exception use a custom RepositoryError exception, if you are lazy you can catch them all using this base exception.
    """


    @abstractmethod
    def get_all(self) -> List[T]:
        """
        Retrieve all items from the repository.

        Raises:
            DatabaseConnectionError: If there is a database connection issue.
            QueryExecutionError: If the query fails to execute.
        """
        pass

    @abstractmethod
    def get_by_id(self, item_id: ID) -> Optional[T]:
        """
        Retrieve a single item by its ID.

        Args:
            item_id (ID): The ID of the item to retrieve.

        Raises:
            InvalidIDError: If the provided ID is invalid.
            DatabaseConnectionError: If there is a database connection issue.
            QueryExecutionError: If the query fails to execute.
        """
        pass

    @abstractmethod
    def add(self, item: list[T]) -> T:
        """
        Add new items to the repository.

        Args:
            item (list(T)): The items to add.

        Raises:
            DatabaseConnectionError: If there is a database connection issue.
            QueryExecutionError: If the query fails to execute.
            CommitError: If the commit operation fails.
        """
        pass

    @abstractmethod
    def update(self, item: T) -> T:
        """
        Update an existing item in the repository.

        Args:
            item (T): The item to update.

        Raises:
            DatabaseConnectionError: If there is a database connection issue.
            QueryExecutionError: If the query fails to execute.
            CommitError: If the commit operation fails.
        """
        pass

    @abstractmethod
    def delete(self, item: T) -> None:
        """
        Delete an item from the repository.

        Args:
            item (T): The item to delete.

        Raises:
            DatabaseConnectionError: If there is a database connection issue.
            QueryExecutionError: If the query fails to execute.
            CommitError: If the commit operation fails.
        """
        pass