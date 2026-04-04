from models import Candidate
from services.embedding import get_embedding
from services.qdrant_service import init_collection, upsert_candidate


candidates = [
    Candidate(
        id=1,
        name="Ayşe Kaya",
        title="Senior Frontend Developer",
        location="İstanbul",
        experience_years=5,
        skills=["React", "TypeScript", "Next.js", "TailwindCSS"],
        university="Koç Üniversitesi",
        department="Bilgisayar Mühendisliği",
        summary=""
    ),
    Candidate(
        id=2,
        name="Mehmet Demir",
        title="Backend Developer",
        location="Ankara",
        experience_years=3,
        skills=["Python", "FastAPI", "PostgreSQL", "Docker"],
        university="ODTÜ",
        department="Yazılım Mühendisliği",
        summary=""
    ),
    Candidate(
        id=3,
        name="Elif Yılmaz",
        title="Full Stack Developer",
        location="İstanbul",
        experience_years=4,
        skills=["React", "Node.js", "TypeScript", "MongoDB"],
        university="İTÜ",
        department="Bilgisayar Mühendisliği",
        summary=""
    ),
    Candidate(
        id=4,
        name="Can Özkan",
        title="DevOps Engineer",
        location="İzmir",
        experience_years=6,
        skills=["Kubernetes", "Docker", "AWS", "Terraform", "CI/CD"],
        university="Ege Üniversitesi",
        department="Bilgisayar Mühendisliği",
        summary=""
    ),
    Candidate(
        id=5,
        name="Zeynep Arslan",
        title="Data Scientist",
        location="İstanbul",
        experience_years=3,
        skills=["Python", "TensorFlow", "Pandas", "SQL", "Scikit-learn"],
        university="Boğaziçi Üniversitesi",
        department="Matematik",
        summary=""
    ),
    Candidate(
        id=6,
        name="Burak Şahin",
        title="Mobile Developer",
        location="Ankara",
        experience_years=4,
        skills=["React Native", "Flutter", "TypeScript", "Firebase"],
        university="Bilkent Üniversitesi",
        department="Elektrik-Elektronik Mühendisliği",
        summary=""
    ),
    Candidate(
        id=7,
        name="Selin Koç",
        title="Backend Developer",
        location="İstanbul",
        experience_years=2,
        skills=["Java", "Spring Boot", "PostgreSQL", "RabbitMQ"],
        university="Sabancı Üniversitesi",
        department="Bilişim Teknolojileri",
        summary=""
    ),
    Candidate(
        id=8,
        name="Emre Aydın",
        title="Frontend Developer",
        location="İzmir",
        experience_years=3,
        skills=["Vue.js", "TypeScript", "Nuxt.js", "SCSS"],
        university="Dokuz Eylül Üniversitesi",
        department="Yönetim Bilişim Sistemleri",
        summary=""
    ),
    Candidate(
        id=9,
        name="Deniz Çelik",
        title="ML Engineer",
        location="İstanbul",
        experience_years=5,
        skills=["Python", "PyTorch", "MLflow", "Docker", "FastAPI"],
        university="İTÜ",
        department="Yapay Zeka ve Veri Mühendisliği",
        summary=""
    ),
    Candidate(
        id=10,
        name="Hakan Yıldız",
        title=".NET Developer",
        location="Bursa",
        experience_years=4,
        skills=["C#", ".NET Core", "SQL Server", "Entity Framework", "Azure"],
        university="Uludağ Üniversitesi",
        department="Bilgisayar Mühendisliği",
        summary=""
    ),
]


def generate_summary(candidate: Candidate) -> str:
    skills_text = ", ".join(candidate.skills)
    return (
        f"{candidate.name} | {candidate.title} | {candidate.location}\n"
        f"{skills_text}\n"
        f"{candidate.experience_years} yıl deneyim\n"
        f"{candidate.university} - {candidate.department}"
    )


def seed():
    print("=" * 50)
    print("Seed başlıyor...")
    print("=" * 50)

    init_collection()

    for candidate in candidates:
        candidate.summary = generate_summary(candidate)
        print(f"\n[Summary] {candidate.name}:")
        print(candidate.summary)

        embedding = get_embedding(candidate.summary)
        upsert_candidate(candidate, embedding)

    print("\n" + "=" * 50)
    print(f"Seed tamamlandı! {len(candidates)} aday Qdrant'a yüklendi.")
    print("=" * 50)


if __name__ == "__main__":
    seed()