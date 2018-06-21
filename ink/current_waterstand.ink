VAR int_vergelijken = -1

== waterstand
// hier dus dat kenmerk verhaal van walter
= doorgeven
{user_identified == false: -> function_id}
{number > -1: -> waterstand.number_known}
Aha, u wilt uw waterstand doorgeven. Uitstekend, dat gaan we voor u regelen!
Oke. Wat is de waterstand?
$wait,1,number
-> waterstand.number_known

= number_known
Oke. Ik begrijp dat de waterstand {number} is, klopt dat?
+$button Dat klopt!
VAR dwg_water_real = -1
$write,number,dwg_water_real
$sql_w,dwg_water_real
~dwg_water_real = -1
Oke, de waterstand is doorgegeven. Bedankt.
~ intent = ""
-> intent_direct
+$button Dat klopt niet!
~ number = -1
-> waterstand.doorgeven

= vergelijken
{user_identified == false: -> function_id}
Ok, ik begrijp dat u uw watergebruik wilt vergelijken. Daar gaan we mee aan de slag.
$sql_vergelijken
{int_vergelijken == - 1: Er is iets fout gegaan -> initial_quickreplies}
{int_vergelijken > 1: De waterstand is hoger dan normaal}
{int_vergelijken < 1: De waterstand is lager dan normaal}
~ int_vergelijken = int_vergelijken * 100
je watergebruik is nu {int_vergelijken}% van het gemiddelde. 
$vergelijken_attachment
~ intent = ""
~ int_vergelijken = -1
-> intent_direct
