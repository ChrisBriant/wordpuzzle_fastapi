from typing import Union, List

from fastapi import FastAPI, Query, HTTPException
from typing import List
from pydantic import BaseModel
from app_database import Database
import os, json, random

app = FastAPI()

#Database
DATABASE_PATH = r"./words.db"

#Models

class WordListResponse(BaseModel):
    id: int
    words: List[str]

class WordSolutionResponse(BaseModel):
    word: str
    score: int
    correct: bool

# class Items(BaseModel):
#     list()

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


# @app.get("/items/{item_id}",response_model=Item)
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}



@app.get("/selectword", response_model=WordListResponse)
async def select_word(
  wordlength: int = Query(4, title="Word Length", ge=1, le=10),
  amount: int = Query(16, title="Word Length", ge=1, le=40)
):
  with open('words.json', 'r') as json_file:
    words_dict = json.load(json_file)
  #words_dict = json.loads('.\words.json')
  print(words_dict[str(wordlength)])
  word_list = []
  #Select three word lists
  for i in range(0,3):
    random_words = random.choice(words_dict[str(wordlength)])
    word_list = [*word_list, *random_words ]
  word_list_set = set(word_list)
  print(word_list_set)
  #Get random words from the set
  final_word_list = []
  #Check there are enough words
  if len(word_list_set) < amount:
     raise HTTPException(status_code=400, detail="There are not enough words")

  for i in range(0,amount):
    selected_word = random.choice(list(word_list_set))
    final_word_list.append(selected_word)
    word_list_set.remove(selected_word)
  print(final_word_list)
  #Pick the solution word
  solution_word = random.choice(final_word_list)
  #Store it in the database
  db_conn = Database(DATABASE_PATH)
  id = db_conn.add_word(solution_word)
  print(id)
  response = WordListResponse(id=id, words=final_word_list)
  return response


@app.get("/checkword", response_model=WordSolutionResponse)
async def check_word(
  id: int = Query(0, title="Word ID"),
  word: str = Query('', title="Word to check"
)):
  #Get the word from the database
  db_conn = Database(DATABASE_PATH)
  check_word = db_conn.get_word(id)
  if not check_word:
    raise HTTPException(status_code=404, detail="Word was not found")
  if len(word) != len(check_word):
    raise HTTPException(status_code=400, detail="Word length does not match")
  print(check_word)
  #Score the word
  #Scoring is based on the same character in the same position
  score = 0
  for i in range(0,len(word)):
    if word[i] == check_word[i]:
      score += 1
  #Check if it is the correct word
  correct =  False
  if score == len(word):
    correct = True
  response = WordSolutionResponse(word=word, score=score, correct=correct)
  #return {'word': word, 'score': score, 'correct': correct}
  return response
  
# @app.get("/allitems/",response_model=List[ItemResponse])
# def get_all_items():
#     db_conn = Database(DATABASE_PATH)
#     items = db_conn.all_items()
#     return items

# @app.put("/items/{item_id}", response_model=ItemResponse)
# def update_item(item_id: int, item: Item):
#     db_conn = Database(DATABASE_PATH)
#     success = db_conn.create_item({
#         'id': item_id,
#         'name':item.name,
#         'price': item.price,
#         'is_offer' : 'TRUE' if item.is_offer else 'FALSE'
#     })
#     print(success)
#     return {"name": item.name, "id": item_id, 'price' : item.price,'is_offer': item.is_offer}

# @app.post("/items/additem", response_model=ItemResponse)
# def add_item(item: Item):
#     db_conn = Database(DATABASE_PATH)
#     print('ITEM',item.price,item.is_offer)
#     #success= 1
#     success = db_conn.add_item({
#         'name':item.name,
#         'price': item.price,
#         'is_offer' : 'TRUE' if item.is_offer else 'FALSE'
#     })
#     print(success)
#     return {"id": success, "name": item.name,'price' : item.price,'is_offer': item.is_offer}