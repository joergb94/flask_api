from app.config import get_db_connection
from app.config import create_app

class BmiLevelModel:
    @staticmethod
    def get_all_bmi_levels():
        app = create_app()
        connection = get_db_connection(app)
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM bmi_levels")
            bmi_levels = cursor.fetchall()
        connection.close()
        return bmi_levels

    @staticmethod
    def get_bmi_level_by_id(id):
        try:
            app = create_app()
            connection = get_db_connection(app)
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM bmi_levels WHERE id=%s", (id,))
                bmi_level = cursor.fetchone()
        except Exception as e:
            bmi_level = None
        finally:
            connection.close()
        
        return bmi_level