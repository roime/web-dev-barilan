from flask import Flask,request
import calc

app = Flask(__name__)

@app.route('/calculate',methods=['POST'])
def calculate():
    if request.method == 'POST':
        data = request.get_json()
        input = data.get("input")
        state = data.get("calculatorState")
        return calc.calculateNextState(state,input)

if __name__ == "__main__":
    app.run(port=3000,host='localhost')