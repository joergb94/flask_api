from app.config import get_db_connection
from app.config import create_app

class UserBmiModel:
    @staticmethod
    def get_all_users_bmi():
        app = create_app()
        connection = get_db_connection(app)
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM user_bmis")
            users = cursor.fetchall()
        connection.close()
        return users

    @staticmethod
    def create_user_bmi(user_id,bmi_level_id,weight,height,description):
        app = create_app()
        connection = get_db_connection(app)
        try:
            with connection.cursor() as cursor:
                # Insert the new user bmi
                cursor.execute("""
                           INSERT INTO user_bmis(user_id,bmi_level_id,weight,height,description) 
                           VALUES (%s, %s, %s, %s, %s)""", (user_id,bmi_level_id,weight,height,description))
                connection.commit()
                last_id = cursor.lastrowid
                
                # get data user
                cursor.execute("SELECT * FROM user_bmis WHERE id = %s", (last_id,))
                user_bmis = cursor.fetchone()
        except Exception as e:
            print(f"An error occurred in user bmis: {e}")
            user_bmis = None
        finally:
            connection.close()
        
        return user_bmis

    @staticmethod
    def update_user_bmi(id, user_id, bmi_level_id, weight, height, description):
        app = create_app()
        connection = get_db_connection(app)
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE user_bmis 
                    SET user_id = %s, bmi_level_id = %s, weight = %s, height = %s, description = %s 
                    WHERE id = %s
                """, (user_id, bmi_level_id, weight, height, description, id))
                connection.commit()

                cursor.execute("SELECT * FROM user_bmis WHERE id = %s", (id,))
                user_bmis = cursor.fetchone()
        finally:
            connection.close()
        return user_bmis