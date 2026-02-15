class RepositoryError(Exception):
    """Base class for repository exceptions."""
    pass

class DatabaseConnectionError(RepositoryError):
    """Raised when there is a database connection issue."""
    pass

class QueryExecutionError(RepositoryError):
    """Raised when a query fails to execute."""
    pass

class CommitError(RepositoryError):
    """Raised when a commit operation fails."""
    pass