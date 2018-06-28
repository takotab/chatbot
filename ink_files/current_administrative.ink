== address_change ==
-> do_you_want
=do_you_want
~ intent = "address_change"
{user_identified == false: -> function_id}
We kunnen nu als u wilt uw adres veranderen, zou u dit willen?
 + $button Jazeker
 -> address_change.change
 + $button Neen
 -> intent_direct
 
=change
$sql_r,sql_city
$sql_r,sql_street
$sql_r,sql_postcode
Uw huidige adres is {sql_street} met postcode {sql_postcode} in {sql_city}.
Waarin zou u dit willen veranderen?
$wait,1,nlp_loc,nlp_street,nlp_postcode
$wait,1,nlp_loc,nlp_street,nlp_postcode
$wait,1,nlp_loc,nlp_street,nlp_postcode
->ready

=ready
Als ik u goed heb begrepen gaat u verhuizen naar de {nlp_street} met postcode {nlp_postcode} te {nlp_loc}, zal ik dit voor u wegschrijven in onze database?
+ $button [Jazeker] Ok, bij deze heb ik het voor je verwerkt!
//    ~ sql_waiting = false
-> address_change.dirty
+ $button Nee, dat klopt niet
 Ok, kunt u het nogmaals zeggen aub?
 ->address_change.change

=dirty
$verhuizen_attachment
$write,nlp_loc,sql_city
$write,nlp_street,sql_street
$write,nlp_postcode,sql_postcode
$sql_w,sql_city
$sql_w,sql_street
$sql_w,sql_postcode
Verwerkt!
~ intent = ""
-> intent_direct

