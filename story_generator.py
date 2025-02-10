import argparse
import os
import re
import time

parser = argparse.ArgumentParser()
parser.add_argument('prompt', type=str)
parser.add_argument('--long', action='store_true')
parser.add_argument('--api_key', type=str)
parser.add_argument('--model', default="gpt-4o-mini", type=str)
args = parser.parse_args()

folder_name = "data"

from openai import OpenAI
client = OpenAI(api_key=args.api_key)

def main():

	output = ""
	failed = True

	os.makedirs(folder_name, exist_ok=True)

	while failed:
		#-------------------------------------------------------------------
		print("Prompt:",args.prompt,"(long)" if args.long else "(short)")
		#-------------------------------------------------------------------
		print("Generating a story...",end="")
		t0 = time.time()
		if True:
			prompt = get_story_about(args.prompt)
			output = ask_gpt(prompt)

			#has_english = bool(re.search(r'[A-Za-z]', output))

			with open(os.path.join(folder_name, "raw.txt"), "w", encoding="utf-8") as file:
				file.write(output.replace("\n", os.linesep))

			#if not has_english:
			#	break
		t1 = time.time()
		print("[",t1-t0," s]")

		#-------------------------------------------------------------------
		print("Translating...",end="")
		t0 = time.time()
		if True:
			prompt = translate(output)
			translation = ask_gpt(prompt)
			translation = translation.replace("。",".")

			with open(os.path.join(folder_name, "translate.txt"), "w", encoding="utf-8") as file:
				file.write(output.replace("\n", os.linesep))
		t1 = time.time()
		print("[",t1-t0," s]")

		#-------------------------------------------------------------------
		print("Processing the result...",end="")
		t0 = time.time()
		if True:
			prompt = process_words(output)
			output = ask_gpt(prompt)
			output = output.replace(".","。")
			output = modify_string(output)

			if not ("[" in output or "]" in output) :
				# the opposite happens when the translation is not faithful
				failed = False

			with open(os.path.join(folder_name, "processed.txt"), "w", encoding="utf-8") as file:
				file.write(output.replace("\n", os.linesep))
		t1 = time.time()
		print("[",t1-t0," s]")

	html = """
		<!DOCTYPE html>
		<html lang="en">
		<head>
		    <meta charset="UTF-8">
		    <meta name="viewport" content="width=device-width, initial-scale=1.0">
		    <title>Translation practice</title>
		    <link rel="stylesheet" type="text/css" href="style.css">
		</head>
		<body>
		<h1>Translation practice</h1>
		<p>By Diptip (via <i>"""+args.model+"""</i>)</p>
		<hr>
		<center>
		<content>
	"""
	html += output.replace("---", "<br>").replace(os.linesep, "<br>")
	html += """
		</content>
		<button class="toggle-btn" onclick="toggleBox()">Toggle translation</button>
		<br><br>
		<div class="box" id="box">
	"""
	html += translation.replace("---", "<br>").replace(os.linesep, "<br>")
	html += """
		</div>
		<hr>
		<p>By Diptip (via <i>"""+args.model+"""</i>)</p>
		</center>
		<script src="script.js"></script>
		</body>
		</html>
	"""
	with open("index.html","w", encoding="utf-8") as file:
		file.write(html)

	print()
	print("Done. Open [index.html]")

def ask_gpt(prompt):
	completion = client.chat.completions.create(
			model=args.model,
			store=True,
			messages=[
				{"role": "user", "content": prompt}
			]
		)
	return completion.choices[0].message.content

def modify_string(input_string):
	#This is used to prepare the HTML file

    # Regex to match the pattern [xxx;yyy;zzz]
    pattern = r'\[([\w\s]*);([^\[\]]*)\]'

    # Find all matches in the string
    matches = list(re.finditer(pattern, input_string))
    
    # Initialize the output string
    modified_string = input_string

    # Process the matches in reverse order to avoid affecting earlier parts of the string
    for match in reversed(matches):
        regex = match.group(0)
        xxx = match.group(1)
        yyy = match.group(2)
        
        xxx_no_spaces = ''.join(xxx.split())

        # Use rfind on input_string, comparing the string without spaces
        index = modified_string.rfind(xxx_no_spaces, 0, match.start())
        jndex = index + len(xxx_no_spaces)
        mid_i = modified_string.rfind(regex, 0, -1)
        mid_j = mid_i + len(regex)

        if index != -1:
            # When found, modify the string by wrapping the matched portion with <note> tag
            middle_string = input_string[jndex:mid_i]
            if yyy[-1]==";":
            	yyy = yyy[:-1]
            value = yyy.replace(";","; ").replace("  "," ")
            
            if yyy.split(";")[0]==xxx:
            	value = value[len(xxx)+2:]
            value = re.sub(r"'|″|″|“|”|‘|’|〝|〟|\"", "&apos;", value)
            value = re.sub(r"\.|․", "。", value)

            modified_string = modified_string[:index] + f"<note value='{value}'>{xxx}</note>" +middle_string+ modified_string[match.end():]
    modified_string = re.sub(r"\.|․", "。", modified_string)
    return modified_string

def get_story_about(theme="a boy playing with his pet"):
	story_size = "long" if args.long else "short"
	prompt = """
		Please write a """+story_size+""" story about """+theme+""", in japanese
		Just give me the story without your reply and story title.
		日本語で書いてください.
		"""
	return prompt

def process_words(story):
	prompt = """
		In the following string, For EVERY word, add a bracket [the original word;its furigana reading;meaning].
		I repeat, EVERY word! For example,
		犬と遊んでいた。 is replaced by 犬[犬;いぬ;dog]と遊んで[遊んで;あそんで;play]いた。
		Just give me the replaced string. Don't add any extra comments.
		The string:
		"""+"\""+story.replace(os.linesep,"---")+"\""
	return prompt

def translate(story):
	prompt = """
		Translate this into english. Don't add any extra comments.:
		"""+"\""+story.replace(os.linesep,"---")+"\""
	return prompt

main()