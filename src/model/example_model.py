from sqlmodel import SQLModel, Field

"""
Example SQLModel definition for demonstration purposes.
"""

class ExampleModel(SQLModel, table=True):
    """
        ExampleModel represents a simple entity with an id, name, value, and description.
    """

    id: int = Field(default=None, primary_key=True)
    name: str
    value: int
    description: str = Field(default=None)