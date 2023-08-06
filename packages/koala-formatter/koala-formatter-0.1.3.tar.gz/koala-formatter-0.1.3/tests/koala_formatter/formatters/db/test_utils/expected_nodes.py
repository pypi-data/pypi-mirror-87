#                         db1
#                       schema1
#           table1                    table2
#            //                         \\
#         column1                      column2

ORACLE_EXPECTED_RESOURCE_NODES = [{'id': 'db1.schema1.table1.column1',
                                   'label': 'oracle_column',
                                   'properties': {'schema_name': 'schema1',
                                                  'db_name': 'db1',
                                                  'table_name': 'table1',
                                                  'column_name': 'column1',
                                                  'data_type': 'number',
                                                  'host': 'host',
                                                  'column_description': 'test_column',
                                                  'type': 'oracle_column'}
                                   },
                                  {'id': 'db1.schema1.table2.column2',
                                   'label': 'oracle_column',
                                   'properties': {
                                       'schema_name': 'schema1',
                                       'db_name': 'db1',
                                       'table_name': 'table2',
                                       'column_name': 'column2',
                                       'data_type': 'date',
                                       'host': 'host',
                                       'column_description': 'test_column',
                                       'type': 'oracle_column'
                                   }
                                   }
                                  ]

ORACLE_EXPECTED_COLLECTION_NODES = [{'id': 'db1.schema1.table1',
                                     'label': 'oracle_table',
                                     'properties': {
                                         'db_name': 'db1',
                                         'host': 'host',
                                         'schema_name': 'schema1',
                                         'table_name': 'table1',
                                         'table_description': 'test_table',
                                         'team_name': 'test_team1',
                                         'type': 'oracle_table'}},
                                    {'id': 'db1.schema1.table2',
                                     'label': 'oracle_table',
                                     'properties': {
                                         'db_name': 'db1',
                                         'host': 'host',
                                         'schema_name': 'schema1',
                                         'table_name': 'table2',
                                         'table_description': 'test_table',
                                         'team_name': 'test_team2',
                                         'type': 'oracle_table'}}]
