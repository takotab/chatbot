VAR context_meeting = false
VAR attendees_known = false
VAR meeting_ids = ""
VAR _location = ""
VAR _date = ""
VAR _time = ""
VAR _link_meeting = ""
VAR _duration = 30


== meeting ==
Met wie wilt u een meeting organiseren?
* Sales
~ meeting_ids = "sales"
~ attendees_known = true
* Roger van Dalen en Tako Tabak
~ meeting_ids = "team_ai"
~ attendees_known = true
* Tako Tabak en Walter Snel
~ meeting_ids = "team_dl"
~ attendees_known = true
\\ wanneer?

{attendees_known == true: -> meeting.attendees_known}
Ik heb niet begrepen met wie u een afspraak wilt maken.
-> variablesetting

= attendees_known
$plan_meeting
Ik ga een meeting met {meeting_ids} organiseren in {_location} {_date} om {_time} van {_duration} minuten.
* $button You rock! Do it!
-> meeting.do_it
\\ * $button other time
\\ -> meeting.do_it
* $button stupid bot je zit fout
~ attendees_known = false

-> variablesetting

= do_it
$make_meeting
De meeting is gepland. Hier is een link naar de afspraak: {_link_meeting}

-> variablesetting
