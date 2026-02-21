# Streamlit SQLModel App

This is a simple template that can be developed into a full-featured CRUD application.

**Author**: Simone Tomada - [SimoneT99 on GitHub](https://github.com/SimoneT99)

## Stack Overview
- **Streamlit**: A temporary presentation layer that allows for fast iteration and prototyping. Eventually, this can be replaced with a more robust frontend framework like React or Vue.
- **SQLModel**: A library for interacting with SQL databases using Python models. It handles model validation and provides an easy interface for database operations.

## Getting Started
1. Run the container
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the application:
    ```bash
    streamlit run main.py
    ```
4. Use the sidebar to navigate between the Home page and the ExampleModel CRUD page.

## Container Notes
- The application is designed to be containerized using Docker.

## Future Evolutions
This project is designed to be easily extendable. You can add new models, pages, etc.
The architecture is designed to keep the presentation separate from the service logic, allowing for easy swapping of the frontend or backend components.

Next steps you can take:
- Introduce a more robust backend framework using FastAPI or Flask.
- Adopt a more sophisticated frontend using React or Vue.

## Status and Production Note
This template is currently under active development and is **not** intended for direct production use in its current form.  
It serves as a starting point to be customized and extended according to the specific needs of your project.

## License
This project is licensed under the MIT License.