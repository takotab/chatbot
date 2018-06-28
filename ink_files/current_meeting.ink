VAR context_meeting = false
VAR attendeess_known = false
VAR meeting_ids = ""
VAR _location = ""
VAR _date = ""
VAR _time = ""
VAR _link_meeting = "no_link"
VAR _duration = 30
VAR start_meeting = "nu" 


== meeting ==
Met wie wilt u een meeting organiseren?
+ Devo DWG
~ meeting_ids = "DWG Devo"
~ attendeess_known = true
-> meeting.attendeess_known
+ Sales
~ meeting_ids = "Sales"
~ attendeess_known = true
-> meeting.attendeess_known
+ BM
~ meeting_ids = "BM"
~ attendeess_known = true
-> meeting.attendeess_known
+ BM + Sales
~ meeting_ids = "BM + Sales"
~ attendeess_known = true
-> meeting.attendeess_known
+ Team AI
~ meeting_ids = "Team AI"
~ attendeess_known = true
-> meeting.attendeess_known
+ Team DL
~ meeting_ids = "Team DL"
~ attendeess_known = true
-> meeting.attendeess_known
\\ wanneer?

{attendeess_known == true: -> meeting.attendeess_known}
Ik heb niet begrepen met wie u een afspraak wilt maken.
-> meeting

= attendeess_known
$plan_meeting
Ik ga een meeting met {meeting_ids} organiseren in {_location} {_date} om {_time} van {_duration} minuten.
+$button Dat is goed!
-> meeting.do_it
\\ * $button other time
\\ -> meeting.do_it
+$button Cancel
~ attendeess_known = false

-> initial_internal_customer

= do_it
$make_meeting
De meeting is gepland. Hier is een link naar de afspraak: 
{_link_meeting}

-> initial_internal_customer

//-> meeting
//debug we zijn aan het einde van de context evals

