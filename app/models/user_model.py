from app.config import get_db_connection
from app.config import create_app

class UserModel:
    #get all user
    @staticmethod
    def get_all_users():
        app = create_app()
        connection = get_db_connection(app)
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
        connection.close()
        return users

    #get user by id
    @staticmethod
    def get_user_by_id(id):
        try:
            app = create_app()
            connection = get_db_connection(app)
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE id=%s", (id,))
                bmi_level = cursor.fetchone()
        except Exception as e:
            bmi_level = None
        finally:
            connection.close()
        
        return bmi_level
    
    #get user by id
    @staticmethod
    def get_user_by_email(email):
        try:
            app = create_app()
            connection = get_db_connection(app)
            with connection.cursor() as cursor:
                cursor.execute("""
                               SELECT 
                               users.id as user_id,
                               user_bmis.id as user_bmi_id
                               FROM users 
                               LEFT JOIN user_bmis
                               ON users.id = user_bmis.user_id WHERE users.email=%s""", (email,))
                bmi_level = cursor.fetchone()
        except Exception as e:
            bmi_level = None
        finally:
            connection.close()
        
        return bmi_level
    
    #create user
    @staticmethod
    def create_user(name, email,phone):
        app = create_app()
        connection = get_db_connection(app)
        try:
            with connection.cursor() as cursor:
                # Insert the new user
                cursor.execute("INSERT INTO users (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
                connection.commit()

                last_id = cursor.lastrowid
                
                # get data user
                cursor.execute("SELECT * FROM users WHERE id = %s", (last_id,))
                user = cursor.fetchone()
        except Exception as e:
            print(f"An error occurred in users: {e}")
            user = None
        finally:
            connection.close()
        
        return user
    
    #update user
    @staticmethod
    def update_user(id,name, email,phone):
        app = create_app()
        connection = get_db_connection(app)
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("UPDATE users SET name = %s, email = %s, phone = %s WHERE id = %s", (name, email,phone, id))
                connection.commit()
        finally:
            connection.close()