import os
import numpy as np
from sqlalchemy.orm import Session
from models import Founder
from sklearn.metrics.pairwise import cosine_similarity
import openai
from dotenv import load_dotenv

dotenv_path = "C:/Users/Aarav/Downloads/CC_Hackethon-main/CC_Hackethon-main/.env"
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def encode_text(text):
    response = openai.Embedding.create(input=text, model="text-embedding-ada-002")
    return np.array(response["data"][0]["embedding"])

def match_founders(founder_id: int, db: Session):
    all_founders = db.query(Founder).all()
    current_founder = db.query(Founder).filter(Founder.id == founder_id).first()
    
    if not current_founder:
        return {"error": "Founder not found"}

    current_vector = encode_text(" ".join(current_founder.skills) + " " + " ".join(current_founder.experience))
    scores = [(f, cosine_similarity([current_vector], [encode_text(" ".join(f.skills) + " " + " ".join(f.experience))])[0][0]) 
               for f in all_founders if f.id != founder_id]

    # Return top 5 matches
    best_matches = sorted(scores, key=lambda x: x[1], reverse=True)[:5]
    matches = [{"name": match[0].name, "job_title": match[0].job_title, "linkedin_url": match[0].linkedin_url, "compatibility_score": match[1]} for match in best_matches]

    return {"matches": matches} if matches else {"message": "No match found"}