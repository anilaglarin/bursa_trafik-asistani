# 🚦 Bursa Trafik Analizi - Text-to-SQL Yapay Zeka Asistanı

Bu proje, Bursa'nın saatlik trafik yoğunluk verilerini analiz eden ve kullanıcılara doğal dilde (Türkçe) rehberlik sağlayan yapay zeka destekli bir sohbet asistanıdır. Kullanıcıların yola çıkmadan önce en mantıklı saatleri bulmalarına yardımcı olurken, arka planda karmaşık veri tabanı sorgularını otonom olarak yönetir.

## 🧩 Mimari ve Temel Bileşenler

Bu projede standart RAG (Retrieval-Augmented Generation) yaklaşımı yerine, yapılandırılmış (structured) verilerle çok daha kesin ve halüsinasyonsuz sonuçlar veren **Text-to-SQL (NL2SQL)** mimarisi tercih edilmiştir:

*   🔄 **Text-to-SQL (NL2SQL) Mimarisi:**
    Kullanıcının doğal dildeki (Türkçe) sorularının, Büyük Dil Modeli (LLM) tarafından anlık olarak algılanıp geçerli PostgreSQL sorgularına dönüştürülmesi ve veritabanından dönen sayısal sonuçların tekrar insan diline çevrilmesi sürecidir.
*   🖥️ **Local LLM Runtime (LM Studio):**
    Veri gizliliğini sağlamak ve bulut API maliyetlerini sıfırlamak için yapay zeka modelinin tamamen cihaz üzerinde (On-Device) çalıştırılmasını sağlayan yerel sunucu ortamıdır.
*   🗄️ **Relational Database (PostgreSQL):**
    Vektör tabanlı (Vector DB) semantik aramalar yerine, saatlik trafik yoğunluk verilerinin katı ve ilişkisel bir yapıda tutulduğu, hızlı analitik sorgulara (AVG, SELECT vb.) imkan tanıyan veritabanı sistemidir.
*   💡 **Gelişmiş Prompt Engineering & Context Management:**
    Yapay zekanın SQL kurallarının dışına çıkmasını engellemek için hazırlanan sistem komutları (System Prompt) ve sohbetin önceki adımlarını (örneğin bahsedilen şehri) doğru hatırlaması için uygulanan bellek yönetimi (Context Flattening) teknikleridir.

## 🛠️ Kullanılan Teknolojiler

- **Arayüz (Frontend):** Python, Streamlit
- **Yapay Zeka (Backend):** OpenAI API Python Client, LM Studio (Qwen2.5-7b-instruct vb. yerel modeller)
- **Veritabanı ve Veri İşleme:** PostgreSQL, Pandas, SQLAlchemy

---

## 🚀 Kurulum ve Çalıştırma

Projeyi kendi bilgisayarınızda (lokalde) çalıştırmak için aşağıdaki adımları sırasıyla izleyin.

### 1. Gereksinimler
- Python 3.8 veya üzeri
- PostgreSQL
- [LM Studio](https://lmstudio.ai/)

### 2. Projeyi Klonlayın

Terminalinizi açın ve projeyi bilgisayarınıza indirin:

```bash
git clone https://github.com/anilaglarin/bursa_trafik-asistani.git```

Proje klasörünün içine girin:

```Bash
cd bursa_trafik-asistani```

3. Kütüphaneleri Yükleyin
Projenin çalışması için gerekli olan Python paketlerini kurun:

```Bash
pip install streamlit openai pandas sqlalchemy psycopg2-binary


4. Veritabanı Kurulumu
Projede bulunan traffic_data.csv dosyasını kendi PostgreSQL veritabanınıza aktarmanız gerekmektedir:

PostgreSQL'de bursa_trafik adında (veya istediğiniz isimde) boş bir veritabanı oluşturun.

DBeaver vb. bir araç kullanarak CSV dosyasını tt_hourlytraffic tablosu olarak içe aktarın (Import).

database.py dosyasındaki veritabanı bağlantı bilgilerini kendi sisteminize göre güncelleyin.

5. LM Studio Yapılandırması
LM Studio'yu açın ve Türkçe yeteneği olan bir model indirin (Örn: Qwen2.5-7b-instruct).

Sol menüden "Local Server" sekmesine gidin.

Portu 1234 olarak ayarlayın ve "Start Server" butonuna basarak API sunucusunu başlatın.


6. Uygulamayı Başlatın
Sistem ve veritabanı hazır olduğunda terminal üzerinden uygulamayı ayağa kaldırın:

Bash
streamlit run app.py


💡 Örnek Kullanım Senaryoları
Arayüz üzerinden asistana aşağıdaki gibi sorular sorabilirsiniz:

"Saat 18:00'de trafik nasıl?"

"Bursa'da yola çıkmak için en sakin saatler hangileri?"

"Akşam 17:00 ile 19:00 arası trafik nasıl, alternatif hangi saatleri önerirsin?"

Asistan bu soruları arka planda SQL'e çevirip tt_hourlytraffic tablosunda sorgular ve size net, anlaşılır bir analiz sunar.
