== function_weather ==

=call
//{synthesis: -> nlp_synthesis.weather}
{not nlp_loc_defined:
Waar en wanneer precies?
$wait,1,nlp_loc,context_sql_lookup,context_sql_change,context_sql_count
->function_weather.call
}
$weather,{nlp_loc},{nlp_time}
-> function_weather.output

=output
{Dus, het|Het|Ik heb het nagevraagd, en het|Het} weer {~is volgens de voorspelling|||} in {nlp_loc} {nlp_time} zal {~||vermoedelijk} zijn {f_weather} en {~de op het moment|de momenteel|de} verwachte temperatuur is {f_temperature}.// %nlp_loc:{nlp_loc}%nlp_time:{nlp_time}
// -> variablesetting //aangepast voor synthesis

//debug we wachten hier ff
$wait,1,nlp_loc,nlp_time,context_sql_lookup,context_sql_change,context_sql_count
-> intent_direct