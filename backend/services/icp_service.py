import json
from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """Sen bir aday arama sorgusu analiz eden asistansın.
Kullanıcının sorgusundan şu bilgileri JSON olarak çıkar:

- location: Şehir adı (bulamazsan null)
- skills: Teknoloji/skill listesi (bulamazsan boş liste [])
- min_experience: Minimum deneyim yılı (bulamazsan null)
- university: Üniversite adı (bulamazsan null)
- search_text: Skill'ler dahil, semantic arama için kullanılacak kısım

Sadece JSON döndür, başka bir şey yazma.

Örnek:
Sorgu: "İstanbul'da 3 yıl deneyimli React bilen full stack developer"
Cevap: {"location": "İstanbul", "skills": ["React"], "min_experience": 3, "university": null, "search_text": "React bilen full stack developer"}

Örnek:
Sorgu: "Boğaziçi mezunu Python bilen backend developer"
Cevap: {"location": null, "skills": ["Python"], "min_experience": null, "university": "Boğaziçi Üniversitesi", "search_text": "Python bilen backend developer"}
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
    except json.JSONDecodeError:
        print("[ICP] JSON parse hatası, fallback kullanılıyor")
        return {
            "location": None,
            "skills": [],
            "min_experience": None,
            "university": None,
            "search_text": query
        }