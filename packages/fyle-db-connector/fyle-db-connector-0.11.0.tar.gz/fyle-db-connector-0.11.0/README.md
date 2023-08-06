# Fyle Database Connector
Connects Fyle to a database to transfer information to and fro. [Fyle](https://www.fylehq.com/) is an expense management system.

## Installation

This project requires [Python 3+](https://www.python.org/downloads/).

1. Download this project and use it (copy it in your project, etc).
2. Install it from [pip](https://pypi.org).

        $ pip install fyle-db-connector

## Usage

To use this connector you'll need these Fyle credentials used for OAuth2 authentication: **client ID**, **client secret** and **refresh token**.

This connector is very easy to use.
1. First you'll need to create a connection using the main class FyleSDK.
```python
import sqlite3

from fylesdk import FyleSDK
from fyle_db_connector import FyleExtractConnector


dbconn = sqlite3.connect('/tmp/temp.db')

connection = FyleSDK(
    base_url='<BASE_URL>',
    client_id="<CLIENT_ID>",
    client_secret='<CLIENT_SECRET>',
    refresh_token='<REFRESH_TOKEN>'
)

fyle_extract = FyleExtractConnector(
    fyle_sdk_connection=connection,
    dbconn=dbconn
)
```
2. After that you'll be able to extract data from fyle and store it in the db
```python
# Create the tables to for all objects
fyle_extract.create_tables()

fyle_extract.extract_expenses(state=['PAYMENT_PROCESSING'])
fyle_extract.extract_settlements()
fyle_extract.extract_employees()
fyle_extract.extract_reimbursements()
fyle_extract.extract_advances()
fyle_extract.extract_advance_requests(state=['PAID'])
fyle_extract.extract_projects()
fyle_extract.extract_cost_centers()
fyle_extract.extract_categories()
```

## Contribute

To contribute to this project follow the steps

* Fork and clone the repository.
* Run `pip install -r requirements.txt`
* Setup pylint precommit hook
    * Create a file `.git/hooks/pre-commit`
    * Copy and paste the following lines in the file - 
        ```bash
        #!/usr/bin/env bash 
        git-pylint-commit-hook
        ```
     * Run `chmod +x .git/hooks/pre-commit`
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
