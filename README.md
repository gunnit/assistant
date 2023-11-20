# Setting Up Django Assistant App

## Prerequisites

- Python 3.x
- Django 3.x
- Other dependencies...

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/gunnit/assistant.git

2. Navigate to the project directory

3. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate
    venv\Scripts\activate     # On Windows

3. Install the required packages:
    ```bash
    pip install -r requirements.txt

4. Before running the app, you need to configure some environment variables. Create a .env file in the project root and add the following:

    # Django secret key
    SECRET_KEY=your_secret_key_here

    # OpenAI API key
    OPENAI_API_KEY=your_openai_api_key_here

    # Django debug mode (set to 'True' in development)
    DEBUG=True