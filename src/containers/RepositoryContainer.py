from dependency_injector import containers, providers
from sqlmodel import create_engine, Session
from infrastructure.SQLModelRepository import SQLModelRepository

class RepositoryContainer(containers.DeclarativeContainer):
    
    # Configurazione del database, da gestire tramite variabili d'ambiente o file di configurazione
    database_url = "sqlite:///database.db"
    engine = providers.Singleton(create_engine, database_url, echo=True)

    session = providers.Factory(Session, engine)