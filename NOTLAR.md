## RAG Nedir, Bu Projede Nasıl Kullandım?
RAG (Retrieval-Augmented Generation) LLM'lerin bilgi sınırlamalarını aşmak için geliştirilen mimaridir. LLM'ler eğitim verisindeki bilgiyi bilir ama eğitim sonrası eklenen verilere erişemiyor. RAG bu sorunu çözüyor.LLM'e cevap üretmeden önce dış kaynaktan ilgili bilgiyi çekip context olarak veriyor.

Retrieval: Bilgi Çekme: Kullanıcının sorgusunu alıp veri kaynagında(Vektör db) en alakalı bilgileri bulunup çekilir.

Generation: Cevap üretme: Bulunan bilgiler LLM'e context olarak verilir LLM bu bilgileri kullanarak kullanıcıya cevap üretir.

### Embedding
Rag'ın retrieval aşamasının çalışması için metinlerin veya sorguların karşılaştırılabilir bi formata dönüşmesi gerekiyor. Bu dönüşüm embedding ile yapılır.
Embedding metni sabit uzunlukta bir sayı dizisine çeviren bir işlemdir(sorgu->vektör)
Bu projede OPENAI text-embedding-3-small modelini kullandım ve her metin 1536 adet sayıdan oluşan bir vektöre dönüşüyor. Metinlerin anlamını bağlam ve ilişkilerini kodluyor. Anlamca birbirine benzer metinler birbirine yakın vektör üretiyor anlamca farklı metinler birbirinden uzak üretiliyor.

Mesela React dev ve frontend dev vektörleri biribirine yakın oluyor. Fakat React dev ve Barista vektörleri birbirinden uzak oluyor.

### Cosine Similarity
İki vektör arasındaki benzerliği ölçmek için kullanılıyor. İki vektör arasındaki açının cos(cosinus)'u hesaplıyor. 0-1 arası  değer. 1 tam eşleşme oluyor 0 ise alakasız oluyor.

### Bu Projede Nasıl Çalışıyor?
Projedeki pipeline şu adımlardan oluşuyor:

Veri Hazırlama (seed.py): 10 demo aday tanımlandı. Her adayın bilgileri (isim, title, lokasyon, skills, deneyim, üniversite) case study'de belirtilen formatta bir özet metne dönüştürüldü. Bu özet metin embedding modeline gönderilerek 1536 boyutlu bir vektör elde edildi. Vektör ve adayın tüm bilgileri (payload olarak) Qdrant vektör veritabanına kaydedildi.

ICP Parsing (icp_service.py): Kullanıcının doğal dildeki sorgusu GPT-4o-mini'ye gönderilir. GPT sorgudan lokasyon, skills, deneyim yılı ve üniversite bilgilerini JSON olarak çıkarır. Bu case study'de bonus olarak belirtilen ICP (Ideal Candidate Profile) özelliğidir. Lokasyon, deneyim ve üniversite bilgileri hard constraint olarak Qdrant metadata filtrelerine dönüştürülür.

HyDE (icp_service.py): Sorguyu direkt embedding'e çevirmek yerine GPT'ye "bu sorguya uyan aday nasıl görünürdü?" diye soruyorum. GPT, gerçek aday summary'leriyle aynı formatta bir hipotetik profil üretiyor. Bu profil embedding'e çevriliyor. Vektör uzayında gerçek adaylara çok daha yakın düşüyor, cosine similarity skorları ciddi ölçüde yükseliyor.

Hybrid Search (qdrant_service.py): ICP'den çıkan kesin kriterler (lokasyon, deneyim, üniversite) Qdrant'a metadata filtresi olarak uygulanır, aday havuzu daraltılır. HyDE embedding'i bu daraltılmış havuzda cosine similarity ile arama yapar. Skills için ayrı bir hard filter uygulamıyorum — HyDE zaten skills'i hipotetik profile dahil ettiği için semantic search bu kısmı hallediyor.

Sonuç Dönme: Qdrant, metadata filtreleri uygulandıktan sonra cosine similarity skoruna göre sıralanmış adayları döndürür. Her adayın bilgileri payload'dan okunur ve frontend'e JSON olarak gönderilir.

### Generation Neden Uygulamadım?
Bu projede RAG'ın Generation aşamasını uygulamadım. Case study'de istenen adayları bulup sıralamaktı, bulunan adaylar üzerinden LLM'e değerlendirme yaptırmak istenmedi.

Generation'ın bu projede en doğal karşılığı **LLM re-ranking** olurdu. Akış şöyle işlerdi: Qdrant'tan dönen adaylar GPT'ye context olarak verilir, GPT "bu sorguya göre hangi adaylar gerçekten alakalı, hangileri değil?" diye değerlendirir ve sıralamayı yeniden düzenlerdi. Generation illa kullanıcıya paragraf yazmak demek değil — retrieval çıktısını alıp LLM'in işlemesi, sıralaması veya filtrelemesi de Generation sayılır.

Bunu test ettiğimde somut bir problemi fark ettim: "React bilen backend developer" aramasında Data Scientist olan Zeynep Arslan 0.54 skor alıyordu. Cosine similarity için bu yüksek — çünkü model "Python, veri analizi, yazılım" ile "backend developer" arasındaki semantik farkı tam çözemedi. Ama GPT'ye bu adayları context olarak versem net olarak eleyecektir. İşte bu fark Generation adımının değeri.

ICP aşamasında LLM'i zaten kullandım (sorgu parsing için) ve HyDE için de kullandım (hipotetik profil üretimi için). Ama bunlar retrieval öncesi adımlar. Re-ranking ise retrieval sonrası, yani gerçek anlamda RAG'ın Generation kısmı olacaktı.

## Neden FastAPI Kullandım?

AI projelerinde Python neredeyse zorunlu — OpenAI SDK, Qdrant client, embedding kütüphaneleri hepsi Python'da. Backend de Python olunca entegrasyon sıfır sürtünme oluyor. FastAPI seçmemin iki somut sebebi var.

Birincisi Pydantic entegrasyonu. models.py'deki Candidate, SearchRequest gibi modeller hem validasyon hem JSON serialization yapıyor, ekstra kod yazmadan. Kullanıcıdan gelen isteği Pydantic otomatik parse ediyor, tip hatası varsa otomatik hata dönüyor.

İkincisi `/docs` endpoint'i. FastAPI çalıştırınca localhost:8000/docs adresinde Swagger UI otomatik geliyor. Geliştirme sürecinde frontend yazmadan API'yi test edebildim, bu ciddi zaman kazandırdı.

## Neden Vektör Veritabanı Kullanıyoruz, SQL'den Farkı Ne?

SQL veritabanında arama kelime eşleşmesine dayanır. WHERE skills LIKE '%React%' yazarsın sadece "React" kelimesi geçen kayıtları bulursun. Kullanıcı "frontend geliştirici" yazarsa React bilen bir adayı bulamazsın çünkü kelimeler farklı. Vektör veritabanında arama anlam benzerliğine dayanır. Metinler embedding modeli ile sayısal vektörlere dönüştürülür. "Frontend geliştirici" ile "React developer" vektör uzayında birbirine yakın noktalardır çünkü anlamca benzer. Cosine similarity ile bu yakınlık ölçülür ve kullanıcı tam kelimeyi bilmese bile anlamca benzer sonuçlar gelir.

Ancak geliştirme sürecinde gördüm ki vektör araması her şeyi çözmüyor özellikle kesin kriterlerde (lokasyon, deneyim yılı, üniversite) semantic search güvenilir değil(kücük model diye de problem yasanmıs olabilir) "İstanbul'da developer" aradığımda Ankara'daki adaylar da geliyordu.
Bu sorunu hybrid search yaklaşımıyla çözdüm. Kesin kriterler (lokasyon, deneyim, üniversite) Qdrant'ın filtreleme özelliğiyle, anlamsal kriterler (rol, genel yetkinlik) ise cosine similarity ile değerlendiriliyor. Araştırmalarımda gördüm ki production seviyesindeki aday arama sistemleri aynı hybrid mimariye ulaşmış — metadata filtreleri havuzu daraltıyor, semantic search bu daraltılmış havuzda sıralama yapıyor.

### Neden Qdrant?
Vektör veritabanı seçenekleri arasında Pinecone, Weaviate, Chroma gibi alternatifler de var. Qdrant'ı tercih etmemin sebebi open source olması ve Docker image'ının hazır gelmesi — tek satır komutla lokalde çalıştırabildim. Ama asıl fark eden özelliği payload filtering. Qdrant'ta her vektörün yanında JSON payload saklayabiliyorsun (lokasyon, deneyim gibi) ve bu alanlara göre filtreleme native olarak destekleniyor. Hybrid search'i mümkün kılan tam da bu özellik.

## Daha Fazla Zamanım Olsaydı Ne Eklerdim?

### Cosine Similarity Skorlarının İyileştirilmesi
Başlangıçta cosine similarity skorları 0.20–0.50 arasında kalıyordu ve adaylar arasında anlamlı bir ayrışma olmuyordu. HyDE ile bu sorunu büyük ölçüde çözdüm, skorlar 0.70+ seviyesine çıktı. Ancak hâlâ iyileştirilebilecek noktalar var.

Kısa summary metinleri: 4-5 satırlık özet metinlerde embedding modeli yeterince anlamsal sinyal bulamıyor. Çözümü summary'lere etiketli alanlar eklemek ("Skills:", "Experience:" gibi) ve proje detayları, sorumluluklar gibi zengin içerik yazmak. Daha fazla adaya da ihtiyaç var — 10 adaylık havuzda tüm skorlar birbirine yakın çıkıyor, aday sayısı arttıkça gerçekten alakasız olanlar ayrışır.

text-embedding-3-small modeli cosine similarity açısından yeterli ama sınırlı. Daha büyük modeller (text-embedding-3-large gibi) daha iyi ayrışma sağlıyor, ancak API maliyeti artıyor.

### Multi-Embedding Yaklaşımı
Şu an her aday için tek bir vektör üretiyorum. Ancak araştırmamda gördüm ki production sistemlerde aday başına birden fazla embedding kullanılıyor skills için ayrı, deneyim için ayrı, eğitim için ayrı vektörler. Bu vektörler ağırlıklı olarak birleştiriliyor (örneğin 0.4 × skills + 0.35 × experience + 0.15 × education + 0.1 × diğer). Qdrant bunu named vectors özelliği ile destekliyor. Bu yaklaşım, tek vektörde farklı bilgilerin birbirine karışması sorununu çözer.

### HyDE (Hypothetical Document Embeddings)
Şu an kullanıcının sorgusunu direkt embedding'e çeviriyorum. Ama sorgu metni ile aday summary'si çok farklı formatlarda  sorgu kısa ve soru tarzında, summary ise yapısal bir özet. HyDE yaklaşımında sorgu önce LLM'e verilir, LLM hipotetik bir ideal aday profili üretir, sonra bu profil embedding'e çevrilir.

**Güncelleme: HyDE'yi implemente ettim.** Sorguyu direkt embed etmek yerine önce GPT-4o-mini'ye "bu sorguya uyan aday nasıl görünürdü?" diye soruyorum, dönen hipotetik profili embed ediyorum. GPT seed.py'deki aday formatında bir metin üretiyor (İsim | Başlık | Şehir, skills, deneyim yılı, üniversite) bu yüzden vektör uzayında gerçek aday summary'lerine çok daha yakın düşüyor. Similarity skorlarında ciddi iyileşme gördüm: önceden 0.20-0.50 arasında takılıyordu, HyDE ile 0.70+ skorlar almaya başladım. Bir not olarak HyDE'deki LLM çağrısı RAG'ın Generation aşamasıyla karıştırılabilir ama aslında farklı şeyler. RAG'ın Generation'ı retrieval sonrası kullanıcıya cevap üretmek için LLM kullanmak, HyDE ise retrieval'dan önce arama vektörünü iyileştirmek için LLM kullanmak. Amaç ve konum farklı.

### Generation Adımı (LLM Re-ranking)
RAG'ın Generation kısmını LLM re-ranking olarak implemente edebilirdim. Qdrant'tan dönen adaylar GPT'ye context olarak verilir, GPT sorguya göre hangisinin alakalı hangisinin alakasız olduğuna karar verir ve sıralamayı yeniden düzenlerdi.

Cosine similarity tek başına yetersiz kalıyor: "React bilen backend developer" aramasında Data Scientist 0.54 alıyor çünkü model her ikisinin de yazılım dünyasında olduğunu görüp tam ayırt edemiyor. GPT bu farkı rahatlıkla anlayacaktır. Re-ranking eklenmiş olsaydı akış şöyle olurdu:

```
Sorgu → ICP → HyDE → Embed → Qdrant (10 aday) → GPT re-ranking → 3-4 gerçekten alakalı aday
```

Her aramada 3 LLM çağrısı (ICP + HyDE + re-ranking) olacaktı, maliyet ve latency artardı ama kalite ciddi iyileşirdi.

### Unit Testler
Projede test yok. Pydantic validasyonları ve saf fonksiyonlar için testler hızlı yazılabilir ama icp_service, embedding ve qdrant_service OpenAI ve Qdrant'a bağımlı olduğu için bunları test etmek mock gerektiriyor. pytest + unittest.mock ile her servis için mock setup yazılması gerekiyor, bu da ciddi zaman alıyor. Önceliğim çalışan sistemi kurmaktı, testler sonraki adım olurdu.

### Diğer Geliştirmeler
Daha büyük ve çeşitli aday veri seti
Frontend'de filtre UI'ı (lokasyon, skill, deneyim dropdown'ları)

## Kaynaklar
Claude Deep Research kullandığım için göz attığı bazı kaynaklar:

- SOO Group: https://thesoogroup.com/blog/semantic-talent-matching-vector-search
- Ingedata: https://anykeyh.hashnode.dev/talent-matching-with-vector-embeddings
- Eightfold AI: https://eightfold.ai/engineering-blog/ai-powered-talent-matching-the-tech-behind-smarter-and-fairer-hiring/
- Qdrant HR Tech: https://qdrant.tech/hr-tech/
- Qdrant Filtering Guide: https://qdrant.tech/articles/vector-search-filtering/
- Qdrant LLM Filter Automation: https://qdrant.tech/documentation/search-precision/automate-filtering-with-llms/
