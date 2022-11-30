
from flask import Flask, request, jsonify
from fetch import fire
import json

app = Flask(__name__)

@app.route('/createapi', methods=['POST'])
def create_api():
	content_type = request.headers.get('Content-Type')
	count = fire.call('taxicounter')

	if count == None:
		fire.send('taxicounter', 1000)

	count = fire.call('taxicounter')
	uid = count+1
	fire.send('taxicounter', uid)
	_path = f"taxiwars/{uid}"

	if content_type == 'application/json':
		content = request.json
		
		content['unique_ID'] = uid
		fire.send(_path, content)
		return content, 201
		

@app.route('/updateapibyid/<uid>', methods=['PUT'])
def update_api_by_id(uid):
	content_type = request.headers.get('Content-Type')
	_path = f"taxiwars/{uid}"
	jsondata = fire.call(_path)

	if jsondata == None:
		return jsonify({
			'error' : {
				'description' : f'Unique ID {uid} not Found in Database.'
			}
		})

	elif content_type == 'application/json':
		content = request.json

		try:
			jsondata['fname'] = content['fname']
		except:
			pass

		try:
			jsondata['lname'] = content['lname']
		except:
			pass

		try:
			jsondata['age']   = content['age']
		except:
			pass

		fire.send(_path, jsondata)
		return jsondata, 201

	else:
		return jsonify({
			'error' : {
				'description' : f'content_type = {content_type} is not Supported.'
			}
		})


@app.route('/getallapis')
def get_all_apis():
	content = fire.call('taxiwars')
	content = json.dumps(content)
	return content, 200


@app.route('/getapibyid/<uid>')
def get_api_by_id(uid):
	_path = f"taxiwars/{uid}"
	content = fire.call(_path)

	if content == None:
		return jsonify({
			'error' : {
				'description' : f'Unique ID {uid} not Found in Database.'
			}
		})

	else:
		content = json.dumps(content)
		return content, 200


@app.route('/deleteapibyid/<uid>', methods=['DELETE'])
def delete_api_by_id(uid):
	_path = f"taxiwars/{uid}"

	if fire.call(_path) == None:
		fire.send('taxicounter', 1000)
		return jsonify({
			'message' : {
				'description' : f'Unique ID {uid} was not found in Database.'
			}
		})

	else:
		fire.send(_path, {})
		return jsonify({
				'message' : {
					'description' : f'Unique ID {uid} has been deleted from Database.'
				}
			})


if __name__ == '__main__':
	app.run(debug = True)
