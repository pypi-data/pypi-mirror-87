#                         db1
#                       schema1
#           table1                    table2
#            //                         \\
#         column1                      column2

ORACLE_POSTGRES_RESOURCES = [{'db_name': 'db1',
                              'schema_name': 'schema1',
                              'table_name': 'table1',
                              'column_name': 'column1',
                              'data_type': 'number',
                              'column_description': 'test_column'},
                             {'db_name': 'db1',
                              'schema_name': 'schema1',
                              'table_name': 'table2',
                              'column_name': 'column2',
                              'data_type': 'date',
                              'column_description': 'test_column'}
                             ]

ORACLE_POSTGRES_COLLECTIONS = [{'db_name': 'db1',
                                'schema_name': 'schema1',
                                'table_name': 'table1',
                                'table_description': 'test_table',
                                'team_name': 'test_team1'},
                               {'db_name': 'db1',
                                'schema_name': 'schema1',
                                'table_name': 'table2',
                                'table_description': 'test_table',
                                'team_name': 'test_team2'}
                               ]

TABLEAU_RESOURCES = [{'project_name': 'project1',
                      'workbook_name': 'workbook1',
                      'contentUrl': 'some_url',
                      'view_name': 'view1',
                      "preview": 'preview1'},
                     {'project_name': 'project1',
                      'workbook_name': 'workbook2',
                      'contentUrl': 'some_url',
                      'view_name': 'view2',
                      "preview": 'preview2'}]


TABLEAU_COLLECTIONS = [{'project_name': 'project1',
                        'workbook_name': 'workbook1',
                        'issued': '01-01-2020',
                        'modified': '01-01-2020'},
                       {'project_name': 'project1',
                        'workbook_name': 'workbook2',
                        'issued': '01-01-2020',
                        'modified': '01-01-2020'}]
