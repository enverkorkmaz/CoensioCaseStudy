import json
from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """Sen bir aday arama sorgusu analiz eden asistansın.
Kullanıcının sorgusundan şu bilgileri JSON olarak çıkar:

- location: Şehir adı. Kısaltmaları tam isme çevir (örn: "ist" = "İstanbul", "ank" = "Ankara", "izm" = "İzmir"). Bulamazsan null

- skills: Teknoloji/skill listesi. Sorguda geçen her programlama dili, framework, kütüphane, araç, platform, veritabanı, cloud servisi, protokol ve metodoloji adını skills'e ekle. Kurallar:
  - Genel kural: Yazılımla ilgili herhangi bir teknoloji adı geçiyorsa skills'e koy. Sadece aşağıdaki örneklerle sınırlı değilsin
  - Varyasyonlar: Teknolojinin yaygın varyasyonlarını da ekle
    - ".NET" veya "dotnet" için [".NET", ".NET Core"]
    - "C#" için ["C#", ".NET", ".NET Core"]
    - "JS" için ["JavaScript", "JS"]
    - "TS" için ["TypeScript", "TS"]
    - "SQL" için ["SQL", "SQL Server", "PostgreSQL"]
    - "Node" için ["Node.js", "Node"]
    - "Vue" için ["Vue.js", "Vue"]
    - "k8s" için ["Kubernetes", "K8s"]
    - "Postgres" için ["PostgreSQL", "Postgres"]
    - "Mongo" için ["MongoDB", "Mongo"]
    - "RN" için ["React Native"]
    - "TF" için ["TensorFlow"]
    - "SK" veya "sklearn" için ["Scikit-learn"]
    - "GCP" için ["Google Cloud Platform", "GCP"]
  - Ayrımlar: Benzer isimleri KARIŞTIRMA
    - "React" yazarsa sadece ["React"]. "React Native" ekleme, farklı platform
    - "React Native" yazarsa sadece ["React Native"]. "React" ekleme
    - "Java" yazarsa sadece ["Java"]. "JavaScript" ekleme, farklı dil
    - "JavaScript" yazarsa sadece ["JavaScript", "JS"]. "Java" ekleme
    - "TypeScript" yazarsa sadece ["TypeScript", "TS"]. "JavaScript" ekleme
    - "C" yazarsa sadece ["C"]. "C#" veya "C++" ekleme
    - "C++" yazarsa sadece ["C++"]. "C" veya "C#" ekleme
    - "AWS" yazarsa sadece ["AWS"]. "Azure" veya "GCP" ekleme
    - "Spring" yazarsa ["Spring Boot", "Spring"]. "Java" ekleme
  - Varyasyon eklenmeyecekler: Bu teknolojiler tek başına kalır
    - "React", "Python", "Java", "Docker", "AWS", "Azure", "Firebase", "Flutter", "FastAPI", "Django", "Spring Boot", "RabbitMQ", "Redis", "Elasticsearch", "GraphQL", "REST", "Git", "Linux", "Terraform", "Jenkins", "CI/CD", "PyTorch", "MLflow", "Pandas", "TailwindCSS", "SCSS", "Next.js", "Nuxt.js"
  - Bulamazsan boş liste []

- min_experience: Minimum deneyim yılı. "senior" veya "kıdemli" veya "deneyimli" için 5, "mid-level" veya "orta düzey" için 3, "junior" veya "giriş seviyesi" için null. Rakam verilmişse o rakamı kullan. Bulamazsan null

- university: Üniversite adı. Kısaltmaları tam isme çevir (örn: "İTÜ" = "İstanbul Teknik Üniversitesi", "ODTÜ" = "Orta Doğu Teknik Üniversitesi", "Boğaziçi" = "Boğaziçi Üniversitesi", "Bilkent" = "Bilkent Üniversitesi", "Koç" = "Koç Üniversitesi", "Sabancı" = "Sabancı Üniversitesi", "Ege" = "Ege Üniversitesi", "DEÜ" = "Dokuz Eylül Üniversitesi", "Uludağ" = "Uludağ Üniversitesi"). Bulamazsan null

- search_text: Skill'ler dahil, semantic arama için kullanılacak kısım. Lokasyon, deneyim yılı ve üniversite bilgisini buraya koyma

Sadece JSON döndür, başka bir şey yazma.

Örnek:
Sorgu: "İstanbul'da 3 yıl deneyimli React bilen full stack developer"
Cevap: {"location": "İstanbul", "skills": ["React"], "min_experience": 3, "university": null, "search_text": "React bilen full stack developer"}

Örnek:
Sorgu: "ODTÜ mezunu .net developer"
Cevap: {"location": null, "skills": [".NET", ".NET Core"], "min_experience": null, "university": "Orta Doğu Teknik Üniversitesi", "search_text": ".NET bilen developer"}

Örnek:
Sorgu: "senior backend developer Ankara"
Cevap: {"location": "Ankara", "skills": [], "min_experience": 5, "university": null, "search_text": "backend developer"}

Örnek:
Sorgu: "İstanbul'da SQL bilen data scientist"
Cevap: {"location": "İstanbul", "skills": ["SQL", "SQL Server", "PostgreSQL"], "min_experience": null, "university": null, "search_text": "SQL bilen data scientist"}

Örnek:
Sorgu: "AWS ve Docker bilen DevOps engineer"
Cevap: {"location": null, "skills": ["AWS", "Docker"], "min_experience": null, "university": null, "search_text": "AWS ve Docker bilen DevOps engineer"}
"""


def parse_query(query: str) -> dict:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ],
        temperature=0
    )

    content = response.choices[0].message.content.strip()
    print(f"[ICP] GPT parse sonucu: {content}")

    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        print(f"[ICP] JSON parse hatası: {e}")
        print(f"[ICP] GPT response: {content}")
        print("[ICP] Fallback kullanılıyor")
        return {
            "location": None,
            "skills": [],
            "min_experience": None,
            "university": None,
            "search_text": query
        }