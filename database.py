import os
import psycopg2
from dotenv import load_dotenv

# .env dosyasındaki gizli bilgileri içe aktar
load_dotenv()

def get_db_connection():
    """PostgreSQL veritabanına güvenli bağlantı açar."""
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        return conn
    except Exception as e:
        print(f"❌ Veritabanı bağlantı hatası: {e}")
        return None

def execute_query(sql_query):
    """Verilen SQL sorgusunu çalıştırır ve sonuçları liste olarak döndürür."""
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        cursor.execute(sql_query)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        print(f"❌ SQL Çalıştırma Hatası: {e}")
        if conn:
            conn.close()
        return None

if __name__ == "__main__":
    print("Veritabanı bağlantısı test ediliyor...")
    try:
        sonuc = execute_query("SELECT COUNT(*) FROM tt_hourlytraffic;")
        if sonuc:
            print(f"✅ Bağlantı başarılı! Tablodaki toplam satır/veri sayısı: {sonuc[0][0]}")
        else:
            print("❌ Bağlantı kurulamadı veya sorgu çalıştırılamadı.")
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {e}")
