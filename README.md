# Inkomsten Belasting 
Only for dutch citizens.
Niks is meer frusterend als techneut om te zien dat er in de financiele sector geen vrije 
programmas bestaan om iets na te rekenen. Neem nou de inkomstenbelasting, ieder jaar weer een 'leuk' tijdverdrijf.
En ieder jaar verbaas ik me erover hoe je nu op een optimale verdeling komt. Ga je zoeken op internet heb je de volgende opties
Of je beland op website waar je voor een randdebiel wordt gehouden zo simpel zijn die en die je op je zakrekenmachine beter kunt doen.
Of je moet een of ander abonnement afsluiten om resultaten te krijgen. 

Ik heb al jaren geleden  een spreadsheet gemaakt met VBA routines om snel het e.e.a na te rekenen.
Maar VBA onderhouden is een uitdaging op zich. Nu met chatgpt en deepseek ben ik eens in Python gedoken.
Met deze code als resultaat.

Hoe gebruik je het:
Je gegevens invullen in de functions_input.py file 
Voor een berekening met de gegevens die je hebt ingevuld gebruik je het programma main_ib.py
Voor een optimale verdelings berekening gebruik je het programma main_verdeling.py daar ee rekent het programma met drie verdelingen parameters.
deel_box1  voor aftrek schulden eigen woning
deel_box3  voor het deel dat je voor rekeneing neemt in box3
deel_div  voor het deel dat je eventuele dividend belasting voor je rekening neemt.
Het geheel wordt met stapjes van 0.5 van 0-1.0 doorgerekent dus 21^3 berekeningen. Dat geeft je een aardig beeld waar ongeveer de optimale verdeling zit.
Aangezien het ±9300 berekeningen zijn duurt het ff (bij mij 30 s)

Als je geen partner hebt worden alle parameters op 1 gezet. En dien je alleen main_ib.py te gebruiken.

Alle belasting gegevens zitten in een sqlite database (bijgevoegd) inclusief een .py om de database te creeren.
Box1 inclusief de heffingskortingen, ouderen korting, arbeidskorting zitten erin
Box3 de nieuwe methode zit erin.
Alle gegevens vanaf 2020 t/m 2024 heb ik geprobeerd erin te zetten er zitten vast nog wel wat type foutjes in. Niettemin was ik verbaast 
hoe het e.e.a overeen kwam met de bdienst.
Box2 heb ik niet toegevoegd. 

Is het compleet? Nee vast niet, maar bij mijn opgaven inclusief partner ging het binnen €10 goed.

En hoewel ik met git werk heb ik er eigenlijk geen compleet beeld van wat allemaal mogelijk is. 
Ben met pensioen heb tijd zat maar het moet wel leuk blijven.  
Niettemin wil ik graag bijleren van de jongere talenten

Ik ga vast nog de input (tkinter) en output verbeteren, tevens kan de verdelings berekening wel wat efficienter.
Eveneens is  de controle op input gegegevens is ver ondermaats. 
Maar ja je moet iets te wensen overhouden.

Ik ben opgegroeid met traditioneel programmeren(fortran en pascal) dus classes en dictionaries was voor mij allemaal niuw. 
Ieder opbouwend commentaar is uiteraard welkom. 

Voor 2024 heeft het mij weer geholpem.! 



