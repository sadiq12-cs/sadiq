

import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="sadiq123",          # اسم المستخدم الذي أنشأته
        password="Sadiq@1212",    # كلمة المرور الخاصة به
        database="university"  # استبدلها باسم قاعدة بياناتك التي أنشأتها
    )
    return conn


def create_database():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS admins (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        full_access TINYINT(1) DEFAULT 0
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_name VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        added_by_admin_id INT,
        FOREIGN KEY (added_by_admin_id) REFERENCES admins(id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS feeders (
        id INT AUTO_INCREMENT PRIMARY KEY,
        feeder_name VARCHAR(255) NOT NULL,
        feeder_type INT NOT NULL,
        added_by_admin_id INT,
        FOREIGN KEY (added_by_admin_id) REFERENCES admins(id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INT AUTO_INCREMENT PRIMARY KEY,
        feeder_id INT NOT NULL,
        feeder_name VARCHAR(255) NOT NULL,
        feeder_type INT NOT NULL,
        off_time DATETIME NOT NULL,
        on_time DATETIME DEFAULT NULL,
        reason TEXT,
        added_by_admin_id INT,
        added_by_user_id INT,
        total_off_duration INT,
        FOREIGN KEY (feeder_id) REFERENCES feeders(id),
        FOREIGN KEY (added_by_admin_id) REFERENCES admins(id),
        FOREIGN KEY (added_by_user_id) REFERENCES users(id)
    )
    """)
   # cur.execute("""
    #        INSERT INTO admins (user_name, email, password, full_access)
     #       VALUES (%s, %s, %s, %s)
      #  """, ("sadiq", "admin@example.com", "111", 1))
    conn.commit()
    conn.close()



    


 # table for admain    
