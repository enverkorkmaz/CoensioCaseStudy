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
        summary="5 yıldır frontend alanında çalışıyorum. React ve TypeScript ana teknolojilerim. Büyük ölçekli SPA projeleri geliştirdim, component mimarisi ve state management konularında deneyimliyim. Next.js ile SSR projeler yaptım."
    ),
    Candidate(
        id=2,
        name="Mehmet Demir",
        title="Backend Developer",
        location="Ankara",
        experience_years=3,
        skills=["Python", "FastAPI", "PostgreSQL", "Docker"],
        university="Orta Doğu Teknik Üniversitesi",
        department="Yazılım Mühendisliği",
        summary="Python ile backend geliştirme yapıyorum. FastAPI ile RESTful API tasarımı, PostgreSQL ile veritabanı yönetimi ve Docker ile konteynerizasyon konularında deneyimliyim. Mikroservis mimarisine hakimim."
    ),
    Candidate(
        id=3,
        name="Elif Yılmaz",
        title="Full Stack Developer",
        location="İstanbul",
        experience_years=4,
        skills=["React", "Node.js", "TypeScript", "MongoDB"],
        university="İstanbul Teknik Üniversitesi",
        department="Bilgisayar Mühendisliği",
        summary="Hem frontend hem backend tarafında çalışabiliyorum. React ile kullanıcı arayüzleri, Node.js ile API geliştirme yapıyorum. MongoDB ile NoSQL veritabanı deneyimim var. Uçtan uca proje geliştirmeyi seviyorum."
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
        summary="DevOps ve bulut altyapı yönetimi konusunda 6 yıllık deneyimim var. Kubernetes ile container orchestration, AWS üzerinde altyapı kurulumu ve Terraform ile infrastructure as code uygulamaları yapıyorum. CI/CD pipeline kurulumu ve yönetimi konusunda deneyimliyim."
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
        summary="Veri bilimi ve makine öğrenmesi alanında çalışıyorum. Python ile veri analizi, TensorFlow ile derin öğrenme modelleri geliştiriyorum. İstatistiksel analiz ve veri görselleştirme konularında deneyimliyim."
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
        summary="Mobil uygulama geliştirme konusunda deneyimliyim. React Native ve Flutter ile cross-platform uygulamalar geliştiriyorum. Firebase ile backend entegrasyonu ve push notification sistemleri kurdum."
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
        summary="Java ve Spring Boot ile backend geliştirme yapıyorum. RESTful API tasarımı, veritabanı yönetimi ve mesaj kuyruk sistemleri konularında deneyim kazandım. Kurumsal projelerde çalıştım."
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
        summary="Vue.js ekosisteminde frontend geliştirme yapıyorum. Nuxt.js ile SSR uygulamalar, SCSS ile responsive ve modern arayüzler geliştiriyorum. Kullanıcı deneyimi odaklı çalışıyorum."
    ),
    Candidate(
        id=9,
        name="Deniz Çelik",
        title="ML Engineer",
        location="İstanbul",
        experience_years=5,
        skills=["Python", "PyTorch", "MLflow", "Docker", "FastAPI"],
        university="İstanbul Teknik Üniversitesi",
        department="Yapay Zeka ve Veri Mühendisliği",
        summary="Makine öğrenmesi modelleri geliştirip production ortamına deploy ediyorum. PyTorch ile model eğitimi, MLflow ile experiment tracking, FastAPI ile model serving ve Docker ile deployment yapıyorum."
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
        summary="C# ve .NET Core ile kurumsal yazılım geliştirme yapıyorum. Entity Framework ile ORM, SQL Server ile veritabanı yönetimi ve Azure üzerinde cloud deployment konularında deneyimliyim."
    ),
]


def generate_summary(candidate: Candidate) -> str:
    skills_text = ", ".join(candidate.skills)
    return (
        f"{candidate.name} | {candidate.title} | {candidate.location}\n"
        f"{skills_text}\n"
        f"{candidate.experience_years} yıl deneyim\n"
        f"{candidate.university} - {candidate.department}\n"
        f"{candidate.summary}"
    )


def seed():
    print("=" * 50)
    print("Seed başlıyor...")
    print("=" * 50)

    init_collection()

    for candidate in candidates:
        full_summary = generate_summary(candidate)
        print(f"\n[Summary] {candidate.name}:")
        print(full_summary)

        embedding = get_embedding(full_summary)
        upsert_candidate(candidate, embedding)

    print("\n" + "=" * 50)
    print(f"Seed tamamlandı! {len(candidates)} aday Qdrant'a yüklendi.")
    print("=" * 50)


if __name__ == "__main__":
    seed()