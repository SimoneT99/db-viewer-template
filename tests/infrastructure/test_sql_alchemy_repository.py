import unittest
from unittest.mock import Mock, MagicMock, patch
from sqlmodel import SQLModel, Field
from sqlalchemy.exc import OperationalError, SQLAlchemyError

from src.infrastructure.Exceptions.RepositoryExceptions import CommitError, DatabaseConnectionError, QueryExecutionError
from src.infrastructure.SQLModelRepository import SQLModelRepository


# Test model for testing purposes
class TestModel(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str


class TestSQLModelRepository(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.mock_session = Mock()
        self.repository = SQLModelRepository(TestModel, self.mock_session)
        self.test_item = TestModel(id=1, name="Test Item")
    
    def tearDown(self):
        """Clean up after each test method"""
        self.mock_session.reset_mock()
    
    # Tests for get_all
    def test_get_all_success(self):
        """Test get_all returns all items successfully"""
        # Arrange
        expected_items = [
            TestModel(id=1, name="Item 1"),
            TestModel(id=2, name="Item 2")
        ]
        mock_result = Mock()
        mock_result.all.return_value = expected_items
        self.mock_session.exec.return_value = mock_result
        
        # Act
        result = self.repository.get_all()
        
        # Assert
        self.assertEqual(result, expected_items)
        self.mock_session.exec.assert_called_once()
    
    def test_get_all_operational_error_on_execution(self):
        """Test get_all raises DatabaseConnectionError on OperationalError during execution"""
        # Arrange
        self.mock_session.exec.side_effect = OperationalError("statement", "params", "orig")
        
        # Act & Assert
        with self.assertRaises(DatabaseConnectionError) as context:
            self.repository.get_all()
        
        self.assertIn("Database connection error executing get_all", str(context.exception))
    
    def test_get_all_sqlalchemy_error_on_execution(self):
        """Test get_all raises QueryExecutionError on SQLAlchemyError during execution"""
        # Arrange
        self.mock_session.exec.side_effect = SQLAlchemyError("Query error")
        
        # Act & Assert
        with self.assertRaises(QueryExecutionError) as context:
            self.repository.get_all()
        
        self.assertIn("Query execution error in get_all", str(context.exception))
    
    # Tests for get_by_id
    def test_get_by_id_success(self):
        """Test get_by_id returns item when found"""
        # Arrange
        expected_item = TestModel(id=1, name="Test Item")
        mock_result = Mock()
        mock_result.first.return_value = expected_item
        self.mock_session.exec.return_value = mock_result
        
        # Act
        result = self.repository.get_by_id(1)
        
        # Assert
        self.assertEqual(result, expected_item)
        self.mock_session.exec.assert_called_once()
    
    def test_get_by_id_not_found(self):
        """Test get_by_id returns None when item not found"""
        # Arrange
        mock_result = Mock()
        mock_result.first.return_value = None
        self.mock_session.exec.return_value = mock_result
        
        # Act
        result = self.repository.get_by_id(999)
        
        # Assert
        self.assertIsNone(result)
    
    def test_get_by_id_operational_error(self):
        """Test get_by_id raises DatabaseConnectionError on OperationalError"""
        # Arrange
        self.mock_session.exec.side_effect = OperationalError("statement", "params", "orig")
        
        # Act & Assert
        with self.assertRaises(DatabaseConnectionError) as context:
            self.repository.get_by_id(1)
        
        self.assertIn("Database connection error executing get_by_id", str(context.exception))
    
    def test_get_by_id_sqlalchemy_error(self):
        """Test get_by_id raises QueryExecutionError on SQLAlchemyError"""
        # Arrange
        self.mock_session.exec.side_effect = SQLAlchemyError("Query error")
        
        # Act & Assert
        with self.assertRaises(QueryExecutionError) as context:
            self.repository.get_by_id(1)
        
        self.assertIn("Query execution error in get_by_id", str(context.exception))
    
    # Tests for add
    def test_add_success(self):
        """Test add successfully adds and returns item"""
        # Arrange
        item = TestModel(id=1, name="New Item")
        
        # Act
        result = self.repository.add(item)
        
        # Assert
        self.mock_session.add.assert_called_once_with(item)
        self.mock_session.commit.assert_called_once()
        self.mock_session.refresh.assert_called_once_with(item)
        self.assertEqual(result, item)
    
    def test_add_operational_error_on_add(self):
        """Test add raises DatabaseConnectionError on OperationalError during add"""
        # Arrange
        self.mock_session.add.side_effect = OperationalError("statement", "params", "orig")
        
        # Act & Assert
        with self.assertRaises(DatabaseConnectionError) as context:
            self.repository.add(self.test_item)
        
        self.assertIn("Database connection error in add", str(context.exception))
    
    def test_add_sqlalchemy_error_on_add(self):
        """Test add raises QueryExecutionError on SQLAlchemyError during add"""
        # Arrange
        self.mock_session.add.side_effect = SQLAlchemyError("Add error")
        
        # Act & Assert
        with self.assertRaises(QueryExecutionError) as context:
            self.repository.add(self.test_item)
        
        self.assertIn("Error adding item in add", str(context.exception))
    
    def test_add_operational_error_on_commit(self):
        """Test add raises DatabaseConnectionError and rolls back on OperationalError during commit"""
        # Arrange
        self.mock_session.commit.side_effect = OperationalError("statement", "params", "orig")
        
        # Act & Assert
        with self.assertRaises(DatabaseConnectionError) as context:
            self.repository.add(self.test_item)
        
        self.mock_session.rollback.assert_called_once()
        self.assertIn("Database connection error during commit in add", str(context.exception))
    
    def test_add_commit_error(self):
        """Test add raises CommitError and rolls back on SQLAlchemyError during commit"""
        # Arrange
        self.mock_session.commit.side_effect = SQLAlchemyError("Commit failed")
        
        # Act & Assert
        with self.assertRaises(CommitError) as context:
            self.repository.add(self.test_item)
        
        self.mock_session.rollback.assert_called_once()
        self.assertIn("Commit error in add", str(context.exception))
    
    def test_add_operational_error_on_refresh(self):
        """Test add raises DatabaseConnectionError on OperationalError during refresh"""
        # Arrange
        self.mock_session.refresh.side_effect = OperationalError("statement", "params", "orig")
        
        # Act & Assert
        with self.assertRaises(DatabaseConnectionError) as context:
            self.repository.add(self.test_item)
        
        self.assertIn("Database connection error during refresh in add", str(context.exception))
    
    def test_add_sqlalchemy_error_on_refresh(self):
        """Test add raises QueryExecutionError on SQLAlchemyError during refresh"""
        # Arrange
        self.mock_session.refresh.side_effect = SQLAlchemyError("Refresh error")
        
        # Act & Assert
        with self.assertRaises(QueryExecutionError) as context:
            self.repository.add(self.test_item)
        
        self.assertIn("Error refreshing item in add", str(context.exception))
    
    # Tests for update
    def test_update_success(self):
        """Test update successfully updates and returns item"""
        # Arrange
        item = TestModel(id=1, name="Updated Item")
        
        # Act
        result = self.repository.update(item)
        
        # Assert
        self.mock_session.add.assert_called_once_with(item)
        self.mock_session.commit.assert_called_once()
        self.mock_session.refresh.assert_called_once_with(item)
        self.assertEqual(result, item)
    
    def test_update_operational_error_on_add(self):
        """Test update raises DatabaseConnectionError on OperationalError during add"""
        # Arrange
        self.mock_session.add.side_effect = OperationalError("statement", "params", "orig")
        
        # Act & Assert
        with self.assertRaises(DatabaseConnectionError) as context:
            self.repository.update(self.test_item)
        
        self.assertIn("Database connection error in update", str(context.exception))
    
    def test_update_sqlalchemy_error_on_add(self):
        """Test update raises QueryExecutionError on SQLAlchemyError during add"""
        # Arrange
        self.mock_session.add.side_effect = SQLAlchemyError("Update error")
        
        # Act & Assert
        with self.assertRaises(QueryExecutionError) as context:
            self.repository.update(self.test_item)
        
        self.assertIn("Error updating item in update", str(context.exception))
    
    def test_update_operational_error_on_commit(self):
        """Test update raises DatabaseConnectionError and rolls back on OperationalError during commit"""
        # Arrange
        self.mock_session.commit.side_effect = OperationalError("statement", "params", "orig")
        
        # Act & Assert
        with self.assertRaises(DatabaseConnectionError) as context:
            self.repository.update(self.test_item)
        
        self.mock_session.rollback.assert_called_once()
        self.assertIn("Database connection error during commit in update", str(context.exception))
    
    def test_update_commit_error(self):
        """Test update raises CommitError and rolls back on SQLAlchemyError during commit"""
        # Arrange
        self.mock_session.commit.side_effect = SQLAlchemyError("Commit failed")
        
        # Act & Assert
        with self.assertRaises(CommitError) as context:
            self.repository.update(self.test_item)
        
        self.mock_session.rollback.assert_called_once()
        self.assertIn("Commit error in update", str(context.exception))
    
    def test_update_operational_error_on_refresh(self):
        """Test update raises DatabaseConnectionError on OperationalError during refresh"""
        # Arrange
        self.mock_session.refresh.side_effect = OperationalError("statement", "params", "orig")
        
        # Act & Assert
        with self.assertRaises(DatabaseConnectionError) as context:
            self.repository.update(self.test_item)
        
        self.assertIn("Database connection error during refresh in update", str(context.exception))
    
    def test_update_sqlalchemy_error_on_refresh(self):
        """Test update raises QueryExecutionError on SQLAlchemyError during refresh"""
        # Arrange
        self.mock_session.refresh.side_effect = SQLAlchemyError("Refresh error")
        
        # Act & Assert
        with self.assertRaises(QueryExecutionError) as context:
            self.repository.update(self.test_item)
        
        self.assertIn("Error refreshing item in update", str(context.exception))
    
    # Tests for delete
    def test_delete_success(self):
        """Test delete successfully deletes item"""
        # Arrange
        item = TestModel(id=1, name="Item to delete")
        
        # Act
        self.repository.delete(item)
        
        # Assert
        self.mock_session.delete.assert_called_once_with(item)
        self.mock_session.commit.assert_called_once()
    
    def test_delete_operational_error_on_delete(self):
        """Test delete raises DatabaseConnectionError on OperationalError during delete"""
        # Arrange
        self.mock_session.delete.side_effect = OperationalError("statement", "params", "orig")
        
        # Act & Assert
        with self.assertRaises(DatabaseConnectionError) as context:
            self.repository.delete(self.test_item)
        
        self.assertIn("Database connection error in delete", str(context.exception))
    
    def test_delete_sqlalchemy_error_on_delete(self):
        """Test delete raises QueryExecutionError on SQLAlchemyError during delete"""
        # Arrange
        self.mock_session.delete.side_effect = SQLAlchemyError("Delete error")
        
        # Act & Assert
        with self.assertRaises(QueryExecutionError) as context:
            self.repository.delete(self.test_item)
        
        self.assertIn("Error deleting item in delete", str(context.exception))
    
    def test_delete_operational_error_on_commit(self):
        """Test delete raises DatabaseConnectionError and rolls back on OperationalError during commit"""
        # Arrange
        self.mock_session.commit.side_effect = OperationalError("statement", "params", "orig")
        
        # Act & Assert
        with self.assertRaises(DatabaseConnectionError) as context:
            self.repository.delete(self.test_item)
        
        self.mock_session.rollback.assert_called_once()
        self.assertIn("Database connection error during commit in delete", str(context.exception))
    
    def test_delete_commit_error(self):
        """Test delete raises CommitError and rolls back on SQLAlchemyError during commit"""
        # Arrange
        self.mock_session.commit.side_effect = SQLAlchemyError("Commit failed")
        
        # Act & Assert
        with self.assertRaises(CommitError) as context:
            self.repository.delete(self.test_item)
        
        self.mock_session.rollback.assert_called_once()
        self.assertIn("Commit error in delete", str(context.exception))
