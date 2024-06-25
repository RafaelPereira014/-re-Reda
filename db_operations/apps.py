from datetime import datetime
import os
from config import DB_CONFIG  # Import the database configuration
from flask import current_app, session, url_for
import mysql.connector  # Import MySQL Connector Python module

def connect_to_database():
    """Establishes a connection to the MySQL database."""
    return mysql.connector.connect(**DB_CONFIG)

def get_all_apps(page, apps_per_page):
    offset = (page - 1) * apps_per_page
    query = """
        SELECT * FROM Resources
        WHERE type_id='3' AND approvedScientific = 1 AND approvedLinguistic = 1
        ORDER BY id DESC
        LIMIT %s OFFSET %s
    """
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, (apps_per_page, offset))
    apps = cursor.fetchall()
    cursor.close()
    conn.close()
    return apps

def get_apps():
    """Get all approved resources from the DB."""
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Resources WHERE type_id='3'  ORDER BY id DESC")
    all_apps = cursor.fetchall()
    cursor.close()
    conn.close()
    return all_apps

def get_apps_from_user(userid):
    """Get all tools from user and their count."""
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    
    apps_user = []
    apps_count = 0
    
    try:
        # Query to fetch all tools
        cursor.execute("SELECT * FROM Resources WHERE user_id=%s AND type_id=%s ORDER BY id DESC", (userid, 3))
        apps_user = cursor.fetchall()
        
        # Query to count the tools
        cursor.execute("SELECT COUNT(*) AS count FROM Resources WHERE user_id=%s AND type_id=%s", (userid, 3))
        apps_count = cursor.fetchone()['count']
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()
    
    return apps_user, apps_count

def get_pendent_apps():
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Resources WHERE type_id='3' AND approved='0' ORDER BY id DESC")
    pendent_apps = cursor.fetchall()
    cursor.close()
    conn.close()
    return pendent_apps

def get_app_slug(resource_id):
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT slug FROM Resources WHERE type_id='3' AND id=%s", (resource_id,))
    slug = cursor.fetchone()  # fetchone is used because we expect only one user with the given username
    cursor.close()
    conn.close()
    
    if slug:
        return slug['slug']
    else:
        return None
    
def get_apps_image_url(resource_slug):
    image_extensions = ['png', 'jpg']
    directory_path = os.path.join(current_app.root_path, 'static', 'files', 'apps', resource_slug)

    if os.path.exists(directory_path) and os.path.isdir(directory_path):
        for ext in image_extensions:
            for filename in os.listdir(directory_path):
                if filename.startswith(resource_slug) and filename.endswith('.' + ext):
                    return url_for('static', filename=f'files/apps/{resource_slug}/{filename}')

    return None  # Return None if no image is found


def get_total_app_count():
    query = """
        SELECT COUNT(*) as count FROM Resources
        WHERE type_id='3'
    """
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result['count']
