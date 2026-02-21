from src.containers.GenericCRUDPageContainer import GenericCRUDPageContainer
from src.containers.RepositoryContainer import RepositoryContainer
from src.model.example_model import ExampleModel
from src.infrastructure.SQLModelRepository import SQLModelRepository
from src.services.CRUDService import CRUDService
from src.view.GenericCRUDPage.BaseCRUDPage import BaseCRUDPage
from src.view.GenericCRUDPage.BaseStreamLitForm import BaseStreamLitForm
from src.view.Interfaces.IStreamLitPage import IStreamLitPage
from src.view.ReadmePage import ReadmePage
from src.view.BasePage import BasePage


def main(entryPage: IStreamLitPage):
    entryPage.render()


if __name__ == "__main__":
    #container wiring
    container = GenericCRUDPageContainer()
    container.wire()

    repository_container = RepositoryContainer()
    repository_container.wire()

    # HomePage
    ReadmePage = ReadmePage()

    # ExampleModel
    ExampleModelCRUDService = CRUDService[ExampleModel](SQLModelRepository(ExampleModel))
    ExampleModelPage = BaseCRUDPage(ExampleModelCRUDService, ExampleModel, BaseStreamLitForm[ExampleModel](ExampleModel))

    # Base Page
    sections = {
        "Home": ReadmePage,
        "ExampleModel CRUD": ExampleModelPage
    }

    BasePage = BasePage(sections)
    main(BasePage)