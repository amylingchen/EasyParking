
from flask import Flask, render_template

from main import get_parking_detail
from serializers import SuccessResponce

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/searchparkingdetail', methods=['get'])
def search_parking_detail():

    parking_detail = get_parking_detail()
    return SuccessResponce(parking_detail)


if __name__ == '__main__':
    app.run(debug=False)
