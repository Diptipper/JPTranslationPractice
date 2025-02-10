# JPTranslationPractice
Use ChatGPT to generate a story for Japanese practice

## Requirements
- Get Python. I recommend installing it in [WSL](https://learn.microsoft.com/en-us/windows/wsl/install) instead of in the windows environment.
- An [OpenAI API key](https://platform.openai.com/docs/pricing). you need to pay for the token credits, tho.
- Get the OpenAI package

## How to use
There are 4 files
- story_generator.py: This is the Python script that does most of the things
- script.js: Javascript for the webpage.
- style.css: Also for the webpage.
- run.bat: For WSL users---optional. You can run with the console if you want.

If you use the console, run the script with
```
python story_generator.py <your prompt> --long --api_key <your key> --model <gpt model>
```
- `<your prompt>`: basic summary of the story you want
- `--long`: This is optional. Omit it if you want a shorter story.
- `--api_key <your key>`: the key you get from OpenAI (the long ass string)
- `--model <gpt model>`: By default is `gpt-4o-mini`. It's a cheap model that does the job well enough.

Example:
```
python story_generator.py "A hero flirting with a female demon lord." --long --api_key xxxyyyzzz123
```

If you use WSL, just modify the parameters in run.bat, then click the file.

## Output
The code will take a few minutes to generate the result. Sometimes it will fail and restart. This happens when the model generates bad results.

You will get a HTML file `index.html` and a folder `data`. Click on the HTML file to use it. There are two sections. The first section is a Japanese passage. Each word can be hovered and it will show a furigana reading and its meaning. When you scroll to the bottom, there is a button that shows the full translation of the passage.
