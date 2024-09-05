import psycopg2


def execute_query(query):
    
    query_type = query.strip().split()[0].upper()

    try:
        connection = psycopg2.connect(
            host='0.0.0.0',
            user='admin',
            password='root',
            database='postgres'
        )

        connection.autocommit=True

        with connection.cursor() as cursor:
            cursor.execute(query)
            if query_type != 'SELECT':
                connection.close()
                return None
            else:
                result = cursor.fetchall()
                connection.close()
                return result

    except Exception as e:
        return e
    
# login req