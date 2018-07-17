INCLUDE current_global_variables.ink
INCLUDE current_vacation.ink
INCLUDE current_intent_direct.ink
INCLUDE current_weather.ink
INCLUDE current_administrative.ink // adreswijziging + vakantiedagen
//INCLUDE current_calendar.ink // vakantiedagen
INCLUDE current_meeting.ink // room booking
INCLUDE current_waterstand.ink // waterstand doorgeven en vergelijken
INCLUDE synthesis.ink // only for data synthesis
INCLUDE synthesis_randomdata.ink // only for data synthesis
INCLUDE vesta30.ink
INCLUDE current_user_id.ink
INCLUDE current_factuur.ink
INCLUDE current_auto_huren.ink

{~Hoi!|Hey!|Hallo!|Gegroet!} <>
Ik ben de Watergroep Virtual Agent!
Waarmee kan ik u {~helpen|van dienst zijn|uit de brand helpen}?
-> initial_quickreplies

== initial_quickreplies ==
// * %go Waterstand doorgeven | Watergebruik analyse | Factuur inzien | Adreswijziging | Auto huren
+ [Waterstand doorgeven] 
 ~ intent = "waterstand_doorgeven"
 -> waterstand.doorgeven
+ [Watergebruik analyse] 
 ~ intent = "waterstand_vergelijken"
 -> waterstand.vergelijken
+ [Factuur inzien] Ik begrijp dat u uw laatste factuur wilt inzien, ik pak hem er even voor u bij.
 ~ intent = "factuur"
 -> factuur
+ [Adreswijziging]
 ~ intent = "factuur"
 -> address_change
+ [Interne klant]
 -> initial_internal_customer
+ [Auto huren]
 ~ intent = "auto_huren"
 -> auto_huren

--> intent_direct // dit doet iets??

~ intent = "" // dit ook niet?

-> initial_quickreplies // als al het andere faalt, dan terug naar het menu??

== initial_internal_customer
Waar kan ik u als medewerker precies mee helpen?
+ [Kamer boeken]
 ~ intent = "meeting"
 -> meeting
+ [Vakantiedagen opvragen] Aha, u wilt weten hoe het zit met uw vakantie dagen!
 ~ intent = "vacation"
 -> vacation
+ [Het weer] Ah, u heeft een vraag over het weer
 ~ intent = "weather"
 -> function_weather.call
+ [Gezichtsherkenning] De gezichtsherkenning loopt via de camera module van Messenger, maak nu een foto!
 Stel je overigens een voor dat je met exact deze techniek in een mobiele app waterstanden middels fotos kunt doorgeven...
 -> initial_internal_customer 
 
