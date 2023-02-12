SMILES

1.  Checkout this project and create a virtual environment.

    ```
    git clone https://github.com/
    cd seagrid
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip setuptools wheel
    pip install -r requirements.txt
    ```

2.  Follow the instructions and run Apache Airavata Data Catalog - https://github.com/apache/airavata-data-catalog

3.  Run the Django application

    ```
    python manage.py runserver
    ```

4.  Run the Django application

    ```
    python manage.py runserver
    ```

5.  Run the Vue.js frontend

    ```
    cd seagrid-view
    yarn install
    yarn run serve
    ```

    Point your browser to http://localhost:8088


Once you hit the "Create Dummy Data" button check the Airavata Catalog DB for the created Data Product

