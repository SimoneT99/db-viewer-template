from typing import Generic, TypeVar, List, Optional, Type
from sqlmodel import SQLModel, Session, select
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from src.infrastructure.Interfaces.IRepository import IRepository
from src.infrastructure.Exceptions.RepositoryExceptions import (
    DatabaseConnectionError,
    QueryExecutionError,
    CommitError
)

T = TypeVar("T", bound=SQLModel)

class SQLModelRepository(IRepository[T, int], Generic[T]):
    
    # Here we should put a dependency injector.
    def __init__(self, model: Type[T], session: Session):
        self.model = model
        self.session = session

    def get_all(self) -> List[T]:
        try:
            statement = select(self.model)
        except OperationalError as e:
            raise DatabaseConnectionError(f"Database connection error in get_all for {self.model.__name__}: {str(e)}") from e
        except SQLAlchemyError as e:
            raise QueryExecutionError(f"Query preparation error in get_all for {self.model.__name__}: {str(e)}") from e
        
        try:
            results = self.session.exec(statement)
            return results.all()
        except OperationalError as e:
            raise DatabaseConnectionError(f"Database connection error executing get_all for {self.model.__name__}: {str(e)}") from e
        except SQLAlchemyError as e:
            raise QueryExecutionError(f"Query execution error in get_all for {self.model.__name__}: {str(e)}") from e

    def get_by_id(self, item_id: int) -> Optional[T]:
        try:
            statement = select(self.model).where(self.model.id == item_id)
        except OperationalError as e:
            raise DatabaseConnectionError(f"Database connection error in get_by_id for {self.model.__name__} with id={item_id}: {str(e)}") from e
        except SQLAlchemyError as e:
            raise QueryExecutionError(f"Query preparation error in get_by_id for {self.model.__name__} with id={item_id}: {str(e)}") from e
        
        try:
            result = self.session.exec(statement).first()
            return result
        except OperationalError as e:
            raise DatabaseConnectionError(f"Database connection error executing get_by_id for {self.model.__name__} with id={item_id}: {str(e)}") from e
        except SQLAlchemyError as e:
            raise QueryExecutionError(f"Query execution error in get_by_id for {self.model.__name__} with id={item_id}: {str(e)}") from e

    def add(self, item: T) -> T:
        try:
            self.session.add(item)
        except OperationalError as e:
            raise DatabaseConnectionError(f"Database connection error in add for {self.model.__name__}: {str(e)}") from e
        except SQLAlchemyError as e:
            raise QueryExecutionError(f"Error adding item in add for {self.model.__name__}: {str(e)}") from e
        
        try:
            self.session.commit()
        except OperationalError as e:
            self.session.rollback()
            raise DatabaseConnectionError(f"Database connection error during commit in add for {self.model.__name__}: {str(e)}") from e
        except SQLAlchemyError as e:
            self.session.rollback()
            raise CommitError(f"Commit error in add for {self.model.__name__}: {str(e)}") from e
        
        try:
            self.session.refresh(item)
        except OperationalError as e:
            raise DatabaseConnectionError(f"Database connection error during refresh in add for {self.model.__name__}: {str(e)}") from e
        except SQLAlchemyError as e:
            raise QueryExecutionError(f"Error refreshing item in add for {self.model.__name__}: {str(e)}") from e
        
        return item

    def update(self, item: T) -> T:
        try:
            self.session.add(item)
        except OperationalError as e:
            raise DatabaseConnectionError(f"Database connection error in update for {self.model.__name__}: {str(e)}") from e
        except SQLAlchemyError as e:
            raise QueryExecutionError(f"Error updating item in update for {self.model.__name__}: {str(e)}") from e
        
        try:
            self.session.commit()
        except OperationalError as e:
            self.session.rollback()
            raise DatabaseConnectionError(f"Database connection error during commit in update for {self.model.__name__}: {str(e)}") from e
        except SQLAlchemyError as e:
            self.session.rollback()
            raise CommitError(f"Commit error in update for {self.model.__name__}: {str(e)}") from e
        
        try:
            self.session.refresh(item)
        except OperationalError as e:
            raise DatabaseConnectionError(f"Database connection error during refresh in update for {self.model.__name__}: {str(e)}") from e
        except SQLAlchemyError as e:
            raise QueryExecutionError(f"Error refreshing item in update for {self.model.__name__}: {str(e)}") from e
        
        return item

    def delete(self, item: T) -> None:
        try:
            self.session.delete(item)
        except OperationalError as e:
            raise DatabaseConnectionError(f"Database connection error in delete for {self.model.__name__}: {str(e)}") from e
        except SQLAlchemyError as e:
            raise QueryExecutionError(f"Error deleting item in delete for {self.model.__name__}: {str(e)}") from e
        
        try:
            self.session.commit()
        except OperationalError as e:
            self.session.rollback()
            raise DatabaseConnectionError(f"Database connection error during commit in delete for {self.model.__name__}: {str(e)}") from e
        except SQLAlchemyError as e:
            self.session.rollback()
            raise CommitError(f"Commit error in delete for {self.model.__name__}: {str(e)}") from e