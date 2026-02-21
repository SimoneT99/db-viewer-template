from dependency_injector import containers, providers
from sqlmodel import SQLModel, create_engine, Session

class RepositoryContainer(containers.DeclarativeContainer):

    def init(self):
        SQLModel.metadata.create_all(self.sqllite_engine)

    wiring_config = containers.WiringConfiguration(modules=[
        "src.infrastructure.SQLModelRepository",
    ])
    
    # Load configuration from YAML file (default: db_config.yml)
    config = providers.Configuration(yaml_files=["db_config.yml"])

    """
        SqlLite configuration
    """

    sqllite_database_url = providers.Factory(
        lambda driver, database: f"{driver}:///{database}",
        driver=config.sqllite.driver,
        database=config.sqllite.database,
    )

    @staticmethod
    def __create_engine(database_url: str):
        engine = create_engine(database_url, echo=True)
        SQLModel.metadata.create_all(engine)
        return engine

    sqllite_engine = providers.Singleton(__create_engine, sqllite_database_url)
    sqllite_session = providers.Factory(
        Session, 
        sqllite_engine
    )