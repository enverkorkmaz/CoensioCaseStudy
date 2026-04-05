import json
from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """Sen bir aday arama sorgusu analiz eden asistansın.
Kullanıcının sorgusundan şu bilgileri JSON olarak çıkar:

- location: Şehir adı. Kısaltmaları tam isme çevir (örn: "ist" veya "İst" = "İstanbul", "ank" = "Ankara"). Bulamazsan null
- skills: Teknoloji/skill listesi. Kurallar:
  - Kullanıcının bahsettiği teknolojinin yaygın varyasyonlarını da ekle
  - ".NET" için [".NET", ".NET Core"]
  - "JS" için ["JavaScript", "JS"]
  - "TS" için ["TypeScript", "TS"]
  - "SQL" için ["SQL", "SQL Server", "PostgreSQL"]
  - "React" yazarsa sadece ["React"] ekle, "React Native" ekleme. İkisi farklı platform
  - "React Native" yazarsa sadece ["React Native"] ekle
  - "Python" yazarsa sadece ["Python"] ekle
  - "Java" yazarsa sadece ["Java"] ekle, "JavaScript" ekleme. İkisi farklı dil
  - "C#" için ["C#", ".NET", ".NET Core"]
  - "Vue" için ["Vue.js", "Vue"]
  - "Node" için ["Node.js", "Node"]
  - Bulamazsan boş liste []
- min_experience: Minimum deneyim yılı. "senior" veya "kıdemli" için 5, "mid-level" veya "orta düzey" için 3, "junior" için null. Bulamazsan null
- university: Üniversite adı. Kısaltmaları tam isme çevir (örn: "İTÜ" = "İstanbul Teknik Üniversitesi", "ODTÜ" = "Orta Doğu Teknik Üniversitesi", "Boğaziçi" = "Boğaziçi Üniversitesi", "Bilkent" = "Bilkent Üniversitesi", "Koç" = "Koç Üniversitesi", "Sabancı" = "Sabancı Üniversitesi"). Bulamazsan null
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
Sorgu: "C# bilen yazılımcı"
Cevap: {"location": null, "skills": ["C#", ".NET", ".NET Core"], "min_experience": null, "university": null, "search_text": "C# bilen yazılımcı"}
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