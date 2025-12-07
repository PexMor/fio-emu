**FIO API**

**BANKOVNICTVÍ**

www.fio.cz

Verze 16.10.2025

**[1 FUNKČNÍ POPIS](#1-funkční-popis)**

**[2 ZÍSKÁNÍ TOKENU](#2-získání-tokenu)**

**[3 TYPY KOMUNIKACE](#3-typy-komunikace)**

- [3.1 GET](#31-get)
- [3.2 POST](#32-post)

**[4 VYSVĚTLIVKY K DATOVÝM TYPUM](#4-vysvětlivky-k-datovým-typum)**

**[5 EXPORT (DOWNLOAD) POHYBU A VÝPISU Z BANKY](#5-export-download-pohybu-a-výpisu-z-banky)**

- [5.1 Podporované formáty dat](#51-podporované-formáty-dat)
- [5.2 Struktura URL dotazu](#52-struktura-url-dotazu)
  - [5.2.1 Pohyby na účtu za určené období](#521-pohyby-na-účtu-za-určené-období)
  - [5.2.2 Oficiální výpisy pohybů z účtu](#522-oficiální-výpisy-pohybů-z-účtu)
  - [5.2.3 Pohyby na účtu od posledního stažení](#523-pohyby-na-účtu-od-posledního-stažení)
  - [5.2.4 Nastavení zarážky](#524-nastavení-zarážky)
  - [5.2.5 Karetní transakce obchodníka za určené období](#525-karetní-transakce-obchodníka-za-určené-období)
  - [5.2.6 Číslo posledního vytvořeného oficiálního výpisu](#526-číslo-posledního-vytvořeného-oficiálního-výpisu)
- [5.3 Struktura formátu](#53-struktura-formátu)
  - [5.3.1 Bankovní pohyby](#531-bankovní-pohyby)
    - [5.3.1.1 Fio XML](#5311-fio-xml)
    - [5.3.1.2 OFX](#5312-ofx)
    - [5.3.1.3 GPC](#5313-gpc)
    - [5.3.1.4 CSV](#5314-csv)
    - [5.3.1.5 HTML](#5315-html)
    - [5.3.1.6 JSON](#5316-json)
    - [5.3.1.7 STA (MT940)](#5317-sta-mt940)
    - [5.3.1.8 SBA XML (camt.053)](#5318-sba-xml-camt053)
    - [5.3.1.9 ČBA XML (camt.053)](#5319-čba-xml-camt053)
  - [5.3.2 Transakce z POS terminálů nebo platební brány obchodníka](#532-transakce-z-pos-terminálů-nebo-platební-brány-obchodníka)
    - [5.3.2.1 XML](#5321-xml)
    - [5.3.2.2 CSV](#5322-csv)

**[6 IMPORT (UPLOAD) PLATEBNÍCH PŘÍKAZU DO BANK](#6-import-upload-platebních-příkazu-do-bank)**

- [6.1 Parametry pro upload dat](#61-parametry-pro-upload-dat)
- [6.2 ABO](#62-abo)
- [6.3 Fio XML](#63-fio-xml)
  - [6.3.1 XML příkaz platba v rámci ČR](#631-xml-příkaz-platba-v-rámci-čr)
  - [6.3.2 XML příkaz Europlatba](#632-xml-příkaz-europlatba)
  - [6.3.3 XML příkaz zahraniční platba](#633-xml-příkaz-zahraniční-platba)
  - [6.3.4 Platební titul](#634-platební-titul)
- [6.4 SEPA (pain)](#64-sepa-pain)
  - [6.4.1 pain.001 (platební příkazy)](#641-pain001-platební-příkazy)
  - [6.4.2 pain.008 (příkazy k inkasu)](#642-pain008-příkazy-k-inkasu)

**[7 UPOZORNĚNÍ NA BEZPEČNOSTNÍ RIZIKA SOUVISEJÍCÍ S POUŽÍVÁNÍM API](#7-upozornění-na-bezpečnostní-rizika-související-s-používáním-api)**

**[8 ZNÁMÉ CHYBOVÉ STAVY](#8-známé-chybové-stavy)**

- [8.1 The server encoutered an internal error () that prevented it from fulfilling this request](#81-the-server-encoutered-an-internal-error--that-prevented-it-from-fulfilling-this-request)
- [8.2 Status Code:404 Not Found](#82-status-code404-not-found)
- [8.3 Status Code:409 Conflict](#83-status-code409-conflict)
- [8.4 Status Code:500 Internal Server Error](#84-status-code500-internal-server-error)
- [8.5 SSL certificate problém: unable to get local issuer certificate](#85-ssl-certificate-problém-unable-to-get-local-issuer-certificate)
- [8.6 Status Code: 413 Příliš mnoho položek](#86-status-code-413-příliš-mnoho-položek)
- [8.7 Error:422](#87-error422)

**[9 ZMĚNY VE VERZÍCH DOKUMENTACE](#9-změny-ve-verzích-dokumentace)**

# 1 FUNKČNÍ POPIS

Automatizace rozhraní s Fio bankovním systémem Vám umožní podávání příkazů a získávání dat z účtůvedených u Fio banky. Rozhraní může být použito pro napojení účetních programů nebo pro automatickéstrojové zpracování pohybů či výpisů (dále data) z bankovního systému. Veškerá komunikace mezi bankou a cílovou stanicí probíhá pomocí SSL protokolu s minimálně 128bitovým šifrováním.

Přístup k datům z účtu vytváří majitel nebo osoba s patřičnými právy ke zvolenému účtu. Ve svém internetovém bankovnictví musí oprávněná osoba vygenerovat token (64 znakový unikátní řetězec), po jehožvytvoření lze po 5 minutách podávat příkazy nebo stahovat data. Pro podání příkazů nebo stažení dat nenínutné být přihlášen do internetového bankovnictví, odpovědi na požadavky se získávají prostřednictvím rozhraní https. Rozhraní má různé metody pro podávání příkazů, získávání strukturovaných dat nebo jejich nastavení.

# 2 ZÍSKÁNÍ TOKENU

Pro získání platného tokenu je zapotřebí provést následující kroky:

1. Oprávněná osoba se musí přihlásit do internetového bankovnictví.

2. Administrace tokenů je přístupná po stisku tlačítka ,,Nastavení" (v pravém horním rohu obrazovky) na obrazovce ,,Nastavení“, poté na záložce ,,API".

3. Požadavek na zřízení tokenu musí být silně autorizován (sms, push notifikace). V případě, že je na příslušném účtu nastavena autorizace více osobami, musí token podepsat všechny podepisujícíosoby. PPo úspěšné autorizaci je token zobrazen v přehledu.

4. Po 5 minutách od úspěšné autorizace lze token použít v API.

## Vlastnosti tokenu:

· Každý token je platný pouze k jednomu účtu. Potřebujete-li přistupovat k více účtům, je nutnévygenerovat další token.

·Je možno volit mezi dvěma typy nastavení práv tokenu:

O Sledování účtu - token pouze pro získání (export) dat z banky. Data z účtu je možnéstahovat současně i v různých formátech. Napr. pohyby v XML a oficiální výpisy v STA. Nedoporučujeme získávat data o pohybech v různých formátech na stejný token. Potřebujete-li dva formáty, vygenerujte si ke stejnému účtu nový token.

O Sledování účtu a zadávání platebních a inkasních příkazů - token pro získání a zároveň i pro odeslání platebních příkazů a inkas (import) do banky

· Platnost tokenu - každý nově založený token musí mít nastavenou platnost, nelze založit token bez doby platnosti nebo platnosti delší jak 180 dní. Pokud je zvoleno automatické prodlužování, tak při každém přihlášení do Internetbankingu nebo Smartbankingu se platnost tokenu prodlouží na 180dnů ode dne přihlášení.

# 3 TYPY KOMUNIKACE

Komunikace s bankovním systémem probíhá přes https pomocí metod GET a POST. GET slouží k získánídat z účtů a nastavení hodnot (zarážek). Metoda POST k podávání platebních příkazů.

## 3.1 GET

# Poskytnutí dat starších více než 90 dní

Pro získání dat mladších 90 dní není potřebná dodatečná silná autorizace v internetovém bankovnictví. Požadujete-li získat data starší 90 dní, tak je nutné dočasně odemknout přístup ke kompletní historii.

Toto odemknutí se nastavuje v internetovém bankovnictví na záložce ,,Nastavení" a zvolte složku ,,API". Kliknutím na ikonku zámku se pro daný token vytvoří autorizační pokyn. Po úspěšné auitorizaci budou historická data, po dobu 10 minut, přístupná.

# Získání dat:

· Stažení pohybů na účtu za dané období

· Stažení oficiálních výpisů na účtu

· Stažení pohybů na účtu od posledního stažení

· Stažení karetních transakcí na platebních terminálech/platební bráně za dané období

# Nastavení hodnot (zarážek) pro následné získání dat:

· Posledního úspěšně staženého ID pohybu

· Datum posledního neúspěšného dne

# 3.2 POST

# Podání platebních příkazů:

· Platba v rámci ČR

· Europlatba

· Zahraniční platba

· Inkaso a SEPA inkaso

# 4 VYSVĚTLIVKY K DATOVÝM TYPUM

| M   | Povinné pole (mandatory)                                                      |
| --- | ----------------------------------------------------------------------------- |
| O   | Nepovinné pole (optional)                                                     |
| C   | Podmínkové pole (conditional) - při vyjmenovaných situacích je pole povinné   |
| X   | Alfanumerické pole                                                            |
| e   | Alfanumerické pole a další povolené znaky:,. / - Mezera                       |
| i   | Alfanumerické pole (včetně diakritiky) a další povolené znaky: , . / - Mezera |
| n   | Numerické pole                                                                |

www.fio.cz

Verze 16.10.2025

| !   | Fixní délka pole                                                          |
| --- | ------------------------------------------------------------------------- |
| d   | Desetinné číslo (Decimal). Tečka jako oddělovač desetinných míst          |
| D   | Desetinné číslo (Decimal). Čárka jako oddělovač desetinných míst          |
| []  | Formát př. [//16x] pole má 16 alfanumerických znaků, které vždy začíná // |

# 5 EXPORT (DOWNLOAD) POHYBU A VÝPISU Z BANKY

## 5.1 Podporované formáty dat

API umožňuje získávat data v následujících formátech:

**Pohyby:**

CSV, GPC, HTML, JSON, OFX, FIO XML

**Výpisy:**

CSV, GPC, HTML, JSON, OFX, XML (Fio), PDF, MT940, ČBA XML (CAMT.053), SBA XML (CAMT.053)

**Typy pohybů na účtu:**

| 1. Příjem převodem uvnitř banky                                                     |
| ----------------------------------------------------------------------------------- |
| 2. Platba převodem uvnitr banky                                                     |
| 3. Vklad pokladnou                                                                  |
| 4. Výběr pokladnou                                                                  |
| 5. Vklad v hotovosti                                                                |
| 6. Výběr v hotovosti                                                                |
| 7. Platba                                                                           |
| 8. Príjem                                                                           |
| 9. Bezhotovostní platba                                                             |
| 10. Bezhotovostní príjem                                                            |
| 11. Platba kartou                                                                   |
| 12. Bezhotovostní platba                                                            |
| 13. Úrok z úvěru                                                                    |
| 14. Sankční poplatek                                                                |
| 15. Posel - předání                                                                 |
| 16. Posel - příjem                                                                  |
| 17. Převod uvnitr konta                                                             |
| 18. Připsaný úrok                                                                   |
| 19. Vyplacený úrok                                                                  |
| 20. Odvod daně z úroků                                                              |
| 21. Evidovaný úrok                                                                  |
| 22. Poplatek                                                                        |
| 23. Evidovaný poplatek                                                              |
| 24. Převod mezi bankovními konty (platba)                                           |
| 25. Převod mezi bankovními konty (příjem)                                           |
| 26. Neidentifikovaná platba z bankovního konta                                      |
| 27. Neidentifikovaný příjem na bankovní konto 28. Vlastní platba z bankovního konta |
| 29. Vlastní příjem na bankovní konto                                                |
| 30. Vlastní platba pokladnou                                                        |
| 31. Vlastní příjem pokladnou                                                        |
| 32. Opravný pohyb                                                                   |
| 33. Přřijatý poplatek                                                               |
| 34. Platba v jiné měně                                                              |
| 35. Poplatek - platební karta                                                       |
| 36. Inkaso                                                                          |
| 37. Inkaso ve prospěch účtu                                                         |
| 38. Inkaso z účtu                                                                   |
| 39. Příjem inkasa z cizí banky                                                      |
| 40. Evidovaný úrok                                                                  |
| 41. Okamžitá príchozí platba                                                        |
| 42. Okamžitá odchozí platba                                                         |
| 43. Poplatek - pojištění hypotéky                                                   |
| 44. Okamžitá příchozí Europlatba                                                    |
| 45. Okamžitá odchozí Europlatba                                                     |

# 5.2 Struktura URL dotazu

Doporučený **nejmenší interval dotazu** na stejný token je **30** **sekund** bez ohledu na typ formátu. Pro účely reálného testování při vývoji je nutné mít zřízen skutečný účet. Všechny pohyby na účtech v bankovním systému jsou evidovány podle **jedinečného** **klíče** **IDpohyb.**

Všechny uvedené příklady mají neplatný vzorový token.

## 5.2.1 Pohyby na účtu za určené období

Struktura: <https://fioapi.fio.cz/v1/rest/periods/{token}/{datum od}/{datum do}/transactions.{format}>

| Proměnná | Popis                                                                     |
| -------- | ------------------------------------------------------------------------- |
| Token    | unikátní vygenerovaný token                                               |
| Datum od | datum - začátek stahovaných příkazů ve formátu rok-měsíc-den (rrrr-mm-dd) |
| Datum do | datum - konec stahovaných příkazů ve formátu rok-měsíc-den (rrrr-mm-dd)   |
| Formát   | formát pohybů                                                             |

Příklad: Získání pohybů v období od 25.8.2023 do 31.8.2023 v xml

- <https://fioapi.fio.cz/v1/rest/periods/aGEMQB9ldh35fh1g51h3ekkQwyGIQ/2023-08-25/2023-08-31/transactions.xml>

## 5.2.2 Oficiální výpisy pohybů z účtu

Struktura: <https://fioapi.fio.cz/v1/rest/by-id/{token}/{year}/{id}/transactions.{format}>

| Proměnná | Popis                       |
| -------- | --------------------------- |
| Token    | unikátní vygenerovaný token |
| Year     | rok -formát: rrrr           |
| Id       | číslo výpisu                |
| Formát   | formát pohybů               |

Příklad: Získání 1. výpisu z roku 2012

- <https://fioapi.fio.cz/v1/rest/by-id/aGEMtmwcsg5EbfljqlhunibjhuvfdtsersxexdtgMldh6u3/2012/1/transactions.cbaxml>

## 5.2.3 Pohyby na účtu od posledního stažení

Při každém dotazu bankovní systém automaticky zapíše novou zarážku posledního IDpohybu nebo data jestliže v odpovědi jsou pohyby na účtu. Pokud odpověď je prázdná, tak zarážka zůstává na serveru stejná a odpověď obsahuje pouze základní informace o účtu (hlavička).

Struktura: <https://fioapi.fio.cz/v1/rest/last/{token}/transactions.{format}>

| Proměnná | Popis                       |
| -------- | --------------------------- |
| Token    | unikátní vygenerovaný token |
| Formát   | formát pohybů               |

Příklad: Získání pohybů od posledního stažení v xml

- <https://fioapi.fio.cz/v1/rest/last/aGEMtmwcsWAjPzhg3bPH3j7lu15g56d66AdEbfljqlgMR9ldh6u3/transactions.xml>

# 5.2.4 Nastavení zarážky

Tato funkce je vhodná zejména při výskytu chyby na stranězpracování pohybů nebo potřebujete-li získat informace zpětně. Vlastní nastavení zarážky se provádí výjimečně. A lze jí nastavit dvěma způsoby:

1. Na ID posledního úspěšně staženého pohybu

Struktura: <https://fioapi.fio.cz/v1/rest/set-last-id/{token}/{id}/>

| Proměnná | Popis                                  |
| -------- | -------------------------------------- |
| Token    | unikátní vygenerovaný token            |
| ld       | ID posledního úspěšně staženého pohybu |

Příklad: Nastavení ID posledního úspěšně staženého pohybu na č. 1147608196

- <https://fioapi.fio.cz/v1/rest/set-last-id/Pu5CMBu5nYBtWAk4gsj0FaUIY7JIjUnYBthKaquSWf1eUI/1147608196/>

2. Na datum posledního neúspěšně staženého dne

Struktura: <https://fioapi.fio.cz/v1/rest/set-last-date/{token}/{rrrr-mm-dd}/>

| Proměnná | Popis                                                                                 |
| -------- | ------------------------------------------------------------------------------------- |
| Token    | unikátní vygenerovaný token                                                           |
| Datum    | datum poslední neúspěšně staženého výpisu ve formátu rok- měsíc- den (rrrr-<br>mm-dd) |

Příklad: Nastavení data posledního neúspěšného stažení pohybu na 27. 7. 2023

- <https://fioapi.fio.cz/v1/rest/set-last-date/Pu5CMBu5nYBthKaqM0FaUIY7JIjUnY0FaUIY7JIjU1eUI/2023-07-27/>

## 5.2.5 Karetní transakce obchodníka za určené období

Struktura: <https://fioapi.fio.cz/v1/rest/merchant/{token}/{datum od}/{datum do}/transactions.{format}>

| Proměnná | Popis                                                                     |
| -------- | ------------------------------------------------------------------------- |
| Token    | unikátní vygenerovaný token                                               |
| Datum od | datum - začátek stahovaných příkazů ve formátu rok-měsíc-den (rrrr-mm-dd) |
| Datum do | datum-konec stahovaných příkazů ve formátu rok-měsíc-den (rrrr-mm-dd)     |
| Formát   | formát pohybu                                                             |

Příklad: Získání karetních transakcí v období od 1. 7. 2023 do 31. 7. 2023 je možné pouze ve formátuxml

- <https://fioapi.fio.cz/v1/rest/merchant/Pu5CMBu5nYBthKaqM0FaUIY7JIjUnY0FaUIY7JIjU1eUI/2023-07-01/2023-07-<br>31/transactions.xml>

# 5.2.6 Číslo posledního vytvořeného oficiálního výpisu

Struktura: <https://fioapi.fio.cz/v1/rest/lastStatement/{token}/statement>

| Proměnná | Popis                       |
| -------- | --------------------------- |
| Token    | unikátní vygenerovaný token |

Příklad: Získání čísla posledního vytvořeného oficiálního výpisu pohybů na účtu

- <https://fioapi.fio.cz/v1/rest/lastStatement/Pu5CMBu5nYBthKaqM0FaUIY7JIjUnY0FaUIY7JIjU1eUl/statement>

# 5.3 Struktura formátu

# ID pohybu

- jednoznačná unikátní číselná identifikace pohybu na účtu, neexistují dva pohyby se stejným ID

# ID pokynu

- číselné označení příkazu bankovním systémem Fio banky, může se vyskytovat vícekrát

**Př.** 1 Klient zadá odchozí zahraniční platbu - pokynID: 123. Bankovní systém Fio banky vytvorí pohyblD:1(samotný převod peněz) a pohyblD:2 (poplatek za převod peněz). Na svém účtu budou zobrazeny pohyby č. 1 a 2, oba se stejným pokynID: 123.

**Př.** **2** Dojde-li ke stornu příchozí platby ze strany banky, bude mít platba a její storno rozdílné ID pohybu, ale stejné ID pokynu. Objem pohybu na účtu u storna bude uveden s opačným znaménkem, než byl původníduplicitní pohyb

# 5.3.1 Bankovní pohyby

## 5.3.1.1 Fio XML

XML se skládá ze dvou částí - Info a TransactionList. Schéma odpovědi v XML uvedena na adrese https://www.fio.cz/xsd/IBSchema.xsd. Číselníky zemí, platebních titulů a typů plateb jsou dostupné v XSD na adrese https://www.fio.cz/schema/fioxmltype.xsd.

Info poskytuje informace o účtu, počátečních a konečných stavech na tomto účtu a období, za které jsou dané transakce zobrazeny, identifikace výpisu, posledního stažení pohybů.

V části TransactionList jsou zobrazeny pohyby na účtu za dané období.

Znaková sada: UTF-8

**Struktura XML Info:**

| Element        | Stav | Formát         | Popis                                                        | Příklad                   |
| -------------- | ---- | -------------- | ------------------------------------------------------------ | ------------------------- |
| accountld      | M    | 16n            | číslo účtu                                                   | 1234562                   |
| currency       | M    | 3!x            | měna účtu dle standardu ISO<br>4217                          | CZK                       |
| iban           | M    | 34x            | mezinárodní číslo bankovního<br>účtu dle standardu ISO 13616 | CZ7820100000000001 234562 |
| bic            | M    | 11x            | bankovní identifikační kód dle<br>standardu ISO 9362         | FIOBCZPPXXX               |
| openingBalance | M    | 18d            | počáteční zůstatek na účtu na<br>počátku zvoleného období    | 123.20                    |
| closingBalance | M    | 18d            | konečný zůstatek na účtu na<br>konci zvoleného období        | 123.22                    |
| dateStart      | O    | rrrr-mm-dd+GMT | počátek zvoleného období                                     | 2012-07-27+02:00          |
| dateEnd        | O    | rrrr-mm-dd+GMT | konec zvoleného období                                       | 2012-01-15+01:00          |
| yearList       | O    | 4!n            | rok zvoleného výpisu                                         | 2012                      |
| idList         | O    | 3n             | číslo zvoleného výpisu                                       | 1                         |
| idFrom         | O    | 12n            | číslo prvního pohybu v daném<br>výběru                       | 1158152824                |
| idTo           | O    | 12n            | číslo posledního pohybu<br>v daném výběru                    | 1158152824                |
| idLastDownload | O    | 12n            | číslo posledního úspěšně<br>staženého pohybu                 | 1158152824                |

**Struktura TransactionList:**

| Atribut                     | Stav | Formát         | Popis                                                            | Příklad                                          |
| --------------------------- | ---- | -------------- | ---------------------------------------------------------------- | ------------------------------------------------ |
| ID pohybu                   | M    | 12n            | jedinečné číslo ID pohybu                                        | 1158152824                                       |
| Datum                       | M    | rrrr-mm-dd+GMT | datum pohybu ve tvaru                                            | 2012-07-27+02:00                                 |
| Objem                       | M    | 18d            | velikost přijaté/odeslané částky                                 | 12225.25                                         |
| Měna                        | M    | 3!x            | měna prijaté /odeslané částky<br>dle standardu ISO 4217          | EUR                                              |
| Protiúčet                   | O    | 255x           | číslo protiúčtu                                                  | 2212-2000000699                                  |
| Název protiúčtu             | O    | 255i           | název protiúčtu                                                  | Béda Trávníček                                   |
| Kód banky                   | O    | 10x            | číslo banky protiúčtu                                            | 2010                                             |
| Název banky                 | O    | 255i           | název banky protiúčtu                                            | Fio banka, a.s.                                  |
| KS                          | O    | 4n             | konstantní symbol                                                | 0558                                             |
| VS                          | O    | 10n            | variabilní symbol                                                | 1234567890                                       |
| SS                          | O    | 10n            | specifický symbol                                                | 1234567890                                       |
| Uživatelská<br>identifikace | O    | 255i           | uživatelská identifikace                                         | Nákup: PENNY<br>MARKET s.r.o.,<br>Jaromer, CZ    |
| Zpráva pro<br>příjemce      | O    | 140i           | zpráva pro příjemce                                              | Libovolný text, který se zobrazí příjemci platby |
| Typ                         | M    | 255i           | typ operace                                                      | Platba převvodem<br>uvnitr banky                 |
| Provedl                     | O    | 50i            | oprávněná osoba, která zadala<br>příkaz                          | Béda Trávníček                                   |
| Upřesnění                   | O    | 255i           | upřesňující informace k pohybu. Zpravidla částka a měna.         | 15.90 EUR                                        |
| Komentár                    | O    | 255i           | upresňující informace                                            | Hračky pro děti v<br>PENNY MARKET                |
| BIC                         | O    | 11x            | bankovní identifikační kód banky protiúčtu dle ISO 9362          | UNCRITMMXXX                                      |
| ID Pokynu                   | O    | 12n            | číslo příkazu                                                    | 2102382863                                       |
| Reference<br>plátce         | O    | 255i           | bližší identifikace platby dle<br>ujednání mezi účastníky platby | 2000000003                                       |

# Výsledek dotazu na pohyby v období od 1.7. 2012 do 31.7.2012

```xml
<AccountStatement>
    <Info>
        <accountId>2111111111</accountId>
        <bankId>2010</bankId>
        <currency>CZK</currency>
        <iban>CZ7920100000002111111111</iban>
        <bic>FIOBCZPPXXX</bic>
        <openingBalance>7356.22</openingBalance>
        <closingBalance>7321.22</closingBalance>
        <dateStart>2012-07-01+02:00</dateStart>
        <dateEnd>2012-07-31+02:00</dateEnd>
        <idFrom>1147608196</idFrom>
        <idTo>1147608197</idTo>
    </Info>
    <TransactionList>
        <Transaction>
            <column_22 id="22" name="ID pohybu">1147608196</column_22>
            <column_0 id="0" name="Datum">2012-07-27+02:00</column_0>
            <column_1 id="1" name="Objem">-15.00</column_1>
            <column_14 id="14" name="Měna">CZK</column_14>
            <column_2 id="2" name="Protiúčet">2222233333</column_2>
            <column_3 id="3" name="Kód banky">2010</column_3>
            <column_12 id="12" name="Název banky">Fio banka, a.s.</column_12>
            <column_7 id="7" name="Uživatelská identifikace"></column_7>
            <column_8 id="8" name="Typ">Platba převodem uvnitř banky</column_8>
            <column_9 id="9" name="Provedl">Novák, Jan</column_9>
            <column_25 id="25" name="Komentář">Můj test</column_25>
            <column_17 id="17" name="ID pokynu">2102392862</column_17>
        </Transaction>
        <Transaction>
            <column_22 id="22" name="ID pohybu">1147608197</column_22>
            <column_0 id="0" name="Datum">2012-07-27+02:00</column_0>
            <column_1 id="1" name="Objem">-20.00</column_1>
            <column_14 id="14" name="Měna">CZK</column_14>
            <column_2 id="2" name="Protiúčet">2222233333</column_2>
            <column_3 id="3" name="Kód banky">2010</column_3>
            <column_12 id="12" name="Název banky">Fio banka, a.s.</column_12>
            <column_7 id="7" name="Uživatelská identifikace"></column_7>
            <column_8 id="8" name="Typ">Platba převodem uvnitř banky</column_8>
            <column_9 id="9" name="Provedl">Novák, Jan</column_9>
            <column_25 id="25" name="Komentář"></column_25>
            <column_17 id="17" name="ID pokynu">2102392863</column_17>
        </Transaction>
    </TransactionList>
</AccountStatement>
```

# Výsledek dotazu na 4. výpis z roku 2012

```xml
<AccountStatement>
    <Info>
        <accountId>2111111111</accountId>
        <bankId>2010</bankId>
        <currency>CZK</currency>
        <iban>CZ7920100000002111111111</iban>
        <bic>FIOBCZPPXXX</bic>
        <openingBalance>7356.22</openingBalance>
        <closingBalance>7362.22</closingBalance>
        <yearList>2012</ yearList >
        <idList>4</ idList >
    </Info>
    <TransactionList>
        <Transaction>
            <column_22 id="22" name="ID pohybu">1147301403</column_22>
            <column_0 id="0" name="Datum">2012-06-30+02:00</column_0>
            <column_1 id="1" name="Objem">7.76</column_1>
            <column_14 id="14" name="Měna">CZK</column_14>
            <column_8 id="8" name="Typ">Připsaný úrok</column_8>
            <column_17 id="17" name="ID pokynu">2099310186</column_17>
        </Transaction>
        <Transaction>
            <column_22 id="22" name="ID pohybu">1147301404</column_22>
            <column_0 id="0" name="Datum">2012-06-30+02:00</column_0>
            <column_1 id="1" name="Objem">-1.00</column_1>
            <column_14 id="14" name="Měna">CZK</column_14>
            <column_8 id="8" name="Typ">Odvod daně z úroků</column_8>
            <column_17 id="17" name="ID pokynu">2099310186</column_17>
        </Transaction>
    </TransactionList>
</AccountStatement>
```

# Výsledek dotazu na pohyby od posledního stažení, zarážka ID 1147608196

```xml
<AccountStatement>
    <Info>
        <accountId>2111111111</accountId>
        <bankId>2010</bankId>
        <currency>CZK</currency>
        <iban>CZ7920100000002111111111</iban>
        <bic>FIOBCZPPXXX</bic>
        <openingBalance>6969.22</openingBalance>
        <closingBalance>6597.22</closingBalance>
        <idFrom>1147608197</idFrom>
        <idTo>1147608198</idTo>
        <idLastDownload>1147608196</idLastDownload>
    </Info>
    <TransactionList>
        <Transaction>
            <column_22 id="22" name="ID pohybu">1147608197</column_22>
            <column_0 id="0" name="Datum">2012-07-27+02:00</column_0>
            <column_1 id="1" name="Objem">-20.00</column_1>
            <column_14 id="14" name="Měna">CZK</column_14>
            <column_2 id="2" name="Protiúčet">2222233333</column_2>
            <column_3 id="3" name="Kód banky">2010</column_3>
            <column_12 id="12" name="Název banky">Fio banka, a.s.</column_12>
            <column_7 id="7" name="Uživatelská identifikace"></column_7>
            <column_8 id="8" name="Typ">Platba převodem uvnitř banky</column_8>
            <column_9 id="9" name="Provedl">Novák, Jan</column_9>
            <column_25 id="25" name="Komentář"></column_25>
            <column_17 id="17" name="ID pokynu">2102382863</column_17>
        </Transaction>
        <Transaction>
            <column_22 id="22" name="ID pohybu">1147608198</column_22>
            <column_0 id="0" name="Datum">2012-07-27+02:00</column_0>
            <column_1 id="1" name="Objem">-352.00</column_1>
            <column_14 id="14" name="Měna">CZK</column_14>
            <column_2 id="2" name="Protiúčet">2222233333</column_2>
            <column_3 id="3" name="Kód banky">2010</column_3>
            <column_12 id="12" name="Název banky">Fio banka, a.s.</column_12>
            <column_7 id="7" name="Uživatelská identifikace"></column_7>
            <column_8 id="8" name="Typ">Platba převodem uvnitř banky</column_8>
            <column_9 id="9" name="Provedl">Novák, Jan</column_9>
            <column_25 id="25" name="Komentář"></column_25>
            <column_17 id="17" name="ID pokynu">2102382864</column_17>
        </Transaction>
    </TransactionList>
</AccountStatement>
```

# Výsledek dotazu na pohyby od posledního stažení, zarážka datum 27.7.2012

```xml
<AccountStatement>
    <Info>
        <accountId>2111111111</accountId>
        <bankId>2010</bankId>
        <currency>CZK</currency>
        <iban>CZ7920100000002111111111</iban>
        <bic>FIOBCZPPXXX</bic>
        <openingBalance>6969.22</openingBalance>
        <closingBalance>6582.22</closingBalance>
        <dateStart>2012-07-27+02:00</dateStart>
        <dateEnd>2012-07-27+02:00</dateEnd>
        <idFrom>1147608196</idFrom>
        <idTo>1147608198</idTo>
        <idLastDownload>1147301404</idLastDownload>
    </Info>
    <TransactionList>
        <Transaction>
            <column_22 id="22" name="ID pohybu">1147608196</column_22>
            <column_0 id="0" name="Datum">2012-07-27+02:00</column_0>
            <column_1 id="1" name="Objem">-15.00</column_1>
            <column_14 id="14" name="Měna">CZK</column_14>
            <column_2 id="2" name="Protiúčet">2222233333</column_2>
            <column_3 id="3" name="Kód banky">2010</column_3>
            <column_12 id="12" name="Název banky">Fio banka, a.s.</column_12>
            <column_7 id="7" name="Uživatelská identifikace"></column_7>
            <column_8 id="8" name="Typ">Platba převodem uvnitř banky</column_8>
            <column_9 id="9" name="Provedl">Novák, Jan</column_9>
            <column_25 id="25" name="Komentář"></column_25>
            <column_17 id="17" name="ID pokynu">2102382862</column_17>
        </Transaction>
        <Transaction>
            <column_22 id="22" name="ID pohybu">1147608197</column_22>
            <column_0 id="0" name="Datum">2012-07-27+02:00</column_0>
            <column_1 id="1" name="Objem">-20.00</column_1>
            <column_14 id="14" name="Měna">CZK</column_14>
            <column_2 id="2" name="Protiúčet">2222233333</column_2>
            <column_3 id="3" name="Kód banky">2010</column_3>
            <column_12 id="12" name="Název banky">Fio banka, a.s.</column_12>
            <column_7 id="7" name="Uživatelská identifikace"></column_7>
            <column_8 id="8" name="Typ">Platba převodem uvnitř banky</column_8>
            <column_9 id="9" name="Provedl">Novák, Jan</column_9>
            <column_25 id="25" name="Komentář"></column_25>
            <column_17 id="17" name="ID pokynu">2102382863</column_17>
        </Transaction>
        <Transaction>
            <column_22 id="22" name="ID pohybu">1147608198</column_22>
            <column_0 id="0" name="Datum">2012-07-27+02:00</column_0>
.
.
.
            <column_9 id="9" name="Provedl">Novák, Jan</column_9>
            <column_25 id="25" name="Komentář"></column_25>
            <column_17 id="17" name="ID pokynu">2102382864</column_17>
        </Transaction>
    </TransactionList>
</AccountStatement>
```

# 5.3.1.2 OFX

Ofx seznamu pohybů se skládá z několika částí

```txt
BANKMSGSRSV1
    STMTTRNRS
        TRNUID - unikátní identifikátor příkazu
        STATUS - část vracející chybová hlášení
            CODE
            SEVERITY
        STMTRS - vlastní odpověď
            CURDEF - měna, ve které je účet veden
            BANKACCTFROM - poskytuje data o účtu
                BANKID
                ACCTID
                ACCTTYPE
            BANKTRANLIST- jednotlivé pohyby na účtu
                DTSTART
                DTEND
                STMTTRN - konkrétní pohyb
                    TRNTYPE
                    DTPOSTED
                    TRNAMT
                    FITD
                    NAME
                    BANKACCTO
                    MEMO
```

Podrobnější informace o formátu ofx lze nalézt na jejich webových stránkách.

Znaková sada: UTF-8

STATUS - část vracející chybová hlášení

| Atribut  | Formát           | Popis              |
| -------- | ---------------- | ------------------ |
| CODE     | 6x               | chybový kód        |
| SEVERITY | INFO,WARN, ERROR | závažnost chyby    |
| MESSAGE  | 255x             | textový popischyby |

BANKACCTFROM- poskytuje data o účtu

| Atribut  | Formát | Popis                                                                                                                               |
| -------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------- |
| BANKID   | 9x     | číslo banky                                                                                                                         |
| ACCTID   | 22x    | číslo účtu                                                                                                                          |
| ACCTTYPE | 22x    | typ účtu:<br>CHECKING - běžný účet<br>SAVINGS - Fio konto, termínovaný<br>vklad atd.<br>CREDITLINE - úvěr, kontokorent,<br>hypotéka |

BANKTRANLIST - jednotlivé pohyby na účtu

| Atribut | Formát                         | Popis                          |
| ------- | ------------------------------ | ------------------------------ |
| DTSTART | RRRRMMDDHHMMSS.000[+HH.MM:ZZZ] | počátek zvoleného období/pohyb |
| DTEND   | RRRRMMDDHHMMSS.000[+HH.MM:ZZZ] | konec zvoleného období/pohyb   |

STMTTRN - konkrétní pohyb

www.fio.cz

| Atribut    | Formát                         | Popis                                                                                                                                                                                                                                                                                              |
| ---------- | ------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TRNTYPE    | 22x                            | typ transakce:<br>CREDIT - příjem na bankov/ní konto<br>DEBIT- platba z bankovního konta<br>INT-úrok<br>FEE- poplatek<br>DEP -vklad v hotovosti<br>ATM -výběr z bankomatu<br>POS-platba kartou/výběr z bankomatu XFER - převod uvnitr banky<br>CASH - výběr v hotovosti<br>OTHER - další transakce |
| DTPOSTED   | RRRRMMDDHHMMSS.000[+HH.MM:ZZZ] | datum pohybu                                                                                                                                                                                                                                                                                       |
| TRNAMT     | 15d                            | částka pohybu                                                                                                                                                                                                                                                                                      |
| FITID      | 255x                           | id pohybu 5                                                                                                                                                                                                                                                                                        |
| NAME       | 32e                            | typ operace                                                                                                                                                                                                                                                                                        |
| MEMO       | 255x                           | komentár                                                                                                                                                                                                                                                                                           |
| BANKACCTTO | 255x                           | informace o protiúčtu                                                                                                                                                                                                                                                                              |

BANKACCTTO

| Atribut  | Formát | Popis                                                                                                                                    |
| -------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------- |
| BANKID   | 9x     | číslo banky protiúčtu                                                                                                                    |
| ACCTID   | 22x    | číslo účtu protiúčtu                                                                                                                     |
| ACCTTYPE | 22x    | Typ protiúčtu:<br>CHECKING - běžný účet<br>SAVINGS - Fio konto, termínovaný<br>vklad atd.<br>CREDITLINE - úvěr, kontokorent,<br>hypotéka |

Transakce jsou ve formátu OFX uváděny v časové zóně UTC -2 (proti CET jsou posunuté o 3 (léto - 4) hodiny.

# Výsledek dotazu na pohyby v období od 1.7. 2012 do 31.7.2012

```xml
<OFX>
    <BANKMSGSRSV1>
        <STMTTRNRS>
            <TRNUID>d94a4b79-694d-419d-ba63-d7ea0d48c042</TRNUID>
            <STATUS>
                <CODE>0</CODE>
                <SEVERITY>INFO</SEVERITY>
            </STATUS>
            <STMTRS>
                <CURDEF>CZK</CURDEF>
                <BANKACCTFROM>
                    <BANKID>2010</BANKID>
                    <ACCTID>2111111111</ACCTID>
                    <ACCTTYPE>CHECKING</ACCTTYPE>
                </BANKACCTFROM>
                <BANKTRANLIST>
                    <DTSTART>20120701000000.000[+02.00:CET]</DTSTART>
                    <DTEND>20120731000000.000[+02.00:CET]</DTEND>
                    <STMTTRN>
                        <TRNTYPE>CHECK</TRNTYPE>
                        <DTPOSTED>20120727000000.000[+02.00:CET]</DTPOSTED>
                        <TRNAMT>-15.0000</TRNAMT>
                        <FITID>1147608196</FITID>
                        <NAME>Prijem prevodem uvnitr banky</NAME>
                        <BANKACCTTO>
                            <BANKID>2010</BANKID>
                            <ACCTID>2222233333</ACCTID>
                            <ACCTTYPE>CHECKING</ACCTTYPE>
                        </BANKACCTTO>
                    </STMTTRN>
                    <STMTTRN>
                        <TRNTYPE>CHECK</TRNTYPE>
                        <DTPOSTED>20120727000000.000[+02.00:CET]</DTPOSTED>
                        <TRNAMT>-20.0000</TRNAMT>
                        <FITID>1147608197</FITID>
                        <NAME>Prijem prevodem uvnitr banky</NAME>
                        <BANKACCTTO>
                            <BANKID>2010</BANKID>
                            <ACCTID>2222233333</ACCTID>
                            <ACCTTYPE>CHECKING</ACCTTYPE>
                        </BANKACCTTO>
                    </STMTTRN>
                    <STMTTRN>
                        <TRNTYPE>CHECK</TRNTYPE>
                        <DTPOSTED>20120727000000.000[+02.00:CET]</DTPOSTED>
                        <TRNAMT>-352.0000</TRNAMT>
                        <FITID>1147608198</FITID>
                        <NAME>Prijem prevodem uvnitr banky</NAME>
                        <BANKACCTTO>
                            <BANKID>2010</BANKID>
                            <ACCTID>2222233333</ACCTID>
                            <ACCTTYPE>CHECKING</ACCTTYPE>
                        </BANKACCTTO>
                    </STMTTRN>
                </BANKTRANLIST>
            </STMTRS>
        </STMTTRNRS>
    </BANKMSGSRSV1>
</OFX>
```

# Výsledek dotazu na na 4. výpis z roku 2012

```xml
<OFX>
    <BANKMSGSRSV1>
        <STMTTRNRS>
            <TRNUID>6036522c-dae4-47a5-93c9-0d27c27488be</TRNUID>
            <STATUS>
                <CODE>0</CODE>
                <SEVERITY>INFO</SEVERITY>
            </STATUS>
            <STMTRS>
                <CURDEF>CZK</CURDEF>
                <BANKACCTFROM>
                    <BANKID>2010</BANKID>
                    <ACCTID>2111111111</ACCTID>
                    <ACCTTYPE>CHECKING</ACCTTYPE>
                </BANKACCTFROM>
                <BANKTRANLIST>
                    <DTSTART>20120630000000.000[+02.00:CET]</DTSTART>
                    <DTEND>20120630000000.000[+02.00:CET]</DTEND>
                    <STMTTRN>
                        <TRNTYPE>CHECK</TRNTYPE>
                        <DTPOSTED>20120630000000.000[+02.00:CET]</DTPOSTED>
                        <TRNAMT>7.760.0000</TRNAMT>
                        <FITID>1147301403</FITID>
                        <NAME> Pripsany urok</NAME>
                    </STMTTRN>
                    <STMTTRN>
                        <TRNTYPE>CHECK</TRNTYPE>
                        <DTPOSTED>20120701000000.000[+02.00:CET</DTPOSTED>
                        <TRNAMT>-1.0000</TRNAMT>
                        <FITID>1147301404</FITID>
                        <NAME>Odvod dane z uroku</NAME>
                    </STMTTRN>
                </BANKTRANLIST>
            </STMTRS>
        </STMTTRNRS>
    </BANKMSGSRSV1>
</OFX>
```

# Výsledek dotazu na pohyby od posledního stažení, zarážka ID 1147608196

```xml
<OFX>
    <BANKMSGSRSV1>
        <STMTTRNRS>
            <TRNUID>0411f79c-d5da-4439-838f-8ed1b032503e</TRNUID>
            <STATUS>
                <CODE>0</CODE>
                <SEVERITY>INFO</SEVERITY>
            </STATUS>
            <STMTRS>
                <CURDEF>CZK</CURDEF>
                <BANKACCTFROM>
                    <BANKID>2010</BANKID>
                    <ACCTID>2111111111</ACCTID>
                    <ACCTTYPE>CHECKING</ACCTTYPE>
                </BANKACCTFROM>
                <BANKTRANLIST>
                    <DTSTART>20120727000000.000[+02.00:CET]</DTSTART>
                    <DTEND>20120727000000.000[+02.00:CET]</DTEND>
                    <STMTTRN>
                        <TRNTYPE>CHECK</TRNTYPE>
                        <DTPOSTED>20120727000000.000[+02.00:CET]</DTPOSTED>
                        <TRNAMT>-20.0000</TRNAMT>
                        <FITID>1147608197</FITID>
                        <NAME>Platba prevodem uvnitr banky</NAME>
                        <BANKACCTTO>
                            <BANKID>2010</BANKID>
                            <ACCTID>2222233333</ACCTID>
                            <ACCTTYPE>CHECKING</ACCTTYPE>
                        </BANKACCTTO>
                    </STMTTRN>
                    <STMTTRN>
                        <TRNTYPE>CHECK</TRNTYPE>
                        <DTPOSTED>20120727000000.000[+02.00:CET]</DTPOSTED>
                        <TRNAMT>-352.0000</TRNAMT>
                        <FITID>1147608198</FITID>
                        <NAME>Platba prevodem uvnitř banky</NAME>
                        <BANKACCTTO>
                            <BANKID>2010</BANKID>
                            <ACCTID>2222233333</ACCTID>
                            <ACCTTYPE>CHECKING</ACCTTYPE>
                        </BANKACCTTO>
                    </STMTTRN>
                </BANKTRANLIST>
            </STMTRS>
        </STMTTRNRS>
    </BANKMSGSRSV1>
</OFX>
```

# Výsledek dotazu na pohyby od posledního stažení, zarážka datum 27.7.2012

```xml
<OFX>
    <BANKMSGSRSV1>
        <STMTTRNRS>
            <TRNUID>14494224-90bf-4d17-9bd5-a820059c6b21</TRNUID>
            <STATUS>
                <CODE>0</CODE>
                <SEVERITY>INFO</SEVERITY>
            </STATUS>
            <STMTRS>
                <CURDEF>CZK</CURDEF>
                <BANKACCTFROM>
                    <BANKID>2010</BANKID>
                    <ACCTID>2111111111</ACCTID>
                    <ACCTTYPE>CHECKING</ACCTTYPE>
                </BANKACCTFROM>
                <BANKTRANLIST>
                    <DTSTART>20120727000000.000[+02.00:CET]</DTSTART>
                    <DTEND>20120727000000.000[+02.00:CET]</DTEND>
                    <STMTTRN>
                        <TRNTYPE>CHECK</TRNTYPE>
                        <DTPOSTED>20120727000000.000[+02.00:CET]</DTPOSTED>
                        <TRNAMT>-15.0000</TRNAMT>
                        <FITID>1147608196</FITID>
                        <NAME>Platba prevodem uvnitr banky</NAME>
                        <BANKACCTTO>
                            <BANKID>2010</BANKID>
                            <ACCTID>2222233333</ACCTID>
                            <ACCTTYPE>CHECKING</ACCTTYPE>
                        </BANKACCTTO>
                    </STMTTRN>
                    <STMTTRN>
                        <TRNTYPE>CHECK</TRNTYPE>
                        <DTPOSTED>20120727000000.000[+02.00:CET]</DTPOSTED>
                        <TRNAMT>-20.0000</TRNAMT>
                        <FITID>1147608197</FITID>
                        <NAME>Platba prevodem uvnitř banky</NAME>
                        <BANKACCTTO>
                            <BANKID>2010</BANKID>
                            <ACCTID>2222233333</ACCTID>
                            <ACCTTYPE>CHECKING</ACCTTYPE>
                        </BANKACCTTO>
                    </STMTTRN>
                </BANKTRANLIST>
            </STMTRS>
        </STMTTRNRS>
    </BANKMSGSRSV1>
</OFX>
```

# 5.3.1.3 GPC

GPC se skládá ze dvou častí - "Data - výpis v Kč"

(informace o účtu) a "Data - obratová položka" (jednotlivé pohyby). Obě části mají pevnou délku 130 znaků. Mezi jednotlivými údaji v záznamu není žádný oddělovač. Do pevné délky jsou údaje doplňovány zleva příslušným počtem znaků nula.

Znaková sada: Windows-1250

**Struktura "Data - výpis v Kč"**

| Byty    | Popis                                                                      |
| ------- | -------------------------------------------------------------------------- |
| 1-3     | "074" = označení typu záznamu "Data - výpis v Kč"                          |
| 4-19    | přidělené č. účtu s vodícími nulami                                        |
| 20-39   | 20 alfanumerických znaků zkráceného názvu účtu, doplněných mezerami zprava |
| 40-45   | datum starého zůstatku ve formátu DDMMRR                                   |
| 46-59   | starý zůstatek v haléřích 14 numerických znaků s vodícími nulami           |
| 60      | znaménko starého zůstatku, 1 znak "+" nebo "-"                             |
| 61-74   | nový zůstatek v haléřích 14 numerických znaků s vodícími nulami            |
| 75      | znaménko nového zůstatku, 1 znak "+" nebo "-"                              |
| 76-89   | obraty debet (MD) v haléřích 14 numerických znaků s vodícími nulami        |
| 90      | znaménko obratů debet (MD), 1 znak "0" nebo "-"                            |
| 91-104  | obraty kredit (D) v haléřích 14 numerických znaků s vodícími nulami        |
| 105     | znaménko obratů kredit (D), 1 znak "0" nebo "-"                            |
| 106-108 | pořadové číslo výpisu                                                      |
| 109-114 | datum účtování ve formátu DDMMRR                                           |
| 115-128 | (vyplněno 14 znaky mezera z důvodu sjednocení délky záznamů)               |
| 129-130 | ukončovací znaky CR a LF                                                   |

**Struktura "Data - obratová položka v Kč"**

| Byty        | Popis                                                                                                                          |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------ |
| 1-3         | "075" = označení typu záznamu "Data - obratová položka"                                                                        |
| 4-19        | přidělené číslo účtu 16 numerických znaků s vodícími nulami                                                                    |
| 20-35       | číslo účtu 16 numerických znaků s vodícími nulami (případně v pořadí předčíslí + číslo účtu)                                   |
| 36-48       | číslo dokladu 13 numerických znaků                                                                                             |
| 49-60       | částka v haléřích 12 numerických znaků s vodícími nulami                                                                       |
| 61          | kód účtování vztažený k číslu účtu:1 = položka debet,2 = položka kredit,4 = storno položky<br>debet, 5 = storno položky kredit |
| 62-71       | variabilní symbol 10 numerických znaků s vodícími nulami                                                                       |
| 72-81       | konstantní symbol 10 numerických znaků s vodícími nulami ve formátu BBBBKSYM, kde:<br>BBBB- kód banky, KSYM- konstantní symbol |
| 82-91       | specifický symbol 10 numerických znaků s vodícími nulami                                                                       |
| 92-97       | "000000" = valuta, platba v ČR - datum splatnosti ve formátu DDMMRR                                                            |
| 98-117      | 20 alfanumerických znaků zkráceného názvu klienta, doplněno mezerami zprava                                                    |
| 118         | "0"                                                                                                                            |
| 119-<br>122 | "0203" = kód měny pro Kč                                                                                                       |
| 123-<br>128 | datum splatnosti ve formátu DDMMRR                                                                                             |
| 129-130     | ukončovací znaky CR a LF                                                                                                       |
| 1-3         | "075" = označení typu záznamu "Data - obratová položka"                                                                        |

# Výsledek dotazu na pohyby v období od 26. 6. 2012 do 30. 6. 2012

```txt
0740000002400222222Novák, Jan
26061200000000019500+00000000019501
+00000000000100-000000000001010000300612FIO
075000000240022222200000029002333330001148734530000000000100200000000000
0201005580000000000260612Novák, Pavel 00203260612
075000000240022222200000029002333330001148734781000000000100100000000000
0201005580000000000260612 00203260612
075000000240022222200000000000000000001149190193000000000001200000000000
0000000000000000000300612Připsaný úrok 00203300612
```

**Výsledek dotazu na 3. výpis z roku 2012**

```txt
0740000002400222222Novák, Jan
01081200000000018503+00000000018505
+000000000000000000000000000020003310812FIO
075000000240022222200000000000000000001155172472000000000002200000000000
0000000000000000000310812Připsaný úrok 00203310812
```

**Výsledek dotazu na pohyby od posledního stažení, zarážka ID 1150392361**

```txt
0740000002400222222Novák, Jan
17071200000000018505+00000000018501
+00000000001500-000000000000060000300912FIO
075000000240022222200000026000444440001150808074000000001500100000000010
0201005580000000002170712 00203170712
075000000240022222200000000000000000001152125621000000000002200000000000
0000000000000000000310712Připsaný úrok 00203310712
075000000240022222200000000000000000001155172472000000000002200000000000
0000000000000000000310812Připsaný úrok 00203310812
075000000240022222200000000000000000001158218819000000000002200000000000
0000000000000000000300912Připsaný úrok 00203300912
```

**Výsledek dotazu na pohyby od posledního stažení, zarážka datum 27.7.2012**

```txt
0740000002400222222Novák, Jan
31071200000000018505+00000000018503
+000000000000000000000000000060000300912FIO
075000000240022222200000000000000000001152125621000000000002200000000000
0000000000000000000310712Připsaný úrok 00203310712
075000000240022222200000000000000000001155172472000000000002200000000000
0000000000000000000310812Připsaný úrok 00203310812
075000000240022222200000000000000000001158218819000000000002200000000000
0000000000000000000300912Připsaný úrok 00203300912
```

## 5.3.1.4 CSV

CSV je textový formát tabulkového souboru, kde jsou jednotlivé sloupce tabulky odděleny středníky. Jednotlivé řádky tabulky jsou oddělené řádkováním. Jednotlivá pole mohou být ještě zabalená do uvozovek, pokud se v nich vyskytuje středník. Každé vložené uvozovky uvnitř pole budou reprezentovány párem uvozovek.

Znaková sada: UTF-8

**Struktura hlavičky**

| Atribut        | Stav | Formát     | Popis                                                        | Příklad                  |
| -------------- | ---- | ---------- | ------------------------------------------------------------ | ------------------------ |
| accountld      | M    | 16n        | číslo účtu                                                   | 1234562                  |
| currency       | M    | 3!x        | měna účtu dle standardu ISO<br>4217                          | CZK                      |
| iban           | M    | 24x        | mezinárodní číslo bankovního<br>účtu dle standardu ISO 13616 | CZ7820100000000001234562 |
| bic            | M    | 11x        | bankovní identifikační kód dle<br>standardu ISO 9362         | FIOBCZPPXXX              |
| openingBalance | M    | 18D        | počáteční zůstatek na účtu na<br>počátku zvoleného období    | 1223,20                  |
| closingBalance | M    | 18D        | konečný zůstatek na účtu na<br>konci zvoleného období        | 1223,22                  |
| dateStart      | O    | dd.mm.rrrr | počátek zvoleného období ve<br>tvaru den.měsíc.rok           | 28.02.2012               |
| dateEnd        | O    | dd.mm.rrrr | konec zvoleného období ve tvaru den.měsíc.rok                | 01.03.2012               |
| idFrom         | O    | 12n        | číslo prvního pohybu v daném<br>výběru                       | 1158152824               |
| idTo           | O    | 12n        | číslo posledního pohybu<br>v daném výběru                    | 1158152824               |

**Struktura pohybu**

| Atribut                     | Stav | Formát     | Popis                                                                                  | Příklad                                              |
| --------------------------- | ---- | ---------- | -------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| ID pohybu                   | M    | 12n        | Jedinečné číslo pohybu                                                                 | 1158152824                                           |
| Datum                       | M    | dd.mm.rrrr | datum pohybu ve tvaru                                                                  | 01.03.2012                                           |
| Objem                       | M    | 18D        | velikost prijaté (odeslané) částky                                                     | 125,30                                               |
| Měna                        | M    | 3!x        | měna prijaté (odeslané) částky dle<br>standardu ISO 4217                               | EUR                                                  |
| Protiúčet                   | O    | 255x       | číslo protiúčtu                                                                        | 2212-2000000699                                      |
| Název protiúčtu             | O    | 255i       | název protiúčtu, pokud hodnota není<br>null, tak je vždy/ v uvozovkách                 | ,,Béda Trávníček"                                    |
| Kód banky                   | O    | 10x        | číslo banky protiúčtu                                                                  | 2010                                                 |
| Název banky                 | O    | 255i       | název banky protiúčtu, pokud hodnota není null, tak je vždy v uvozovkách               | ,,Fio banka, a.s."                                   |
| KS                          | O    | 4n         | konstantní symbol                                                                      | 0558                                                 |
| VS                          | O    | 10n        | variabilní symbol                                                                      | 1234567890                                           |
| SS                          | O    | 10n        | specifický symbol                                                                      | 1234567890                                           |
| Uživatelská<br>identifikace | O    | 255i       | uživatelská identifikace, pokud<br>hodnota není null, tak je vždy v<br>uvozovkách      | ,Nákup:""PENNY""<br>MARKET s.r.o., Jaromer, CZ"      |
| Zpráva pro<br>príjemce      | O    | 140i       | zpráva pro příjemce, pokud hodnota<br>není null, tak je vždy v uvozovkách              | ,Libovolný text,který se<br>zobrazí příjemci platby" |
| Typ                         | M    | 255i       | typ operace                                                                            | Platba prevodem uvnitr<br>banky                      |
| Provedl                     | O    | 50i        | oprávněná osoba, která zadala příkaz,pokud hodnota není null, tak je vždy v uvozovkách | ,Béda Trávníček"                                     |
| Upřesnění                   | O    | 255i       | upřesňující informace k pohybu.                                                        | ,,15.90 EUR"                                         |
|                             |      |            | Zpravidla to bývá kurz, pokud hodnota není null, tak je vždy v uvozovkách              |                                                      |
| Komentár                    | O    | 255i       | upřesňující informace, pokud hodnota není null, tak je vždy v uvozovkách               | ,Hračky pro děti v<br>PENNY MARKET"                  |
| BIC                         | O    | 11x        | bankovní identifikační kód banky<br>protiúčtu dle standardu ISO 9362                   | FIOBCZPPXXX                                          |
| ID Pokynu                   | O    | 12n        | jedinečné číslo příkazu                                                                | 2102382863                                           |

# Výsledek dotazu na pohyby v období od 26. 6. 2012 do 30.6.2012

```txt
accountId;2200018111
bankId;2010
currency;CZK
iban;CZ3520100000002200018111
bic;FIOBCZPPXXX
openingBalance;12894,79
closingBalance;12845,93
dateStart;25.07.2012
dateEnd;15.09.2012
idFrom; 1252062368
idTo; 1255107881
idLastDownload; 1252062367
ID pohybu;Datum;Objem;Měna;Protiúčet;Název protiúčtu;Kód banky;Název banky;KS;VS;SS;Uživatelská identifikace;Zpráva pro příjemce;Typ;Provedl;Upřesnění;Komentář;BIC;ID pokynu;
1252062368;31.07.2012;0,07;CZK;;;;;;;;;;Připsaný úrok;;;;;2120891307;1252273009;01.08.2012;-49,00;CZK;1231231231;;2010;"Fio banka, a.s.";0558;;; ;;Platba převodem uvnitř banky;"Béda, ""Trávníček""";;;;2121709706;<br>1255107881;31.08.2012;0,07;CZK;;;;; ; ;;;;Připsaný úrok;; ; ; ;2134853563;
```

# Výsledek dotazu - pohyby na POS terminálu v období od 1. 7. 2012 do 31.7.2012

```txt
accountId;2200018111
bankId;2010
currency;CZK
iban;CZ3520100000002200018111
bic;FIOBCZPPXXX
dateStart;01.07.2012
dateEnd;31.07.2012
ID pohybu;ID pokynu;Datum;Objem;Poznámka;Název pobočky;Identifikátor transakce;Číslo zařízení;Datum transakce;Autorizační číslo;Číslo karty;Objem;Měna;Typ;Vystavitel karty;Poplatky celkem;Poplatek Fio;Poplatek intercharge;Poplatek karetní asociace;Zaúčtováno;Datum zaúčtování
8216165940;9277937165;19.07.2015;4700,00;Zaúčtování POS terminálu MasterCard, Operace ON-US;Potrefený Sokol;28;002030999999 1;16.04.201511:28:12;997476;553937**\*\***9052;200,00;CZK;ONUS;MASTERCARD;0,00;;;;true;19.07.2015
```

# 5.3.1.5 HTML

HTML používá znakovou sadu UTF-8 a má následují strukturu.

| Atribut                     | Stav | Popis          | Popis                                                             | Příklad                                          |
| --------------------------- | ---- | -------------- | ----------------------------------------------------------------- | ------------------------------------------------ |
| accountld                   | M    | 16n            | číslo účtu                                                        | 1234562                                          |
| bankld                      | O    | 10x            | číslo banky - 4 numerické znaky                                   | 2010                                             |
| currency                    | M    | 3!x            | měna účtu dle standardu ISO<br>4217                               | CZK                                              |
| iban                        | M    | 24x            | mezinárodní číslo bankovního<br>účtu dle standardu ISO 13616      | CZ782010000000000<br>1234562                     |
| bic                         | M    | 11x            | bankovní identifikační kód dle<br>standardu ISO 9362              | FIOBCZPPXXX                                      |
| openingBalance              | M    | 18d            | počáteční zůstatek na účtu na<br>počátku zvoleného období         | 123.20                                           |
| closingBalance              | M    | 18d            | konečný zůstatek na účtu na<br>konci zvoleného období             | 123.22                                           |
| dateStart                   | O    | rrrr-mm-dd+GMT | počátek zvoleného období ve<br>tvaru den.měsíc.rok                | 2012-07-27+0200                                  |
| dateEnd                     | O    | rrrr-mm-dd+GMT | konec zvoleného období                                            | 2012-01-15+0100                                  |
| yearList                    | O    | 4!n            | rok zvoleného výpisu                                              | 2012                                             |
| idList                      | O    | 3n             | číslo zvoleného výpisu                                            | 1                                                |
| idFrom                      | O    | 12n            | číslo prvního pohybu v daném<br>výběru                            | 1158152824                                       |
| idTo                        | O    | 12n            | číslo posledního pohybu v daném<br>výběru                         | 1158152824                                       |
| idLastDownload              | O    | 12n            | číslo posledního úspěšně<br>staženého pohybu                      | 1158152824                                       |
| ID pohybu                   | M    | 12n            | unikátní číslo pohybu                                             | 1158152824                                       |
| Datum                       | M    | rrrr-mm-dd+GMT | datum                                                             | 2012-07-27+02:00                                 |
| Objem                       | M    | 18d            | velikost prijaté (odeslané) částky                                | 12225.25                                         |
| Měna                        | M    | 3!x            | měna přijaté (odeslané) částky dle standardu ISO 4217             | EUR                                              |
| Protiúčet                   | O    | 255x           | číslo protiúčtu                                                   | 2212-2000000699                                  |
| Kód banky                   | O    | 10x            | číslo banky protiúčtu                                             | 2010                                             |
| Název protiúčtu             | O    | 255i           | název protiúčtu                                                   | Béda Trávníček                                   |
| Název banky                 | O    | 255i           | název banky protiúčtu                                             | Fio banka, a.s.                                  |
| KS                          | O    | 4n             | konstantní symbol                                                 | 0558                                             |
| VS                          | O    | 10n            | variabilní symbol                                                 | 1234567890                                       |
| SS                          | O    | 10n            | specifický symbol                                                 | 1234567890                                       |
| Uživatelská<br>identifikace | O    | 255i           | uživatelská identifikace                                          | Nákup: PENNY<br>MARKET s.r.o.,<br>Jaromer, CZ    |
| Zpráva<br>propříjemce       | O    | 140i           | zpráva pro příjemce                                               | Libovolný text, který se zobrazí příjemci platby |
| Typ                         | M    | 255i           | typ operace                                                       | Platba převodem<br>uvnitr banky                  |
| Provedl                     | O    | 50i            | oprávněná osoba, která zadala<br>příkaz                           | Béda Trávníček                                   |
| Upřesnění                   | O    | 255i           | upřesňující informace (zpravidla<br>to bývá kurz)                 | 15.90 EUR                                        |
| Komentár                    | O    | 255i           | upřesňující informace                                             | Hračky pro děti<br>v PENNY MARKET                |
| BIC                         | O    | 11x            | bankovní identifikační kód banky protiúčtu dle standardu ISO 9362 | UNCRITMMXXX                                      |
| ID Pokynu                   | O    | 12x            | číslo příkazu                                                     | 2102382863                                       |

## 5.3.1.6 JSON

JSON je založen na podmnožině programovacího jazyka JavaScript. Data jsou v JSON ve dvou hlavních strukturách, ve dvojicích název:hodnota a v tříděných seznamech hodnot. Podrobnější informace o formátu lze nalézt na jejich webových stránkách.

JSON seznamu pohybů se skládá ze dvou hlavních částí - info a transactionList. Info poskytuje informace o účtu, počátečních a konečných stavech na tomto účtu a období, za které jsou dané pohyby zobrazeny, identifikace výpisu, posledního stažení pohybů. V části transactionList jsou zobrazeny pohyby na účtu za dané období.

Znaková sada: UTF-8

**Struktura Info**

| Atribut        | Popis                                                     |
| -------------- | --------------------------------------------------------- |
| accountld      | číslo účtu                                                |
| bankld         | číslo banky - 4 numerické znaky                           |
| currency       | měna účtu dle standardu ISO 4217                          |
| IBAN           | mezinárodní číslo bankovního účtu dle standardu ISO 13616 |
| BIC            | bankovní identifikační kód dle standardu ISO 9362         |
| openingBalance | počáteční zůstatek na účtu na počátku zvoleného období    |
| closingBalance | konečný zůstatek na účtu na konci zvoleného období        |
| dateStart      | počátek zvoleného období ve tvaru rrrr-mm-dd+GMT          |
| dateEnd        | konec zvoleného období ve tvaru rrrr-mm-dd+GMT            |
| yearList       | rok zvoleného výpisu                                      |
| idList         | číslo zvoleného výpisu                                    |
| idFrom         | číslo prvního pohybu v daném výběru                       |
| idTo           | číslo posledního pohybu v daném výběru                    |
| idLastDownload | číslo posledního úspěšně staženého pohybu                 |

**Struktura TransactionList**

| ID sloupce | Atribut                  | Popis                                                             |
| ---------- | ------------------------ | ----------------------------------------------------------------- |
| Column22   | ID pohybu                | unikátní číslo pohybu - 10 numerických znaků                      |
| Column0    | Datum                    | datum pohybu ve tvaru rrrr-mm-dd+GMT                              |
| Column1    | Objem                    | velikost přijaté (odeslané) částky                                |
| Column14   | Měna                     | měna přijaté (odeslané) částky dle standardu ISO 4217             |
| Column2    | Protiúčet                | číslo protiúčtu                                                   |
| Column10   | Název protiúčtu          | název protiúčtu                                                   |
| Column3    | Kód banky                | číslo banky protiúčtu                                             |
| Column12   | Název banky              | název banky protiúčtu                                             |
| Column4    | KS                       | konstantní symbol                                                 |
| Column5    | VS                       | variabilní symbol                                                 |
| Column6    | SS                       | specifický symbol                                                 |
| Column7    | Uživatelská identifikace | uživatelská identifikace                                          |
| Column16   | Zpráva pro príjemce      | zpráva pro příjemce                                               |
| Column8    | Typ pohybu               | typ operace                                                       |
| Column9    | Provedl                  | oprávněná osoba, která zadala příkaz                              |
| Column18   | Upřesnění                | upřesňující informace                                             |
| Column25   | Komentár                 | komentár                                                          |
| Column26   | BIC                      | bankovní identifikační kód banky protiúčtu dle standardu ISO 9362 |
| Column17   | ID pokynu                | číslo příkazu                                                     |
| Column27   | Reference plátce         | bližší identifikace platby dle ujednání mezi účastníky platby     |

# Výsledek dotazu na pohyby v období od 26. 6. 2012 do 30. 6. 2012

```json
{
  "accountStatement": {
    "info": {
      "accountId": "2400222222",
      "bankId": "2010",
      "currency": "CZK",
      "iban": "CZ7920100000002400222222",
      "bic": "FIOBCZPPXXX",
      "op eningBalance": 195.0,
      "closingBalance": 195.01,
      "dateStart": 1340661600000,
      "dateEnd": 1341007200000,
      "yearList": null,
      "idList": null,
      "idFrom": 1148734530,
      "idTo": 1149190193,
      "idLastDownload": 1149190192
    },
    "transactionList": {
      "transaction": [
        {
          "column22": { "value": 1148734530, "name": "ID pohybu", "id": 22 },
          "column0": { "value": 1340661600000, "name": "Datum", "id": 0 },
          "column1": { "value": 1.0, "name": "Objem", "id": 1 },
          "column14": { "value": "CZK", "name": "Měna", "id": 14 },
          "column2": { "value": "2900233333", "name": "Protiúčet", "id": 2 },
          "column10": {
            "value": "Pavel, Novák",
            "name": "Názevprotiúčtu",
            "id": 10
          },
          "column3": { "value": "2010", "name": "Kód banky", "id": 3 },
          "column12": {
            "value": "Fio banka, a.s.",
            "name": "Název banky",
            "id": 12
          },
          "column4": { "value": "0558", "name": "KS", "id": 4 },
          "column5": null,
          "column6": null,
          "column7": null,
          "column16": null,
          "column8": {
            "value": "Příjem převodem uvnitřbanky",
            "name": "Typ",
            "id": 8
          },
          "column9": null,
          "column18": null,
          "column25": null,
          "column26": null,
          "column17": { "value": 2105685816, "name": "ID pokynu", "id": 17 }
        },
        {
          "column22": { "value": 1148734781, "name": "ID pohybu", "id": 22 },
          "column0": { "value": 1340661600000, "name": "Datum", "id": 0 },
          "column1": { "value": -1.0, "name": "Objem", "id": 1 },
          "column14": { "value": "CZK", "name": "Měna", "id": 14 },
          "column2": { "value": "2900233333", "name": "Protiúčet", "id": 2 },
          "column10": null,
          "column3": { "value": "2010", "name": "Kód banky", "id": 3 },
          "column12": {
            "value": "Fio banka, a.s.",
            "name": "Název banky",
            "id": 12
          },
          "column4": { "value": "0558", "name": "KS", "id": 4 },
          "column5": null,
          "column6": null,
          "column7": {
            "value": " ",
            "name": "Uživatelská identifikace",
            "id": 7
          },
          "column16": null,
          "column8": {
            "value": "Platba převodem uvnitř banky",
            "name": "Typ",
            "id": 8
          },
          "column9": { "value": "Novák, Jan", "name": "Proved1", "id": 9 },
          "column18": null,
          "column25": { "value": "", "name": "Komentář", "id": 25 },
          "column26": null,
          "column17": { "value": 2105687343, "name": "ID pokynu", "id": 17 }
        },
        {
          "column22": { "value": 1149190193, "name": "ID pohybu", "id": 22 },
          "column0": { "value": 1341007200000, "name": "Datum", "id": 0 },
          "column1": { "value": 0.01, "name": "Objem", "id": 1 },
          "column14": { "value": "CZK ", "name": "Měna", "id": 14 },
          "column2": null,
          "column10": null,
          "column3": null,
          "column12": null,
          "column4": null,
          "column5": null,
          "column6": null,
          "column7": null,
          "column16": null,
          "column8": { "value": "Připsaný úrok", "name": "Typ", "id": 8 },
          "column9": null,
          "column18": null,
          "column25": null,
          "column26": null,
          "column17": { "value": 2107642322, "name": "ID pokynu", "id": 17 }
        }
      ]
    }
  }
}
```

# Výsledek dotazu na 3. výpis z roku 2012

```json
{
  "accountStatement": {
    "info": {
      "accountId": "2400222222",
      "bankId": "2010",
      "currency": "CZK",
      "iban": "CZ7920100000002400222222",
      "bic": "FIOBCZPPXXX",
      "op eningBalance": 185.03,
      "closingBalance": 185.05,
      "dateStart": 1343772000000,
      "dateEnd": 1346364000000,
      "yearList": 2012,
      "idList": 3,
      "idFrom": 1155172472,
      "idTo": 1155172472,
      "idLastDownload": null
    },
    "transactionList": {
      "transaction": [
        {
          "column22": { "value": 1155172472, "name": "ID pohybu", "id": 22 },
          "column0": { "value": 1346364000000, "name": "Datum", "id": 0 },
          "column1": { "value": 0.02, "name": "Objem", "id": 1 },
          "column14": { "value": "CZK", "name": "Měna", "id": 14 },
          "column2": null,
          "column10": null,
          "column3": null,
          "column12": null,
          "column4": null,
          "column5": null,
          "column6": null,
          "column7": null,
          "column16": null,
          "column8": { "value": "Připsaný úrok", "name": "Typ", "id": 8 },
          "column9": null,
          "column18": null,
          "column25": null,
          "column26": null,
          "column17": { "value": 2135081594, "name": "ID pokynu", "id": 17 }
        }
      ]
    }
  }
}
```

# Výsledek dotazu na pohyby od posledního stažení, zarážka ID 1150392361

```json
{
  "accountStatement": {
    "info": {
      "accountId": "2400222222",
      "bankId": "2010",
      "currency": "CZK",
      "iban": "CZ7920100000002400222222",
      "bic": "FIOBCZPPXXX",
      "op eningBalance": 185.05,
      "closingBalance": 185.01,
      "dateStart": 1342476000000,
      "dateEnd": 1348956000000,
      "yearList": null,
      "idList": null,
      "idFrom": null,
      "idTo": null,
      "idLastDownload": 1150392361
    },
    "transactionList": {
      "transaction": [
        {
          "column22": { "value": 1150808074, "name": "ID pohybu", "id": 22 },
          "column0": { "value": 1342476000000, "name": "Datum", "id": 0 },
          "column1": { "value": -15.0, "name": "Objem", "id": 1 },
          "column14": { "value": "CZK", "name": "Měna", "id ": 14 },
          "column2": { "value": "2600044444", "name": "Protiúčet", "id": 2 },
          "column 10": null,
          "column3": { "value": "2010", "name": "Kód banky", "id": 3 },
          "column12": {
            "value": "Fio banka, a.s.",
            "name": "Název banky",
            "id": 12
          },
          "column4": { "value": "0558", "name": "KS", "id": 4 },
          "column5": { "value": "0001", "name": "VS", "id": 5 },
          "column6": { "value": "0002", "name": "SS ", "id": 6 },
          "column7": {
            "value": " ",
            "name": "Uživatelská identifikace",
            "id": 7
          },
          "column16": null,
          "column8": {
            "value": "Platba převodem uvnitř banky",
            "name": "Typ",
            "id": 8
          },
          "column9": { "value": "Novák, Jan", "name": "Proved1", "id": 9 },
          "column18": null,
          "column25": { "value": "", "name": "Komentář", "id": 25 },
          "column26": null,
          "column17": { "value": 2115327276, "name": "ID pokynu", "id": 17 }
        },
        {
          "column22": { "value": 1152125621, "name": "ID pohybu", "id": 22 },
          "column0": { "value": 1343685600000, "name": "Datum", "id": 0 },
          "column1": { "value": 0.02, "name": "Objem", "id": 1 },
          "column14": { "value": "CZK", "name": "Měna", "id": 14 },
          "column2": null,
          "column10": null,
          "column3": null,
          "column12": null,
          "column4": null,
          "column5": null,
          "column6": null,
          "column7": null,
          "column16": null,
          "column8": { "value": "Připsaný úrok", "name": "Typ", "id": 8 },
          "column9": null,
          "column18": null,
          "column25": null,
          "column26": null,
          "column17": { "value": 2121115983, "name": "ID pokynu", "id": 17 }
        },
        {
          "column22": { "value": 1155172472, "name": "ID pohybu", "id": 22 },
          "column0": { "value": 1346364000000, "name": "Datum", "id": 0 },
          "column1": { "value": 0.02, "name": "Objem", "id": 1 },
          "column14": { "value": "CZK", "name": "Měna", "id": 14 },
          "column2": null,
          "column10": null,
          "column3": null,
          "column12": null,
          "column4": null,
          "column5": null,
          "column6": null,
          "column7": null,
          "column16": null,
          "column8": { "value": "Připsaný úrok", "name": "Typ", "id": 8 },
          "column9": null,
          "column18": null,
          "column25": null,
          "column26": null,
          "column17": { "value": 2135081594, "name": "ID pokynu", "id": 17 }
        },
        {
          "column22": { "value": 1158218819, "name": "ID pohybu", "id": 22 },
          "column0": { "value": 1348956000000, "name": "Datum", "id": 0 },
          "column1": { "value": 0.02, "name": "Objem", "id": 1 },
          "column14": { "value": "CZK", "name": "Měna", "id": 14 },
          "column2": null,
          "column10": null,
          "column3": null,
          "column12": null,
          "column4": null,
          "column5": null,
          "column6": null,
          "column7": null,
          "column16": null,
          "column8": { "value": "Připsaný úrok", "name": "Typ", "id": 8 },
          "column9": null,
          "column18": null,
          "column25": null,
          "column26": null,
          "column17": { "value": 2151261787, "name": "ID pokynu", "id": 17 }
        }
      ]
    }
  }
}
```

# Výsledek dotazu na pohyby od posledního stažení, zarážka datum 30.7.2012

```json
{
  "accountStatement": {
    "info": {
      "accountId": "2400222222",
      "bankId": "2010",
      "currency": "CZK",
      "iban": "CZ7920100000002400222222",
      "bic": "FIOBCZPPXXX",
      "op eningBalance": 185.05,
      "closingBalance": 185.03,
      "dateStart": 1343685600000,
      "dateEnd": 1348956000000,
      "yearList": null,
      "idList": null,
      "idFrom": 1152125621,
      "idTo": 1158218819,
      "idLastDownload": 1150808074
    },
    "transactionList": {
      "transaction": [
        {
          "column22": { "value": 1152125621, "name": "ID pohybu", "id": 22 },
          "column0": { "value": 1343685600000, "name": "Datum", "id": 0 },
          "column1": { "value": 0.02, "name": "Objem", "id": 1 },
          "column14": { "value": "CZK", "name": "Měna", "id": 14 },
          "column2": null,
          "column10": null,
          "column3": null,
          "column12": null,
          "column4": null,
          "column5": null,
          "column6": null,
          "column7": null,
          "column16": null,
          "column8": { "value": "Připsaný úrok", "name": "Typ", "id": 8 },
          "column9": null,
          "column18": null,
          "column25": null,
          "column26": null,
          "column17": { "value": 2121115983, "name": "ID pokynu", "id": 17 }
        },
        {
          "column22": { "value": 1155172472, "name": "ID pohybu", "id": 22 },
          "column0": { "value": 1346364000000, "name": "Datum", "id": 0 },
          "column1": { "value": 0.02, "name": "Objem", "id": 1 },
          "column14": { "value": "CZK ", "name": "Měna", "id": 14 },
          "column2": null,
          "column10": null,
          "column3": null,
          "column12": null,
          "column4": null,
          "column5": null,
          "column6": null,
          "column7": null,
          "column16": null,
          "column8": { "value": "Připsaný úrok", "name": "Typ", "id": 8 },
          "column9": null,
          "column18": null,
          "column25": null,
          "column26": null,
          "column17": { "value": 2135081594, "name": "ID pokynu", "id": 17 }
        },
        {
          "column22": { "value": 1158218819, "name": "ID pohybu", "id": 22 },
          "column0": { "value": 1348956000000, "name": "Datum", "id": 0 },
          "column1": { "value": 0.02, "name": "Objem", "id": 1 },
          "column14": { "value": "CZK", "name": "Měna", "id": 14 },
          "column2": null,
          "column10": null,
          "column3": null,
          "column12": null,
          "column4": null,
          "column5": null,
          "column6": null,
          "column7": null,
          "column16": null,
          "column8": { "value": "Připsaný úrok", "name": "Typ", "id": 8 },
          "column9": null,
          "column18": null,
          "column25": null,
          "column26": null,
          "column17": { "value": 2151261787, "name": "ID pokynu", "id": 17 }
        }
      ]
    }
  }
}
```

# 5.3.1.7 STA (MT940)

Formát výpisů z účtu je založen na mezinárodním SWIFT formátu MT940. Systém generuje vždy příponu **STA.** MT940 je pouze pro výpisy a nelze jej použít pro výpis pohybů na účtu.

Jeden logický výpis z účtu může mít jednu nebo více stránek (listů). Každá stránka výpisu z účtu se skládáze záhlaví, textového bloku a ukončovacích znaků.

Struktura výpisů obsažených v souboru vypadá tak, že každý výpis je tvořen bloky, které jsou rozpoznatelnépomocí složených závorek {1:} {2:} atd. Hlavní tělo výpisu se nachází v poli {4:}

Maximální délka zprávy je 2000 znaků. Znaková sada: UTF-8

> Pole uvozená a ukončená `:` jsou oddělena pomocí `<CR><LF>`

> Pole `:86:` je maximálně dlouhé 65x. Pokud je pole větší, jsou hodnoty odděleny `<CR><LF>`

# Blok 1

Struktura: `{1:F01aaaaaaaaAbbbccccdddddd}`

| Pole         | Popis                                                                        |
| ------------ | ---------------------------------------------------------------------------- |
| {1:          | Začátek bloku 1                                                              |
| F01          | Zpráva - vždy hodnota: F01                                                   |
| aaaaaaaaAbbb | BIC Fio Banky, kde:<br>aaaaaaaa: BIC8<br>Logical terminal: A<br>Pobočka: XXX |
| CCCC         | Stav (session number) - vždy hodnota: 0000                                   |
| dddddd       | Číslo transakce - vždy hodnota: 0000                                         |
| }            | Konec bloku 1                                                                |

Příklad: Blok 1 z Fio banka ČR

```txt
1:F01FIOBCZPPAXXX0000000000
```

**Blok 2**

Struktura: `{2:1940aaaaaaaaAbbbcdeee}`

| Pole         | Popis                                                                        |
| ------------ | ---------------------------------------------------------------------------- |
| {2:          | Začátek bloku 2                                                              |
| 1940         | Vstup;Typ zprávy -vždy hodnota: 1940                                         |
| aaaaaaaaAbbb | BIC Fio Banky, kde:<br>aaaaaaaa: BIC8<br>Logical terminal: A<br>Pobočka: XXX |
| C            | Priorita - vždy hodnota: N                                                   |
| d            | Monitorování - vždy hodnota: mezera                                          |
| eee          | Zastarávání - vždy hodnota: 020                                              |
| }            | Konec bloku 2                                                                |

Příklad: Blok 1 z Fio banka ČR

```txt
2:1940FIOZSKBAAXXXN 020
```

**Blok 4**

Blok 4 bude vždy začínat {4**:**

| Pole  | Status | Sub pole | Formát                             | Formát                             | Popis                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | Příklad                           |
| ----- | ------ | -------- | ---------------------------------- | ---------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------- |
| :20:  | M      |          | 16x                                | 16x                                | referenční číslo výpisů<br>YYMMDDHHMMSS-<br>ČísloStránkyVýpisu                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | :20:120812095511-1                |
| :25:  | M      |          | 35x                                | 35x                                | číslo účtu ve formátu IBAN                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | :25:<br>CZ78201000000000 01234562 |
| :28C: | M      |          | 5n[/5n]                            | 5n[/5n]                            | číslo výpisu/číslo stránky                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | :28C:00124/00003                  |
| :60a: | M      |          | 1!a6!n3!a15d                       | 1!a6!n3!a15d                       | Počáteční stav účtu                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | :60F:C120611CZK53                 |
|       |        |          |                                    |                                    | $60a=typsalda:$F= počáteční saldo<br>$M\text {mezisouet}$1!a označení druhu transakce:<br>$C=kreditni$ $D=debetni$ $6!n=uetniden(YYMMDD)$ $3!a=kodmenydleISO4217$15d = částka s desetinným<br>$oddelovaem$                                                                                                                                                                                                                                                                                                                         | 6,72                              |
| :61:  | O      |          | 6!n[4!n]2a[1!a]15d1!a3!c16x[//16x] | 6!n[4!n]2a[1!a]15d1!a3!c16x[//16x] | $Strukturovaneudajeopohybu$6!n = datum splatnosti<br>$4!datuzautova$ $2a=typzautovani$ $C=kredit,$ $D=debet,$ $RC=stornokredit,$ $RD=stornodebet$ $3!a=k$ měny dle l $ISO4217$ $15d=\text {}\text {stka}$ $1!a=Typtransakce$ $S=SWIFTtransfer$ $N=non-SWIFT$transfer<br>$3!c=Oznaenitransakce$ $103=swiftovaklientskaplatba$ $DDT=inkaso$ $\text {CHG=poplatek}$ $INT=uroky$ $\text {MSC=ostatni}$ $\text {TRF=prevod}$16x reference klienta (pokud není<br>uvede se NONREF)<br>[//16x] jedinečný identifikátor banky<br>(pohybID) |                                   |
| :86:  | M      |          |                                    | 3!n                                | vždy hodnota 010                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |                                   |
| :86:  | O      | ?00      | ?00                                | 27x                                | slovní popis transakce (viz. Tabulka<br>transakcí)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |                                   |
| :86:  | O      | ?20      | ?20                                | 27x                                | číslo účtu plátce(příjemce)/kód banky                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |                                   |
| :86:  | O      | ?21      | ?21                                | $[\text {VS27x}]$                  | variabilní číslo (VS)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |                                   |
| :86:  | O      | ?22      | ?22                                | $[SS27x]$                          | specifické číslo (SS)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |                                   |
| :86:  | O      | ?23      | ?23                                | $[KS27x]$                          | konstatní symbol (KS)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |                                   |
| :86:  | O      | ?24      | ?24                                | 27x                                | vaše označení                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |                                   |
| :86:  | O      | ?25      | ?25                                | 27x                                | vaše označení                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |                                   |
| :86:  | O      | ?26      | ?26                                | 27x                                | vaše označení                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |                                   |
| :86:  | O      | ?27      | ?27                                | 27x                                | vaše označení                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |                                   |
| :86:  | O      | ?28      | ?28                                | 27x                                | zpráva pro příjemce                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |                                   |
| :86:  | O      | ?29      | ?29                                | 27x                                | zpráva pro příjemce                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |                                   |
| :86:  | M      |          |                                    | 3!n                                | vždy hodnota 020                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |                                   |
| :86:  | O      | ?00      | ?00                                | 27x                                | slovní popis transakce (viz. Tabulka<br>transakcí)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |                                   |
| :86:  | O      | ?20      | ?20                                | 27x                                | identifikace bankovního účtu (př.<br>IBAN, číslo účtu, ABA)                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |                                   |
| :86:  | O      | ?21      | ?21                                | 27x                                | kód banky (BIC, identifikace banky)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |                                   |
| :86:  | O      | ?22      | ?22                                | 27x                                | preváděná měna a částka                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | CZK1234567890,00                  |
| :86:  | O      | ?23      | ?23                                | 27x                                | směnný kurz                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |                                   |
| :86:  | O      | ?24      | ?24                                | 27x                                | vaše označení                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |                                   |
| :86:  | O      | ?25      | ?25                                | 27x                                | vaše označení                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |                                   |
|       | O      | ?26      | ?26                                | 27x                                | vaše označení                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |                                   |
|       | O      | ?27      | ?27                                | 27x                                | vaše označení                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |                                   |
|       | O      | ?28      | ?28                                | 27x                                | zpráva pro příjemce                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |                                   |
|       | O      | ?29      | ?29                                | 27x                                | zpráva pro příjemce                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |                                   |
|       | O      | ?32      | ?32                                | 27x                                | název příjemce/plátce                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |                                   |
|       | O      | ?33      | ?33                                | 27x                                | název příjemce/plátce                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |                                   |
|       | M      |          |                                    | 3!n                                | hodnota 030 vyjadřuje ostatní platby                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |                                   |
|       | O      | ?00      | ?00                                | 27x                                | slovní popis transakce (viz. Tabulka                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |                                   |
|       | O      | ?00      | ?00                                | 27x                                | transakcí)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |                                   |
|       | O      | ?20      | ?20                                | 27x                                | variabilní číslo (VS)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | VS0000000000                      |
|       | O      | ?21      | ?21                                | 27x                                | specifické číslo (SS)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | SS0000000000                      |
|       | O      | ?22      | ?22                                | 27x                                | konstatní symbol (KS)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | KS0000                            |
|       | O      | ?23      | ?23                                | 27x                                | vaše označení                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |                                   |
|       | O      | ?24      | ?24                                | 27x                                | vaše označení                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |                                   |
|       | O      | ?25      | ?25                                | 27x                                | vaše označení                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |                                   |
|       | O      | ?26      | ?26                                | 27x                                | vaše označení                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |                                   |
|       | O      | ?27      | ?27                                | 27x                                | zpráva pro příjemce                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |                                   |
|       | O      | ?28      | ?28                                | 27x                                | zpráva pro příjemce                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |                                   |
|       | O      | ?29      | ?29                                | 27x                                | zpráva pro příjemce                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |                                   |
|       |        |          |                                    | 1!a6!n3!a15                        | počáteční stav účtu<br>kde a = typ salda:<br>F - počáteční saldo<br>M - mezisoučet                                                                                                                                                                                                                                                                                                                                                                                                                                                 |                                   |
| :62a: | M      |          |                                    | d                                  | další subpole (viz. ciselnik60a)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |                                   |

```txt
{1:F01FIOBCZPPAXXX0000000000}{2:I940FIOBCZPPAXXXN 020}{4:
:20:121003163157-1
:25:CZ7920100000002400222222
:28C:00121/00001
:60F:C120101CZK106,17
:61:1201020102CCZK49981,25NTRFFREMIS A.S.//1144273065
:86:010?00TP_PRIJEM?20168851386/0600?21VS110456?23KS0008?24FREMIS A.S.
:61:1201020102DCZK-3000,00NTRFPřevod do GE MB//1134290899
:86:010?00TP_PLATBA?20196704703/0600?23KS0558?24Převod do GE MB?28Převod do GE MB
:61:1201020102CCZK2454,48NMSCNONREF//1144307477
:86:010?00TP_PREVOD_UVNITR?202100131680/2010?23KS0558?28ARCO feed převod ze SÚ na B?29Ú
:61:1201020102DCZK-5723,97NTRFNONREF//1144307518
:86:010?00TP_PLATBA?20000000-0017145783/0300?21VS0000729776?23KS0308
:61:1201020102DCZK-12200,00NTRFNONREF//1144307519
:86:010?00TP_PLATBA?20000019-1249450247/0100?21VS0000331641?23KS0308
:61:1201020102CCZK11000,00NMSCNONREF//1144307593
:86:010?00TP_PREVOD_UVNITR?202100131680/2010?23KS0558?28ARCO deed převod ze SÚ na B?29Ú
:61:1201020102DCZK-10943,52NMSCNákup EUR//1144307632
:86:010?00TP_PREVOD_UVNITR?202600131679/2010?23KS0558?24Nákup EUR?28Nákup EUR
:61:1201030103CCZK19800,00NTRFZEMĚDĚLSKÁ SPOLEČN//1144359806
:86:010?00TP_PRIJEM?20174385908/0600?21VS110465?23KS0308?24ZEMĚDĚLSKÁ SPOLEČN
:61:1201030103CCZK30000,00NTRF123456789//1144367297
:86:010?00TP_PRIJEM?205855970267/0100?21VS110446?22SS0?23KS0008?24PALOMO, A.S.
:61:1201030103CCZK3674,00NTRFAGRO//1144376794
:86:010?00TP_PRIJEM?201163555339/0800?21VS110431?23KS0308?24AGRO Chomutice
:62M:C120131CZK55148,41-}${1:F01FIOBCZPPAXXX0000000000}{2:I940FIOBCZPPAXXXN 020}{4:
:20:121003163157-8
:25:CZ7920100000002400222222
:28C:00121/00002
:60M:C120131CZK55148,41
:61:1201040104CCZK60000,00NTRFVÝROBNĚ-OBCHODNÍ D//1144429094
:86:010?00TP_PRIJEM?20754307674/0600?21VS110466?23KS0008?24VÝROBNĚ-OBCHODNÍ D
:61:1201040104CCZK58296,00NTRFZOD POTĚHY//1144432377
:86:010?00TP_PRIJEM?20512161/0100?21VS110458?22SS0?23KS0008?24ZODPOTĚHY
:62F:C120131CZK173444,41-}
```

**Popis transakčních kódů**

| Transakce kód           | Význam                                     |
| ----------------------- | ------------------------------------------ |
| TPPREVODUVNITR          | Převod uvnitr Fio                          |
| TPVKLAD                 | Vklad v hotovosti                          |
| TPVYBER                 | Výběr v hotovosti                          |
| TPBLOKACE               | Blokace                                    |
| TPUROK                  | Úrok                                       |
| TPUROKDAN               | Daň z úroku                                |
| TPEVIDUROK              | Evidovaný úrok                             |
| TPEVIDPOPLATEK          | Evidovaný poplatek                         |
| TPPLATBA                | Platba ven z modulu                        |
| TPPRIJEM                | Příjem zvenčí modulu                       |
| TPPOPLATEK              | Poplatek                                   |
| TPPLATBAKARTOU          | Platba kartou                              |
| TPPLATBAPOTVRZENI       | Potvrzeni platby ven z modulu              |
| TPUROKKK                | Úrok z úvěru                               |
| TPUROKSANKCNI           | Sankční poplatek                           |
| TPPREVODKONTO           | Převod v rámci jednoho konta               |
| TPUROKRUCNI             | Úrok (opravný pohyb)                       |
| TPUROKDANRUCNI          | Daň z úroku (opravný pohyb)                |
| TPEVIDUROKRUCNI         | Evidovaný úrok (opravný pohyb)             |
| TPPOPLATEKRUCNI         | Poplatek (opravný pohyb)                   |
| TPEVIDPOPLATEKRUCNI     | Evidovaný poplatek (opravný pohyb)         |
| TPBANKABANKAPLATBA      | Platba z bankovního konta (na jiné konto)  |
| TPBANKABANKAPRIJEM      | Příjem na bankovní konto (z jiného konta)  |
| TPBANKAVLASTNIPLATBA    | Platba z bankovního konta (vlastní platba) |
| TPBANKAVLASTNIPRIJEM    | Příjem na bankovní konto (vlastní příjem)  |
| TPPOKLADNAVLASTNIPLATBA | Platba z pokladny (vlastní platba)         |
| TPPOKLADNAVLASTNIPRIJEM | Příjem do pokladny (vlastní příjem)        |
| TPOPRAVNYPOHYB          | Opravný pohyb                              |
| TPPLACPOPPRIJEM         | Přijatý poplatek                           |
| TPPLATBACM              | Platba cizoměnová či zahraniční            |
| TPKARTAPOPLATEK         | Poplatek za používání platební karty       |
| TPINKASO                | Inkaso z účtu                              |
| TPAVIZOPLATBAKARTOU     | Avizovaná platba kartou                    |
| TPINKASOFIO             | Inkaso z účtu v rámci FIO                  |
| TPINKASOPRIJEM          | Příjem inkasa z cizí banky                 |
| TPAVIZOPLATBAKARTOU     | Avizovaná platba kartou                    |

www.fio.cz

Verze 16. 10. 2025

## 5.3.1.8 SBA XML (camt.053)

Jedná se o jednotný slovenský národní formát XML výpisu vycházející z ISO 20022 CAMT.053.001.02.

## 5.3.1.9 ČBA XML (camt.053)

Jedná se o český národní formát výpisu vycházející z ISO 20022 CAMT.053.001.02, určený pro výpisy z účtu.

# Oddělovače VS, KS, SS

Od 6. 4. 2020 dochází ke změnám v oddělování variabilního, specifického a konstantního symbolu platby.

Stávající oddělování pomocí lomítka - zaniká: `/VS/1234567890/SS/1234567890/KS/1234`

Nový způsob oddělování je pomocí dvojtečky: `VS:1234567890SS:1234567890KS:1234`

# 5.3.2 Transakce z POS terminálů nebo platební brány obchodníka

Klienti s podnikatelským účtem využívající Platební terminály nebo e-shopy s platební bránou si mohou získávat informace o karetních transakcích. API nabízí data o karetních transakcích ve dvou formátech XML a CSV.

## 5.3.2.1 XML

XML se skládá ze dvou částí - Info a TransactionList. Schéma odpovědi v XML uvedena na adrese https://www.fio.cz/xsd/IBSchema.xsd

Info poskytuje informace o účtu a vybraném období.

V části TransactionList jsou zobrazeny karetní transakce a transakce přes platební bránu za dané období. Znaková sada: UTF-8

**Struktura XML Info:**

| Element   | Sta V | Formát         | Popis                                                     | Příklad                   |
| --------- | ----- | -------------- | --------------------------------------------------------- | ------------------------- |
| accountld | M     | 16n            | číslo účtu                                                | 1234562                   |
| bankld    | M     | 4!n            | bankovní identifikační kód ve formátu BBAN                | 2010                      |
| currency  | M     | 3!x            | měna účtu dle standardu ISO 4217                          | CZK                       |
| iban      | M     | 34x            | mezinárodní číslo bankovního účtu dle standardu ISO 13616 | CZ78201000000000 01234562 |
| bic       | M     | 11x            | bankovní identifikační kód dle standardu ISO 9362         | FIOBCZPPXXX               |
| dateStart | O     | rrrr-mm-dd+GMT | počátek zvoleného období                                  | 2012-07-27+02:00          |
| dateEnd   | O     | rrrr-mm-dd+GMT | konec zvoleného období                                    | 2012-01-15+01:00          |

**Struktura TransactionList:**

| Atribut             | Sta V | Formát         | Popis                                                                                    | Příklad                                                     |
| ------------------- | ----- | -------------- | ---------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| operationld         | M     | 12n            | jedinečné číslo pohybu karetnítransakce                                                  | 8216165940                                                  |
| orderld             | M     | 12n            | jedinečné číslo příkazu karetnítransakce                                                 | 9277937165                                                  |
| date                | M     | rrrr-mm-dd+GMT | datum provedení ve tvaru rok-měsíc-den                                                   | 2012-07-27+02:00                                            |
| amount              | M     | 18d            | suma transakcí v hromadné dávce                                                          | 4700.0000                                                   |
| note                | O     | 50e            | poznámka - upřesňující informace o transakci                                             | Zaúčtování POS<br>terminálů<br>MasterCard,<br>Operace ON-US |
| branchName          | O     | 50e            | identifikace pobočky                                                                     | Provozovna Ječná                                            |
| transactionld       | O     | 12n            | jedinečné identifikační číslo transakce                                                  | 28                                                          |
| deviceld            | O     | 20e            | číslo zařízení - identifikace platebního terminálu/brány                                 | 002030999999 1                                              |
| transactionDateTime | O     | rrrr-mm-dd+GMT | datum transakce ve tvaru rok měsíc den                                                   | 2012-07-27+02:00                                            |
| autorizationNumber  | O     | 10x            | jedinečné autorizační číslo transakce                                                    | 997476                                                      |
| cardNumber          | O     | 50e            | číslo karty ve zkráceném tvaru                                                           | 553553**\*\***5553                                          |
| transactionAmount   | O     | 18d            | objem dané transakce                                                                     | 200.0000                                                    |
| transactionCurrency | O     | 3!x            | měna transakce dle standardu ISO 4217                                                    | CZK                                                         |
| type                | O     | 12e            | typ transakce, ONUS - kartou Fio / DOMESTIC - českou kartou / FOREIGN - zahraničníkartou | ONUS                                                        |
| cardlssuer          | O     | 12x            | vystavitel karty                                                                         | MASTERCARD                                                  |
| totalFees           | O     | 18d            | celkové poplatek spojený s transakcí                                                     | 20.0000                                                     |
| fioFee              | O     | 18d            | poplatek Fio spojený s transakcí                                                         | 5.0000                                                      |
| interchangeFee      | O     | 18d            | mezibankovní poplatek spojený s transakcí                                                | 5.0000                                                      |
| cardAsosiationFee   | O     | 18d            | poplatek karetní asociace spojený s transakcí                                            | 10.000                                                      |
| flexibleCommission  | O     | 18d            | Poplatek vydavatele karty spojený s transakcí                                            | 5.0000                                                      |
| settlement          | O     | 5x             | zaúčtování pohybu true/false                                                             | true                                                        |
| settlementDate      | O     | rrrr-mm-dd+GMT | datum zaúčtování ve tvaru rok měsíc den                                                  | 2012-07-27+02:00                                            |
| VS                  | O     | 20n            | Variabilní symbol, unikátní označení transakce zadané během POS/ecomm transakce          | 12345678911234567<br>891                                    |

# Výsledek dotazu na karetní transakce v období od 1. 7. 2012 do 31. 7. 2012

```xml
<MerchantStatement>
    <Info>
        <accountId>2111111111</accountId>
        <bankId>2010</bankId>
        <currency>CZK</currency>
        <iban>CZ7920100000002111111111</iban>
        <bic>FIOBCZPPXXX</bic>
        <dateStart>2012-07-01</dateStart>
        <dateEnd>2012-07-31</dateEnd>
    </Info>
    <TransactionList>
        <Transaction>
            <operationId>9277937165</operationId>
            <orderId>8216165940</orderId>
            <date>2012-07-19+02:00</date>
            <amount>4700.0000</amount>
            <note>Zaúčtování POS terminálu MasterCard, Operace ON-US</note>
            <branchName>Pobocka 1</branchName>
            <transactionId>28</transactionId>
            <deviceId>002030999999 1</deviceId>
            <transactionDateTime>2012-07-16T11:28:12+02:00</transactionDateTime>
            <autorizationNumber>997476</autorizationNumber>
            <cardNumber>553937**\*\***9052</cardNumber>
            <transactionAmount>200.0000</transactionAmount>
            <transactionCurrency>CZK</transactionCurrency>
            <type>ONUS</type>
            <cardIssuer>MASTERCARD</cardIssuer>
            <totalFees>0.0000</totalFees>
            <fioFee>1.3</fioFee>
            <interchangeFee>0.0000</interchangeFee>
            <cardAsosiationFee>0.25</cardAsosiationFee>
            <flexibleCommission>1.84</flexibleCommission>
            <settlement>true</settlement>
            <settlementDate>2012-07-19+02:00</settlementDate>
        </Transaction>
    </TransactionList>
</MerchantStatement>
```

## 5.3.2.2 CSV

CSV je textový formát tabulkového souboru, kde jsou jednotlivé sloupce tabulky odděleny středníky. Jednotlivé řádky tabulky jsou oddělené řádkováním. Jednotlivá pole mohou být ještě zabalená do uvozovek, pokud se v nich vyskytuje středník. Každé vložené uvozovky uvnitř pole budou reprezentovány párem uvozovek.

Znaková sada: UTF-8

**Struktura hlavičky**

| Atribut   | Stav | Formát     | Popis                                                     | Příklad                  |
| --------- | ---- | ---------- | --------------------------------------------------------- | ------------------------ |
| accountld | M    | 16n        | číslo účtu                                                | 1234562                  |
| bankld    | M    | 4!n        | bankovní identifikační kód ve formátu BBAN                | 2010                     |
| currency  | M    | 3!x        | měna účtu dle standardu ISO 4217                          | CZK                      |
| iban      | M    | 24x        | mezinárodní číslo bankovního účtu dle standardu ISO 13616 | CZ7820100000000001234562 |
| bic       | M    | 11x        | bankovní identifikační kkód dle standardu ISO 9362        | FIOBCZPPXXX              |
| dateStart | O    | dd.mm.rrrr | počátek zvoleného období ve tvaru den.měsíc.rok           | 28.02.2012               |
| dateEnd   | O    | dd.mm.rrrr | konec zvoleného období ve tvaru den.měsíc.rok             | 01.03.2012               |

**Struktura pohybu**

| Atribut                      | Stav | Formát     | Popis                                                                                         | Příklad                                                  |
| ---------------------------- | ---- | ---------- | --------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| ID pohybu                    | M    | 12n        | jedinečné číslo pohybu karetní<br>transakce                                                   | 1158152824                                               |
| ID Pokynu                    | O    | 12n        | jedinečné číslo příkazu karetní<br>transakce                                                  | 2102382863                                               |
| Poznámka                     | O    | 50e        | poznámka - upřesňující informace o<br>transakci                                               | Zaúčtování POS<br>terminálů MasterCard,<br>Operace ON-US |
| Název pobočky                | O    | 50e        | identifikace pobočky                                                                          | Provozovna Ječná                                         |
| Identifikátor<br>transakce   | O    | 12n        | jedinečné identifikační číslo transakce                                                       | 28                                                       |
| Číslo zařízení               | O    | 20e        | identifikace platebního terminálu/brány                                                       | 002030999999 1                                           |
| Datum transakce              | O    | dd-mm-rrrr | datum transakce ve tvaru den měsíc<br>rok                                                     | 19.07.2012                                               |
| Autorizační číslo            | O    | 10n        | jedinečné autorizační číslo transakce                                                         | 997476                                                   |
| Číslo karty                  | O    | 50e        | číslo karty ve zkráceném tvaru                                                                | 553553**\*\***5553                                       |
| Typ                          | O    | 12e        | typ transakce, ONUS - kartou Fio /<br>DOMESTIC - českou kartou /<br>FOREIGN-zahraniční kartou | ONUS                                                     |
| Vystavitel karty             | O    | 12x        | karetní značka                                                                                | MASTERCARD                                               |
| Poplatky celkem              | O    | 18D        | celkové poplatek spojený s transakcí                                                          | 20,00                                                    |
| Poplatek Fio                 | O    | 18D        | poplatek Fio spojený s transakcí                                                              | 5,00                                                     |
| Poplatek<br>intercharge      | O    | 18D        | mezibankovní poplatek spojený s<br>transakcí                                                  | 5,00                                                     |
| Poplatek karetní<br>asociace | O    | 18D        | poplatek karetní asociace spojený s<br>transakcí                                              | 5,00                                                     |
| Poplatek<br>vydavatele karty | O    | 18D        | Poplatek vydavatele karty spojený s<br>transakcí                                              | 5,00                                                     |
| Zaúčtováno                   | O    | 5x         | zaúčtování pohybu true/false                                                                  | true                                                     |
| Datum zaúčtování             | O    | dd-mm-rrrr | datum transakce ve tvaru den měsíc<br>rok                                                     | 19.07.2012                                               |
| VS                           | O    | 20n        | Variabilní symbol, unikátní označení<br>transakce zadané během POS/ecommtransakce             | 12345678911234567891                                     |

# Výsledek dotazu na karetní transakce v období od 1. 7.2012 do 31.7.2012

```txt
accountId;2111111111
bankId;2010
currency;CZK
iban;CZ7920100000002111111111
bic;FIOBCZPPXXX
dateStart;01.07.2012
dateEnd;31.07.2012
ID pohybu;ID pokynu;Datum;Objem;Poznámka;Název pobočky;Identifikátor transakce;Číslo zařízení;Datum transakce;Autorizační číslo;Číslo karty;Objem;Měna;Typ;Vystavitel karty;Poplatky celkem;Poplatek Fio;Poplatek intercharge;Poplatek karetní asociace;Poplatek vydavatele karty;Zaúčtováno;Datum zaúčtování
8216165940;9277937165;19.07.2015;4700,00;Zaúčtování POS terminálů MasterCard, Operace ON-US;Pobocka 1;28;00203O999999 1;16.07.2012 11:28:12;997476;553937******9052;200,00;CZK;ON_US;MASTERCARD;0,00;1,3;0,00;0,25;1,84;true;19.07.2012
```

# 6 IMPORT (UPLOAD) PLATEBNÍCH PŘÍKAZU DO BANK

Platební příkazy jsou importovány skrze adresu <https://fioapi.fio.cz/v1/rest/import/>

Po úspěšném uploadu dat se příkazy sdruží v bankovním systému do dávky, která musí být dodatečněautorizována (sms, fio podpis) oprávněnou osobou na účtu. Bez dodatečné autorizace nebudou příkazy zpracovány.

## 6.1 Parametry pro upload dat

| Parametr | Stav | Hodnoty                                | Popis                                       |
| -------- | ---- | -------------------------------------- | ------------------------------------------- |
| token    | M    |                                        | 64 znakový unikátní řetězec                 |
| type     | M    | abo<br>xml<br>pain001xml<br>pain008xml | Formát importu                              |
| file     | M    |                                        | Soubor s daty                               |
| Ing      | O    | CS<br>sk<br>en                         | Zvolení jazyka popisků v odpovědích serveru |

Soubor s příkazy se posílají s kódováním **multipart/form-data** (data jsou oddělena hraniční čarou $"boundary"$ . Data jsou identifikována jménem "file" s elementem puvodního názvu souboru "filename" v hlavičce content-disposition: form-data.

Nejjednodušší je použití již hotových knihoven na posílání dat, např. knihovny cURL

# Příklad použití cURL

Knihovnu cURL je možné stáhnout z jejich webových stránek.

Jestliže operační systém nezná certifikační autoritu, tak je nutné stáhnout certifikát (Root 5 - GeoTrust Primary Certification Authority - G3) a umístit ho do adresáre s curl.exe nebo na úložiště certifikátů a potépoužít příkaz.

Je dále nutné, aby na počítači byl naistalován Open SSL.

# Windows a Linux:

```bash
curl -S -s \
    --cacert GeoTrust_Primary_CA.pem -X POST \
    -F "type=xml" \
    -F "token=aGEMQB9Idh35fxxxxxxxxxxxxxQwyGlQ" \
    -F "file=@C:\davka.xml" \
    https://fioapi.fio.cz/v1/rest/import/ > result.xml 2>errorlog.txt
```

# Odpověď na dávku příkazu je vždy ve formátu XML

| Element       | Hodnota | Popis                                                                                                                   |
| ------------- | ------- | ----------------------------------------------------------------------------------------------------------------------- |
| errorCode     | 0       | ok-príkaz byl přijat                                                                                                    |
| errorCode     | 1       | nalezené chyby při kontrole příkazů                                                                                     |
| errorCode     | 2       | varování kontrol - chybně vyplněné hodnoty                                                                              |
| errorCode     | 11      | syntaktická chyba                                                                                                       |
| errorCode     | 12      | prázdný import - v souboru nejsou žádné příkazy                                                                         |
| errorCode     | 13      | příliš dlouhý soubor - soubor je delší než 2 MB                                                                         |
| errorCode     | 14      | prázdný soubor - soubor neobsahuje příkazy                                                                              |
| idInstruction |         | číslo dávky - jednoznačný identifikátor dávky                                                                           |
| status        | ok      | příkaz přijat                                                                                                           |
| status        | error   | hrubá chyba v příkazu, dávka se všemi příkazy nebude přijata                                                            |
| status        | warning | varování, některý z údajů nesouhlasí (např. měna platby a měna<br>účtu), příkazy s odpovědí warning byly prijaty bankou |

|           | fatal | chyba na straně bankovního systému banky, všechny pokyny se<br>odmitly |
| --------- | ----- | ---------------------------------------------------------------------- |
| sumDebet  | 18d   | suma debetních položek v dávce                                         |
| sumCredit | 18d   | suma kreditních položek v dávce                                        |

Schéma XML odpovědi je uvedena na adrese https://www.fio.cz/schema/responselmportlB.xsd

# 6.2 ABO

Import příkazů ve formátu ABO v měně CZK je určen pouze pro banky v České republice. **Ostatní** **měny** **jsou přípustné pouze v rámci Fio banky (kód banky 2010).** Měna příkazů se určuje podle účtu odesílatele. Příkazy do slovenských bank v EUR nejsou tímto způsobem již možné. Struktura ABO souboru je uvedena na adrese https://www.fio.cz/docs/cz/struktura-abo.pdf

# 6.3 Fio XML

Je-li v rámci jednoho xml souboru podáno více typů pokynů, musí být pokyny v tomto pořadí: tuzemsképlatby, europlatby, zahraniční platby. V případě nedodržení tohoto pořadí bude soubor odmítnut. XSD pro všechny typy je dostupné zde: https://www.fio.cz/schema/importlB.xsd.

## 6.3.1 XML příkaz platba v rámci ČR

Tento pokyn je možné použít i k převodu cízích měn mezi účty v rámci Fio banky.

| Element             | Stav | Formát     | Popis                                                                                                          | Příklad                                        |
| ------------------- | ---- | ---------- | -------------------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| accountFrom         | M    | 16n        | číslo účtu příkazce                                                                                            | 1234562                                        |
| currency            | M    | 3!x        | měna účtu dle standardu ISO<br>4217                                                                            | CZK                                            |
| amount              | M    | 18d        | částka příkazu                                                                                                 | 100.00                                         |
| accountTo           | M    | 6n-10n     | číslo učtu<br>príjemce/inkasovaného                                                                            | 2212-2000000699                                |
| bankCode            | M    | 4!n        | banka přijemce/inkasovaného                                                                                    | 0300                                           |
| ks                  | O    | 4n         | konstantní symbol                                                                                              | 0558                                           |
| VS                  | O    | 10n        | variabilní symbol                                                                                              | 1234567890                                     |
| SS                  | O    | 10n        | specifický symbol                                                                                              | 1234567890                                     |
| date                | M    | RRRR-MM-DD | datum                                                                                                          | 2013-04-25                                     |
| messageForRecipient | O    | 140i       | zpráva pro příjemce                                                                                            | Libovolný text, kterýse zobrazí příjemciplatby |
| comment             | O    | 255i       | Vaše označení                                                                                                  | Hračky pro děti<br>v PENNY MARKET              |
| paymentReason       | O    | 3!n        | platební titul -viz 6.3.4 Platebnítitul                                                                        | 110                                            |
| paymentType         | O    | 6!n        | přípustné hodnoty typu platby<br>jsou:<br>431001 -standardní<br>431005 - prioritní<br>431022 - příkaz k inkasu | 431001                                         |

# Příklad platby v rámci ČR

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Import xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://www.fio.cz/schema/importIB.xsd">
    <Orders>
        <DomesticTransaction>
            <accountFrom>1234562</accountFrom>
            <currency>CZK</currency>
            <amount>100.00</amount>
            <accountTo>2212-2000000699</accountTo>
            <bankCode>0300</bankCode>
            <ks>0558</ks>
            <vs>1234567890</vs>
            <ss>1234567890</ss>
            <date>2013-04-25</date>
            <messageForRecipient>Hračky pro děti v PENNY MARKET</messageForRecipient>
            <comment></comment>
            <paymentType>431001</paymentType>
        </DomesticTransaction>
    </Orders>
</Import>
```

## 6.3.2 XML příkaz Europlatba

| Element         | Stav | Formát     | Popis                                                                                                                                                     | Příklad               |
| --------------- | ---- | ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- |
| accountFrom     | M    | 16n        | číslo účtu příkazce                                                                                                                                       | 1234562               |
| currency        | M    | 3!x        | měna účtu dle standardu ISO<br>4217                                                                                                                       | EUR                   |
| amount          | M    | 18d        | částka příkazu                                                                                                                                            | 100.00                |
| accountTo       | M    | 34x        | mezinárodní číslo bankovního<br>účtu příjemce/inkasovaného dle standardu ISO 13616                                                                        | AT6119043002345 73201 |
| ks              | O    | 4n         | konstantní symbol                                                                                                                                         | 0558                  |
| VS              | O    | 10n        | variabilní symbol                                                                                                                                         | 1234567890            |
| SS              | O    | 10n        | specifický symbol                                                                                                                                         | 1234567890            |
| bic             | O    | 11!x       | bankovní identifikační kód dle<br>standardu ISO 9362                                                                                                      | ABAGATWWXXX           |
| date            | M    | RRRR-MM-DD | datum                                                                                                                                                     | 2013-04-25            |
| comment         | O    | 140e       | Vaše označení                                                                                                                                             | Erste Zahlung         |
| benefName       | M    | 35e        | majitel účtu                                                                                                                                              | Hans Gruber           |
| benefStreet     | O    | 35x        | bydliště majitele účtu-ulice                                                                                                                              | Gugitzgasse 2         |
| benefCity       | O    | 35x        | bydliště majitele účtu-město                                                                                                                              | Wien                  |
| benefCountry    | O    | 3x         | země majitele účtu - viz. 12.2.1                                                                                                                          | AT                    |
| remittancelnfo1 | O    | 35x        | informace pro prijemce                                                                                                                                    |                       |
| remittancelnfo2 | O    | 35x        | informace pro prijemce                                                                                                                                    |                       |
| remittancelnfo3 | O    | 35x        | informace pro prijemce                                                                                                                                    |                       |
| paymentReason   | C    | 3!n        | platební titul -povinný jen u<br>účtů vedených Fio bankou<br>pobočce zahraniční banky v SR pouze při platbě nad 50 000<br>EUR<br>viz 6.3.4 Platební titul | 110                   |
| paymentType     | O    | 6!n        | Přípustné typy plateb jsou:<br>431008- standardní<br>431009 - prioritní<br>431018 - okamžitá                                                              | 431008                |

# Příklad Europlatba

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Import xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://www.fio.cz/schema/importIB.xsd">
    <Orders>
        <T2Transaction>
            <accountFrom>1234562</accountFrom>
            <currency>EUR</currency>
            <amount>100.00</amount>
            <accountTo>AT611904300234573201</accountTo>
            <ks>0558</ks>
            <vs>1234567890</vs>
            <ss>1234567890</ss>
            <bic>ABAGATWWXXX</bic>
            <date>2013-04-25</date>
            <comment>Erste Zahlung</comment>
            <benefName>Hans Gruber</benefName>
            <benefStreet>Gugitzgasse 2</benefStreet>
            <benefCity>Wien</benefCity>
            <benefCountry>AT</benefCountry>
            <remittanceInfo1></remittanceInfo1>
            <remittanceInfo2></remittanceInfo2>
            <remittanceInfo3></remittanceInfo3>
            <paymentType>431008</paymentType>
        </T2Transaction>
    </Orders>
</Import>
```

Země majitele účtu

| Kód Název země | Kód Název země                          | Kód Název země | Kód Název země                               | Kód Název země | Kód Název země                            |
| -------------- | --------------------------------------- | -------------- | -------------------------------------------- | -------------- | ----------------------------------------- |
| AF             | Afghánistán                             | AX             | Alandské ostrovy                             | AL             | Albánie                                   |
| DZ             | Alžírsko                                | VI             | Americké Panenské ostrovy                    | AS             | Americká Samoa                            |
| AD             | Andorra                                 | AO             | Angola                                       | AI             | Anguilla                                  |
| AQ             | Antarktida                              | AG             | Antigua a Barbuda                            | AR             | Argentina                                 |
| AM             | Arménie                                 | AW             | Aruba                                        | AU             | Austrálie                                 |
| AZ             | Ázerbájdžán                             | BS             | Bahamy                                       | BH             | Bahrajn                                   |
| BD             | Bangladéš                               | BB             | Barbados                                     | BE             | Belgie                                    |
| BZ             | Belize                                  | BY             | Bělorusko                                    | BJ             | Benin                                     |
| BM             | Bermudy                                 | BT             | Bhútán                                       | BO             | Mnohonárodní stát Bolívie                 |
| BQ             | Bonaire, Svatý Eustach a<br>Saba        | BA             | Bosna a Hercegovina                          | BW             | Botswana                                  |
| BV             | Bouvetuv ostrov                         | BR             | Brazílie                                     | IO             | Britské indickooceánské<br>území          |
| VG             | Britské Panenské ostrovy                | BN             | Brunej Darussalam                            | BG             | Bulharsko                                 |
| BF             | Burkina Faso                            | BI             | Burundi                                      | TD             | Čad                                       |
| CK             | Cookovy ostrovy                         | CI             | Pobřeží Slonoviny                            | CW             | Curaçao                                   |
| ME             | Černá Hora                              | CZ             | Česká republika                              | CN             | Čína                                      |
| DK             | Dánsko                                  | TL             | Demokratická republika<br>Východní Timor     | GP             | Guadeloupe                                |
| GF             | Francouzská Guyana                      | MQ             | Martinik                                     | RE             | Réunion                                   |
| DM             | Dominika                                | DO             | Dominikánská republika                       | DJ             | Džibutsko                                 |
| EG             | Egypt                                   | EC             | Ekvádor                                      | ER             | Eritrea                                   |
| EE             | Estonsko                                | ET             | Etiopie                                      | FO             | Faerské ostrovy                           |
| FK             | Falklandské ostrovy<br>(Malvíny)        | FJ             | Fidži                                        | PH             | Filipíny                                  |
| FI             | Finsko                                  | FR             | Francie                                      | TF             | Francouzská jižní území                   |
| PF             | Francouzská Polynésie                   | GA             | Gabon                                        | GM             | Gambie                                    |
| GH             | Ghana                                   | GI             | Gibraltar                                    | GD             | Grenada                                   |
| GL             | Grónsko                                 | GE             | Gruzie                                       | GU             | Guam                                      |
| GT             | Guatemala                               | GG             | Guernsey                                     | GW             | Guinea-Bissau                             |
| GN             | Guinea                                  | GY             | Guyana                                       | HT             | Haiti                                     |
| HM             | Heardúv ostrov a<br>McDonaldovy ostrovy | HN             | Honduras                                     | HK             | Hongkong                                  |
| CL             | Chile                                   | HR             | Chorvatsko                                   | IN             | Indie                                     |
| ID             | Indonésie                               | IQ             | Irák                                         | IR             | Írán (islámská republika)                 |
| IE             | Irsko                                   | IS             | Island                                       | IT             | Itálie                                    |
| IL             | Izrael                                  | JM             | Jamajka                                      | JP             | Japonsko                                  |
| YE             | Jemen                                   | JE             | Jersey                                       | ZA             | Jižní Afrika                              |
| JO             | Jordánsko                               | GS             | Jižní Georgie a Jižní<br>Sandwichovy ostrovy | KY             | Kajmanské Ostrovy                         |
| KH             | Kambodža                                | CM             | Kamerun                                      | CA             | Kanada                                    |
| CV             | Kapverdy                                | QA             | Katar                                        | KZ             | Kazachstán                                |
| KE             | Keña                                    | KI             | Kiribati                                     | CC             | Kokosové (Keelingovy)<br>ostrovy          |
| CO             | Kolumbie                                | KM             | Komory                                       | CD             | Kongo, demokratická<br>republika          |
| CG             | Kongo, republika                        | KR             | Korejská republika                           | KP             | Korejská lidově<br>demokratická republika |
| CR             | Kostarika                               | TO             | Tonga                                        | XK             | Kosovo                                    |
| CU             | Kuba                                    | KW             | Kuvajt                                       | CY             | Kypr                                      |
| KG             | Kyrgyzstán                              | LA             | Laoská lidově demokratickárepublika          | LS             | Lesotho                                   |
| LB             | Libanon                                 | LR             | Libérie                                      | LY             | Libye                                     |
| LI             | Lichtenštejnsko                         | LT             | Litva                                        | LV             | Lotyšsko                                  |
| LU             | Lucembursko                             | MO             | Macao                                        | MG             | Madagaskar                                |
| HU             | Madarsko                                | MK             | Makedonie, bývalá<br>jugoslávská republika   | MY             | Malajsie                                  |
| MW             | Malawi                                  | MV             | Maledivská republika                         | ML             | Mali                                      |
| MT             | Malta                                   | MA             | Maroko                                       | MH             | Marshallovy ostrovy                       |
| MU             | Mauricius                               | MR             | Mauritánie                                   | UM             | Menší odlehlé ostrovy USA                 |
| MX             | Mexiko                                  | FM             | Mikronésie, federativní státy                | MD             | Moldavská republika                       |
| MC             | Monako                                  | MN             | Mongolsko                                    | MS             | Montserrat                                |
| MZ             | Mosambik                                | MM             | Myanmar                                      | NA             | Namibie                                   |
| NR             | Nauru                                   | DE             | Německo                                      | NP             | Nepál                                     |
| WS             | Samoa                                   | NE             | Niger                                        | NG             | Nigérie                                   |
| NI             | Nikaragua                               | NU             | Niue                                         | NL             | Nizozemsko                                |
| AN             | Nizozemské Antily                       | NF             | Ostrov Norfolk                               | NO             | Norsko                                    |
| NC             | Nová Kaledonie                          | NZ             | Nový Zéland                                  | PS             | Palestinské území<br>(okupované)          |
| OM             | Omán                                    | IM             | Ostrov Man                                   | TC             | Ostrovy Turks a Caicos                    |
| PK             | Pákistán                                | PW             | Palau                                        | PA             | Panama                                    |
| PG             | Papua Nová Guinea                       | PY             | Paraguay                                     | PE             | Peru                                      |
| PN             | Pitcairn                                | PL             | Polsko                                       | PR             | Portoriko                                 |
| PT             | Portugalsko                             | AT             | Rakousko                                     | GQ             | Rovníková Guinea                          |
| RO             | Rumunsko                                | RU             | Ruská federace                               | RW             | Rwanda                                    |
| GR             | Řecko                                   | SV             | Salvador                                     | PM             | Saint-Pierre a Miquelon                   |
| SM             | San Marino                              | SA             | Saúdská Arábie                               | SN             | Senegal                                   |
| SC             | Seychely                                | SL             | Sierra Leone                                 | SG             | Singapur                                  |
| SK             | Slovensko                               | SI             | Slovinsko                                    | SO             | Somálsko                                  |
| AE             | Spojené arabské emiráty                 | MP             | Severní Mariany                              | LK             | Srí Lanka                                 |
| RS             | Srbsko                                  | CF             | Středoafrická republika                      | SD             | Súdán                                     |
| SR             | Surinam                                 | SJ             | Svalbard a Jan Mayen                         | SH             | Svatá Helena                              |
| LC             | Svatá Lucie                             | BL             | Svatý Bartoloměj                             | KN             | Svatý Kryštof a Nevis                     |
| MF             | Svatý Martin (francouzskáčást)          | SX             | Svatý Martin (nizozemská<br>část)            | ST             | Svatý Tomáš a PPrincuv<br>ostrov          |
| VC             | Svatý Vincenc a Grenadiny               | SZ             | Svazijsko                                    | SY             | Syrská arabská republika                  |
| SB             | Šalomounovy ostrovy                     | ES             | Španělsko                                    | SE             | Švédsko                                   |
| CH             | Švýcarsko                               | TJ             | Tádžikistán                                  | TZ             | Tanzanská sjednocená<br>republika         |
| TH             | Thajsko                                 | TW             | Tchaj-Wan,čínská provincie                   | TCH            | Tichomorské ostrovy (USA)                 |
| TK             | Tokelau                                 | TG             | Togo                                         | TT             | Trinidad a Tobago                         |
| TN             | Tunisko                                 | TR             | Turecko                                      | TM             | Turkmenistán                              |
| TV             | Tuvalu                                  | UG             | Uganda                                       | UA             | Ukrajina                                  |
| UY             | Uruguay                                 | US             | Spojené státy americké                       | UZ             | Uzbekistán                                |
| YT             | Mayotte                                 | CX             | Vánoční ostrov                               | VU             | Vanuatu                                   |
| VA             | Vatikán                                 | GB             | Velká Británie                               | VE             | Bolívarovská republika<br>Venezuela       |
| VN             | Vietnam                                 | TP             | Východní Timor                               | WF             | Wallis a Futuna                           |
| ZM             | Zambie                                  | EH             | Západní Sahara                               | ZW             | Zimbabwe                                  |

## 6.3.3 XML příkaz zahraniční platba

| Element          | Stav | Formát     | Popis                                                                                                 | Příklad                     |
| ---------------- | ---- | ---------- | ----------------------------------------------------------------------------------------------------- | --------------------------- |
| accountFrom      | M    | 16n        | číslo účtu příkazce                                                                                   | 1234562                     |
| currency         | M    | 3!x        | měna účtu dle standardu ISO<br>4217                                                                   | USD                         |
| amount           | M    | 18d        | částka príkazu                                                                                        | 100.00                      |
| accountTo        | M    | 34x        | číslo učtu<br>příjemce/inkasovaného                                                                   | PK36SCBL000000 1123456702   |
| bic              | M    | 11!x       | bankovní identifikační kód dle<br>standardu ISO 9362                                                  | ALFHPKKAXXX                 |
| date             | M    | RRRR-MM-DD | datum                                                                                                 | 2013-04-25                  |
| comment          | O    | 140e       | upřesňující informace                                                                                 | Payment a0315               |
| benefName        | M    | 35e        | majitel účtu                                                                                          | Amir Khan                   |
| benefStreet      | M    | 35x        | bydliště majitele účtu-ulice                                                                          | Nishtar Rd 13               |
| benefCity        | M    | 35x        | bydliště majitele účtu-město                                                                          | Karachi                     |
| benefCountry     | M    | 3x         | země majitele účtu                                                                                    | PK                          |
| remittancelnfo1  | M    | 35x        | informace pro přijemce                                                                                | Payment for hotel<br>032013 |
| remittancelnfo2  | O    | 35x        | informace pro přijemce                                                                                |                             |
| remittancelnfo3  | O    | 35x        | informace pro prijemce                                                                                |                             |
| remittancelnfo4  | O    | 35x        | informace pro přijemce                                                                                |                             |
| detailsOfCharges | M    | 6!n        | poplatky:<br>470501 - vše plátce (OUR)<br>470502 - vše přijemce (BEN)<br>470503 - každý sám své (SHA) | 470502                      |
| paymentReason    | M    | 3!n        | platební titul viz 6.3.4 Platební<br>titul                                                            | 348                         |

# Příklad zahraniční platby

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Import xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://www.fio.cz/schema/importIB.xsd">
    <Orders>
        <ForeignTransaction>
            <accountFrom>1234562</accountFrom>
            <currency>USD</currency>
            <amount>100.00</amount>
            <accountTo>PK36SCBL0000001123456702</accountTo>
            <bic>ALFHPKKAXXX</bic>
            <date>2013-04-25</date>
            <comment>Payment a0315</comment>
            <benefName>Amir Khan</benefName>
            <benefStreet>Nishtar Rd 13</benefStreet>
            <benefCity>Karachi</benefCity>
            <benefCountry>PK</benefCountry>
            <remittanceInfo1>Payment for hotel 032013</remittanceInfo1>
            <remittanceInfo2></remittanceInfo2>
            <remittanceInfo3></remittanceInfo3>
            <remittanceInfo4></remittanceInfo4>
            <detailsOfCharges>470502</detailsOfCharges>
            <paymentReason>348</paymentReason>
        </ForeignTransaction>
    </Orders>
</Import>
```

# 6.3.4 Platební titul

| Hodnota | Popis                                                                                                  |
| ------- | ------------------------------------------------------------------------------------------------------ |
| 110     | Vývoz zboží                                                                                            |
| 112     | Finanční pronájem (leasing) - vývoz                                                                    |
| 120     | Dovoz zboží                                                                                            |
| 122     | Finanční pronájem (leasing)-dovoz                                                                      |
| 130     | Reexport                                                                                               |
| 132     | Zpracování                                                                                             |
| 135     | Opravy                                                                                                 |
| 190     | Transakce z použití směnek a šeků                                                                      |
| 195     | Časově neidentifikované platební tituly                                                                |
| 210     | Železniční nákladní - inkasa a platby spojené s přepravou zboží po železnici                           |
| 211     | Železniční osobní - inkasa a platby spojené s přepravou osob po železnici                              |
| 212     | Železniční ostatní                                                                                     |
| 213     | Námorní nákladní                                                                                       |
| 214     | Námořní osobní                                                                                         |
| 215     | Námořní ostatní                                                                                        |
| 216     | Vnitrozemská vodní nákladní                                                                            |
| 217     | Vnitrozemská vodní osobní                                                                              |
| 218     | Vnitrozemská vodní ostatní                                                                             |
| 219     | Letecká nákladní                                                                                       |
| 220     | Letecká osobní                                                                                         |
| 221     | Letecká ostatní                                                                                        |
| 222     | Silniční nákladní                                                                                      |
| 223     | Silniční osobní                                                                                        |
| 224     | Silniční ostatní                                                                                       |
| 226     | Kombinovaná doprava                                                                                    |
| 233     | Kosmická doprava                                                                                       |
| 235     | Potrubní tranzit                                                                                       |
| 239     | Ostatní přepravní služby                                                                               |
| 260     | Nákup cizí měny za hotovost                                                                            |
| 262     | Nákup cizí měny s připsáním na účet fyzické osoby v Kč                                                 |
| 265     | Nákup cizí měny s připsáním na účet právnické osoby v Kč                                               |
| 270     | Prodej cizí měny za hotovost                                                                           |
| 272     | Prodej cizí měny s odepsáním z účtu fyzické osoby v Kč                                                 |
| 275     | Prodej cizí měny s odepsáním z účtu právnické osoby v Kč                                               |
| 280     | Aktivní cestovní ruch                                                                                  |
| 282     | Pasivní cestovní ruch                                                                                  |
| 285     | Mimobankovní směnárny                                                                                  |
| 295     | Transakce z použití platebních karet                                                                   |
| 310     | Poštovní služby                                                                                        |
| 311     | Kurýrní služby                                                                                         |
| 312     | Telekomunikační a radiokomunikační služby                                                              |
| 315     | Stavební a montážní práce v zahraničí                                                                  |
| 318     | Stavební a montážní práce v tuzemsku                                                                   |
| 320     | Ziskové operace se zbožím                                                                              |
| 325     | Opravy                                                                                                 |
| 326     | Pojištění zboží                                                                                        |
| 327     | Zajištění (pojišťoven)                                                                                 |
| 328     | Pomocné služby při pojištění                                                                           |
| 330     | Ostatní pojištění                                                                                      |
| 332     | Životní a penzijní pojištění                                                                           |
| 335     | Finanční služby                                                                                        |
| 340     | Reklama                                                                                                |
| 345     | Právní služby                                                                                          |
| 346     | Účetnické a auditorské služby                                                                          |
| 347     | Poradenství v podnikání a řízení, služby v oblasti vytváření vztahu k veřejnosti - public<br>relations |
| 348     | Nájemné                                                                                                |
| 352     | Pronájem strojů a zařízení                                                                             |
| 355     | Výzkum a vývoj                                                                                         |
| 360     | Autorské honoráře, licenční poplatky                                                                   |
| 361     | Ochranné známky, franšízy                                                                              |
| 365     | Služby výpočetní techniky                                                                              |
| 368     | Informační služby                                                                                      |
| 369     | Služby mezi podniky v rámci přímých investic                                                           |
| 370     | Diplomatická zastoupení České republiky v zahraničí                                                    |
| 372     | Zahraniční diplomatická zastoupení v České republice                                                   |
| 375     | Vládní příjmy a výdaje                                                                                 |
| 376     | Ostatní vládní příjmy a výdaje                                                                         |
| 378     | Zprostředkovatelské služby                                                                             |
| 380     | Ostatní služby obchodní povahy                                                                         |
| 382     | Audiovizuální služby                                                                                   |
| 384     | Služby v oblasti vzdělávání                                                                            |
| 385     | Služby v oblasti kultury, zábavy, sportu a rekreace                                                    |
| 386     | Služby v oblasti zdravotnictví a veterinární péče                                                      |
| 387     | Služby v oblasti zemědělství                                                                           |
| 388     | Služby v oblasti odpadového hospodárství                                                               |
| 390     | Technické služby                                                                                       |
| 392     | Služby v oblasti těžebního průmyslu                                                                    |
| 395     | Zastoupení českých firem v zahraničí                                                                   |
| 397     | Zastoupení zahraničních firem v ČR                                                                     |
| 410     | Převody pracovních příjmů u krátkodobého pobytu                                                        |
| 412     | Převody pracovních příjmů u dlouhodobého pobytu                                                        |
| 510     | Výnosy z přímých investic                                                                              |
| 520     | Výnosy z portfoliových investic                                                                        |
| 530     | Úroky - přímé investice                                                                                |
| 532     | Úroky - portfoliové investice                                                                          |
| 535     | Úroky z finančních a ostatních úvěrů                                                                   |
| 538     | Úroky z obchodních úvěrů                                                                               |
| 540     | Úroky z depozit                                                                                        |
| 550     | Duchody z půdy                                                                                         |
| 610     | Převody (nenávratné) - podpory, odškodnění, věna apod.                                                 |
| 612     | Dědictví a dary                                                                                        |
| 615     | Výživné                                                                                                |
| 618     | Penze                                                                                                  |
| 620     | Příspěvky mezinárodním organizacím ze státního rozpočtu                                                |
| 622     | Příspěvky mezinárodním organizacím mimo státní rozpočet                                                |
| 625     | Převody v souvislosti s vystěhováním                                                                   |
| 628     | Zahraniční pomoc                                                                                       |
| 630     | Dotace                                                                                                 |
| 632     | Pokuty, penále                                                                                         |
| 635     | Daně a poplatky                                                                                        |
| 640     | Nákup a prodej vlastnických práv a nefinančních aktiv                                                  |
| 650     | Ostatní finanční převody                                                                               |
| 652     | Příspěvky a výhry                                                                                      |
| 653     | Vklady a příspěvky do nadací a nadačních fondů                                                         |
| 725     | Finanční deriváty                                                                                      |
| 735     | Nákup a prodej nemovitostí v zahraničí                                                                 |
| 740     | Poskytnuté úvěry krátkodobé účelové                                                                    |
| 742     | Poskytnuté úvěry krátkodobé finanční (bez stanoveného účelu)                                           |
| 745     | Poskytnuté úvěry střednědobé a dlouhodobé účelové                                                      |
| 748     | Poskytnuté úvěry střednědobé a dlouhodobé finanční (bez stanoveného účelu)                             |
| 750     | Vklady a výběry z vkladů promptních a krátkodobých                                                     |
| 752     | Dotace účtů                                                                                            |
| 755     | Vklady a výběry z vkladů střednědobých a dlouhodobých                                                  |
| 760     | Konverze, arbitráže a další operace                                                                    |
| 762     | Rízení likvidity peněžních prostředků (cash-pooling, zero balancing)                                   |
| 770     | Členské podíly v mezinárodních organizacích                                                            |
| 790     | Zajištění závazků cizozemce                                                                            |
| 818     | Tuzemské portfoliové investice                                                                         |
| 820     | Tuzemské dluhové cenné papíry krátkodobé                                                               |
| 822     | Tuzemské dluhové cenné papíry strednědobé a dlouhodobé                                                 |
| 825     | Finanční deriváty                                                                                      |
| 835     | Nákup a prodej nemovitostí v tuzemsku                                                                  |
| 850     | Vklady a výběry z vkladů promptních a krátkodobých                                                     |
| 852     | Dotace účtu                                                                                            |
| 855     | Vklady a výběry z vkladů střednědobých a dlouhodobých                                                  |
| 862     | Řízení likvidity peněžních prostredků (cash-pooling, zero balancing)                                   |
| 890     | Zajištění závazku tuzemce                                                                              |
| 950     | Převody mezi tuzemci                                                                                   |
| 952     | Převody mezi cizozemci                                                                                 |

# 6.4 SEPA (pain)

## 6.4.1 pain.001 (platební příkazy)

Zpracování dávkového souboru ve strukture pain.001.001.03 nebo novější verze pain.001.001.09 odpovídástandardu, který je definovaný ve standardu SEPA Credit Transfer Scheme Customer-to-Bank Implementation Guidelines Version.

**Import plateb Ize provést pouze v měně EUR. Jiná měna není povolena.**

XSD je dostupné zde: <https://www.fio.cz/schema/pain.001.001.03.xsd> a <https://www.fio.cz/schema/pain.001.001.09.xsd>

**Elementy `<BIC>` a `<BIC Or BEI>` jsou nepovinná. Je-li použit jeden z těchto elementů, tak obsah polímusí být v souladu s XSD a splňovat jeho formát.**

# Příklad platebního EUR příkazu:

```xml
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<Document xmlns="urn:iso:std:iso:20022:tech:xsd:pain.001.001.03"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:iso:std:iso:20022:tech:xsd:pain.001.001.03 pain.001.001.03.xsd">
    <CstmrCdtTrfInitn>
        <GrpHdr>
            <MsgId>MCCT000000035166629</MsgId>
            <CreDtTm>2015-11-11T09:46:06</CreDtTm>
            <NbOfTxs>000000000000003</NbOfTxs>
            <CtrlSum>16.00</CtrlSum>
            <InitgPty>
                <Nm>Jan Novák</Nm>
            </InitgPty>
        </GrpHdr>
        <PmtInf>
            <PmtInfId>15100700002</PmtInfId>
            <PmtMtd>TRF</PmtMtd>
            <BtchBookg>true</BtchBookg>
            <NbOfTxs>000000000000003</NbOfTxs>
            <CtrlSum>16.00</CtrlSum>
            <PmtTpInf>
                <InstrPrty>NORM</InstrPrty>
                <SvcLvl>
                    <Cd>SEPA</Cd>
                </SvcLvl>
                <LclInstrm>
                    <Cd>INST</Cd>
                </LclInstrm>
            </PmtTpInf>
            <ReqdExctnDt>2025-11-11</ReqdExctnDt>
            <Dbtr>
                <Nm>Jan Novák</Nm>
                <PstlAdr>
                    <Ctry>CZ</Ctry>
                    <AdrLine>Novakova 178</AdrLine>
                    <AdrLine>Praha 1</AdrLine>
                </PstlAdr>
            </Dbtr>
            <DbtrAcct>
                <Id>
                    <IBAN>CZ5220100000000000000123</IBAN>
                </Id>
                <Ccy>EUR</Ccy>
            </DbtrAcct>
            <DbtrAgt>
                <FinInstnId>
                    <BIC>FIOBCZPPXXX</BIC>
                </FinInstnId>
            </DbtrAgt>
            <ChrgBr>SLEV</ChrgBr>
            <CdtTrfTxInf>
                <PmtId>
                    <InstrId>191</InstrId>
                    <EndToEndId>/VS0123456789/SS9876543210/KS1234</EndToEndId>
                </PmtId>
                <Amt>
                    <InstdAmt Ccy="EUR">1.00</InstdAmt>
                </Amt>
                <CdtrAgt>
                    <FinInstnId>
                        <BIC>KOMBCZPPXXX</BIC>
                    </FinInstnId>
                </CdtrAgt>
                <Cdtr>
                    <Nm>Sepa,s.r.o.</Nm>
                    <PstlAdr>
                        <Ctry>CZ</Ctry>
                        <AdrLine>Okruzni 55</AdrLine>
                        <AdrLine>Praha 1</AdrLine>
                    </PstlAdr>
                </Cdtr>
                <CdtrAcct>
                    <Id>
                        <IBAN>CZ6701000000000000123123</IBAN>
                    </Id>
                </CdtrAcct>
                <RmtInf>
                </RmtInf>
            </CdtTrfTxInf>
            <CdtTrfTxInf>
                <PmtId>
                    <InstrId>192</InstrId>
                    <EndToEndId>/VS0123456789/SS9876543210/KS1234</EndToEndId>
                </PmtId>
                <Amt>
                    <InstdAmt Ccy="EUR">5.00</InstdAmt>
                </Amt>
                <CdtrAgt>
                    <FinInstnId>
                        <BIC>DABASESXXXX</BIC>
                    </FinInstnId>
                </CdtrAgt>
                <Cdtr>
                    <Nm>Adrian Sweet</Nm>
                    <PstlAdr>
                        <Ctry>SE</Ctry>
                        <AdrLine>Street 225</AdrLine>
                        <AdrLine>Stockholm</AdrLine>
                    </PstlAdr>
                </Cdtr>
                <CdtrAcct>
                    <Id>
                        <IBAN>SE6412000000012170145230</IBAN>
                    </Id>
                </CdtrAcct>
                <RmtInf>
                </RmtInf>
            </CdtTrfTxInf>
            <CdtTrfTxInf>
                <PmtId>
                    <InstrId>190</InstrId>
                    <EndToEndId>example of end2end</EndToEndId>
                </PmtId>
                <Amt>
                    <InstdAmt Ccy="EUR">10.00</InstdAmt>
                </Amt>
                <CdtrAgt>
                    <FinInstnId>
                        <BIC>WBKPPLPPXXX</BIC>
                    </FinInstnId>
                </CdtrAgt>
                <Cdtr>
                    <Nm>Poland Marco</Nm>
                    <PstlAdr>
                        <Ctry>PL</Ctry>
                        <AdrLine>Address 11</AdrLine>
                        <AdrLine>Wroclaw</AdrLine>
                    </PstlAdr>
                </Cdtr>
                <CdtrAcct>
                    <Id>
                        <IBAN>PL37109024020000000610000434</IBAN>
                    </Id>
                </CdtrAcct>
                <RmtInf>
                </RmtInf>
            </CdtTrfTxInf>
        </PmtInf>
    </CstmrCdtTrfInitn>
</Document>
```

# 6.4.2 pain.008 (príkazy k inkasu)

Zpracování dávkového souboru ve struktuře pain.008.001.02 odpovídá standardu.

XSD je dostupné zde: <https://www.fio.cz/schema/pain.008.001.02.xsd>

# Příklad SEPA inkaso:

```xml
<?xml version="1.0" encoding="utf-8"?>
<Document xmlns="urn:iso:std:iso:20022:tech:xsd:pain.008.001.02"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:iso:std:iso:20022:tech:xsd:pain.008.001.02 pain.008.001.02.xsd">
    <CstmrDrctDbtInitn>
        <GrpHdr>
            <MsgId>MCCT000000032497622</MsgId>
            <CreDtTm>2015-11-13T09:01:37</CreDtTm>
            <NbOfTxs>000000000000001</NbOfTxs>
            <CtrlSum>25.00</CtrlSum>
            <InitgPty>
                <Nm>firma, a.s.</Nm>
            </InitgPty>
        </GrpHdr>
        <PmtInf>
            <PmtInfId>15100700002</PmtInfId>
            <PmtMtd>DD</PmtMtd>
            <BtchBookg>true</BtchBookg>
            <NbOfTxs>000000000000001</NbOfTxs>
            <CtrlSum>25.00</CtrlSum>
            <PmtTpInf>
                <SvcLvl>
                    <Cd>SEPA</Cd>
                </SvcLvl>
                <LclInstrm>
                    <Cd>CORE</Cd>
                </LclInstrm>
            </PmtTpInf>
            <ReqdColltnDt>2015-11-17</ReqdColltnDt>
            <Cdtr>
                <Nm>firma, a.s.</Nm>
            </Cdtr>
            <CdtrAcct>
                <Id>
                    <IBAN>SK6383300000000000000123</IBAN>
                </Id>
                <Ccy>EUR</Ccy>
            </CdtrAcct>
            <CdtrAgt>
                <FinInstnId>
                    <BIC>FIOZSKBAXXX</BIC>
                </FinInstnId>
            </CdtrAgt>
            <DrctDbtTxInf>
                <PmtId>
                    <InstrId>183</InstrId>
                    <EndToEndId>/VS555/KS0309/SS12345</EndToEndId>
                </PmtId>
                <PmtTpInf>
                    <SeqTp>OOFF</SeqTp>
                </PmtTpInf>
                <InstdAmt Ccy="EUR">25.00</InstdAmt>
                <ChrgBr>SLEV</ChrgBr>
                <DrctDbtTx>
                    <MndtRltdInf>
                        <MndtId>12345</MndtId>
                        <DtOfSgntr>2009-01-19</DtOfSgntr>
                        <AmdmntInd>false</AmdmntInd>
                    </MndtRltdInf>
                    <CdtrSchmeId>
                        <Id>
                            <PrvtId>
                                <Othr>
                                    <Id>SK251235222</Id>
                                    <SchmeNm>
                                        <Prtry>SEPA</Prtry>
                                    </SchmeNm>
                                </Othr>
                            </PrvtId>
                        </Id>
                    </CdtrSchmeId>
                </DrctDbtTx>
                <DbtrAgt>
                    <FinInstnId>
                        <BIC>SUBASKBXXXX</BIC>
                    </FinInstnId>
                </DbtrAgt>
                <Dbtr>
                    <Nm>Klient</Nm>
                    <PstlAdr>
                        <Ctry>SK</Ctry>
                        <AdrLine>Adresa</AdrLine>
                        <AdrLine>Bratislava</AdrLine>
                    </PstlAdr>
                </Dbtr>
                <DbtrAcct>
                    <Id>
                        <IBAN>SK1502000000001444615051</IBAN>
                    </Id>
                </DbtrAcct>
                <RmtInf>
                    <Ustrd>Testovaci prikaz k inkasu (VS555/KS/SS)</Ustrd>
                </RmtInf>
            </DrctDbtTxInf>
        </PmtInf>
    </CstmrDrctDbtInitn>
</Document>
```

# 7 UPOZORNĚNÍ NA BEZPEČNOSTNÍ RIZIKA SOUVISEJÍCÍ S POUŽÍVÁNÍM API

a. Data obsažená v konfiguraci API jsou velmi citlivé údaje, a to zejména token k účtům. Chraňte svůj soubor nebo uložená data s konfigurací k API proti jejich zneužití, zejména proti odcizení, okopírování apod. Zneužitím Vašich konfiguračních údajů může jiná osoba předstírat Vaši identitu a zadávat pokyny Vaším jménem či získávat informace o pohybech. Zneužití souboru s konfiguracínebo dat Vám může způsobit škodu.

b. Soubor s konfigurací nebo data uchovávejte pouze na počítači, o kterém víte, že je chráněn proti možným hrozbám plynoucím z připojení k datové síti. Neukládejte konfiguraci na počítač, který je veřejně přístupný.

c. Uchováváte-li konfiguraci na jiném přenosném médiu, ukládejte toto médium na místo, kde nedojde k jeho zneužití, zejména odcizení, okopírování nebo poškození.

# 8 ZNÁMÉ CHYBOVÉ STAVY

## 8.1 The server encoutered an internal error () that prevented it from fulfilling this request.

Pokoušíte se soubor odeslat jako klasický POST a nikoli jako přílohu. Viz část 6.1 Parametry pro upload dat.

## 8.2 Status Code:404 Not Found

Špatně zaslaný dotaz, na který server nemůže řádně odpovědět. Zkontrolujte si parametry URL v dotazu/importu.

## 8.3 Status Code:409 Conflict

Není dodržen minimální interval 30 sekund mezi stažením dat z banky / uploadem dat do banky u konkrétního tokenu (bez ohledu na typ formátu). Konkrétní token lze použít pouze 1x pro čtení nebo zápis během 30 sekund

## 8.4 Status Code:500 Internal Server Error

Chyba indikuje neexistující nebo neaktivní token. Zkontrolujte si platnost a správnost tokenu v internetovém bankovnictví.

## 8.5 SSL certificate problém: unable to get local issuer certificate

Při importu příkazů do bankovního systému probíhá kontrola certifikátu certifikační autority. Tato kontrola selhala a je nutné získat nový používaný certifikát, a to buď dle bodu 6.1., anebo přímo ze stránek Fio banky:

Pro uživatele Google Chrome:

    a. ib.fio.cz/ib/login
    b. kliknout na zámeček v URL prohlížeče
    c. prokliknout certifikát
    d. záložka Cesta k certifikátu
    e. zvolte první řádek (root CA)
    f. tlačítko Zobrazit certifikát
    g. záložka Podrobnosti
    h. tlačítko Kopírovat do souboru
    i. po vyžádání typu formátu zvolte X.509, kódování Base-64(CER)
    j. vyplňte umístění, kam chcete soubor s certifikátem uložit
    k. po dokončení najděte soubor v adresári a změňte koncovku na .pem
    l. v bodu e. zvolte prostřední řádek (intermediate certifikát) a pokračujte až do bodu k.
    m. nahrajte oba certifikáty do truststore aplikace používané k vytvoření SSL komunikace

### Pro uživatele Mozilla Firefox:

    a. ib.fio.cz/ib/login
    b. kliknout na zámeček v URL prohlížeče
    c. šipkou doprava Zobrazte podrobnosti spojení
    d. tlačítko Více informací
    e. záložka Zabezpečení
    f. tlačítko Zobrazit certifikkát
    g. nahoře kliknout na prostřední (intermediate) certifikát
    h. v řádku Stáhnout prokliknout nápis PEM (certifikát)
    i. nahoře kliknout na pravý (root CA) certifikát
    j. v řádku Stáhnout prokliknout nápis PEM (certifikát)
    k. nahrajte oba certifikáty do truststore aplikace používané k vytvoření SSL komunikace

## 8.6 Status Code: 413 Příliš mnoho položek

Stahujete velkou množinu dat. Limit pro stažení je nastaven na max 50 000 pohybu.

Upravte si adekvátně datumový rozsah v zasílaném dotazu nebo je nutné nastavit zarážku na novější pohyb.

# 8.7 Error: 422

Jsou požadována data starší 90 dní, aniž byl přístup k historickým datům silně autorizován. Pro získání dat je potřeba postupovat dle 3.1.

# 9 ZMĚNY VE VERZÍCH DOKUMENTACE

| Verze       | Datum               | Obsah                                                                        | Změna z                                                                                                                                                                                            | Změna na                                                                                                                                                                                                                                                                                        |
| ----------- | ------------------- | ---------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0.9.1       | 5.10.2012           | 0                                                                            | Chybný příklad<br>v dokumentaci<br>dateStart, dateEnd<br>příklad: 2012-07-27+02:00                                                                                                                 | Opraveno na<br>dateStart, dateEnd<br>příklad: 2012-07-27+0200                                                                                                                                                                                                                                   |
| 0.9.1       | 5.10.2012           | 5.3.1.7                                                                      |                                                                                                                                                                                                    | Přidáno upozornění do<br>dokumentace:<br>Pole :86: je maximálně dlouhé 65x.<br>Pokud je pole větší, tak hodnoty jsou odděleny `<CR><LF>`;                                                                                                                                                       |
| 0.9.1       | 5.10.2012           | 5.3.1.7                                                                      | Chyba v příkladu<br>v dokumentaci<br>:20:1210031631571<br>:20:1210031631578                                                                                                                        | :20:121003163157-1<br>:20:121003163157-8                                                                                                                                                                                                                                                        |
| 0.9.2       | 24.10.2012          | 5.3.1.4                                                                      | Za posledním polem u<br>pohybu na řádku<br>obsahovala hodnota<br>oddělovač a `<CR><LF>`;                                                                                                           | Hodnota má za sebou pouze<br>`<CR><LF>`                                                                                                                                                                                                                                                         |
| 0.9.2.      | 25.10.2012          | 5.3.1.4                                                                      |                                                                                                                                                                                                    | Hodnoty u pohybů ve sloupcích:<br>Název protiúčtu, Název banky,<br>Uživatelská identifikace, Zpráva pro<br>príjemce, Provedl, Upřesnění,<br>Komentár budou v polích zobrazeny vždy v uvozovkách, pokud bude pole obsahovat data. Mají-li hodnoty již<br>v sobě uvozovky, pak budou<br>zdvojeny. |
| 0.9.2.      | 26.10.2012          | 5.3.1<br>5.3.1.4<br>5.3.1.6                                                  | U formátů json, html, csv,<br>xml se v hlavičce<br>nevyskytovaly vyplněné<br>hodnoty idFrom, idTo                                                                                                  | Příklady v API a v dokumentaci<br>opraveny.                                                                                                                                                                                                                                                     |
| 1.0.        | 1.11.2012           | Vyhlášena verze 1.0.                                                         | Vyhlášena verze 1.0.                                                                                                                                                                               | Vyhlášena verze 1.0.                                                                                                                                                                                                                                                                            |
| 1.0.1       | 5.11.2012           | 5.3.1<br>až<br>5.3.1.7                                                       |                                                                                                                                                                                                    | Doplněn chybějící popis znakové<br>sady do specifikace k jednotlivým<br>formátům.                                                                                                                                                                                                               |
| 1.0.2       | 6.11.2012           | 5.2.2                                                                        | Uvedeny špatné formáty<br>dat pro Rok výpisu a ID                                                                                                                                                  | rok-formát: rrrr<br>id - číslo výpisu                                                                                                                                                                                                                                                           |
| 1.0.3       | 20.11.2012          | 5.2.4                                                                        | Struktura příklad:<br>https://ww.fio.cz                                                                                                                                                            | Oprava na <https://www.fio.cz>                                                                                                                                                                                                                                                                  |
| 1.0.4.      | 14.1.2013           | 5.3.1.2                                                                      | Úprava času                                                                                                                                                                                        | Doplněny časové zóny                                                                                                                                                                                                                                                                            |
| 1.0.4.      | 14.1.2013           | 5.3.1.3                                                                      |                                                                                                                                                                                                    | Doplněny čísla výpisu v příkladu<br>pozice 106-108                                                                                                                                                                                                                                              |
| 1.0.5.      | 20.2.2013           | 5.2<br>5.2.3<br>5.2.4                                                        |                                                                                                                                                                                                    | Upřesnění významů popisu.                                                                                                                                                                                                                                                                       |
| 1.0.6       | 23.2.2013           | 5                                                                            |                                                                                                                                                                                                    | Doplněny typy pohybů.                                                                                                                                                                                                                                                                           |
| 1.0.7       | 22.4.2013           | 5.3.1                                                                        | Špatná délka IBANu                                                                                                                                                                                 | Opraveno na korektní délku 34<br>znaků.                                                                                                                                                                                                                                                         |
| 1.2         | 25.4.2013           | 4                                                                            |                                                                                                                                                                                                    | Vytvořeny podporované formáty<br>podávaní příkazů, ABO příkaz a XML příkaz.                                                                                                                                                                                                                     |
| 1.2.1 1.2.2 | 12.6.2013 13.6.2013 | 5.3.1.8 6.1                                                                  | Oprava popisku errorCode                                                                                                                                                                           | Doplněny parametry uploadu                                                                                                                                                                                                                                                                      |
| 1.2.3       | 14.6.2013           | 6.1                                                                          |                                                                                                                                                                                                    | Doplněno volání o multipart/form-<br>data                                                                                                                                                                                                                                                       |
| 1.2.4       | 24.6.2013           | 5.1                                                                          |                                                                                                                                                                                                    | Nový formát dat: PDF (výpisy)                                                                                                                                                                                                                                                                   |
| 1.2.4       | 24.6.2013           | 5.2.6                                                                        |                                                                                                                                                                                                    | Doplněny informace o rozdílu mezi<br>Idpohyb a Idpokyn                                                                                                                                                                                                                                          |
| 1.2.4       | 24.6.2013           | 5.3.1.8                                                                      |                                                                                                                                                                                                    | Importovaná data musejí být<br>autorizovány                                                                                                                                                                                                                                                     |
| 1.2.5       | 10.7.2013           | 6.4                                                                          |                                                                                                                                                                                                    | Přidáno bezpečnostní upozornění                                                                                                                                                                                                                                                                 |
| 1.2.6       | 2.10.2013           | 6.1                                                                          |                                                                                                                                                                                                    | Přidány příklady použití cURL                                                                                                                                                                                                                                                                   |
| 1.2.7       | 16.11.2013          | 8                                                                            |                                                                                                                                                                                                    | Přidány známé chybové stavy                                                                                                                                                                                                                                                                     |
| 1.2.8       | 14.1.2014           | 5.2.6                                                                        |                                                                                                                                                                                                    | Přidán další příklad rozdílu mezi<br>pohybem a pokynem                                                                                                                                                                                                                                          |
| 1.2.9       | 20.4.2014           | 6.1                                                                          |                                                                                                                                                                                                    | Opraven příklad curl pro Windows                                                                                                                                                                                                                                                                |
| 1.3.0       | 29.5.2014           | 0                                                                            |                                                                                                                                                                                                    | Opraveny chybné názvy zemí                                                                                                                                                                                                                                                                      |
| 1.3.1       | 22.7.2014           | 2                                                                            |                                                                                                                                                                                                    | Přidán popis typů (práv) tokenu                                                                                                                                                                                                                                                                 |
| 1.3.2       | 10.12.2014          | 6.3.1<br>6.3.2<br>6.3.3                                                      |                                                                                                                                                                                                    | Opraveno v elementu ,,date" stav<br>z nepovinné (O) na povinné (M)                                                                                                                                                                                                                              |
| 1.3.3       | 14.1.2015           | vše                                                                          |                                                                                                                                                                                                    | Grafická korekce dokumentu                                                                                                                                                                                                                                                                      |
| 1.3.4       | 15.1.2015           | 2                                                                            |                                                                                                                                                                                                    | Doplňující informace o autorizaci<br>tokenu i více osobami                                                                                                                                                                                                                                      |
| 1.3.5       | 20.2.2015           | 6.3.2<br>6.3.3                                                               | Špatná délka znaků<br>v údajích o příjemci $(50x)$                                                                                                                                                 | Element benefName, benefStreet a<br>benefCity přijme pouze 35 znaku.                                                                                                                                                                                                                            |
| 1.3.6       | 24.2.2015           | 6.3.                                                                         |                                                                                                                                                                                                    | Doplněna informace o pořadí<br>tuzemských, euro a zahraničních<br>plateb                                                                                                                                                                                                                        |
| 1.3.7       | 7.4.2015            | 5.3.6.                                                                       | Špatně definovaný atribut<br>ve strukture JSON<br>`accounld` v dokumentaci                                                                                                                         | Nahrazen správným ,,accountld"                                                                                                                                                                                                                                                                  |
| 1.3.8       | 6.5.2015            | 5.3.1.<br>5.3.5.                                                             | Špatný formát dat<br>`dd-mm-rrrr+GMT`                                                                                                                                                              | Data opraveny na správný formát<br>rrrr-mm-dd+GMT                                                                                                                                                                                                                                               |
| 1.3.9       | 26.5.2015           | 6.1                                                                          | Certifikát certifikační<br>autority Root 1                                                                                                                                                         | Nový certifikát certifikační autority<br>Root 3                                                                                                                                                                                                                                                 |
| 1.3.9       | 26.5.2015           | 8.3.                                                                         |                                                                                                                                                                                                    | Nová známá chyba SSL certificate<br>57roblém: unable to get local issuer<br>certificate                                                                                                                                                                                                         |
| 1.4.0       | 21.7.2015           | 8.1.                                                                         | Viz část 7.1 Parametry pro<br>upload dat.                                                                                                                                                          | Viz část 6.1 Parametry pro upload<br>dat.                                                                                                                                                                                                                                                       |
| 1.4.1       | 7.9.2015            | 4                                                                            | Parametr benefName                                                                                                                                                                                 | Definován nový datový typ " $"e$                                                                                                                                                                                                                                                                |
| 1.4.2       | 11.11.2015          | 6.4.1<br>6.4.2                                                               |                                                                                                                                                                                                    | Nový typ formátu pro import dat.<br>Pain.001 a pain.008                                                                                                                                                                                                                                         |
| 1.4.2       | 11.11.2015          | 5.3.8<br>5.3.9                                                               |                                                                                                                                                                                                    | Nový typ formátu pro stažení výpisů<br>camt.053                                                                                                                                                                                                                                                 |
| 1.4.3       | 25.11.2015          | 6.3.1<br>6.3.2                                                               | Povinný parametr<br>paymentType (M)                                                                                                                                                                | Nepovinný parametr paymentType<br>(O)                                                                                                                                                                                                                                                           |
| 1.4.4       | 17.12.2015          | 6.1                                                                          |                                                                                                                                                                                                    | Doplněn typ dat pro import pain.                                                                                                                                                                                                                                                                |
| 1.4.5       | 14.3.2016           | 6.1.                                                                         | Již starý typ certifikátu Root 3                                                                                                                                                                   | Upraven odkaz na nový typ<br>certifikátu Root 5                                                                                                                                                                                                                                                 |
| 1.4.6       | 27.5.2016           | 3.2<br>6.3.1<br>6.3.2                                                        | Již staré typy plateb do ČR<br>a SR                                                                                                                                                                | 3.2. Platba do ČR a SR změněna na Platba do ČR<br>6.3.1 Platba do ČR a SR změněna<br>na Platba do ČR, v elementu<br>currency odstraněna věta Pro platbu do SR použít EUR<br>6.3.2 U elementu bic změněn stav<br>z M na O                                                                        |
| 1.4.7       | 27.5.2016           | 6.2.                                                                         | ABO                                                                                                                                                                                                | Příkazy ve formátu ABO Ize pouze<br>odesílat do ČR bank v CZK nebo<br>v jiných měnách pouze v rámci Fio<br>banky (2010). Příkazy do<br>slovenských bank nejsou tímto<br>způsobem již možné.                                                                                                     |
| 1.4.8       | 27.5.2016           | 6.1                                                                          | Špatný příklad použití cURL                                                                                                                                                                        | Příklad byl opraven.                                                                                                                                                                                                                                                                            |
| 1.4.9       | 31.5.2016           | 8                                                                            |                                                                                                                                                                                                    | Nové chybové stavy.                                                                                                                                                                                                                                                                             |
| 1.5.0       | 31.5.2016           | 6.3.2                                                                        | Chybné označení<br>povinného parametru<br>benefCountry M                                                                                                                                           | benefCountry O                                                                                                                                                                                                                                                                                  |
| 1.5.1       | 7.6.2016            | 6.3                                                                          |                                                                                                                                                                                                    | Link na XSD                                                                                                                                                                                                                                                                                     |
| 1.5.2       | 16.12.2016          | 5.3.1                                                                        | Chybný popis pole<br>Upřesnění.                                                                                                                                                                    | Příklad opraven.                                                                                                                                                                                                                                                                                |
| 1.6.0       | 24.2.2017           | 3.1<br>5.2.5<br>5.3.2                                                        |                                                                                                                                                                                                    | Nový dataset Karetní transakce<br>z POS terminálů nebo Platební brányobchodníka                                                                                                                                                                                                                 |
| 1.6.1       | 30.3.2017           | 5.2.5                                                                        | Chybná struktura dotazu,<br>obsahovala řetězec pos                                                                                                                                                 | Opraveno na merchant.                                                                                                                                                                                                                                                                           |
| 1.6.2       | 3.5.2017            | 6.3.1                                                                        | XML příkaz platba do ČR                                                                                                                                                                            | Změněno na XML Příkaz platba<br>v rámci ČR                                                                                                                                                                                                                                                      |
| 1.6.3       | 9.11.2017           | 5.3.1.1                                                                      | Fio XML                                                                                                                                                                                            | Přidán odkaz na xsd s číselníky                                                                                                                                                                                                                                                                 |
| 1.6.4       | 14.12.2017          | 6.3.1                                                                        | Zrychlená platba - payment type 431004                                                                                                                                                             | Vymazána z dokumentace                                                                                                                                                                                                                                                                          |
| 1.6.5       | 17.4.2018           | 6.3.1<br>6.3.2<br>6.3.3<br>6.4.1<br>6.4.2                                    | Změna znaku " ve<br>vzorových příkladech                                                                                                                                                           | Nahrazeno znakem,,                                                                                                                                                                                                                                                                              |
| 1.6.6       | 31.10.2018          | 5.2.5                                                                        | Chybná struktura dotazu,<br>chybějící část rest                                                                                                                                                    | Struktura dotazu opravena                                                                                                                                                                                                                                                                       |
| 1.6.7       | 31. 10.2018         | 6.4.1                                                                        |                                                                                                                                                                                                    | Přidáno upozornění o polích<br>`<BIC></BIC>` a `<BIC Or BEI></BIC Or BEI>`                                                                                                                                                                                                                      |
| 1.6.8 1.6.9 | 10.1.2019 24.1.2019 | 5.3.2.2 5.2.6                                                                | Chybný typ formátu u<br>atributu autorizationNumber                                                                                                                                                | Opraveno na 10x Nový příkaz pro zjištění čísla<br>posledního vytvořeného oficiálního<br>výpisu                                                                                                                                                                                                  |
| 1.6.10      | 26.6.2019           | 5.3.1.6                                                                      |                                                                                                                                                                                                    | Rozšíreny informace v tabulce<br>`Struktura TransactionList` o `ID<br>sloupce`                                                                                                                                                                                                                  |
| 1.6.11      | 7.11.2019           | 4.                                                                           |                                                                                                                                                                                                    | Přidán datový typ i                                                                                                                                                                                                                                                                             |
| 1.6.12      | 7.11.2019           | 6.3.1                                                                        | Chybný typ formátu u<br>atributu comment (255x) a<br>messageForRecipient<br>(140x)                                                                                                                 | Opraveno na 255i a 140i                                                                                                                                                                                                                                                                         |
| 1.6.13      | 8.11.2019           | 5.3.1.1                                                                      | Chybný typ formátu u<br>Názvu protiúčtu (255x)<br>Název banky (255x)<br>Uživ. Identifikace (255x)<br>Zpráva pro příjemce (140x) Typ (255x)<br>Provedl (50x)<br>Upřesnění (255x)<br>Komentár (255x) | Opraveno na 255i<br>Opraveno na 255i<br>Opraveno na 255i<br>Opraveno na 140i<br>Opraveno na 255i<br>Opraveno na 50i<br>Opraveno na 255e<br>Opraveno na 255i                                                                                                                                     |
| 1.6.14      | 8.11.2019           | 5.3.1.2                                                                      | Chybný typ formátu u<br>atributu NAME (32x)                                                                                                                                                        | Opraveno na 32i                                                                                                                                                                                                                                                                                 |
| 1.6.15      | 8.11.2019           | 5.3.1.4                                                                      | Chybný typ formátu u<br>Názvu protiúčtu (255x)<br>Název banky (255x)<br>Uživ. Identifikace (255x)<br>Zpráva pro příjemce (140x) Typ (255x)<br>Provedl (50x)<br>Komentár (255x)                     | Opraveno na 255i<br>Opraveno na 255i<br>Opraveno na 255i<br>Opraveno na 140i<br>Opraveno na 255i<br>Opraveno na 50i<br>Opraveno na 255i                                                                                                                                                         |
| 1.6.16      | 8.11.2019           | 5.3.1.5.                                                                     | Chybný typ formátu u<br>Názvu protiúčtu (255x)<br>Název banky (255x)<br>Uživ. Identifikace (255x)<br>Zpráva pro příjemce (140x) Typ (255x)<br>Provedl (50x)<br>Komentár (255x)                     | Opraveno na 255i<br>Opraveno na 255i<br>Opraveno na 255i<br>Opraveno na 140i<br>Opraveno na 255i<br>Opraveno na 50i<br>Opraveno na 255i                                                                                                                                                         |
| 1.6.17      | 18.11.2019          | 5.3.1.1<br>5.3.1.4<br>5.3.1.5                                                | Chybný typ fromátu u<br>Upřesnění                                                                                                                                                                  | Opraveno na 255i                                                                                                                                                                                                                                                                                |
| 1.6.18      | 18.11.2019          | 6.1                                                                          |                                                                                                                                                                                                    | U parametru status v odpovědi na<br>dávku přidány výsledky jednotlivých<br>stavů                                                                                                                                                                                                                |
| 1.6.19      | 15.12.2019          | 5.2.6                                                                        | Chyba v struktuře příkazu                                                                                                                                                                          | Statemen opraven na statement                                                                                                                                                                                                                                                                   |
| 1.6.20      | 03.1.2020           | 5.1.                                                                         | Přidány nové typy plateb                                                                                                                                                                           | Okamžité platby                                                                                                                                                                                                                                                                                 |
| 1.6.21      | 13.2.2020           | 5.3.1.9                                                                      |                                                                                                                                                                                                    | Doplněno upozornění na změnu<br>oddělovačů u VS, SS a KS                                                                                                                                                                                                                                        |
| 1.6.22      | 17.4.2020           | 8.6                                                                          |                                                                                                                                                                                                    | Přidán nový chybový stav status<br>code 413                                                                                                                                                                                                                                                     |
| 1.6.23      | 22.4.2020           | 5.3.1.8                                                                      | Nové umístnění dokumentůna stránce sbaonline.sk                                                                                                                                                    | Upravení odkazů na nejnovější<br>umístění dokumentů                                                                                                                                                                                                                                             |
| 1.6.24      | 22.4.2020           | 6.3.2<br>6.3.3                                                               | Špatný formát parametru<br>comment                                                                                                                                                                 | Změněno z 255x na 140e                                                                                                                                                                                                                                                                          |
| 1.6.25      | 22.4.2020           | 6.3.3                                                                        | Špatný formát parametru<br>comment                                                                                                                                                                 | Změněno z 12n na 140e                                                                                                                                                                                                                                                                           |
| 1.6.26      | 5.8.2020            | 6.3.1                                                                        |                                                                                                                                                                                                    | Doplněna informace o možnosti<br>cizoměnových převodů v rámci Fia.                                                                                                                                                                                                                              |
| 1.6.27      | 11.8.2020           | 5.3.1.8<br>5.3.1.9                                                           | Nové umístnění dokumentůna stránkách sbaonline.sk a cbaonline.cz                                                                                                                                   | Upravení odkazů na nejnovější<br>umístění dokumentů                                                                                                                                                                                                                                             |
| 1.6.28      | 7.10.2020           | 5.3.1.1<br>5.3.1.6                                                           | Přidán nový atribut                                                                                                                                                                                | Reference plátce                                                                                                                                                                                                                                                                                |
| 1.7         | 9.4.2021            | 8.5                                                                          |                                                                                                                                                                                                    | Aktualizace postupu Firefox a<br>chrome                                                                                                                                                                                                                                                         |
| 1.7.1       | 13.7.2021           | 5.3.1.2<br>5.3.1.5<br>5.3.1.6<br>5.3.1.8<br>5.3.1.9<br>6.1<br>6.4.1<br>6.4.2 | Nefunkční odkazy na<br>externí subjekty                                                                                                                                                            | Odkazy odstraněny z dokumentace                                                                                                                                                                                                                                                                 |
| 1.7.2       | 20.7.2021           | 6.3.1                                                                        | Chybný typ formátu u<br>bankCode (18d)                                                                                                                                                             | Opraveno na 4!n                                                                                                                                                                                                                                                                                 |
| 1.7.3.      | 2.2.2022            | 5.3.2                                                                        | Doplnění elementu VS                                                                                                                                                                               | Nová položka                                                                                                                                                                                                                                                                                    |
| 1.7.4.      | 16.8.2022           | 6.3.1<br>6.3.2<br>6.3.3<br>6.4.1<br>6.4.2                                    | Oprava chybného typu<br>uvozovek v záhlaví příkladů                                                                                                                                                | Uvozovky " znak ASCII 34                                                                                                                                                                                                                                                                        |
| 1.7.5       | 17.2.2023           | 6.3.4                                                                        | Doplněno označení<br>odkazovaného odstavce                                                                                                                                                         | Doplněno číselné označení 6.3.4                                                                                                                                                                                                                                                                 |
| 1.7.6       | 20.3.2023           | 5.3.2.1<br>5.3.2.2                                                           | Přidány nové atributy                                                                                                                                                                              | flexibleCommission<br>Poplatek vydavatele karty                                                                                                                                                                                                                                                 |
| 1.7.7       | 26.07.2023          | 2<br>3.1<br>8.7                                                              | Přidány informace o<br>omezení přístupu k datům<br>za období starší než 90 dní.                                                                                                                    | Doplněné informace<br>Návod k získání dat starších 90 dnů<br>Informace k chybě 422                                                                                                                                                                                                              |
| 1.8         | 17.5.2024           | 5.1<br>5.2<br>6                                                              | Doplnění nových typů<br>platby<br>Úprava původní struktury<br>dotazů:<br><https://www.fio.cz/ibapi/>                                                                                               | Doplněny typy pohybu 44 a 45<br>Nová struktura:<br><https://fioapi.fio.cz/v1/>                                                                                                                                                                                                                  |
| 1.9         | 15.10.2025          | 6.3<br>6.4.1                                                                 |                                                                                                                                                                                                    | Doplnění nových typů platby                                                                                                                                                                                                                                                                     |
