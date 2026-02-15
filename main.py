from database import create_db_and_tables, get_session
from src.model.model import ExampleModel
from src.infrastructure.SQLModelRepository import SQLModelRepository
from src.services.CRUDService import CRUDService
from src.view.BaseCRUDPage import BaseCRUDPage
from src.view.BaseStreamLitForm import BaseStreamLitForm
from src.view.Interfaces.IStreamLitPage import IStreamLitPage
from src.view.ReadmePage import ReadmePage
from src.view.BasePage import BasePage


def main(entryPage: IStreamLitPage):
    entryPage.render()


if __name__ == "__main__":
    create_db_and_tables()  # Ensure tables are created before starting the app
    session = next(get_session())

    # HomePage
    ReadmePage = ReadmePage()

    # ExampleModel
    ExampleModelCRUDService = CRUDService[ExampleModel](SQLModelRepository(ExampleModel, session))
    ExampleModelPage = BaseCRUDPage(ExampleModelCRUDService, ExampleModel, BaseStreamLitForm[ExampleModel](ExampleModel))

    # Base Page
    sections = {
        "Home": ReadmePage,
        "ExampleModel CRUD": BaseCRUDPage(CRUDService[ExampleModel](SQLModelRepository(ExampleModel, session)), ExampleModel, BaseStreamLitForm[ExampleModel](ExampleModel))
    }

    BasePage = BasePage(sections)
    main(BasePage)