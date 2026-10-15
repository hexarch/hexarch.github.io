#!/usr/bin/env python3
"""hexarch.github.io — dizi.jpg blogu. Düz HTML üretir: python3 build.py"""
import html, json, os, re
from datetime import date

KOK = os.path.dirname(os.path.abspath(__file__))
SITE = "https://hexarch.github.io"
APP = "https://dizijpg.com"
PLAY = "https://play.google.com/store/apps/details?id=com.dizijpg.dizijpg"
IOS = "https://apps.apple.com/app/id6806987135"
IG = "https://www.instagram.com/dizi.jpg/"

DIL = {
    "tr": dict(ad="Türkçe", kok="/", blog="dizi.jpg Blog", slogan="Dizi ve film takibi üzerine notlar",
               yazilar="Yazılar", indir="Uygulamayı indir", web="Webde aç", oku="Devamını oku",
               dk="dk okuma", yazar="dizi.jpg geliştiricisi", kutu="Dizilerini ve filmlerini tek yerde takip et.",
               alt="Bu blog dizi.jpg uygulamasının geliştiricisi tarafından yazılır. İçerik verileri TMDB, yayın platformu bilgileri JustWatch kaynaklıdır.",
               app=APP + "/", locale="tr_TR"),
    "en": dict(ad="English", kok="/en/", blog="dizi.jpg Blog", slogan="Notes on tracking TV shows and movies",
               yazilar="Posts", indir="Get the app", web="Open on the web", oku="Read more",
               dk="min read", yazar="developer of dizi.jpg", kutu="Track your shows and movies in one place.",
               alt="This blog is written by the developer of dizi.jpg. Content data comes from TMDB, streaming availability from JustWatch.",
               app=APP + "/en", locale="en_US"),
    "es": dict(ad="Español", kok="/es/", blog="Blog de dizi.jpg", slogan="Notas sobre cómo seguir series y películas",
               yazilar="Artículos", indir="Descargar la app", web="Abrir en la web", oku="Seguir leyendo",
               dk="min de lectura", yazar="desarrollador de dizi.jpg", kutu="Sigue tus series y películas en un solo lugar.",
               alt="Este blog lo escribe el desarrollador de dizi.jpg. Datos de contenido de TMDB y disponibilidad en plataformas de JustWatch.",
               app=APP + "/es", locale="es_ES"),
}

def gorsel(dil, ad, alt):
    return (f'<figure><img src="/img/{dil}-{ad}.webp" width="540" height="960" loading="lazy" '
            f'alt="{html.escape(alt)}"><figcaption>{html.escape(alt)}</figcaption></figure>')

YAZILAR = []

# ---------------------------------------------------------------- TR 1
YAZILAR.append(dict(
    dil="tr", slug="dizi-film-kaydetme", tarih="2026-09-25",
    baslik="Dizi film kaydetme: izlediklerini kaybetmeden tutmanın en düzenli yolu",
    ozet="Not defteri, Excel, ekran görüntüsü… İzlediğin dizi ve filmleri kaydetmenin yollarını denedim; neden bir takip uygulamasında karar kıldığımı ve dizi.jpg'de bunu nasıl kurduğumu anlatıyorum.",
    govde=lambda: f"""
<p>Bir noktadan sonra herkes aynı soruya çarpıyor: <em>"Bunu izlemiş miydim?"</em> Film adını hatırlıyorsun ama sonunu hatırlamıyorsun. Bir dizinin üçüncü sezonunu açıyorsun, ilk bölümün ilk sahnesinde "ben bunu gördüm" diyorsun. İzlediklerini bir yere kaydetmemenin bedeli budur.</p>

<p>Ben bu blogu yazan kişiyim ve aynı zamanda <a href="{APP}/">dizi.jpg</a> adlı dizi ve film takip uygulamasının geliştiricisiyim. Bu yazıda dizi film kaydetme işini yıllar içinde hangi yollarla denediğimi, hangisinin neden dağıldığını ve sonunda nasıl bir düzen kurduğumu anlatacağım.</p>

<h2>Denediğim yöntemler ve neden bıraktım</h2>

<h3>1. Telefonun not uygulaması</h3>
<p>En kolay başlangıç. "İzlediklerim" diye bir not açıyorsun, altına adları yazıyorsun. İlk ay mükemmel çalışıyor. Sonra şu olur: diziler için bölüm bölüm yazmak zorlaşır, sıralama bozulur, aynı adı iki kez yazarsın, hangi yıl izlediğini bilemezsin. Not, bir liste olarak kalır; takip aracına dönüşmez.</p>

<h3>2. Excel veya Google E-Tablolar</h3>
<p>Düzenli insanın ikinci durağı. Sütunlar: ad, tür, puan, tarih. Güzel görünür ama dizilerde çöker. Bir dizinin 60 bölümünü tabloya işlemek kimsenin yapmak isteyeceği bir şey değil. Yeni sezon çıktığını da tablo sana söylemez.</p>

<h3>3. Ekran görüntüsü ve Instagram kaydedilenler</h3>
<p>"Sonra izlerim" diye afişlerin ekran görüntüsünü almak ya da gönderileri kaydetmek. Galeri bir mezarlığa dönüşür. İzleyeceklerini biriktirmek için iş görür ama izlediklerini kaydetmek için hiç görmez.</p>

<h2>Bir kaydın gerçekten işe yaraması için ne gerekiyor?</h2>
<p>Bu denemelerden sonra listem netleşti. İzlediklerini kaydettiğin yerin şu dört şeyi yapabilmesi lazım:</p>
<ol>
<li><strong>Bölüm düzeyinde takip.</strong> Filmde "izledim" yeterli; dizide "3. sezon 5. bölümdeyim" bilgisi gerekiyor.</li>
<li><strong>Kendi kendine güncellenmek.</strong> Yeni bölüm çıktığında senin haberin olmalı, sen aramadan.</li>
<li><strong>Durum ayrımı.</strong> İzleyeceğim, izliyorum, bitirdim, bıraktım. Bunlar ayrı raflarda durmalı.</li>
<li><strong>Taşınabilirlik.</strong> Kayıtların senin olmalı; istediğin an dosya olarak alabilmelisin.</li>
</ol>

<h2>dizi.jpg'de dizi ve film kaydetme nasıl işliyor?</h2>
<p>Bu dört maddeyi karşılamak için dizi.jpg'yi yazdım. Kısaca şöyle çalışıyor:</p>

<p><strong>Bölümü tek dokunuşla işaretliyorsun.</strong> Dizinin sayfasında sezonlar açılıyor, izlediğin bölüme dokunuyorsun, sezon ilerleme çubuğu doluyor.</p>
{gorsel("tr", "3-bolum-isaretleme", "dizi.jpg'de bölüm işaretleme ekranı")}

<p><strong>Kütüphanen kendiliğinden ayrılıyor.</strong> Eklediğin her yapım İzleyeceğim, İzliyorum, Bitirdim ya da Bıraktım rafına düşüyor. Filmler ve diziler ayrı sayılıyor, istatistik ekranında kaç saatini ekrana verdiğini görüyorsun.</p>

<p><strong>Yeni bölümler takvime düşüyor.</strong> Takip ettiğin dizilerin yaklaşan bölümleri <a href="{APP}/takvim">takvim ekranında</a> diziye göre gruplu duruyor; kaç bölüm geride olduğun da yazıyor. Yeni bölüm yayınlandığında telefonuna bildirim geliyor.</p>
{gorsel("tr", "4-takvim", "Yaklaşan bölümlerin listelendiği takvim ekranı")}

<p><strong>Puan ve not ekliyorsun.</strong> Her yapıma ve her bölüme puan verebiliyorsun; istersen kısa bir inceleme yazıyorsun. Aynı filmi ikinci kez izlediysen tekrar izleme olarak sayılıyor, ilk kaydın silinmiyor.</p>

<h2>Eski kayıtlarını taşımak</h2>
<p>Sıfırdan başlamak en büyük vazgeçme sebebi. Bu yüzden içe aktarımı ilk iş olarak yazdım:</p>
<ul>
<li><strong>TV Time</strong> kapanırken herkese verdiği dışa aktarma dosyası okunuyor; işaretli bölümlerin ve puanların yerine geliyor.</li>
<li><strong>Letterboxd</strong> dışa aktarımı okunuyor: izlediğin filmler, puanların ve listelerin.</li>
<li>Tek bir CSV ya da JSON dosyası da kabul ediliyor; ZIP şart değil.</li>
</ul>
<p>Kapı ters yöne de açık: Ayarlar'dan bütün verini dışa aktarabiliyorsun (ZIP e-postana gelir), hesabını da tamamen silebiliyorsun. Kaydın senin.</p>

<h2>Kaydetmenin bir yan etkisi: ne izleyeceğine karar vermek</h2>
<p>Kayıt tutmaya başlayınca "izleyeceklerim" listesi büyüyor ve bu sefer seçememe sorunu başlıyor. dizi.jpg'de bunun için iki şey var:</p>
<ul>
<li><strong>Çark:</strong> İzleyeceğim listeni çeviriyor, rastgele bir yapım seçiyor. Kararsız akşamlar için birebir.</li>
<li><strong>Bölüm ısı haritası:</strong> Bir dizinin bütün bölüm puanları sezon × bölüm ızgarasında. Hangi sezonun düştüğünü, nerede toparladığını tek bakışta görüyorsun. Örneğin <a href="{APP}/icerik/tv/1396">Breaking Bad sayfasında</a> bakabilirsin.</li>
</ul>
{gorsel("tr", "5-bolum-isi-haritasi", "Bir dizinin bölüm puanlarını gösteren ısı haritası")}

<h2>Kısa özet</h2>
<p>Dizi film kaydetme işini not uygulamasında ya da tabloda tutabilirsin; filmler için bir süre yeter de. Dizilere geçtiğin an bölüm takibi, yeni bölüm uyarısı ve durum rafları gerekiyor. Ben bu yüzden bir takip uygulamasına geçtim ve istediğim gibisini bulamayınca kendim yazdım.</p>
<p><a href="{APP}/">dizi.jpg</a> webde açılıyor; <a href="{PLAY}">Google Play</a> ve <a href="{IOS}">App Store</a>'da da var. Üye olmadan <a href="{APP}/kesfet">Keşfet sayfasını</a> gezebilirsin.</p>
"""))

# ---------------------------------------------------------------- TR 2
YAZILAR.append(dict(
    dil="tr", slug="tv-time-alternatifi", tarih="2026-09-25",
    baslik="TV Time kapandı: verilerini nereye taşımalısın?",
    ozet="TV Time kapanırken dışa aktarma dosyası verdi. O dosyayla ne yapabileceğini, bir TV Time alternatifinde nelere bakman gerektiğini ve dosyayı dizi.jpg'ye nasıl yükleyeceğini adım adım anlatıyorum.",
    govde=lambda: f"""
<p>Yıllarca TV Time kullananlar için kapanış haberi, izleme geçmişinin bir anda askıda kalması demekti. İyi tarafı şu: TV Time kapanmadan önce herkese verilerini dışa aktarma imkânı tanıdı. Kötü tarafı: elinde bir dosya var ve o dosyanın gideceği yer belli değil.</p>
<p>Ben de aynı durumdaydım. Bu yazıda bir TV Time alternatifi seçerken neye baktığımı ve dışa aktarma dosyasını <a href="{APP}/">dizi.jpg</a>'ye nasıl taşıyacağını anlatıyorum. Baştan söyleyeyim: dizi.jpg'nin geliştiricisi benim.</p>

<h2>Elindeki dosyada ne var?</h2>
<p>TV Time'ın dışa aktarımı bir ZIP dosyasıdır ve içinde birkaç CSV bulunur. En önemlileri izlenen bölümler, takip edilen diziler ve filmler ile puanlardır. Dosyayı açıp bakmak zorunda değilsin ama saklamalısın: başka bir yere taşımanın tek yolu bu dosya.</p>

<h2>Bir TV Time alternatifinde nelere bakmalı?</h2>
<ol>
<li><strong>TV Time dosyasını doğrudan içe aktarabiliyor mu?</strong> Elle tek tek işaretlemek yüzlerce saat sürer.</li>
<li><strong>Bölüm bazında takip var mı?</strong> Bazı uygulamalar sadece "izledim" listesi tutar; TV Time'ın asıl gücü bölüm takibiydi.</li>
<li><strong>Yaklaşan bölüm takvimi ve bildirim var mı?</strong></li>
<li><strong>Türkçe arayüz ve Türkçe içerik özetleri var mı?</strong></li>
<li><strong>Verini geri alabiliyor musun?</strong> Bir uygulamanın kapanabileceğini artık biliyoruz. Dışa aktarma şart.</li>
</ol>

<h2>Dosyayı dizi.jpg'ye yükleme adımları</h2>
<ol>
<li><a href="{APP}/">dizijpg.com</a>'da ya da uygulamada hesap aç.</li>
<li><strong>Ayarlar</strong> bölümünde <strong>Veri içe aktar (.zip / .csv)</strong> satırına dokun.</li>
<li>TV Time'dan indirdiğin ZIP dosyasını seç. Tek bir CSV de kabul ediliyor.</li>
<li>Aktarım bitince izlediğin bölümler işaretli, puanların yerinde olur. Kütüphanen İzliyorum / Bitirdim raflarına kendiliğinden ayrılır.</li>
</ol>
<p>Film geçmişini Letterboxd'da tutuyorsan onun dışa aktarımını da aynı ekrandan yükleyebilirsin; iki geçmiş tek kütüphanede birleşir.</p>

<h2>Taşıdıktan sonra neler var?</h2>
<p>TV Time'dan alışık olduğun temel şeyler yerinde: bölüm işaretleme, sezon ilerlemesi, yaklaşan bölümler, istatistikler. Bunların üstüne eklediklerim:</p>
<ul>
<li><strong>İki katmanlı spoiler koruması.</strong> Yorumu yazan spoiler işaretleyebiliyor; ayrıca sen bir bölümü izlemediysen o bölüme ait yorumlar sana bulanık geliyor, kimse işaretlemese bile.</li>
<li><strong>Bölüm ısı haritası ve puan dağılımı.</strong> Bir diziye başlamadan önce nerede düştüğünü görüyorsun.</li>
<li><strong>Nerede izlenir bilgisi.</strong> Yapımın hangi platformda olduğu sayfasında yazıyor.</li>
<li><strong>Birlikte izleme odaları ve mesajlaşma.</strong> Arkadaşlarınla aynı anda izleyip konuşabiliyorsun.</li>
</ul>
{gorsel("tr", "7-incelemeler", "dizi.jpg'de spoiler korumalı incelemeler")}

<h2>Bir daha aynı şeyi yaşamamak için</h2>
<p>dizi.jpg'de Ayarlar'dan bütün verini istediğin an dışa aktarabiliyorsun; ZIP dosyası e-postana gelir. İçinde TV Time biçiminde CSV'ler ve kayıpsız geri yükleme için bir JSON dosyası var. Yani bir gün başka yere geçmek istersen, bugün TV Time'dan aldığın kolaylığı sen de alırsın.</p>
<p>Uygulama webde, <a href="{PLAY}">Android</a>'de ve <a href="{IOS}">iPhone</a>'da var. Önce bakmak istersen <a href="{APP}/kesfet">Keşfet sayfası</a> üyelik istemiyor.</p>
"""))

# ---------------------------------------------------------------- TR 3
YAZILAR.append(dict(
    dil="tr", slug="ekim-izleme-rehberi", tarih="2026-10-15",
    baslik="Ekim izleme rehberi: en iyi korku filmleri, bilim kurgu ve 2026'nın en çok izlenen dizileri",
    ozet="Ekim akşamları için hazır listeler: izleyici puanına göre en iyi korku ve bilim kurgu filmleri, 2026'da en çok izlenen diziler ve yarım kalan sezonlara bölüm bölüm dönmenin yolu.",
    govde=lambda: f"""
<p>Ekim, korku filmlerinin ve yeni sezonların ayı. Ne izleyeceğine karar vermek için saatlerce afiş kaydırmak yerine hazır listelerden başlamak daha hızlı. Bu yazıda <a href="{APP}/">dizi.jpg</a>'deki listeleri nasıl kullandığımı ve yarım kalan dizilere nasıl döndüğümü anlatıyorum.</p>

<h2>En iyi korku filmleri: puanla sıralı liste</h2>
<p><a href="{APP}/raf/en-iyi-korku-filmleri">En iyi korku filmleri</a> listesi tüm zamanlardan, yeterli oy almış korku filmlerini izleyici puanına göre sıralıyor. İlk sıralarda <a href="{APP}/icerik/movie/539">Sapık</a>, <a href="{APP}/icerik/movie/694">Cinnet</a> ve <a href="{APP}/icerik/movie/25237">Gel ve Gör</a> var; hemen arkalarında Yaratık ve Şey gibi klasikler geliyor. Listede izlediklerini işaretleyince geriye kalanlar senin Ekim listen olur.</p>

<h2>En iyi bilim kurgu filmleri</h2>
<p>Korku sana göre değilse <a href="{APP}/raf/en-iyi-bilim-kurgu-filmleri">en iyi bilim kurgu filmleri</a> listesi aynı mantıkla çalışıyor. Başlarda Kurtuluş Projesi, <a href="{APP}/icerik/movie/157336">Yıldızlararası</a> ve Başlangıç var. Her filmin sayfasında oyuncular, puan dağılımı ve hangi platformda izlenebildiği yazıyor.</p>

<h2>2026'nın en çok izlenen dizileri</h2>
<p><a href="{APP}/raf/2026-yilinin-en-cok-izlenen-dizileri">2026'nın en çok izlenen dizileri</a> listesi bu yıl yeni bölümü yayınlanan dizileri izleyici oyu sayısına göre sıralıyor. Başta The Boys, Rick and Morty ve Peaky Blinders var. Yeni sezonu başlayan bir diziyi takibe aldığında yeni bölümler takvimine düşüyor.</p>

<h2>Yarım kalan sezona bölüm bölüm dön</h2>
<p>Bir diziye ara verdiysen sorun genelde "hangi bölümde kalmıştım?" sorusu. dizi.jpg'de her bölümün kendi sayfası var: örneğin <a href="{APP}/dizi/60625/sezon/9/bolum/10">Rick and Morty 9. sezon 10. bölüm</a> ya da <a href="{APP}/dizi/113962/sezon/3/bolum/4">Lioness 3. sezon 4. bölüm</a> sayfasında bölümün konusunu, konuk oyuncularını ve izleyici puanını görüp izledim olarak işaretleyebilirsin. Spoiler içeren yorumlar sen o bölümü izleyene kadar bulanık kalıyor.</p>

<h2>Listeyi kendine göre kullanmak</h2>
<ul>
<li>Listede izlediklerini işaretle; kalanlar izleme sıran olur.</li>
<li>Beğendiğin filmleri kendi listene ekle: "Ekim korku gecesi" gibi.</li>
<li>Arkadaşlarınla aynı filmi izleyeceksen izleme odası açıp aynı anda izleyebilirsin.</li>
</ul>
<p>dizi.jpg webde açılıyor; <a href="{PLAY}">Google Play</a> ve <a href="{IOS}">App Store</a>'da da var.</p>
"""))

# ---------------------------------------------------------------- EN
YAZILAR.append(dict(
    dil="en", slug="tv-movie-tracker", tarih="2026-09-25",
    baslik="What a good TV & movie tracker should do (and why I built one)",
    ozet="Episode-level progress, a real release calendar, spoiler-safe reviews and an export button. Here is the checklist I used when TV Time shut down, and how dizi.jpg handles each item.",
    govde=lambda: f"""
<p>A TV &amp; movie tracker sounds like a simple thing: a list of what you have watched. In practice most of them fall apart the moment you follow more than a handful of shows. I have been keeping a watch log for years, and when TV Time shut down I went looking for a replacement. I did not find one I liked, so I built <a href="{APP}/en">dizi.jpg</a>. Full disclosure: I am its developer.</p>
<p>This post is the checklist I ended up with. You can use it to judge any tracker, including mine.</p>

<h2>1. It tracks episodes, not just titles</h2>
<p>For movies, "watched" is enough. For shows you need to know that you are on season 3, episode 5. A good tracker lets you tick an episode with one tap, fills a progress bar per season.</p>
{gorsel("en", "3-bolum-isaretleme", "Marking an episode as watched in dizi.jpg")}

<h2>2. It tells you when new episodes arrive</h2>
<p>The whole point of tracking is not having to remember. dizi.jpg keeps an <a href="{APP}/takvim">upcoming episodes calendar</a> grouped by show, with how many episodes you are behind, and sends a notification to your phone when a new one airs.</p>
{gorsel("en", "4-takvim", "Upcoming episodes calendar")}

<h2>3. It keeps your library in clear states</h2>
<p>Watchlist, watching, completed, dropped. Four shelves, filled automatically as you mark episodes. Rewatches are counted separately instead of overwriting your first watch, and ratings go down to decimals if you care about the difference between a 4.2 and a 4.5.</p>

<h2>4. It protects you from spoilers</h2>
<p>Reading reactions after an episode is half the fun, and the fastest way to get spoiled. dizi.jpg uses two layers: the reviewer can flag a spoiler, and the server also knows where you are. If you have not watched S3E4, reviews about S3E4 are blurred for you even if nobody flagged them. Reviews written in other languages are shown translated, with the original one tap away.</p>
{gorsel("en", "7-incelemeler", "Spoiler-safe reviews")}

<h2>5. It helps you decide what to watch next</h2>
<ul>
<li><strong>Episode heatmap:</strong> every episode rating of a show on a season × episode grid. See where a show dips before you commit. Try it on <a href="{APP}/icerik/tv/1396?dil=en">Breaking Bad</a>.</li>
<li><strong>Rating distribution:</strong> an average of 6.0 can mean "everyone thought it was okay" or "half loved it, half hated it". The histogram tells you which.</li>
<li><strong>Where to watch:</strong> streaming, rent and buy options on each title page.</li>
<li><strong>The wheel:</strong> spin your watchlist and let it pick. Surprisingly, this is the feature I use most.</li>
</ul>
{gorsel("en", "5-bolum-isi-haritasi", "Episode rating heatmap")}

<h2>6. It lets you bring your history in, and take it out</h2>
<p>Starting from zero is why most people never switch. dizi.jpg imports the TV Time export file and Letterboxd exports (watched films, ratings, lists), and a single CSV or JSON works too. In the other direction, you can export everything at any time (the ZIP is sent to your email) and delete your account completely. Apps shut down; your log should not go with them.</p>

<h2>7. It works where you are</h2>
<p>dizi.jpg runs on the <a href="{APP}/en">web</a>, on <a href="{PLAY}">Android</a> (including Android TV) and on <a href="{IOS}">iPhone</a>, in 46 languages. There are no ads and no in-app purchases.</p>

<h2>Try it</h2>
<p>You can browse without an account: the <a href="{APP}/kesfet">Discover page</a> is open to everyone. If you are coming from TV Time, bring your export file along. Feedback of any kind is welcome.</p>
"""))

# ---------------------------------------------------------------- ES
YAZILAR.append(dict(
    dil="es", slug="aplicacion-para-seguir-series", tarih="2026-09-25",
    baslik="Aplicación para seguir series: cómo no volver a perder el capítulo",
    ozet="Si sigues varias series a la vez, olvidar en qué capítulo ibas es cuestión de semanas. Te cuento qué debe tener una buena aplicación para seguir series y películas y cómo funciona dizi.jpg.",
    govde=lambda: f"""
<p>Sigues seis series a la vez, te vas de viaje tres semanas y al volver no sabes en qué capítulo ibas en ninguna. Te pasa a ti y nos pasa a todos. Una aplicación para seguir series existe para resolver exactamente eso.</p>
<p>Yo soy el desarrollador de <a href="{APP}/es">dizi.jpg</a>, una aplicación para seguir series y películas. En este artículo explico qué le pido a una app de este tipo y cómo lo resolví.</p>

<h2>Lo mínimo que debe hacer</h2>
<ol>
<li><strong>Seguimiento por capítulo.</strong> Marcar un episodio con un toque y ver el progreso de cada temporada.</li>
<li><strong>Calendario de estrenos.</strong> Saber cuándo sale el próximo capítulo sin buscarlo.</li>
<li><strong>Notificaciones.</strong> Que el móvil te avise cuando se estrena un episodio nuevo.</li>
<li><strong>Estados claros.</strong> Pendiente, viendo, terminada, abandonada.</li>
<li><strong>Tus datos son tuyos.</strong> Poder importarlos y exportarlos cuando quieras.</li>
</ol>

<h2>Cómo funciona en dizi.jpg</h2>
<p><strong>Marcas el capítulo y listo.</strong> En la página de la serie abres la temporada, tocas el episodio visto y la barra de progreso se llena.</p>
{gorsel("es", "3-bolum-isaretleme", "Marcar un capítulo como visto en dizi.jpg")}

<p><strong>El calendario trabaja por ti.</strong> Los próximos capítulos de las series que sigues aparecen en el <a href="{APP}/takvim">calendario</a>, agrupados por serie y con cuántos episodios te faltan. Cuando se estrena uno nuevo, te llega una notificación.</p>
{gorsel("es", "4-takvim", "Calendario de próximos capítulos")}

<p><strong>Tu biblioteca se ordena sola.</strong> Cada título cae en su estante según lo que marcas. En estadísticas ves cuántas horas llevas frente a la pantalla, series y películas por separado.</p>

<h2>Sin spoilers</h2>
<p>Leer opiniones después de un capítulo es parte de la experiencia, y también la forma más rápida de comerse un spoiler. En dizi.jpg hay dos capas de protección: quien escribe puede marcar el spoiler y, además, si tú no has visto un capítulo, las reseñas sobre ese capítulo te aparecen difuminadas aunque nadie las haya marcado. Las reseñas en otros idiomas se muestran traducidas al tuyo.</p>
{gorsel("es", "7-incelemeler", "Reseñas protegidas contra spoilers")}

<h2>Para decidir qué ver esta noche</h2>
<ul>
<li><strong>Mapa de calor de episodios:</strong> las notas de todos los capítulos en una cuadrícula temporada × episodio. Mira dónde baja una serie antes de empezarla, por ejemplo <a href="{APP}/icerik/tv/1396?dil=es">Breaking Bad</a>.</li>
<li><strong>Dónde verla:</strong> plataformas de streaming, alquiler y compra en la ficha de cada título.</li>
<li><strong>La ruleta:</strong> gira tu lista de pendientes y deja que elija por ti.</li>
</ul>
{gorsel("es", "5-bolum-isi-haritasi", "Mapa de calor con la nota de cada capítulo")}

<h2>Trae tu historial</h2>
<p>Si venías de TV Time, su archivo de exportación se puede importar directamente: capítulos vistos y notas incluidos. Lo mismo con la exportación de Letterboxd para películas. Y cuando quieras, exportas todo (el ZIP te llega por correo) o borras tu cuenta por completo.</p>

<h2>Dónde descargarla</h2>
<p>dizi.jpg funciona en la <a href="{APP}/es">web</a>, en <a href="{PLAY}">Android</a> y en <a href="{IOS}">iPhone</a>, en 46 idiomas, sin anuncios ni compras dentro de la app. Puedes explorar sin cuenta desde la página <a href="{APP}/kesfet">Descubrir</a>.</p>
"""))

# ---------------------------------------------------------------- şablon
CSS_SURUM = "1"

def kelime(s):
    return len(re.sub(r"<[^>]+>", " ", s).split())

def yazi_url(y):
    return f"{DIL[y['dil']]['kok']}{y['slug']}/"

def kabuk(dil, baslik, aciklama, yol, govde, ek_head="", og_tur="website"):
    d = DIL[dil]
    alternatif = ""
    if yol in ("/", "/en/", "/es/"):
        alternatif = "".join(f'<link rel="alternate" hreflang="{k}" href="{SITE}{v["kok"]}">' for k, v in DIL.items())
        alternatif += f'<link rel="alternate" hreflang="x-default" href="{SITE}/">'
    diller = " · ".join(f'<a href="{v["kok"]}"{" aria-current=page" if k == dil else ""}>{v["ad"]}</a>' for k, v in DIL.items())
    return f"""<!doctype html>
<html lang="{dil}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(baslik)}</title>
<meta name="description" content="{html.escape(aciklama)}">
<link rel="canonical" href="{SITE}{yol}">
{alternatif}
<meta property="og:type" content="{og_tur}">
<meta property="og:site_name" content="{d['blog']}">
<meta property="og:locale" content="{d['locale']}">
<meta property="og:title" content="{html.escape(baslik)}">
<meta property="og:description" content="{html.escape(aciklama)}">
<meta property="og:url" content="{SITE}{yol}">
<meta property="og:image" content="{SITE}/img/og.png">
<meta name="twitter:card" content="summary">
<meta name="theme-color" content="#0d0d0d">
<link rel="icon" href="/favicon.png" type="image/png">
<link rel="alternate" type="application/rss+xml" title="{d['blog']}" href="{SITE}/feed.xml">
<link rel="stylesheet" href="/style.css?v={CSS_SURUM}">
{ek_head}
</head>
<body>
<header class="ust"><div class="kap">
<a class="marka" href="{d['kok']}"><img src="/img/logo.png" width="36" height="36" alt="">{d['blog']}</a>
<nav><a class="dugme" href="{d['app']}">{d['web']}</a></nav>
</div></header>
<main class="kap">
{govde}
</main>
<footer class="alt"><div class="kap">
<p class="diller">{diller}</p>
<p><a href="{APP}/">dizijpg.com</a> · <a href="{PLAY}">Google Play</a> · <a href="{IOS}">App Store</a> · <a href="{IG}">Instagram</a></p>
<p class="kucuk">{d['alt']}</p>
</div></footer>
</body>
</html>
"""

def indirme_kutusu(dil):
    d = DIL[dil]
    return f"""<aside class="kutu">
<img src="/img/logo.png" width="64" height="64" alt="dizi.jpg">
<div><strong>dizi.jpg</strong><p>{d['kutu']}</p>
<p class="dugmeler"><a class="dugme" href="{d['app']}">{d['web']}</a> <a class="dugme ikincil" href="{PLAY}">Google Play</a> <a class="dugme ikincil" href="{IOS}">App Store</a></p></div>
</aside>"""

def yazi_sayfasi(y):
    d = DIL[y["dil"]]
    govde = y["govde"]()
    dk = max(1, round(kelime(govde) / 220))
    yol = yazi_url(y)
    ld = {
        "@context": "https://schema.org", "@type": "BlogPosting",
        "headline": y["baslik"], "description": y["ozet"], "inLanguage": y["dil"],
        "datePublished": y["tarih"], "dateModified": y["tarih"],
        "mainEntityOfPage": SITE + yol, "image": SITE + "/img/og.png",
        "author": {"@type": "Organization", "name": "dizi.jpg", "url": APP + "/"},
        "publisher": {"@type": "Organization", "name": "dizi.jpg", "url": APP + "/",
                      "logo": {"@type": "ImageObject", "url": SITE + "/img/logo.png"}},
        "about": {"@type": "SoftwareApplication", "name": "dizi.jpg", "url": APP + "/",
                  "applicationCategory": "EntertainmentApplication", "operatingSystem": "Android, iOS, Web"},
    }
    ek = f'<meta property="article:published_time" content="{y["tarih"]}">\n<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'
    govde_html = f"""<article class="yazi">
<p class="ust-bilgi"><a href="{d['kok']}">{d['yazilar']}</a> · <time datetime="{y['tarih']}">{tarih_yaz(y['tarih'], y['dil'])}</time> · {dk} {d['dk']}</p>
<h1>{html.escape(y['baslik'])}</h1>
<p class="giris">{html.escape(y['ozet'])}</p>
{govde}
</article>
{indirme_kutusu(y['dil'])}"""
    return kabuk(y["dil"], f"{y['baslik']} | dizi.jpg", y["ozet"], yol, govde_html, ek, "article")

AYLAR = {"tr": "Ocak Şubat Mart Nisan Mayıs Haziran Temmuz Ağustos Eylül Ekim Kasım Aralık",
         "en": "January February March April May June July August September October November December",
         "es": "enero febrero marzo abril mayo junio julio agosto septiembre octubre noviembre diciembre"}

def tarih_yaz(t, dil):
    g = date.fromisoformat(t)
    ay = AYLAR[dil].split()[g.month - 1]
    return f"{ay} {g.day}, {g.year}" if dil == "en" else (f"{g.day} de {ay} de {g.year}" if dil == "es" else f"{g.day} {ay} {g.year}")

def liste_sayfasi(dil):
    d = DIL[dil]
    kartlar = "".join(f"""<article class="kart">
<p class="ust-bilgi"><time datetime="{y['tarih']}">{tarih_yaz(y['tarih'], dil)}</time></p>
<h2><a href="{yazi_url(y)}">{html.escape(y['baslik'])}</a></h2>
<p>{html.escape(y['ozet'])}</p>
<p><a class="oku" href="{yazi_url(y)}">{d['oku']} →</a></p>
</article>""" for y in YAZILAR if y["dil"] == dil)
    ld = {"@context": "https://schema.org", "@type": "Blog", "name": d["blog"], "url": SITE + d["kok"], "inLanguage": dil,
          "publisher": {"@type": "Organization", "name": "dizi.jpg", "url": APP + "/"}}
    govde = f"""<section class="kahraman"><h1>{d['blog']}</h1><p>{d['slogan']}</p></section>
{kartlar}
{indirme_kutusu(dil)}"""
    return kabuk(dil, f"{d['blog']} · {d['slogan']}", d["slogan"] + " — dizi.jpg", d["kok"], govde,
                 f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>')

def yaz(yol, icerik):
    tam = os.path.join(KOK, yol.lstrip("/"))
    os.makedirs(os.path.dirname(tam), exist_ok=True)
    with open(tam, "w", encoding="utf-8") as f:
        f.write(icerik)

def main():
    for dil, d in DIL.items():
        yaz(d["kok"] + "index.html", liste_sayfasi(dil))
    for y in YAZILAR:
        yaz(yazi_url(y) + "index.html", yazi_sayfasi(y))
    urller = [(d["kok"], "2026-09-25") for d in DIL.values()] + [(yazi_url(y), y["tarih"]) for y in YAZILAR]
    yaz("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"<url><loc>{SITE}{u}</loc><lastmod>{t}</lastmod></url>\n" for u, t in urller) + "</urlset>\n")
    yaz("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    ogeler = "".join(f"""<item><title>{html.escape(y['baslik'])}</title><link>{SITE}{yazi_url(y)}</link><guid>{SITE}{yazi_url(y)}</guid><pubDate>{date.fromisoformat(y['tarih']).strftime('%a, %d %b %Y')} 09:00:00 +0300</pubDate><description>{html.escape(y['ozet'])}</description></item>
""" for y in YAZILAR)
    yaz("feed.xml", f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel><title>dizi.jpg Blog</title><link>{SITE}/</link><description>Dizi ve film takibi üzerine notlar</description>
{ogeler}</channel></rss>
""")
    yaz("404.html", kabuk("tr", "Sayfa bulunamadı | dizi.jpg Blog", "Sayfa bulunamadı", "/404.html",
                          '<section class="kahraman"><h1>Sayfa bulunamadı</h1><p><a href="/">Blog ana sayfasına dön</a></p></section>')
        .replace('<link rel="canonical"', '<meta name="robots" content="noindex"><link rel="canonical"'))
    yaz(".nojekyll", "")
    print("tamam:", len(YAZILAR), "yazı")

if __name__ == "__main__":
    main()
