== function_id ==

=begin
VAR temp_intent = ""
$write,intent,temp_intent
{function_id.firstloop == 0: -> function_id.firstloop}
-> function_id.nameseeking

=firstloop
Om je te kunnen helpen met administrative handelingen, moet ik eerst bevestigen wie je bent.
{~Hoe heet je?|Wat is je voor en achternaam?|Hoe kan ik je noemen?|Zou je me kunnen vertellen hoe je heet?}
$wait,1,nlp_f_name,nlp_l_name,intent
-> nameseeking

=nameseeking
{not nlp_f_name_defined:
{not nlp_l_name_defined:
Ik heb je voor en achternaam nodig! 
$wait,1,nlp_f_name,nlp_l_name,intent
-> nameseeking
}
}

{not nlp_f_name_defined:
En wat is je voornaam?
$wait,1,nlp_f_name,nlp_l_name,intent
-> nameseeking
}

{not nlp_l_name_defined:
En wat is je achternaam?
$wait,1,nlp_f_name,nlp_l_name,intent
-> nameseeking
}

-> names

=names

$sql_r,sql_id // dit zet user_identified op true als gevonden
{user_identified == true: -> function_id.found}
{user_identified == false: -> function_id.notfound}

=found
{user_identified == true:
Ok ik heb je gevonden in het systeem {nlp_f_name} {nlp_l_name} en je ID is {sql_id}. Dit klopt allemaal?
 + $button Jazeker
  $write,temp_intent,intent // to make sure we did not lose the intent durring this this
 -> intent_direct
 + $button Neen
 -> wrong_name

}
=notfound
Ik kan je niet vinden in het systeem als {nlp_f_name} {nlp_l_name}, klopt je naam?
+ $button Jazeker
 Dan kan ik je helaas niet helpen.
 -> initial_quickreplies
+ $button Neen
-> wrong_name
 
= wrong_name
 Exuses
 ~nlp_f_name = ""
 ~nlp_l_name = ""
 ~sql_id = ""
 ~nlp_f_name_defined = false
 ~nlp_f_name_defined = false
 Wat is dan je naam?
 -> nameseeking
