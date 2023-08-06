ORACLE_POSTGRES_EXPECTED_EDGES = [{'inV': 'db1.schema1.table1',
                                   'outV': 'db1.schema1.table1.column1',
                                   'label': 'memberOf'
                                   },
                                  {'inV': 'db1.schema1.table1.column1',
                                   'outV': 'db1.schema1.table1',
                                   'label': 'hasMember'
                                   },
                                  {'inV': 'db1.schema1.table2',
                                   'outV': 'db1.schema1.table2.column2',
                                   'label': 'memberOf'
                                   },
                                  {'inV': 'db1.schema1.table2.column2',
                                   'outV': 'db1.schema1.table2',
                                   'label': 'hasMember'
                                   }
                                  ]