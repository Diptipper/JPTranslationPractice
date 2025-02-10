@echo off

:: your prompt for the story
set prompt=A hero flirting with a female demon lord.

:: set to true if you want to make your story longer
set is_long=true

:: which gpt model you want to use? (default is gpt-4o-mini)
set model=gpt-4o-mini

:: Your OpenAI API key
set api_key=

:: ---------------------------------------------------------------------------------------
if "%is_long%"=="true" (
    set long_option=--long
) else (
    set long_option=
)
wsl python3 story_generator.py "%prompt%" %long_option% --api_key %api_key% --model %model%

pause
