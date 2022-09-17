from flask import Flask, json, request, jsonify
import sys

app = Flask(__name__)

@app.route('/future_protest', methods = ['POST'])
def Future_protest():
    print(request.json)
    answer = {
        "version" : "2.0",
        "template" : {
            "outputs" : [
                {
                    "simpleText" : {
                        "text" : "Testing."
                    }
                }
            ]
        }
    }
    
    return jsonify(answer)
   
   
if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 5000)
    
    
    
    
#https://fourz.tistory.com/7?category=947336
