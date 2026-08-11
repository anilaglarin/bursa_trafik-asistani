from openai import OpenAI
from database import execute_query

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

def generate_sql(kullanici_sorusu):
    schema = """Sen sadece PostgreSQL kodu üreten bir yapay zekasın. 
Tablo Adı: tt_hourlytraffic
Kolonlar: ulke(TEXT), sehir(TEXT), tarih(INT), gun(INT), h00, h01, h02, h03, h04, h05, h06, h07, h08, h09, h10, h11, h12, h13, h14, h15, h16, h17, h18, h19, h20, h21, h22, h23 (INT).

KURAL 1: Açıklama, yorum veya markdown kullanma. SADECE SQL KODU YAZ.
KURAL 2: GROUP BY KULLANMA. Her zaman TEK SATIR (AVG) döndür.
KURAL 3: Soru "alternatif", "en uygun saat", "en yoğun", "akıllıca", "mantıksız" vb. kelimeler içeriyorsa 24 saatin tamamını (h00'dan h23'e kadar) SELECT et.
KURAL 4: Şehir veya ülke filtrelemesi yaparken HER ZAMAN LOWER() kullan. Örn: WHERE LOWER(sehir) = 'bursa'

ÖRNEKLER:
Soru: Saat 1'de trafik nasıl?
Cevap: SELECT AVG(h01) FROM tt_hourlytraffic;

Soru: Yarın bursa trafiğine çıkacağım mantıklı mı, alternatif saatler söyle
Cevap: SELECT AVG(h00), AVG(h01), AVG(h02), AVG(h03), AVG(h04), AVG(h05), AVG(h06), AVG(h07), AVG(h08), AVG(h09), AVG(h10), AVG(h11), AVG(h12), AVG(h13), AVG(h14), AVG(h15), AVG(h16), AVG(h17), AVG(h18), AVG(h19), AVG(h20), AVG(h21), AVG(h22), AVG(h23) FROM tt_hourlytraffic WHERE LOWER(sehir) = 'bursa';
"""
    
    response = client.chat.completions.create(
        model="qwen2.5-7b-instruct-1m", 
        messages=[
            {"role": "system", "content": schema},
            {"role": "user", "content": kullanici_sorusu}
        ],
        temperature=0.0 
    )
    return response.choices[0].message.content.strip()

def analyze_traffic(kullanici_sorusu, sql_sonucu):
    analiz_promptu = """Sen bir trafik asistanısın. 
Aşağıda kullanıcının sorusu ve veritabanından çekilen trafik yoğunluk verileri var.

KURAL 1: Veritabanından gelen veriler "None" veya "NULL" ise doğrudan "Bu kritere uygun veri bulunamadı." de.
KURAL 2: Kullanıcı alternatif veya en mantıklı/mantıksız saatleri soruyorsa, verilerdeki en düşük ve en yüksek yoğunluklu saatleri analiz edip saat aralıkları ver.
KURAL 3: Gelen verideki sayıları KESİNLİKLE METNE YAZMA. Sayıları sadece aşağıdaki skalaya göre çevirerek yorumla:
   - 0 ile 20 arası: Trafik çok sakin ve akıcı.
   - 21 ile 40 arası: Trafik normal ve orta yoğunlukta.
   - 41 ile 60 arası: Trafik yoğun.
   - 61 ve üzeri: Trafik çok yoğun veya kilitli.
KURAL 4: KESİNLİKLE SADECE TÜRKÇE YANIT VER.

ÖRNEKLER:
Soru: Saat 12'de trafik nasıl?
Veri: [(16.53,)]
Cevap: Saat 12'de trafik çok sakin ve akıcı görünüyor. Yola çıkmak için harika bir zaman.

Soru: Bana bursada trafiğe çıkmanın en akıllıca olduğu zamanları ve en mantıksız zamanları söyle.
Veri: [(12.1, 10.5, 9.2, 8.4, 11.2, 15.6, 25.4, 45.2, 42.1, 35.6, 30.2, 32.5, 33.1, 34.2, 35.8, 38.4, 40.1, 48.5, 52.3, 41.2, 30.5, 22.1, 18.4, 14.2)]
Cevap: Trafiğe çıkmak için en mantıksız zamanlar, trafiğin yoğun olduğu sabah 07:00-09:00 arası ve akşam 17:00-19:00 arasıdır. En akıllıca zamanlar ise trafiğin çok sakin ve akıcı olduğu gece saatleri (00:00-06:00) ile akşam 21:00 sonrasıdır.
"""
    
    response = client.chat.completions.create(
        model="qwen2.5-7b-instruct-1m",
        messages=[
            {"role": "system", "content": analiz_promptu},
            {"role": "user", "content": f"Soru: {kullanici_sorusu}\nVeri: {sql_sonucu}"}
        ],
        temperature=0.1 
    )
    return response.choices[0].message.content.strip()

def process_request(kullanici_sorusu):
    sql_query = generate_sql(kullanici_sorusu)
    
    if "SELECT" in sql_query.upper():
        sql_query = sql_query[sql_query.upper().find("SELECT"):]
    if ";" in sql_query:
        sql_query = sql_query[:sql_query.find(";")+1]
        
    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
    
    print(f"Üretilen SQL:\n{sql_query}\n")
    
    db_sonuc = execute_query(sql_query)
    
    if not db_sonuc or all(x is None for x in db_sonuc[0]):
        return "Veritabanında belirttiğiniz kriterlere uygun veri bulunamadı."
    
    if len(db_sonuc) > 5:
        db_sonuc = db_sonuc[:5]
    
    return analyze_traffic(kullanici_sorusu, db_sonuc)

if __name__ == "__main__":
    print("🚦 Trafik Asistanı Terminal Sohbetine Hoş Geldiniz!")
    print("(Çıkmak için 'q' veya 'çıkış' yazabilirsiniz)\n")
    
    while True:
        soru = input("Sen: ")
        
        if soru.lower() in ['q', 'çıkış', 'exit']:
            print("Sohbet sonlandırıldı. İyi günler!")
            break
            
        if not soru.strip():
            continue
            
        cevap = process_request(soru)
        print(f"\n🤖 Asistan:\n{cevap}\n")
        print("-" * 50)