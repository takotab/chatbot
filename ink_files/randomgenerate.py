import codecs
import clr
import time
import sys
from random import randint


output_file = sys.argv[2]+".csv"
loop_num = sys.argv[3]
end_of_text ="XDISCONNECT"
ink_dir = "/home/roger.van.daalen/va/ink/"
ink_engine_filename = "ink-engine-runtime.dll"
ink_engine_path = ink_dir + ink_engine_filename
story_json_filename = sys.argv[1]+".json"
#story_json_filename = "choices.json"
story_json_file_path = ink_dir + story_json_filename

with codecs.open(story_json_file_path, 'r', 'utf-8-sig') as data_file:
	ink_json = data_file.read()

clr.AddReference(ink_engine_path) #import the ink-engine assembly
import Ink.Runtime
from Ink.Runtime import Story

#for i in range (100000):
ink_story = Story(ink_json) #create the instance

#openning csv file
file = open(output_file,"w")
#file.writecolumns = (['ind', 'text', 'speaker', 'f_name', 'l_name', 'b_day'])

for loop in range(int(loop_num)):
		
	ink_story = Story(ink_json) #create the instance
#	ink_story.variablesState["seednumber"] = randint(1,100000000)
	while True:
		while ink_story.canContinue:
			next = ink_story.Continue().replace(",","").replace("%%",",")
			print(next)
			if not next.__contains__(end_of_text):
				file.write(str(loop+1) + "," + next)
			
		if ink_story.currentChoices.Count >0:
			#for i in range (ink_story.currentChoices.Count):
				#print(str(i+1),".",ink_story.currentChoices[i].text)
			#print(randint(0, ink_story.currentChoices.Count-1))
			
			
			#picking random number
			ink_story.ChooseChoiceIndex(randint(0, ink_story.currentChoices.Count-1))
			
			#print(andint(0, ink_story.currentChoices.Count-1))
			
		if next.__contains__(end_of_text):
			break

file.close
