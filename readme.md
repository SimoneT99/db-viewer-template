# Streamlit SQLModel Template

This is a simple template that serves a a starting point for the development of a CRUD application.

**Author**: Simone Tomada - [SimoneT99 on GitHub](https://github.com/SimoneT99)

## Stack Overview
- **Streamlit**: A temporary presentation layer that allows for fast iteration and prototyping. Eventually, this can be replaced with a more robust frontend framework like React or Vue.
- **SQLModel**: A library for interacting with SQL databases using Python models. It handles model validation and provides an easy interface for database operations.

## Project Structure
The project follows a modular architecture, organized as follows:
- **Model**: Uses SQLModel to define your data structures.
- **Services**: Depend on models and implement business logic and use cases.
- **Views**: Depend on services (and models; eventually, you may want to separate database models from DTOs). Uses Streamlit as the framework for the presentation layer.
- **Infrastructure**: Provides external dependencies for services (such as database connections). Includes a repository abstraction for managing CRUD operations, with a basic SQLAlchemy implementation. You can implement your own repository for custom behavior.


**NOTE**: This structure is flexible and should be adapted to your specific needs. Keeping the view and service layers separate is recommended, as it allows for easier upgrades to a more complex UI or a multi-tier application in the future.

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

## Status and Production Note
This template is currently under active development and is **not** intended for direct production use in its current form.  
It serves as a starting point to be customized and extended according to the specific needs of your project.

Pull request are welcome for improvements and bugfixing.

## License
This project is licensed under the MIT License.