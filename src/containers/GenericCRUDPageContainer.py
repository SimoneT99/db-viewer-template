from dependency_injector import containers, providers
from src.view.GenericCRUDPage.StreamLitFieldDispatcher import BooleanFieldRenderer, FloatFieldRenderer, IntegerFieldRenderer, StreamLitFieldDispatcher, TextFieldRenderer

class GenericCRUDPageContainer(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=[
        "src.view.GenericCRUDPage.BaseStreamLitForm",
        "src.view.GenericCRUDPage.BaseCRUDPage",
        # aggiungi altri moduli se necessario
    ])

    default_text_field_renderer = providers.Factory(
        TextFieldRenderer
    )

    default_integer_field_renderer = providers.Factory(
        IntegerFieldRenderer
    )

    default_float_field_renderer = providers.Factory(
        FloatFieldRenderer
    )

    default_boolean_field_renderer = providers.Factory(
        BooleanFieldRenderer
    )

    standard_field_builder = providers.Factory(
        StreamLitFieldDispatcher,
            dispatcher={
                str: providers.Factory(TextFieldRenderer)(),
                int: providers.Factory(IntegerFieldRenderer)(),
                float: providers.Factory(FloatFieldRenderer)(),
                bool: providers.Factory(BooleanFieldRenderer)(),
            }
        )
    
