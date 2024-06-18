import os

from flask import Flask, request, make_response, jsonify

app = Flask(__name__)

import cloudinary

cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key=os.environ.get('CLOUDINARY_API_KEY'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET'),
    secure=True,
)

'''
    Si no funciona, probar con:

    cloudinary.config(
        cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
        api_key=os.environ.get('CLOUDINARY_API_KEY'),
        api_secret=os.environ.get('CLOUDINARY_API_SECRET'),
        api_proxy = "http://proxy.server:3128"
    )
'''

import cloudinary.uploader
import cloudinary.api


@app.after_request
def after_request_func(response):
    origin = request.headers.get('Origin')
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Headers', 'x-csrf-token')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE')
        if origin:
            response.headers.add('Access-Control-Allow-Origin', origin)
    else:
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        if origin:
            response.headers.add('Access-Control-Allow-Origin', origin)

    return response


@app.route("/")
def index():
    return jsonify({'status': 200, 'message': 'Hello Flask!'}), 200


@app.route('/images/<public_id>', methods=['PUT'])
def upload_image(public_id):
    file = request.stream.read()
    try:
        response = cloudinary.uploader.upload(file, public_id=public_id, resource_type="image", overwrite=True)
        return jsonify({'message': 'file uploaded', 'url': response['secure_url']}), 200
    except Exception as error:
        return jsonify({'error': str(error)}), 500


@app.route('/images/<public_id>', methods=['GET'])
def get_image(public_id):
    try:
        response = cloudinary.api.resource(public_id, type="upload")
        return jsonify({'message': 'image retrieved', 'image': response}), 200
    except Exception as error:
        return jsonify({'error': str(error)}), 500


@app.route('/images', methods=['GET'])
def search_images():
    try:
        response = cloudinary.api.resources(type='upload')
        return jsonify({'message': 'images retrieved', "images": response['resources']}), 200
    except Exception as error:
        return jsonify({'error': error}), 500


@app.route('/images/<public_id>', methods=['DELETE'])
def delete_image(public_id):
    try:
        response = cloudinary.uploader.destroy(public_id, invalidate=True)
        if response.get('result') == 'not found':
            jsonify({'message': 'image not found', 'data': response}), 200
        return jsonify({'message': 'image deleted', 'data': response}), 200
    except Exception as error:
        return jsonify({'error': str(error)}), 500
