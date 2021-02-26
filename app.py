from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn

app = Flask(__name__)


with open('model_pickle','rb') as f:
    mp = pickle.load(f)


@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        age = int(request.form['age'])
        bmi = float(request.form['bmi'])
        children = int(request.form['children'])
        yes = request.form['yes']
        male = request.form['gender']
        northwest = request.form['northwest']
        
        if(yes=='yes'):
                yes=1
        else:
                yes=0
            
        if(male=='male'):
            male=1
        else:
            male=0
        
        if(northwest=='northwest'):
            northwest=1
            southeast=0
            southwest=0
        elif(northwest=='southeast'):
            northwest=0
            southeast=1
            southwest=0
        elif(northwest=='southwest'):
            northwest=0
            southeast=0
            southwest=1
        else:
            northwest=0
            southeast=0
            southwest=0
            
          
        array = np.array([age,bmi,children,yes,male,northwest,southeast,southwest])    
        array = array.reshape(1,-1)   
        prediction = mp.predict(array)
        output=round(prediction[0],2)
        if output>0:
            return render_template('index.html',prediction_texts="Your medical costs are predicted to be {}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)
    