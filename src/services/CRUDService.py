from typing import Generic, List, Optional, TypeVar
from sqlmodel import SQLModel
from src.infrastructure.Interfaces.IRepository import IRepository
from src.infrastructure.Exceptions.RepositoryExceptions import RepositoryError

T = TypeVar("T", bound=SQLModel)

class CRUDService(Generic[T]):
    """A generic CRUD service that provides high-level operations for managing entities.
    
    This service acts as a facade over the repository layer, providing business logic
    and simplified interfaces for common CRUD operations.
    
    Type Parameters:
        T: The entity type, must be a SQLModel subclass.
    
    Attributes:
        repository (IRepository[T, int]): The repository instance used for data access.
    """
    
    def __init__(self, repository: IRepository[T, int]):
        """Initialize the CRUD service with a repository.
        
        Args:
            repository (IRepository[T, int]): The repository instance for data access operations.
        Raises:
            ValueError: If the repository is None.
        """
        if repository is None:
            raise ValueError("Repository cannot be None")
        self.repository = repository
    
    def get_items(self, skip: int = 0, limit: int = 10) -> List[T]:
        """Retrieve a paginated list of items.
        
        Args:
            skip (int, optional): Number of items to skip. Defaults to 0.
            limit (int, optional): Maximum number of items to return. Defaults to 10.
        
        Returns:
            List[T]: A list of items within the specified range.
        
        Raises:
            RepositoryError: If there is an error retrieving items from the repository.
        """
        try:
            items = self.repository.get_all()
        except RepositoryError as e:
            raise RepositoryError(f"Error retrieving items: {str(e)}") from e
        return items[skip:skip + limit]

    def get_item(self, item_id: int) -> Optional[T]:
        """Retrieve a single item by its ID.
        
        Args:
            item_id (int): The unique identifier of the item to retrieve.
        
        Returns:
            Optional[T]: The item if found, None otherwise.
        
        Raises:
            RepositoryError: If there is an error retrieving the item from the repository.
        """
        try:
            return self.repository.get_by_id(item_id)
        except RepositoryError as e:
            raise RepositoryError(f"Error retrieving item with ID {item_id}: {str(e)}") from e

    def create_item(self, item: T) -> T:
        """Create a new item in the repository.
        
        Args:
            item (T): The item to create.
        
        Returns:
            T: The created item with any database-generated fields populated.
        
        Raises:
            RepositoryError: If there is an error creating the item in the repository.
        """
        try:
            return self.repository.add(item)
        except RepositoryError as e:
            raise RepositoryError(f"Error creating item: {str(e)}") from e

    def update_item(self, item_id: int, item_data: dict) -> Optional[T]:
        """Update an existing item with new data.
        
        Args:
            item_id (int): The unique identifier of the item to update.
            item_data (dict): A dictionary containing the fields to update and their new values.
        
        Returns:
            Optional[T]: The updated item if found, None if the item doesn't exist.
        
        Raises:
            DatabaseConnectionError: If there is a database connection issue.
            QueryExecutionError: If the query fails to execute.
            CommitError: If the commit operation fails.
        """
        item = self.repository.get_by_id(item_id)
        if item:
            for key, value in item_data.items():
                setattr(item, key, value)
            self.repository.update(item)
            return item
        return None

    def delete_item(self, item_id: int) -> Optional[T]:
        """Delete an item from the repository.
        
        Args:
            item_id (int): The unique identifier of the item to delete.
        
        Returns:
            Optional[T]: The deleted item if found, None if the item doesn't exist.
        
        Raises:
            DatabaseConnectionError: If there is a database connection issue.
            QueryExecutionError: If the query fails to execute.
            CommitError: If the commit operation fails.
        """
        item = self.repository.get_by_id(item_id)
        if item:
            self.repository.delete(item)
            return item
        return None