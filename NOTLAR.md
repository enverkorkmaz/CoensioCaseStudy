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
Projedeki Retrieval pipeline şu adımlardan oluşuyor:

Veri Hazırlama(seed.py): 10 demo aday tanımlandı. Her adayın bilgileri (isim, title, lokasyon, skills, deneyim, üniversite) case study'de belirtilen formatta bir özet metne dönüştürüldü. Bu özet metin embedding modeline gönderilerek 1536 boyutlu bir vektör elde edildi. Vektör ve adayın tüm bilgileri (payload olarak) Qdrant vektör veritabanına kaydedildi.
Sorgu İşleme(icp_service.py): Kullanıcının doğal dildeki sorgusu önce GPT-4o-mini'ye gönderilir. GPT, sorgudan yapısal bilgileri (lokasyon, skills, deneyim yılı, üniversite) JSON olarak çıkarır. Bu, case study'de bonus olarak belirtilen ICP (Ideal Candidate Profile) özelliğidir. Geriye kalan serbest metin ise semantic arama için kullanılır.
Hybrid Search(qdrant_service.py + main.py): ICP'den çıkan kesin kriterler (lokasyon, deneyim, üniversite) Qdrant'a metadata filtresi olarak gönderilir havuz daraltılır. Serbest metin ise embedding'e çevrilerek Qdrant'ta cosine similarity ile aranır. Skills için dual representation uyguladım skills hem ICP tarafından ayrı çıkarılıp Python'da case-insensitive olarak filtreleniyor hem de search_text içinde kalarak semantic aramaya dahil oluyor.
Sonuç Dönme: Qdrant, filtreler uygulandıktan sonra cosine similarity skoruna göre sıralanmış adayları döndürür. Her adayın bilgileri payload'dan okunur ve frontend'e JSON olarak gönderilir.

### Generation Neden Uygulamadım?
Bu projede RAG'ın Generation aşamasını uygulamadım. Case study'de istenen, adayları bulup sıralamaktı. bulunan adaylar üzerinden LLM'e değerlendirme yaptırmak istenmedi. Ancak Generation eklenmiş olsaydı, akış şu şekilde devam ederdi: Qdrant'tan dönen en uygun adaylar GPT'ye context olarak verilir, GPT "Bu adaylardan hangisi sorguya en uygun ve neden?" gibi karşılaştırmalı bir değerlendirme çıktısı üretirdi. Bu yaklaşım, cosine similarity skorlarının birbirine çok yakın çıktığı durumlarda mesela 0.4753 vs 0.4699, daha doğru ve açıklanabilir sıralama sağlardı.
ICP aşamasında LLM'i farklı bir amaçla (sorgu parsing) kullandım. Bu tam anlamıyla Generation değil ama bir LLM adımı eklemiş oldu.

## Neden Vektör Veritabanı Kullanıyoruz, SQL'den Farkı Ne?

SQL veritabanında arama kelime eşleşmesine dayanır. WHERE skills LIKE '%React%' yazarsın sadece "React" kelimesi geçen kayıtları bulursun. Kullanıcı "frontend geliştirici" yazarsa React bilen bir adayı bulamazsın çünkü kelimeler farklı. Vektör veritabanında arama anlam benzerliğine dayanır. Metinler embedding modeli ile sayısal vektörlere dönüştürülür. "Frontend geliştirici" ile "React developer" vektör uzayında birbirine yakın noktalardır çünkü anlamca benzer. Cosine similarity ile bu yakınlık ölçülür ve kullanıcı tam kelimeyi bilmese bile anlamca benzer sonuçlar gelir.

Ancak geliştirme sürecinde gördüm ki vektör araması her şeyi çözmüyor özellikle kesin kriterlerde (lokasyon, deneyim yılı, üniversite) semantic search güvenilir değil(kücük model diye de problem yasanmıs olabilir) "İstanbul'da developer" aradığımda Ankara'daki adaylar da geliyordu.
Bu sorunu hybrid search yaklaşımıyla çözdüm kesin kriterler (lokasyon, deneyim, üniversite) Qdrant'ın filtreleme özelliğiyle, anlamsal kriterler (rol, genel yetkinlik) ise cosine similarity ile değerlendiriliyor. Skills için de dual representation uyguladım  skills hem metadata  filtreleniyor hem de search_text içinde kalarak semantic arama'ya dahil oluyor. Claude ile araştırmalar yaptım ve bunlara göre production seviyesindeki aday arama sistemleri aynı hybrid mimariye ulaşmış. Metadata filtreleri havuzu daraltıyor semantic search bu daraltılmış havuzda sıralama yapıyor.

## Daha Fazla Zamanım Olsaydı Ne Eklerdim?

### Cosine Similarity Skorlarının İyileştirilmesi
bunun için bi süre ugraştım
Şu anki sistemde cosine similarity skorları düşük çıkıyor (0.20–0.50 arası genellikle max 0.60 geliyor) ve birbirine çok yakın. Bunun iki ana sebebi var

Kısa summary metinleri:
4 satırlık özet metinlerde embedding modeli yeterince anlamsal sinyal bulamıyor. Farklı profiller birbirine çok yakın vektörler üretiyor. Araştırmamda gördüm ki bu bilinen bir sorun çözümü, summary'lere etiketli alanlar eklemek ("Skills:", "Experience:" gibi) ve proje detayları, sorumluluklar gibi zengin içerik yazmak.(Yine de daha fazla adaya ve bilgiye(Metin, vektör için) ihtiyac var)

text-embedding-3-small modelinin: 
Bu model düşük cosine similarity skorları üretiyor. Daha büyük modellerde veya daha iyi modellerde daha iyi similarity skorları görebiliriz.

Küçük veri seti: 10 adaylık bir havuzda tüm skorlar birbirine yakın çıkıyor. Aday sayısı arttıkça gerçekten alakasız olanlar düşük alakalılar yüksek skor alır ve ayrışma netleşir.

### Multi-Embedding Yaklaşımı
Şu an her aday için tek bir vektör üretiyorum. Ancak araştırmamda gördüm ki production sistemlerde aday başına birden fazla embedding kullanılıyor skills için ayrı, deneyim için ayrı, eğitim için ayrı vektörler. Bu vektörler ağırlıklı olarak birleştiriliyor (örneğin 0.4 × skills + 0.35 × experience + 0.15 × education + 0.1 × diğer). Qdrant bunu named vectors özelliği ile destekliyor. Bu yaklaşım, tek vektörde farklı bilgilerin birbirine karışması sorununu çözer.

### HyDE (Hypothetical Document Embeddings)
Şu an kullanıcının sorgusunu direkt embedding'e çeviriyorum. Ama sorgu metni ile aday summary'si çok farklı formatlarda  sorgu kısa ve soru tarzında, summary ise yapısal bir özet. HyDE yaklaşımında sorgu önce LLM'e verilir, LLM hipotetik bir ideal aday profili üretir, sonra bu profil embedding'e çevrilir.

### Generation Adımı
RAG'ın Generation kısmı eklenebilirdi. Bulunan adaylar GPT'ye context olarak verilip karşılaştırmalı bir değerlendirme çıktısı üretilebilirdi. Cosine similarity skorlarının yetersiz kaldığı durumlarda (.NET Developer'ın Full Stack Developer'dan önce gelmesi gibi) daha doğru ve açıklanabilir sonuçlar sağlar.

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
