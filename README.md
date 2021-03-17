# 1. DOMAČA NALOGA: POROČILO 
Za bolj podrobne opise glejte kodo s komentarji. V sledečem besedilu sledi kratek opis in ugotovitve iz 1. domače naloge.

## Vigenere

Šifriranja in dešifriranja sem se lotil kot razširitev Cezarjeve šifre (kot je tudi poimenovano in implementirano v kodi).

Za ugotovitev dolžine besedila sem izbral Friedmanov test (indeks koincidence), opisan na Wikipediji (link v kodi) in s preprosto formulo dobil približek za dolžino ključa (ki je bil sprva napačen (prevelik), na kar je sicer v opisu članka opozorjeno in priporočeno, da se sproba okolico ocene in ne samo zaokrožitev.

Po ugotovljeni dolžini gesla se program loti razbijanja n (v tem primeru 4) posamičnih Cezarjevih šifer z frekvenčno analizo (distribucija pridobljena z Wikipedije).

### Preprost primer:
Kriptogram: ```VOCPBF```

Čistopis: ```VNAPAD```


### Naloga:
Pridobljeno geslo je: ```MATH```

Pridobljeno besedilo pa: 
```ITHASLONGBEENAGRAVEQUESTIONWHETHERANYGOVERNMENTNOTTOOSTRONGFORTHELIBERTIESOFITSPEOPLECANBESTRONGENOUGHTOMAINTAINITSEXISTENCEINGREATEMERGENCIESONTHISPOINTTHEPRESENTREBELLIONBROUGHTOURREPUBLICTOASEVERETESTANDTHEPRESIDENTIALELECTIONOCCURRINGINREGULARCOURSEDURINGTHEREBELLIONADDEDNOTALITTLETOTHESTRAINTHESTRIFEOFTHEELECTIONISBUTHUMANNATUREPRACTICALLYAPPLIEDTOTHEFACTSINTHECASE```


## Hill
Šifriranje in dešifriranje sem implementiral z matričnim množenjem (po definiciji). Če dolžina besedila ni deljiva z geslom, se besedilo podaljša z »A« do ustrezne dolžine (za večjo varnost bi se lahko besedilo ovilo okoli sebe ali dopolnilo z naključnimi simboli).

Hillova šifra je precej odporna na dešifriranje brez poznavanja para čistopis-kriptogram (na tak tip napada pa je zelo občutljiva, saj je popolnoma linearna).

Razbijanja šifre sem se lotil kar z grobo silo (poiščem vse obrnljive matrične ključe dolžine 4 in poskusim z njimi dešifrirati besedilo, tisti, ki ima najboljšo oceno s frekvenčno analizo je pravi). Vredno je omeniti, da je glede na naravo same šifre prvi najden ključ ravno obraten od iskanega (zamenjati je potrebno stolpce). 

Moj program ne bi deloval za matrike, večje od 2x2, saj sem dosti zadev zaradi te predpostavke lahko »hardcodal« (računanje inverza matrike , sam princip lotevanja reševanja z grobo silo). Glede na to, da sem se lotil razbijanja šifre z grobo silo, bi tudi računal večji ključ (nesprejemljivo) dlje, medtem ko za ključ dolžine 4 razbije, kljub slabi časovni kompleksnosti, še v zadovoljivem času.

Lahko bi se lotil še izboljšave programa, recimo z posameznim razbijanjem ključev za sode in lihe elemente kriptograma (prva vrstica ključa vpliva samo na sode in podobno za drugo vrstico ključa na lihe), kar bi časovno kompleksnost znižalo iz 26^4 na 2*26^2.
Za večje matrike to spet ne bi zadoščalo (morda z vzporednim procesiranjem).

### Preprost primer:
Kriptogram: ```HUHYVRLKFKBMHODQPVAA```

Čistopis: ```KRIPTOGRAFIJAHILLAAA```

### Naloga:
Pridobljeno geslo je: ZAFD
```(25 0 )¦(5   3)```    oz.     ```(Z A )¦(F D)```

Pridobljen čistopis pa:
```ITISAVERYPOORTHINGWHETHERFORNATIONSORINDIVIDUALSTOADVANCETHEHISTORYOFGREATDEEDSDONEINTHEPASTASANEXCUSEFORDOINGPOORLYINTHEPRESENTBUTITISANEXCELLENTTHINGTOSTUDYTHEHISTORYOFTHEGREATDEEDSOFTHEPASTANDOFTHEGREATMENWHODIDTHEMWITHANEARNESTDESIRETOPROFITTHEREBYSOASTORENDERBETTERSERVICEINTHEPRESENTINTHEIRESSENTIALSTHEMENOFTHEPRESENTDAYAREMUCHLIKETHEMENOFTHEPASTANDTHELIVEISSUESOFTHEPRESENTCANBEFACEDTOBETTERADVANTAGEBYMENWHOHAVEINGOODFAITHSTUDIEDHOWTHELEADERSOFTHENATIONFACEDTHEDEADISSUESOFTHEPASTSUCHASTUDYOFLINCOLNSLIFEWILLENABLEUSTOAVOIDTHETWINGULFSOFIMMORALITYANDINEFFICIENCYTHEGULFSWHICHALWAYSLIEONEONEACHSIDEOFTHECAREERSALIKEOFMANANDOFNATIONITHELPSNOTHINGTOHAVEAVOIDEDONEIFSHIPWRECKISENCOUNTEREDINTHEOTHERA```




