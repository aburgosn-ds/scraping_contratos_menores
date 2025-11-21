import sqlite3
import logging

class DbManager:
    def __init__(self, database_name):
        self.database_name = database_name
        self.logger = logging.getLogger(self.__class__.__name__)

    def _create_table_once(self, table_name):
        with sqlite3.connect(self.database_name) as conn:
            query = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                codigo TEXT PRIMARY KEY,
                titulo TEXT NOT NULL,
                empresa TEXT NOT NULL,
                objeto TEXT NOT NULL,
                descripcion TEXT,
                cotizacion_comienzo DATETIME NOT NULL,
                cotizacion_fin DATETIME NOT NULL,
                fecha_publicacion TEXT NOT NULL,
                url TEXT,
                util BOOLEAN NOT NULL
            );
            """
            conn.execute(query)
            conn.commit()
    
    def select_all_codes(self, table_name) -> list[str]:
        result = None
        with sqlite3.connect(self.database_name) as conn:
            query = f"SELECT codigo FROM {table_name};"

            cursor = conn.cursor() 
            cursor.execute(query)
            result = cursor.fetchall()

        result = [tuple_[0] for tuple_ in result]
        self.logger.info(f"Current codes in db: {len(result)}")

                
        return result