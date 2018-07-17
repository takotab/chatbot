== auto_huren
Op welke manier wilt u de juiste auto kiezen?
+$button aantal passagiers
-> auto_huren.aantal_passagiers
+$button jaartal
-> auto_huren.jaartal

= aantal_passagiers
Met hoeveel passagiers wilt u op reis gaan?
+$button 1-2
-> auto_huren.kleine_auto

+$button 3-5
-> auto_huren.grote_auto

= jaartal
Hoe nieuw wilt u uw auto hebben?
+$button Vóór 2000
-> auto_huren.oud

+$button Na 2000
-> auto_huren.nieuw

= kleine_auto
We hebben deze opties aan kleine auto's beschikbaar. Welke heeft uw voorkeur?
+$button opel corsa
Bedankt voor uw keuze. De auto staat voor u gereed
~ intent = ""
-> intent_direct

+$button Ford fiesta
Bedankt voor uw keuze. De auto staat voor u gereed
~ intent = ""
-> intent_direct

= grote_auto
We hebben deze opties aan grote auto's beschikbaar. Welke heeft uw voorkeur?
+$button opel astra
Bedankt voor uw keuze. De auto staat voor u gereed
~ intent = ""
-> intent_direct

+$button volvo V60
Bedankt voor uw keuze. De auto staat voor u gereed
~ intent = ""
-> intent_direct

= nieuw
We hebben deze opties aan nieuwe auto's beschikbaar. Welke heeft uw voorkeur?
+$button Tesla model S
Bedankt voor uw keuze. De auto staat voor u gereed
~ intent = ""
-> intent_direct

+$button BMW 3 serie
Bedankt voor uw keuze. De auto staat voor u gereed
~ intent = ""
-> intent_direct

= oud
We hebben deze opties aan oude auto's beschikbaar. Welke heeft uw voorkeur?
+$button Ford focus
Bedankt voor uw keuze. De auto staat voor u gereed
~ intent = ""
-> intent_direct

+$button Audi A3
Bedankt voor uw keuze. De auto staat voor u gereed
~ intent = ""
-> intent_direct