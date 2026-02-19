# Inkomsten Belasting 

__De jaarlijkse belasting invul oefeningen zijn er weer.__
Ik heb al jaren geleden  een spreadsheet gemaakt met VBA routines om snel het e.e.a na te rekenen.
Maar VBA onderhouden is een uitdaging op zich, bovendien stonden alle getalletjes in de code en dat was ook niet optimaal. 
Nu met chatgpt en deepseek ben ik eens in Python gedoken.
Met deze code als resultaat.
De belangrijkste dingen staan nu in classes 

1. class LoonbelastingCalculator  
2. class VermogensBelastingCalculator
3. class HeffingskortingCalculator
4. class ArbeidskortingCalculator
5. class PremiesVolksverzekeringen
6. class EigenWoningForfaitCalculator
7. class OuderenKorting
8. class TariefAanpassingEigenWoning

Alle getalletjes staan in eenSQLite dabase mijn_belastingen.db die je eenvoudig kunt aanmaken met create_tax_database.py. getallen staan erin vanaf 2020 t/m 2025. 2026 is voorbereid als kopie van 2025. 
De getallen staan in diverse tabellen nl:
- tax_loonheffing
- tax_heffingskorting
- tax_arbeidskorting
- tax_vermogensbelasting
- tax_premies_volksverzekeringen
- tax_box3
- tbl_eigenwoningforfait
- tbl_ouderenkorting
- tbl_tarief_aanpassing

AOW zit erin zowel voor en na 1946. Krijg je midden in het jaar AOW; die berekening zit er (nog) niet in.

Box2 zit er (nog) niet bij 

# Hoe gebruik je het:
Start het programma op met main-belastingen.py. Er opent zich een GUI screen aan de linkerkant van het scherm.
Dit scherm bevat 3 tabs General, Primary en Partner.
Vul de benodigde invoer in en druk op calculate

Parameters om de verdeling te berekenen worden aan de eerste persoon gehangen. De tweede persoon wordt uitgerekend
- deel_box1  voor aftrek schulden eigen woning
- deel_box3  voor het deel dat je voor rekening neemt in box3
- deel_div  voor het deel dat je eventuele dividend belasting voor je rekening neemt.

# Berekenings Modus: Normal (1) vs Beste Verdeling (2) vs Loop Salaris(3) (zie belastingen.py)
- Program Setting Mode 1: Normal

Als bij general program settings normal invoert rekent het programma met de opgegeven verdeling. 

- Program Setting Mode 2: Beste verdeling

Wanneer je kiest voor beste verdeling. Gaat het programma de beste verdeling zoeken voor deel_box1, deel_box3 en deel_div
Het geheel wordt met stapjes van 0.1 van 0-1.0 doorgerekent, voor ieder deel dus 10^3 berekeningen. Dat geeft je een aardig beeld waar ongeveer de optimale verdeling zit.
Aangezien het een flink aantal berekeningen zijn duurt het ff (bij mij 30 s). G

Als je geen partner hebt worden alle parameters op 1 gezet en wordt het zoeken naar de beste verdeling overgeslagen.

- Program Setting Mode 3: Loop salaris (controle kortingsgrafieken)

Gebruik: Kies deze modus en druk op calculate. 
Ik was even vergeten dat ik deze er ingezet had. Meer ter controle van de database en nog niet perfect zie ik nu.
Deze modus loopt met stapjes van 1000 euro richting de 120000 (geen partner en geen AOW ongeacht input)
En creert een tabbed graph om te zien of de data van de kortingen redelijk consistent zijn. 
- Inkomen vs Loonheffing 
- Inkomen vs Arbeidskorting en Heffingskorting
- Inkomen vs Premies

Ouderenkorting werkt nog niet 
Dit is wel nuttig dus ik ga hier binnenkort nog wat tijd aan besteden en uitbreiden.

# To-Do 
Is het compleet? Nee vast niet, maar bij mijn opgaven inclusief partner ging het binnen €10 goed.

En hoewel ik met git werk heb ik er eigenlijk geen compleet beeld van wat allemaal mogelijk is. 
Ben met pensioen heb tijd zat maar het moet wel leuk blijven.  
Niettemin wil ik graag bijleren van de jongere talenten

In de laatste update heb ik geprobeerd wat input checks erop los te laten.
Ben er nog niet echt tevreden mee maar het schijnt te werken.

Ieder opbouwend commentaar is uiteraard welkom. 




