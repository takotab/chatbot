VAR synthesis = false
~ temp nlp_context_weather = "{~weersomstandigheden|weer|het weer|weer|de temperatuur}"
~ temp internal_loop_count = 0

== nlp_synthesis ==

= weather
+ manier van iets zeggen 1
+ manier 2
+ manier 3
-->weathercontinue

= weathercontinue
~ internal_loop_count = internal_loop_count + 1

-> function_weather.output