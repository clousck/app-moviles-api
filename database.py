import pypyodbc as odbc

def execute_query(query):
    """
    Ejecuta una consulta que retorna registros (e.g., SELECT).
    """
    try:
        conn = odbc.connect(connection_string)
        cursor = conn.cursor()

        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in rows]

        conn.close()
        return results

    except Exception as ex:
        print(f"Error: {ex}")
        return {"error": str(ex)}

def execute_non_query(query):
    """
    Ejecuta una consulta que no retorna registros (e.g., INSERT, UPDATE, DELETE).
    """
    try:
        conn = odbc.connect(connection_string)
        cursor = conn.cursor()

        cursor.execute(query)
        conn.commit()
        conn.close()
        return {"success": True}

    except Exception as ex:
        print(f"Error: {ex}")
        return {"error": str(ex)}


DRIVER_NAME = 'ODBC Driver 18 for SQL Server'
SERVER_NAME = 'app-moviles-utn-server'
DATABASE_NAME = 'app-moviles-utn-database'

connection_string = f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME}.database.windows.net;
    DATABASE={DATABASE_NAME};
    UID=victorees;
    PWD=Palommv123.;
"""
