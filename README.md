# Plugin Backend

A scrapper was created to get the article texts and process them, creating the embeddings. This was done to gather a few articles to experiment with the recommendation model, before scaling up to te whole database.

The scrapper was used to gather aprx. 1800 articles ranging from Jan. 2015 to Dec. 2024.


Afterwards an indexed database based on Opensearch was created, with the article url, article text, and article embeddings. The recommendation system that finds similar articles employs the knn algorithm for the vector embeddings.

## Examples

1. For [this article](https://www.zdg.md/stiri/stiri-economice/oficial-preturi-mai-mari-incepand-de-astazi-la-energie-electrica-si-termica/), the recommendation system gives the following recommendations:

``` 
1. Title: Curentul electric se ieftinește pentru consumatori. ANRE a aprobat micșorarea prețurilor, Score: 0.7489982, URL: https://www.zdg.md/stiri/ultima-ora-curentul-electric-se-ieftineste-pentru-consumatori-anre-a-aprobat-micsorarea-preturilor
2. Title: SA „Energocom” a semnat un contract nou de achiziție a energiei electrice de la MGRES, Score: 0.68695515, URL: https://www.zdg.md/stiri/stiri-sociale/sa-energocom-a-semnat-un-contract-nou-de-achizitie-a-energiei-electrice-de-la-mgres
3. Title: Viceprim-ministrul Andrei Spînu, despre livrările de energie electrică pentru iulie și august: „Prețul rămâne neschimbat”, Score: 0.68401265, URL: https://www.zdg.md/stiri/stiri-sociale/viceprim-ministrul-andrei-spinu-despre-livrarile-de-energie-electrica-pentru-iulie-si-august-pretul-ramane-neschimbat
4. Title: Precizările viceprim-ministrului Andrei Spînu privind evoluția situației energetice din R. Moldova: „Nu s-a semnat contract de livrare a energiei electrice cu MGRES”, Score: 0.6709881, URL: https://www.zdg.md/stiri/stiri-sociale/precizarile-viceprim-ministrului-andrei-spinu-privind-evolutia-situatiei-energetice-din-r-moldova-nu-s-a-semnat-contract-de-livrare-a-energiei-electrice-cu-mgres        
5. Title: Ministerul Energiei: Construcția Liniei Electrice Aeriene Vulcănești – Chișinău avansează cu circa 160 de fundații finalizate, Score: 0.6489572, URL: https://www.zdg.md/stiri/ministerul-energiei-constructia-liniei-electrice-aeriene-vulcanesti-chisinau-avanseaza-cu-circa-160-de-fundatii-finalizate
6. Title: Zece mii de tone de păcură, eliberate din rezervele de stat, cu titlu de împrumut, către S.A. „Termoelectrica”, Score: 0.6248128, URL: https://www.zdg.md/stiri/stiri-economice/zece-mii-de-tone-de-pacura-eliberate-din-rezervele-de-stat-cu-titlu-de-imprumut-catre-s-a-termoelectrica
7. Title: Astăzi va fi marcată „Ora Pământului”, Score: 0.58783174, URL: https://www.zdg.md/stiri/astazi-va-fi-marcata-ora-pamantului
8. Title: Deputații sunt îndemnați să evite utilizarea ascensoarelor. Ce măsuri a luat Parlamentul pentru economisirea energiei electrice și termice, Score: 0.58518106, URL: https://www.zdg.md/stiri/deputatii-sunt-indemnati-sa-evite-utilizarea-ascensoarelor-ce-masuri-a-luat-parlamentul-pentru-economisirea-energiei-electrice-si-termice
9. Title: Premierul Filip afirmă că tarifele la gazele naturale ar putea fi reduse cu 20%, Score: 0.5839557, URL: https://www.zdg.md/stiri/politic/premierul-filip-afirma-ca-tarifele-la-gazele-naturale-ar-putea-fi-reduse-cu-20
10. Title: Dezastru ecologic: Un oraș din Rusia, inundat cu petrol, Score: 0.58180815, URL: https://www.zdg.md/stiri/stiri-externe/dezastru-ecologic-un-oras-din-rusia-inundat-cu-petrol
```

2. The search can also work with just simple prompts or sentences instead of whole articles (although are a bit less accurate). Recommendations for the user input "Universitatea Tehnică a Moldovei" are:

```
1. Title: USM și UTM ar putea deveni o singură universitate. Ministrul Educației: „Inițiativa vine din partea rectorilor”, Score: 0.5386022, URL: https://www.zdg.md/stiri/usm-si-utm-ar-putea-deveni-o-singura-universitate-ministrul-educatiei-initiativa-vine-din-partea-rectorilor
2. Title: Cine este și ce avere are înlocuitorul Lilianei Palihovici în Parlamentul R. Moldova, Score: 0.47355542, URL: https://www.zdg.md/stiri/politic/cine-este-si-ce-avere-are-inlocuitorul-lilianei-palihovici-in-parlamentul-r-moldova
3. Title: Ce spun studenții, CEC-ul, Ministerul Educației și Partidul Democrat despre lansarea lui Marian Lupu în fața Universității de Stat, Score: 0.46727467, URL: https://www.zdg.md/stiri/politic/ce-spun-studentii-cec-ul-ministerul-educatiei-si-partidul-democrat-despre-lansarea-lui-marian-lupu-in-fata-universitatii-de-stat
4. Title: Președinta Maia Sandu are o nouă consilieră în domeniul justiției, Score: 0.46489766, URL: https://www.zdg.md/stiri/presedinta-maia-sandu-are-o-noua-consiliera-in-domeniul-justitiei
5. Title: Două instituții superioare de învățământ din țară, absorbite de USM și Academia de Administrare Publică. Studenții urmează a fi transferați, Score: 0.46444172, URL: https://www.zdg.md/stiri/stiri-sociale/doc-doua-institutii-superioare-de-invatamant-din-tara-absorbite-de-usm-si-academia-de-administrare-publica-studentii-urmeaza-a-fi-transferati
6. Title: Campanie împotriva diasporei promovată intens de unele partide și propagandiști după alegerile prezidențiale, Score: 0.46063474, URL: https://www.zdg.md/stiri/stiri-sociale/campanie-impotriva-diasporei-promovata-intens-de-unele-partide-si-propagandisti-dupa-alegerile-prezidentiale
7. Title: America Bus – un centru cultural mobil, care are misiunea de a aduce valorile americane mai 
aproape de poporul moldovenesc, Score: 0.45690218, URL: https://www.zdg.md/stiri/stiri-sociale/america-bus-un-centru-cultural-mobil-care-are-misiunea-de-a-aduce-valorile-americane-mai-aproape-de-poporul-moldovenesc
8. Title: Un Centru de Informare și Documentare ONU, în incinta Bibliotecii Naționale, Score: 0.45636633, URL: https://www.zdg.md/stiri/stiri-sociale/un-centru-de-informare-si-documentare-onu-in-incinta-bibliotecii-nationale
9. Title: Marina Radvan și Virgiliu Pâslariuc ar putea deveni deputați, Score: 0.45250034, URL: https://www.zdg.md/stiri/politic/marina-radvan-si-virgiliu-paslariuc-ar-putea-deveni-deputati
10. Title: Scenarii apocaliptice despre prețul la gaz  vs deconectarea curentului chiar „de mâine”. Falsul lunii decembrie, Score: 0.42304984, URL: https://www.zdg.md/stiri/video-scenarii-apocaliptice-despre-pretul-gazului-vs-deconectarea-curentului-chiar-de-maine-falsul-lunii-decembrie
Search completed in 0.31 seconds.
```

The searches in the database take less than one second.