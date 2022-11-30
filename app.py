
from flask import Flask, request, jsonify
from fetch import fire
import json

app = Flask(__name__)

@app.route('/start', methods=['POST'])
def create_api():

	count = fire.call('taxicounter')
	if count == None:
		fire.send('taxicounter', 1000)

	count = fire.call('taxicounter')
	uid = count+1

	fire.send('taxicounter', uid)
	_path = f"taxiwars/{uid}"

	content = {"mystring" : ""}
	content['game_ID'] = uid
	content['ispalindrome'] = False

	fire.send(_path, content)
	return content, 201


@app.route('/updateBoard/<uid>', methods=['PUT'])
def update_api_by_id(uid):

	_path = f"taxiwars/{uid}"
	content = fire.call(_path)

	if content == None:
		return jsonify({
			'error' : {
				'description' : f'Unique ID {uid} not Found in Database.'
			}
		})

	try:
		content['mystring'] += request.args.get('onechar')
		import random
		content['mystring'] += f"{random.choice('1234567890')}"

		if (len(content['mystring']) >= 6) and (content['mystring'] == content['mystring'][::-1]):
			content['ispalindrome'] = True
	except:
		pass

	fire.send(_path, content)
	return content, 201


@app.route('/listofgameapi')
def get_all_apis():
	content = fire.call('taxiwars')
	content = json.dumps(content)
	return content, 200


@app.route('/getBoard/<uid>')
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
