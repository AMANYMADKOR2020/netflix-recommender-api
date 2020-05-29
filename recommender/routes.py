import os
from flask import Flask, request, jsonify
from recommender.train import load_cos, recommendations,train
PICKLES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pickles")

app = Flask(__name__)

#test endpoint
@app.route("/")
def index():
    return "all is up and running"

@app.route("/train/")
def train_on():
    cos_path = os.path.join(PICKLES_PATH, "cos.pkl")
    if os.path.exists(cos_path):
        pass
    else:
        train()

        
    return jsonify ({"status":"success",    "cosine_sim":"trained"})

    


@app.route("/title", methods=['post'])
def recommend_title():
    try:
        title = request.json['title']
        top_5_rec=recommendations(title,load_cos())
            
        
        return jsonify(top_5_rec)
    except Exception as e:
        print(e)
        return jsonify({
            "status": "failed",
            "response": "Check the input json",
            "error": str(e)
            })
