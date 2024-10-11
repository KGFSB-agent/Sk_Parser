# **Site Parser**

This is a test parser for extracting newses and saving them to a CSV file using the library **Selenium**.

## **Setup**

### **Requirements**
- `selenium`
- `webdriver-manager`

### **Installation**

1. **Clone the repository**:
    ```bash
    git clone https://github.com/KGFSB-agent/Sk_Parser.git
    cd telegram-parser
    ```

2. **Install Poetry**:
    ```bash
    (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
    poetry --version
    ```

3. **Install Project Dependencies**:
    ```bash
    poetry install
    ```

4. **Running the Code**:

    - **5.1. Activate the virtual environment created by Poetry**:
        ```bash
        poetry shell
        ```

    - **5.2. Run the script to start fetching messages from Telegram**:
        ```bash
        poetry run python src/main.py
        ```

5. **Output**:
    
    After running the script, the extracted messages will be saved in a CSV file located at `data/data/results.csv`. The file will include details like main sector, title, sectors, readiness lvl, description, advantages of the technology, references and technology url.
