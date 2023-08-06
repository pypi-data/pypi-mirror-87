ORACLE_EXPECTED_COLLECTION_NODE_TYPE = "oracle_table"

ORACLE_EXPECTED_RESOURCE_NODE_TYPE = "oracle_column"

POSTGRES_EXPECTED_COLLECTION_NODE_TYPE = "postgres_table"

POSTGRES_EXPECTED_RESOURCE_NODE_TYPE = "postgres_column"

TABLEAU_EXPECTED_COLLECTION_NODE_TYPE = "tableau_workbook"

TABLEAU_EXPECTED_RESOURCE_NODE_TYPE = "tableau_view"

ORACLE_POSTGRES_EXPECTED_REQUIRED_COLLECTION_NODE_FIELDS = ('db_name', 'schema_name', 'table_name', 'table_description',
                                                            'team_name')

ORACLE_POSTGRES_EXPECTED_REQUIRED_RESOURCE_NODE_FIELDS = ('db_name', 'schema_name', 'table_name', 'column_name',
                                                          'column_description', 'data_type')

TABLEAU_EXPECTED_REQUIRED_COLLECTION_NODE_FIELD = ('project_name', 'workbook_name', 'issued', 'modified')

TABLEAU_EXPECTED_REQUIRED_RESOURCE_NODE_FIELD = ('project_name', 'workbook_name', 'contentUrl', "view_name", "preview")


EXPECTED_HOST_URL = "host"

HOST_URL = "oracle://user:pass@host:1234/db"
