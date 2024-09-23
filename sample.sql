TRUNCATE 
tlaras.user, 
tlaras.course, 
tlaras.course_user, 
tlaras.course_article, 
tlaras.exercise_text, 
tlaras.exercise_choice, 
tlaras.exercise_choice_option,
tlaras.points 
RESTART IDENTITY;


INSERT INTO tlaras.user (username, password, is_teacher) VALUES
('Oona Opettaja', '', TRUE)
;


INSERT INTO tlaras.course (user_id, name, description) VALUES
( 1, 'Avokadon Ystävät: Tiede ja Taide',
'Tutustu avokadon monipuolisiin käyttötapoihin keittiössä ja kosmetiikassa. Kurssi sisältää myös avokadon viljelyn perusteet ja sen terveysvaikutukset.'),

( 1, 'Kissan Kuiskaajan Opas',
'Opi ymmärtämään ja kommunikoimaan kissojen kanssa. Kurssi kattaa kissojen käyttäytymisen, koulutuksen ja hyvinvoinnin.'),

( 1, 'Virtuaalimatkailu: Maailman Ihmeet Kotisohvalta',
'Matkusta maailman ympäri virtuaalisesti. Tutustu eri kulttuureihin, nähtävyyksiin ja paikallisiin herkkuihin ilman passia tai lentolippua.'),

( 1, 'Kahvin Salat: Baristan Taidot',
'Syvenny kahvin maailmaan ja opi valmistamaan täydellinen espresso, latte ja cappuccino. Kurssi sisältää myös kahvin historiaa ja makuprofiileja.'),

( 1, 'Zombiapokalypsin Selviytymisopas',
'Valmistaudu mahdolliseen zombiapokalypsiin. Kurssi kattaa selviytymisstrategiat, tarvittavat varusteet ja turvalliset paikat.')
;


INSERT INTO tlaras.course_article (course_id, title, content) VALUES
(1, 'Avokadon Historia ja Viljely', 'Avokado, tunnettu myös nimellä “alligaattoripäärynä”, on kotoisin Keski- ja Etelä-Amerikasta. Sen historia ulottuu tuhansien vuosien taakse, ja se on ollut tärkeä osa paikallisten kulttuurien ruokavaliota. Avokadon viljely alkoi todennäköisesti Meksikossa, jossa sitä on kasvatettu jo yli 5000 vuotta. Avokadoa pidettiin pyhänä hedelmänä, ja sitä käytettiin usein rituaaleissa ja juhlamenoissa. Avokaadopuun istutuksesta kestää noin 3 vuotta ennen kuin puu alkaa tuottaa hedelmää.'),

(1, 'Avokadon Terveysvaikutukset', 'Avokado on täynnä terveellisiä rasvoja, vitamiineja ja mineraaleja, mikä tekee siitä erinomaisen lisän terveelliseen ruokavalioon. Se sisältää runsaasti kertatyydyttymättömiä rasvahappoja, jotka ovat hyviä sydämelle ja auttavat alentamaan “huonoa” LDL-kolesterolia samalla kun ne nostavat “hyvää” HDL-kolesterolia. Avokado on myös erinomainen kuidun, kaliumin ja C-vitamiinin lähde.

Tutkimukset ovat osoittaneet, että avokadon säännöllinen käyttö voi auttaa parantamaan sydämen terveyttä, alentamaan verenpainetta ja vähentämään tulehdusta. Lisäksi avokado sisältää antioksidantteja, kuten luteiinia ja zeaksantiinia, jotka ovat tärkeitä silmien terveydelle. Avokadon sisältämä E-vitamiini auttaa myös suojaamaan soluja vaurioilta ja tukee immuunijärjestelmän toimintaa.'),

(1, 'Avokado Reseptit', 'Guacamolesta Suklaamousseen Avokado on monipuolinen raaka-aine, joka sopii sekä suolaisiin että makeisiin ruokiin. Klassinen guacamole on helppo valmistaa murskaamalla avokado ja sekoittamalla siihen limeä, suolaa, tomaattia, sipulia ja korianteria. Guacamole on täydellinen lisuke nachoille, tacoille tai vaikka leivän päälle.

Avokadoa voi käyttää myös monissa muissa resepteissä, kuten salsoissa, salaateissa ja smoothieissa. Se tuo kermaisen koostumuksen ilman maitotuotteita, mikä tekee siitä erinomaisen vaihtoehdon vegaanisiin ja laktoosittomiin ruokiin. Makeisiin herkkuihin avokado sopii esimerkiksi suklaamousseen, jossa avokado tuo kermaisen koostumuksen ja terveellisiä rasvoja. Suklaamousse valmistetaan sekoittamalla avokadoa, kaakaojauhetta, makeutusainetta ja vaniljaa, ja se on herkullinen ja terveellinen jälkiruoka.'),


(2, 'Kissojen Käyttäytymisen Ymmärtäminen', 'Kissat ovat itsenäisiä ja joskus arvaamattomia eläimiä, joiden käyttäytymisen ymmärtäminen vaatii tarkkaa havainnointia ja tietoa. Kissojen elekieli on monimutkaista, ja niiden viestintä perustuu pitkälti kehon kieleen, ääntelyyn ja hajuihin. Esimerkiksi hännän asento ja korvien liikkeet voivat kertoa paljon kissan mielialasta. Kissan kehräys voi olla merkki tyytyväisyydestä, mutta myös kivusta tai stressistä.

Kissat käyttävät myös erilaisia ääniä kommunikoidakseen. Maukuminen, murina, sähinä ja kehräys ovat kaikki osa kissan äänivalikoimaa. Jokaisella äänellä on oma merkityksensä, ja kissanomistajan on tärkeää oppia tunnistamaan ja ymmärtämään nämä äänet. Lisäksi kissat käyttävät hajuja merkitsemään reviiriään ja viestimään muiden kissojen kanssa. Ne hierovat poskiaan ja kehoaan esineisiin jättääkseen hajumerkkejä, jotka kertovat muille kissoille niiden läsnäolosta ja reviiristä.'),

(2, 'Kissan Koulutus', 'Vinkkejä ja Niksejä Vaikka kissat eivät ole yhtä helposti koulutettavissa kuin koirat, ne voivat oppia monia asioita, kuten hiekkalaatikon käyttöä ja raapimispuun hyödyntämistä. Positiivinen vahvistaminen, kuten herkut ja kehuminen, on tehokas tapa kouluttaa kissaa. Tärkeää on myös johdonmukaisuus ja kärsivällisyys. Kissan kouluttaminen vaatii aikaa ja kärsivällisyyttä, mutta se voi olla erittäin palkitsevaa sekä kissalle että omistajalle.

Kissan koulutuksessa on tärkeää ymmärtää kissan luontaisia käyttäytymismalleja ja tarpeita. Esimerkiksi raapiminen on kissalle luonnollinen tapa teroittaa kynsiään ja merkitä reviiriään. Tarjoamalla kissalle sopivia raapimispaikkoja ja palkitsemalla sitä niiden käytöstä voidaan vähentää ei-toivottua raapimiskäyttäytymistä. Lisäksi kissan leikkiminen ja virikkeellistäminen ovat tärkeitä sen hyvinvoinnille ja käyttäytymisen hallinnalle.'),

(2, 'Kissan Hyvinvointi ja Terveys', 'Kissan hyvinvointi koostuu monista tekijöistä, kuten ravinnosta, liikunnasta ja terveydentilan seurannasta. Laadukas ruoka, säännölliset eläinlääkärikäynnit ja virikkeellinen ympäristö ovat avainasemassa. Kissan ruokavalion tulisi olla tasapainoinen ja sisältää kaikki tarvittavat ravintoaineet. Kissoille on tarjolla monenlaisia kaupallisia ruokia, mutta myös kotiruokaa voi valmistaa, kunhan varmistaa, että se täyttää kissan ravitsemukselliset tarpeet.

Liikunta ja leikki ovat tärkeitä kissan fyysiselle ja henkiselle hyvinvoinnille. Kissojen lelut, kuten pallot, höyhenet ja interaktiiviset lelut, voivat tarjota paljon virikkeitä ja pitää kissan aktiivisena. Lisäksi on tärkeää huolehtia kissan hampaiden ja turkin hoidosta. Säännöllinen hampaiden harjaus ja turkin harjaaminen auttavat ehkäisemään terveysongelmia ja pitävät kissan hyvässä kunnossa.'),


(3, 'Virtuaalimatkailun Tekniikat ja Välineet', 'Virtuaalimatkailu mahdollistaa maailman tutkimisen mukavasti kotisohvalta käsin. Tarvitset vain VR-lasit ja älypuhelimen tai tietokoneen. Monet sovellukset ja alustat, kuten Google Earth VR ja YouTube 360, tarjoavat upeita virtuaalimatkakokemuksia. Virtuaalimatkailu on erinomainen tapa tutustua uusiin paikkoihin ja kulttuureihin ilman matkustamisen vaivaa ja kustannuksia.

Virtuaalimatkailun tekniikat kehittyvät jatkuvasti, ja tarjolla on yhä realistisempia ja immersiivisempiä kokemuksia. VR-lasien avulla voit kokea olevasi paikan päällä ja tutkia ympäristöäsi 360 asteen näkymässä. Lisäksi monet virtuaalimatkailusovellukset tarjoavat interaktiivisia elementtejä, kuten opastettuja kierroksia ja tietovisoja, jotka tekevät matkakokemuksesta entistä mielenkiintoisemman ja opettavaisemman.'),

(3, 'Virtuaalimatka Euroopan Suurkaupunkeihin', 'Euroopan suurkaupungit, kuten Pariisi, Lontoo ja Rooma, ovat täynnä historiaa ja kulttuuria. Virtuaalimatkalla voit tutustua näiden kaupunkien kuuluisimpiin nähtävyyksiin, kuten Eiffel-torniin, Big Beniin ja Colosseumiin. Voit myös nauttia paikallisista herkuista virtuaalisesti ja oppia lisää kunkin kaupungin historiasta ja kulttuurista.

Pariisissa voit vierailla Louvre-museossa ja ihailla Mona Lisaa, kävellä Champs-Élysées’llä ja nauttia näkymistä Eiffel-tornista. Lontoossa voit tutustua Buckinghamin palatsiin, Big Beniin ja Tower of Londoniin. Roomassa voit vierailla Colosseumilla, Pietarinkirkossa ja Vatikaanin museoissa. Virtuaalimatkailu tarjoaa mahdollisuuden tutustua näihin ikonisiin kohteisiin ja oppia niiden historiasta ja kulttuurista.'),

(3, 'Eksoottiset Kohteet', 'Amazonin Sademetsästä Antarktikseen Virtuaalimatkailu vie sinut myös eksoottisiin kohteisiin, kuten Amazonin sademetsään ja Antarktikseen. Amazonin sademetsä on yksi maailman monimuotoisimmista ekosysteemeistä, ja siellä elää tuhansia kasvi- ja eläinlajeja, joita ei löydy mistään muualta. Virtuaalimatkalla voit tutustua sademetsän tiheään kasvillisuuteen, kuunnella lintujen laulua ja nähdä eksoottisia eläimiä, kuten jaguaareja ja tukaaneja.

Antarktis puolestaan on maailman kylmin ja syrjäisin maanosa, jossa asuu vain harvoja eläinlajeja, kuten pingviinejä ja hylkeitä. Virtuaalimatkalla voit tutustua Antarktiksen jäätiköihin, nähdä jäävuoria ja oppia lisää tämän ainutlaatuisen alueen ekologiasta ja tutkimuksesta. Virtuaalimatkailu tarjoaa mahdollisuuden oppia ja kokea uusia asioita turvallisesti ja mukavasti kotona.'),


(4, 'Kahvin Historia ja Alkuperä', 'Kahvin historia ulottuu tuhansien vuosien taakse. Legendan mukaan kahvi löydettiin Etiopiassa, kun paimen nimeltä Kaldi huomasi vuohien olevan erityisen energisiä syötyään tiettyjä marjoja. Kahvin viljely ja käyttö levisivät nopeasti Lähi-itään, jossa siitä tuli tärkeä osa islamilaista kulttuuria. 1500-luvulla kahvi saapui Eurooppaan, ja siitä tuli nopeasti suosittu juoma.

Nykyään kahvia viljellään ympäri maailmaa, ja sen alkuperä vaikuttaa merkittävästi makuun ja aromiin. Kahvin maku riippuu monista tekijöistä, kuten maaperästä, ilmastosta ja viljelymenetelmistä. Esimerkiksi Etiopian kahvit ovat tunnettuja hedelmäisistä ja kukkaisista aromeistaan, kun taas Kolumbian kahvit ovat usein pehmeitä ja tasapainoisia. Kahvin alkuperä ja viljelymenetelmät vaikuttavat myös sen eettisyyteen ja ympäristövaikutuksiin.'),

(4, 'Erilaiset Kahvijuomat ja Niiden Valmistus', 'Kahvijuomia on monenlaisia, ja niiden valmistus vaatii taitoa ja tarkkuutta. Espresso on kahvin perusta, josta valmistetaan monia muita juomia, kuten latte, cappuccino ja americano. Espresso valmistetaan pakottamalla kuuma vesi hienoksi jauhetun kahvin läpi korkealla paineella, mikä tuottaa vahvan ja aromikkaan juoman.

Latte valmistetaan lisäämällä espressoon höyrytettyä maitoa, kun taas cappuccino sisältää yhtä paljon espressoa, höyrytettyä maitoa ja maitovaahtoa. Americano valmistetaan lisäämällä espressoon kuumaa vettä, mikä tekee siitä miedomman ja suuremman juoman. Jokaisella juomalla on oma valmistustapansa ja vaatimuksensa, jotka baristan tulee hallita. Lisäksi on olemassa monia erikoiskahveja, kuten macchiato, mocha ja flat white, jotka tarjoavat erilaisia makuelämyksiä.'),

(4, 'Kahvin Maailma: Maku ja Aromi', 'Kahvin maku ja aromi riippuvat monista tekijöistä, kuten pavun alkuperästä, paahtoasteesta ja valmistustavasta. Kahvin maistelussa, eli cuppingissa, arvioidaan kahvin eri ominaisuuksia, kuten happamuutta, makeutta ja jälkimakua. Tämä auttaa löytämään juuri itselle sopivan kahvin.

Kahvin paahtoaste vaikuttaa merkittävästi sen makuun. Vaaleapaahtoinen kahvi on usein hapokasta ja hedelmäistä, kun taas tummapaahtoinen kahvi on täyteläistä ja suklaista. Valmistustapa, kuten suodatinmenetelmä, pressopannu tai espressokone, vaikuttaa myös kahvin makuun ja aromiin. Kahvin maistelussa on tärkeää kiinnittää huomiota kaikkiin aisteihin ja nauttia kahvin monipuolisista makuelämyksistä.'),


(5, 'Selviytymisstrategiat ja -taidot', 'Zombiapokalypsiin varautuminen vaatii monia taitoja ja strategioita. Tärkeintä on pysyä rauhallisena ja suunnitella etukäteen. Selviytymisstrategioihin kuuluu turvallisen paikan löytäminen, ruokavarastojen kerääminen ja itsepuolustustaitojen harjoittelu. On tärkeää tietää, miten suojautua ja puolustautua mahdollisilta uhkilta.

Selviytymisstrategioihin kuuluu myös ryhmätyö ja yhteistyö muiden selviytyjien kanssa. Yhdessä toimiminen voi parantaa selviytymismahdollisuuksia ja tarjota tukea vaikeissa tilanteissa. On tärkeää kehittää selviytymistaitoja, kuten ensiaputaitoja, vedenpuhdistusta ja ruoan säilöntää. Lisäksi on hyvä harjoitella erilaisia skenaarioita ja valmistautua henkisesti mahdollisiin haasteisiin.'),

(5, 'Tarvittavat Varusteet ja Välineet', 'Selviytymisvarusteisiin kuuluu monia tärkeitä esineitä, kuten ensiapupakkaus, taskulamppu, veitsi ja vedenpuhdistustabletit. Lisäksi on hyvä varata riittävästi ruokaa ja vettä. Varusteiden valinnassa on tärkeää huomioida niiden monikäyttöisyys ja kestävyys. Esimerkiksi monitoimityökalu voi olla erittäin hyödyllinen erilaisissa tilanteissa.

Muita tärkeitä varusteita ovat esimerkiksi lämpimät vaatteet, makuupussi, tulentekovälineet ja kartta. On myös hyvä varata lääkkeitä ja hygieniatarvikkeita. Selviytymisvarusteiden tulisi olla helposti saatavilla ja pakattuna niin, että ne on helppo ottaa mukaan tarvittaessa. Lisäksi on hyvä harjoitella varusteiden käyttöä etukäteen, jotta osaa toimia nopeasti ja tehokkaasti hätätilanteessa.'),

(5, 'Turvalliset Paikat ja Piilopaikat', 'Zombiapokalypsissä turvalliset paikat ovat ensiarvoisen tärkeitä. Hyviä piilopaikkoja ovat esimerkiksi vahvat rakennukset, joissa on vain vähän sisäänkäyntejä. Myös maanalaiset tilat ja syrjäiset alueet voivat tarjota suojaa. Tärkeintä on löytää paikka, jossa voi olla turvassa ja josta on helppo paeta tarvittaessa.

Turvallisen paikan valinnassa on tärkeää huomioida sen sijainti, suojattavuus ja resurssit. Esimerkiksi maaseudulla sijaitseva maatila voi tarjota paljon tilaa ja mahdollisuuksia viljellä ruokaa, mutta se voi olla vaikeampi suojata. Kaupungissa sijaitseva vahva rakennus voi tarjota hyvän suojan, mutta siellä voi olla enemmän uhkia. On tärkeää arvioida eri vaihtoehtoja ja valita paras mahdollinen paikka selviytymiseen.')
;


INSERT INTO tlaras.exercise_choice (course_article_id, question) VALUES
(1, 'Missä avokadon viljely todennäköisesti alkoi?'),
(2, 'Mikä seuraavista ei ole avokadon terveysvaikutus?'),
(3, 'Mikä on klassisen guacamolen pääraaka-aine?'),
(4, 'Mitä kissan kehräys voi tarkoittaa?'),
(5, 'Mikä on tehokas tapa kouluttaa kissaa?'),
(6, 'Mikä seuraavista ei ole tärkeä kissan hyvinvoinnille?'),
(7, 'Mitä tarvitaan virtuaalimatkailuun?'),
(8, 'Mikä seuraavista ei ole virtuaalimatkailun etu?'),
(10, 'Missä maassa kahvin uskotaan alun perin löytyneen?'),
(11, 'Mikä kahvijuoma valmistetaan lisäämällä espressoon kuumaa vettä?'),
(12, 'Mikä paahtoaste tekee kahvista usein hapokasta ja hedelmäistä?'),
(13, 'Mikä on tärkein asia zombiapokalypsiin varautumisessa?'),
(14, 'Mikä varuste on erityisen hyödyllinen monissa tilanteissa?'),
(15, 'Mikä on tärkein tekijä turvallisen paikan valinnassa?')
;

INSERT INTO tlaras.exercise_choice_option (exercise_choice_id, label, is_correct) VALUES
(1, 'Peru', FALSE),
(1, 'Meksiko', TRUE),
(1, 'Dominikaaninen tasavalta', FALSE),
(1, 'Yhdysvallat', FALSE),

(2, 'Alentaa verenpainetta', FALSE),
(2, 'Parantaa näköä', FALSE),
(2, 'Nostaa LDL-kolesterolia', TRUE),
(2, 'Tukee immuunijärjestelmää', FALSE),

(3, 'Tomaatti', FALSE),
(3, 'Sipuli', FALSE),
(3, 'Avokado', TRUE),
(3, 'Lime', FALSE),


(4, 'Tyytyväisyyttä', FALSE),
(4, 'Kivun merkkiä', FALSE),
(4, 'Stressiä', FALSE),
(4, 'Kaikkia edellä mainittuja', TRUE),

(5, 'Rangaistus', FALSE),
(5, 'Positiivinen vahvistaminen', TRUE),
(5, 'Huomiotta jättäminen', FALSE),
(5, 'Äänikomennot', FALSE),


(6, 'Laadukas ruoka', FALSE),
(6, 'Säännölliset eläinlääkärikäynnit', FALSE),
(6, 'Liikunta ja leikki', FALSE),
(6, 'Yksinolo', TRUE),

(7, 'VR-lasit ja älypuhelin tai tietokone', TRUE),
(7, 'Lentoliput', FALSE),
(7, 'Matkaopas', FALSE),
(7, 'Kamera', FALSE),

(8, 'Matkustamisen vaivattomuus', FALSE),
(8, 'Kustannusten säästö', FALSE),
(8, 'Fyysinen läsnäolo kohteessa', TRUE),
(8, 'Uusien paikkojen ja kulttuurien tutkiminen', FALSE),

(9, 'Kolumbia', FALSE),
(9, 'Etiopia', TRUE),
(9, 'Brasilia', FALSE),
(9, 'Vietnam', FALSE),

(10, 'Latte', FALSE),
(10, 'Cappuccino', FALSE),
(10, 'Americano', TRUE),
(10, 'Macchiato', FALSE),

(11, 'Vaaleapaahto', TRUE),
(11, 'Keskipaahto', FALSE),
(11, 'Tumma paahto', FALSE),
(11, 'Espresso paahto', FALSE),

(12, 'Ruokavarastojen kerääminen', FALSE),
(12, 'Itsepuolustustaitojen harjoittelu', FALSE),
(12, 'Rauhallisena pysyminen ja suunnittelu', TRUE),
(12, 'Turvallisen paikan löytäminen', FALSE),

(13, 'Ensiapupakkaus', FALSE),
(13, 'Monitoimityökalu', TRUE),
(13, 'Taskulamppu', FALSE),
(13, 'Vedenpuhdistustabletit', FALSE),

(14, 'Sijainti', FALSE),
(14, 'Suojattavuus', FALSE),
(14, 'Resurssit', FALSE),
(14, 'Kaikki edellä mainitut', TRUE)
;


INSERT INTO tlaras.exercise_text (course_article_id, question, answer) VALUES
(1, 'Monta vuotta avokadopuun istutuksesta kestää, ennen kuin se alkaa tuottaa hedelmiä?', '3'),
(4, 'Mitä kissat käyttävät merkitsemään reviiriään ja viestimään muiden kissojen kanssa?', 'hajuja')
;
