images = {}
def m(phenny, input):
	word = input.group(2)
	if word:
		word = word.split()
		if len(word) > 0:
			key = word[0]
			if key in images:
				phenny.say(images[key])
			else:
				if len(word) > 1:
					word = word[1]
					images[key] = word
					phenny.say(key + " = " + word)
				else:
					phenny.say("No value for key " + key)	
	else:
		phenny.say("-- .m <key> <value>")
m.commands = ['m']
m.priority = 'low'
