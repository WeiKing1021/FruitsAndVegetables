import numpy as np
import pandas as pd
import os
import cv2
import matplotlib.pyplot as plt
import tensorflow
from keras.models import Sequential

IMG_SIZE=100

model: Sequential = tensorflow.keras.models.load_model('./keras_model.h5');

train_path = "./input/fruit-and-vegetable-image-recognition/train"
test_path  = "./input/fruit-and-vegetable-image-recognition/test"

categories = os.listdir(train_path)
categories.sort()

price = []

for index in range(len(categories)):
    price.append((index + 1) * 10)
    print('> Price of ' + categories[index] + ' is: ' + str(price[index]))

def predict(img) -> int:

    result = model.predict(np.array([img]))

    posible = -1
    posibleWeight = -1

    for index in range(len(result[0])):
        if (posibleWeight < result[0][index]):
            posible = index
            posibleWeight = result[0][index]

    return posible

from flask import Flask, request, Response
from flask_cors import CORS
import jsonpickle
import numpy as np
import cv2

import ssl
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

# Initialize the Flask application
app = Flask(__name__)
CORS(app)

totalPrice = 0

@app.route('/reset', methods=['GET'])
def reset():
    global totalPrice
    totalPrice = 0
    print('>>>>>>')
    print('Total price reset to 0')
    print('>>>>>>')

# route http posts to this method
@app.route('/addToCart', methods=['POST'])
def addToCart():

    r = request

    print('>>>>>>')
    print('Process purchase from request: ' + request.remote_addr)
    print('>>>>>>')

    # convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)

    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # do some fancy processing here....
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img = np.array(img) / 255

    result = predict(img);

    print('>>>>>>')
    print('The image most like to: ' + categories[result])
    print('Price: ' + str(price[result]))
    print('>>>>>>')

    global totalPrice

    totalPrice = totalPrice + price[result]

    # build a response dict to send back to client
    response = {
        'itemName': categories[result],
        'price': price[result],
        'totalPrice': totalPrice
    }

    print('>>>>>>')
    print('Total Price' + str(totalPrice))
    print('>>>>>>')
    
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")


# start flask app
app.run(host="0.0.0.0", port=5000)