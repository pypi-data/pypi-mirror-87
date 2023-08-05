Hvad er Protector API?
------------------------------------------
papi er en API wrapper, 
der samler en masse brugbare,
danske api'er i simple python funktioner.


Sådan anvendes Protector API
---------------------------------------------------
(Husk at kopiere 'papi' til din egen filstruktur,
der hvor du ønsker at anvende api wrapperen.)

1) importer det API du vil bruge fra papi. F.eks. 'dst' (Danmarks Statistik API)

>>> from papi import dst


2) Nu kan du kalde det importerede api's funktioner. 
(Referer til det enkelte api's dokumentation)
F.eks. har 'dst' en funktion, der henter og udskriver
metadata om et angivet datasæt fra Danmarks Statistik.

>>> dst.explore('PRIS111')

