# PdAzTables

This is a simple library that makes it easy to get a Pandas DataFrame from a table in Azure Table Storage (Azure Data Lake's Table service)


```python
# Import library
from pdaztables import AzTable

# Create service object with login info
table_service = AzTable('Your data lake conn string here')

# Get Pandas DataFrame!
table_service.get_table('Table name here')

```