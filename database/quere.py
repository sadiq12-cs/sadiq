import mysql.connector
from mysql.connector import Error
from database.mydata import get_connection  # تأكد أن هذه دالة اتصال MySQL

class Login:

    def __init__(self, page=None):
        self.page = page

    def login(self, username, password):
        if not username or not password:
            return False, "⚠️ All fields are required, please.", None

        try:
            conn = get_connection()
            cur = conn.cursor(buffered=True, dictionary=True)  # dict للحصول على الأعمدة بالاسم
            
            query = "SELECT * FROM admins WHERE user_name = %s AND password = %s"
            cur.execute(query, (username, password))
            admin = cur.fetchone()

            if not admin:
                return False, "❌ This username or password is incorrect.", None

            user_data = {
                "id": admin['id'],
                "user_name": admin['user_name'],
                "email": admin['email'],
                "full_access": admin['full_access']
            }

            return True, "✅ Login successful.", user_data

        except Error as e:
            return False, f"❌ Error: {e}", None

        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    def login_users(self, username, password):
        if not username or not password:
            return False, "⚠️ All fields are required, please.", None

        try:
            conn = get_connection()
            cur = conn.cursor(buffered=True, dictionary=True)

            query = "SELECT * FROM users WHERE user_name = %s AND password = %s"
            cur.execute(query, (username, password))
            user = cur.fetchone()

            if not user:
                return False, "❌ This username or password is incorrect.", None

            user_data = {
                "id": user['id'],
                "user_name": user['user_name']
            }

            return True, "✅ Login successful.", user_data

        except Error as e:
            return False, f"❌ Error: {e}", None

        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    def Create_user(self, usname, password, id_creator):
        if not usname or not password:
            return False, "⚠️ All fields are required, please."

        try:
            conn = get_connection()
            cur = conn.cursor(buffered=True, dictionary=True)

            cur.execute("SELECT user_name FROM users WHERE user_name = %s", (usname,))
            if cur.fetchone():
                return False, "❌ This username is already taken."

            cur.execute(
                "INSERT INTO users (user_name, password, added_by_admin_id) VALUES (%s, %s, %s)",
                (usname, password, id_creator)
            )
            conn.commit()

            return True, "تم اضافة مستخدم واحد بنجاح ✅"

        except Error as e:
            return False, f"❌ Error: {e}"

        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    def Create_admin(self, usname, password):
        if not usname or not password:
            return False, "⚠️ All fields are required, please."

        try:
            conn = get_connection()
            cur = conn.cursor(buffered=True, dictionary=True)

            cur.execute("SELECT user_name FROM admins WHERE user_name = %s", (usname,))
            if cur.fetchone():
                return False, "❌ This username is already taken."

            full_access = True
            email = "exampl@gmail.com"
            cur.execute(
                "INSERT INTO admins (user_name, password, email, full_access) VALUES (%s, %s, %s, %s)",
                (usname, password, email, full_access)
            )
            conn.commit()

            return True, "تم اضافة مدير واحد بنجاح ✅"

        except Error as e:
            return False, f"❌ Error: {e}"

        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()


    def get_all_users_with_creator(self):
        try:
            conn = get_connection()
            cur = conn.cursor(buffered=True, dictionary=True)

            cur.execute("""
                SELECT u.user_name, u.password AS user, a.user_name AS added_by
                FROM users u
                LEFT JOIN admins a ON u.added_by_admin_id = a.id
            """)

            rows = cur.fetchall()
            users = []
            for row in rows:
                users.append({
                    "username": row["user_name"],
                    "added_by": row["added_by"] or "❓ غير معروف",
                    "password": row["user"]
                })

            return True, users

        except Exception as e:
            return False, f"❌ Error: {e}"

        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()


    def Create_feeder(self, name, id_creator, type1):
        if not name or not type1:
            return False, "⚠️ All fields are required, please."

        try:
            conn = get_connection()
            cur = conn.cursor(buffered=True, dictionary=True)

            # التحقق من توفر اسم الفيدر
            cur.execute("SELECT feeder_name FROM feeders WHERE feeder_name = %s", (name,))
            if cur.fetchone():
                return False, "❌ This Feeder name is already taken."

            # إدخال الفيدر الجديد
            cur.execute(
                "INSERT INTO feeders (feeder_name, feeder_type, added_by_admin_id) VALUES (%s, %s, %s)",
                (name, type1, id_creator)
            )

            conn.commit()

            return True, "تم اضافة مغذي واحد بنجاح ✅"

        except Exception as e:
            return False, f"❌ Error: {e}"

        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()


    def get_all_feeders_with_creator(self):
        try:
            conn = get_connection()
            cur = conn.cursor(buffered=True, dictionary=True)

            cur.execute("""
                SELECT u.id, u.feeder_name, u.feeder_type, a.user_name AS added_by
                FROM feeders u
                LEFT JOIN admins a ON u.added_by_admin_id = a.id
            """)

            rows = cur.fetchall()
            feeders = []
            for row in rows:
                feeders.append({
                    "id": row["id"],
                    "feeder_name": row["feeder_name"],
                    "feeder_type": row["feeder_type"],
                    "added_by": row["added_by"] or "❓ غير معروف"
                })

            return True, feeders

        except Exception as e:
            return False, f"❌ Error: {e}"

        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
    

    def insert_event(self, feeder_id, off_time, reason, added_by_admin_id=None, added_by_user_id=None):
        try:
            conn = get_connection()
            cur = conn.cursor(buffered=True, dictionary=True)

            # تحويل off_time إلى نص بصيغة "YYYY-MM-DD HH:MM:SS"
            off_time_str = off_time.strftime("%Y-%m-%d %H:%M:%S") if hasattr(off_time, "strftime") else off_time

            # جلب اسم ونوع الفيدر من جدول feeders
            cur.execute("SELECT feeder_name, feeder_type FROM feeders WHERE id = %s", (feeder_id,))
            row = cur.fetchone()

            if not row:
                return False, "❌ لم يتم العثور على الفيدر المطلوب"

            feeder_name = row['feeder_name']
            feeder_type = row['feeder_type']


            # إدخال الحدث مع اسم ونوع الفيدر
            cur.execute("""
                INSERT INTO events (
                    feeder_id, feeder_name, feeder_type, off_time, reason,
                    added_by_admin_id, added_by_user_id
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                feeder_id, feeder_name, feeder_type,
                off_time_str, reason,
                added_by_admin_id, added_by_user_id
            ))

            conn.commit()
            return True, "تمت الإضافة بنجاح ✅"

        except Exception as e:
            return False, f"❌ خطأ: {e}"

        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()


    def update_event_on_time(self, feeder_id, on_time):
        try:
            conn = get_connection()
            cur = conn.cursor(buffered=True, dictionary=True)

            on_time_str = on_time.strftime("%Y-%m-%d %H:%M:%S")

            # الحصول على آخر حدث بدون on_time
            cur.execute("""
                SELECT id, off_time FROM events
                WHERE feeder_id = %s AND on_time IS NULL
                ORDER BY off_time DESC LIMIT 1
            """, (feeder_id,))
            row = cur.fetchone()

            if not row:
                return False, "لا يوجد حدث إطفاء بدون تشغيل"

            # تعديل هنا
            event_id = row['id']
            off_time_str = row['off_time']

            from datetime import datetime
            off_time_dt = datetime.strptime(str(off_time_str), "%Y-%m-%d %H:%M:%S")
            on_time_dt = datetime.strptime(on_time_str, "%Y-%m-%d %H:%M:%S")
            duration_seconds = int((on_time_dt - off_time_dt).total_seconds())
            duration_minutes = duration_seconds // 60

            cur.execute("""
                UPDATE events
                SET on_time = %s, total_off_duration = %s
                WHERE id = %s
            """, (on_time_str, duration_minutes, event_id))

            conn.commit()
            return True, f"✅ تم تسجيل وقت التشغيل. المدة: {duration_minutes} دقيقة."

        except Exception as e:
            return False, f"❌ خطأ: {e}"

        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()


    def delete_feeder_by_id(self, feeder_id):
        try:
            conn = get_connection()
            cur = conn.cursor(buffered=True, dictionary=True)

            cur.execute("DELETE FROM feeders WHERE id = %s", (feeder_id,))
            conn.commit()

            if cur.rowcount == 0:
                return False, "❌ لم يتم العثور على الفيدر المحدد."
            else:
                return True, "✅ تم حذف الفيدر بنجاح."

        except Exception as e:
            return False, f"❌ خطأ: {e}"

        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    def delete_user_by_id(self,user_name):
        if not user_name :
            return False,"يرجى ملئ جميع الحقول !!"
        
        try:
            conn = get_connection()
            cur =conn.cursor(dictionary=True,buffered=True)

            cur.execute("""DELETE FROM users WHERE user_name = %s""",(user_name,))
            conn.commit()

            if cur.rowcount == 0:
                return False, "❌ لم يتم العثور على المستخدم المحدد."
            else :
              return True, "   تم حذف المستخدم ينجاح✅    ."
            
        except Exception as e:
            return False, f"❌ خطأ: {e}"

        finally:
            if cur:
                cur.close()
            if conn:
                conn.close



    def update_feeder(self, feeder_id, new_name, new_type):
        try:
            conn = get_connection()
            cur = conn.cursor(buffered=True, dictionary=True)

            # تحديث جدول feeders
            cur.execute("""
                UPDATE feeders
                SET feeder_name = %s, feeder_type = %s
                WHERE id = %s
            """, (new_name, new_type, feeder_id))
            feeders_updated = cur.rowcount  # عدد الصفوف التي تم تحديثها في جدول feeders

            # تحديث جدول events لنفس الفيدر
            cur.execute("""
                UPDATE events
                SET feeder_name = %s, feeder_type = %s
                WHERE feeder_id = %s
            """, (new_name, new_type, feeder_id))
            events_updated = cur.rowcount  # عدد الصفوف التي تم تحديثها في جدول events (قد تكون صفر)

            conn.commit()

            if feeders_updated == 0:
                return False, "❌ لم يتم العثور على الفيدر المحدد للتعديل."
            else:
                return True, f"✅ تم تعديل بيانات الفيدر بنجاح. ({events_updated} حدث/أحداث تم تحديثها)"

        except Exception as e:
            return False, f"❌ خطأ: {e}"

        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()


    def fetch_events(self):
        try:
            conn = get_connection()
            cur = conn.cursor(buffered=True, dictionary=True)
            cur.execute("""
                SELECT feeder_name, feeder_type, off_time, on_time
                FROM events
                ORDER BY off_time DESC
                LIMIT 50
            """)
            rows = cur.fetchall()
            return rows
        except Exception as e:
            print("Error fetching events:", e)
            return []
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
