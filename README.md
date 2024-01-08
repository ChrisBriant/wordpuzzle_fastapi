# WORD PUZZLE

##This is a simple back end to handle a puzzle game where a user guesses a randomly selected word

### Uses a word list to generate a random list of words then selects on word and the user has to guess the correct word.

### It has an enpoint to create the word list and an endpoint to check the word against the stored one on the database. Visit http://localhost:8000/docs# for details.


TO RUN API

uvicorn main:app --reload

URL = http://localhost:8000/docs#


DOCUMENTATION:

https://fastapi.tiangolo.com/#installation

Run the UVICORN server

uvicorn main:app --reload


SQL Lite

https://www.sqlitetutorial.net/sqlite-python/insert/


Useful documentation

https://fastapi.tiangolo.com/tutorial/response-model/