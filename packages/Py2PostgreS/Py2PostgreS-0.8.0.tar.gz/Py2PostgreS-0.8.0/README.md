# Install library

```
pip install Py2PostgreS
```

# Example using Py2PostgreS library

Full example can be viewed in ```example.py```

1. Add library to module

   ```python
   from Py2PostgreS import Py2SQL
   ```
2. Create connection to database
    ```python
   py2sql = Py2SQL()
   py2sql.db_connect({'name': 'dds65no8mnedpv',
                       'user': 'vecriqxloxrdqd',
                       'password': 'd000f559133dc29adeb06fe1591c124ad8cf4b23d4aa4ec15047fe01af3a2112',
                       'host': 'ec2-176-34-123-50.eu-west-1.compute.amazonaws.com',
                       'port': '5432'})
    ```

3. Use this functions to get information about database
    - Version of the database engine
    ```python
   print(py2sql.db_engine())
   
   # Example output: PostgreSQL 12.4 (Ubuntu 12.4-1.pgdg16.04+1) on x86_64-pc-linux-gnu
    ```
   - Name of the database
    ```python
    print(py2sql.db_name())
   
   # Example output: dds65no8mnedpv
    ```
    - List of table names
    ```python
    print(py2sql.db_tables())
   
   # Example output: ['countries', 'users', 'languages', 'tags', 'quizzes', 'categories', 'favorite_quizzes']
    ```
    - Get list of attribute names and types of table
    ```python
    print(py2sql.db_table_structure('tags'))
   
   # Example output: [(1, 'id', 'integer'), (2, 'name', 'character varying')]
    ```
    - Get size of the database
    ```python
    print(py2sql.db_size())
   
    # Example output: 8601 kB
    ```
    - Get size of table
    ```python
    print(py2sql.db_table_size('users'))
   
    # Example output: 24 kB
    ```
4. Python to PostgreSQL and PostgreSQL to Python
    - Get table entries containing specified attributes with supporting the parameters the parameters field__gt, field__lt, field__gte, field__lte, field__in, field__not_in
    
   ```python
    print(py2sql.find_objects_by('tags', [('id', 0, 'field__gte'), ('name', 'Default')]))
   
    # Example output: [(1, 'Default')]
    ```
    - Get attributes of table that represents a class if exists
    
    ```python
   print(py2sql.find_class(globals().get('Tags')))
   
   # Example output: [('id', 'integer'), ('name', 'character varying')]
    ```
    - Get attributes of table that has given attributes
    
    ```python
   print(py2sql.find_classes_by([('id',), ('name',)]))
   
   # Example output: {'countries': [('id', 'integer'), ('name', 'character varying')], 'users': [('id', 'integer'), ('email', 'character varying'), ('password', 'character varying'), ('name', 'character varying'), ('surname', 'character varying'), ('image', 'bytea'), ('birthdate', 'date'), ('country_id', 'integer'), ('city', 'character varying'), ('rating', 'integer'), ('about', 'text'), ('active', 'boolean'), ('language_id', 'integer')], 'languages': [('id', 'integer'), ('name', 'character varying')], 'tags': [('id', 'integer'), ('name', 'character varying')], 'quizzes': [('id', 'integer'), ('name', 'character varying'), ('image', 'bytea'), ('author', 'integer'), ('category_id', 'integer'), ('date', 'date'), ('description', 'text'), ('modification_time', 'timestamp without time zone')], 'categories': [('id', 'integer'), ('name', 'character varying')]}
    ```
    - Creates a new class based on the table from the database
    
    ```python
    py2sql.create_class('quizzes', 'quiz', globals())
    ```
    - Create table by class if not exists
    
    ```python
    py2sql.save_class(globals().get('Test'))
    ```
    - Delete table from the database by class if exists
    
    ```python
   py2sql.delete_class(globals().get('Test'))
    ```
    - Find a table entry with the same parameters as given object
    
    ```python
   print(py2sql.find_object('tags', Tags()))
   
   # Example output: [('id', 'integer', 0), ('name', 'character varying', 'Default')]
    ```
    - Create object from table entry with given id
    
    ```python
   py2sql.create_object('tags', 1, globals())
    ```
    - Create objects from table entries with id in range
    
    ```python
    py2sql.create_objects('tags', 1, 2, globals())
    ```
    - Find all hierarchies in database
    
    ```python
   print(py2sql.find_hierarchies())
    ```
    - Create hierarchy of classes from table hierarchy in database
    
    ```python
   py2sql.create_hierarchy('users', 'quiz', globals())
    ```
    - Delete hierarchy from the database
    
    ```python
   py2sql.delete_hierarchy(globals().get('A'), globals())
    ```
    - Save object to the database
    
    ```python
   py2sql.save_object(Tags())
    ```
    - Delete object from the database
    
    ```python
   py2sql.delete_object(Tags())
    ```
    - Create table hierarchy from the class hierarchy
    
    ```python
   py2sql.save_hierarchy(globals().get('A'), globals())
    ```
    
5. **Do NOT forget to close connection to the database**

    ```python
   py2sql.db_disconnect()
    ```

# Remote database credentials

**Database name:**  dds65no8mnedpv

**User:**  vecriqxloxrdqd

**Password:**  d000f559133dc29adeb06fe1591c124ad8cf4b23d4aa4ec15047fe01af3a2112

**Host:**  vecriqxloxrdqd

**Port:**  5432

If you want to run database locally you can use ddl.sql script to create the same sample database.

# Sample database structure

![Database structure](database.png)