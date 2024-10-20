
from flask import Flask, render_template

from main import get_parking_detail
from serializers import SuccessResponce
from test import *

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/searchparkingdetail', methods=['get'])
def search_parking_detail():

    parking_detail = get_parking_detail()
    return SuccessResponce(parking_detail)

@app.route('/api/searchParkingCountHistory', methods=['get'])
def search_parking_count_history():

    count_history = get_parking_count_history()
    return SuccessResponce(count_history)

if __name__ == '__main__':
    app.run(debug=False)
