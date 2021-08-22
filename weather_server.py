from fastapi import FastAPI
import uvicorn
from sqlite3 import connect
from datetime import datetime
from typing import Optional
from hashlib import sha256
from pydantic import BaseModel

app = FastAPI(debug=False, docs_url=None, redoc_url=None)

class Auth(BaseModel):
     auth : str

class Search(BaseModel):
     auth : str
     search_term : str

class Entry(BaseModel):
     auth : str
     place : str
     datetime : Optional[datetime]
     temp: float
     humid : float

@app.post('/entry')
async def home(entry : Entry):
     try:
          if type(entry.auth) == str:
               if sha256(entry.auth.encode()).hexdigest() == '94c494aebbf25e1f2551121686719ff800557d5ade5af583628cd8bfe0c5c691':
                    if (type(entry.temp) == float and type(entry.humid) == float and type(entry.place) == str) or (type(entry.temp) == int and (entry.humid) == int and type(entry.place) == str):
                         if  (entry.temp) < 89.0 or (entry.humid) < 89.0 or (entry.temp) > -100 or (entry.humid) > -100:
                              if (entry.place) != 'string' and (entry.place) != 'STRING' and (entry.place) != 'str':
                                   if (entry.place) != '' and (entry.place) != 'noplace' and (entry.place) != None and 'ABCD' not in (entry.place) and 'abcd' not in (entry.place) and 'ABCDE' not in (entry.place) and 'abcde' not in (entry.place) and len(entry.place) > 3:
                                        tempe = float(entry.temp)
                                        humide = float(entry.humid)
                                        if (entry.datetime) == None:
                                             date = datetime.now()
                                        else:
                                             date = entry.datetime
                                        placee = str(entry.place)
                                        conn = connect('db.db')
                                        cursor = conn.cursor()
                                        cursor.execute("CREATE TABLE IF NOT EXISTS weather(id INTEGER PRIMARY KEY,place TEXT NOT NULL,temperature FLOAT NOT NULL, humidity FLOAT NOT NULL,date DATE NOT NULL);")
                                        vr = ("INSERT INTO weather(place,temperature,humidity,date) VALUES (?,?,?,?)")
                                        cursor.execute(vr, (placee,tempe, humide,date))
                                        conn.commit()
                                        return {"Status":"Sucess"}
                                   else:
                                        return {"Status" : "Invalid place name"}
                              else:
                                   return {"Status" : "Place name cannot be 'string' or 'STRING'"}
                         else:
                              return {"Status" : "Temperature and humidity cannot be greater than 89 or less than -100"}
                    else:
                         return {"Status" : "Temperature and humidity should be a float or an integer and place should be a string"}
               else:
                    return {"Status" : "Invalid auth token"}
          else:
               return {"Status" : "Auth token must be a string"}
     except Exception as e:
          return {"Status":"An exception occured: " + str(e)}

@app.post('/all')
async def all(entry : Auth):
     try:
          if sha256(entry.auth.encode()).hexdigest() == '94c494aebbf25e1f2551121686719ff800557d5ade5af583628cd8bfe0c5c691':
               conn = connect('db.db')
               cursor = conn.cursor()
               cursor.execute("CREATE TABLE IF NOT EXISTS weather(id INTEGER PRIMARY KEY,place TEXT NOT NULL,temperature FLOAT NOT NULL, humidity FLOAT NOT NULL,date DATE NOT NULL);")
               cursor.execute("SELECT * FROM weather")
               return cursor.fetchall()
          else:
               return {"Status" : "Invalid auth token"}
     except Exception as e:
          return {"Status":"An exception occured: " + str(e)}

@app.post('/max/temp')
async def max(entry : Auth):
     try:
          if sha256(entry.auth.encode()).hexdigest() == '94c494aebbf25e1f2551121686719ff800557d5ade5af583628cd8bfe0c5c691':
               conn = connect('db.db')
               cursor = conn.cursor()
               cursor.execute("CREATE TABLE IF NOT EXISTS weather(id INTEGER PRIMARY KEY,place TEXT NOT NULL,temperature FLOAT NOT NULL, humidity FLOAT NOT NULL,date DATE NOT NULL);")
               cursor.execute("SELECT MAX(temperature) FROM weather")
               return cursor.fetchall()
          else:
               return {"Status" : "Invalid auth token"}
     except Exception as e:
          return {"Status":"An exception occured: " + str(e)}

@app.post('/min/temp')
async def max(entry : Auth):
     try:
          if sha256(entry.auth.encode()).hexdigest() == '94c494aebbf25e1f2551121686719ff800557d5ade5af583628cd8bfe0c5c691':
               conn = connect('db.db')
               cursor = conn.cursor()
               cursor.execute("CREATE TABLE IF NOT EXISTS weather(id INTEGER PRIMARY KEY,place TEXT NOT NULL,temperature FLOAT NOT NULL, humidity FLOAT NOT NULL,date DATE NOT NULL);")
               cursor.execute("SELECT MIN(temperature) FROM weather")
               return cursor.fetchall()
          else:
               return {"Status" : "Invalid auth token"}
     except Exception as e:
          return {"Status":"An exception occured: " + str(e)}

@app.post('/search/place')
async def max(entry : Search):
     try:
          if sha256(entry.auth.encode()).hexdigest() == '94c494aebbf25e1f2551121686719ff800557d5ade5af583628cd8bfe0c5c691':
               conn = connect('db.db')
               cursor = conn.cursor()
               cursor.execute("CREATE TABLE IF NOT EXISTS weather(id INTEGER PRIMARY KEY,place TEXT NOT NULL,temperature FLOAT NOT NULL, humidity FLOAT NOT NULL,date DATE NOT NULL);")
               cursor.execute("SELECT * FROM weather WHERE ? IN date", [(entry.search_term)])
               results = cursor.fetchall()
               if results != []:
                    return results
               else:
                    return {"Status" : "No search results"}
          else:
               return {"Status" : "Invalid auth token"}
     except Exception as e:
          return {"Status":"An exception occured: " + str(e)}
     
@app.post('/search/date')
def max(entry : Search):
     try:
          if sha256(entry.auth.encode()).hexdigest() == '94c494aebbf25e1f2551121686719ff800557d5ade5af583628cd8bfe0c5c691':
               conn = connect('db.db')
               cursor = conn.cursor()
               cursor.execute("CREATE TABLE IF NOT EXISTS weather(id INTEGER PRIMARY KEY,place TEXT NOT NULL,temperature FLOAT NOT NULL, humidity FLOAT NOT NULL,date DATE NOT NULL);")
               cursor.execute("SELECT * FROM weather WHERE date = ?", [(entry.search_term)])
               results = cursor.fetchall()
               if results != []:
                    return results
               elif results == []:
                    return {"Status" : "No search results"}
               else:
                    return {"Status" : "An error occured"}
          else:
               return {"Status" : "Invalid auth token"}
     except Exception as e:
          return {"Status":"An exception occured: " + str(e)}
     

if __name__ == '__main__':
     uvicorn.run("weather_server:app", reload=True)
