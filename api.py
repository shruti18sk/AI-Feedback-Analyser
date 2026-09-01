from google import genai
from fastapi import FastAPI
from google.genai import types
from pydantic import BaseModel,Field
from typing import Literal
from dotenv import load_dotenv
load_dotenv()

client=genai.Client()

class Review(BaseModel):
  text:str
  
class Analysis(BaseModel):
  sentiment:Literal["positive", "negative", "neutral"] #review sentiment
  score: int=Field(ge=1, le=5) #from 1(very bad) to 5(very good)
  theme:str  #what the review is about (e.g. oneword (delivery))
  confidence: int=Field(ge=0, le=100)
  status:Literal["needs_attention", "resolved", "satisfied"]
  insight:str
  keywords:list[str]
  

app=FastAPI()
@app.post('/analyze', response_model=Analysis)

def analyzefunc(review:Review):
  response=client.models.generate_content(model='gemini-3.5-flash', contents=f"""Analyze this customer review given: {review.text}\n 
               Sentiment should be classified into either 'positive' or 'negative' or 'neutral'\n 
               Score should be given from 1 to 5, where 1 is very bad while 5 is very good\n 
               Theme must be ONE lowercase word for the main topic. For example: delivery, taste, price, service quality.\n 
               confidence:Give a confidence score from 0 to 100 representing how confident you are in your sentiment, score, theme, and overall analysis.Higher value means higher confidence.\n status:Determine the current status of the customer's experience based on the review.Use only one of the allowed status values defined in the response schema.\n insight:Provide a short and useful business insight based on the review.Mention the main positive point, negative point, or area that needs improvement.Keep it concise and specific to the review.\n keywords:Extract the most important words or short phrases from the review that represent its main topics.Return 3-5 relevant keywords.Do not include unnecessary or generic words.Base all fields strictly on the customer's review and do not make assumptions beyond the information provided.""",
  config=types.GenerateContentConfig(response_mime_type='application/json', response_schema=Analysis,),)
  
  return response.parsed