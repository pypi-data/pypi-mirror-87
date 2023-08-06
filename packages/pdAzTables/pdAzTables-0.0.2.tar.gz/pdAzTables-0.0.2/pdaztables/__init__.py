from azure.cosmosdb.table.tableservice import TableService
import pandas

class AzTable():
    def __init__(self, lake_con_string):
        self.table_service = TableService(connection_string=lake_con_string)
    
    def get_table(self, table_name):
        return pandas.DataFrame(self.__get_data_from_table_storage_table(self.table_service, table_name))

    def __get_data_from_table_storage_table(self, table_service, table_name):
            """ Retrieve data from Table Storage """
            SOURCE_TABLE = table_name
            for record in table_service.query_entities(
                SOURCE_TABLE
            ):
                yield record