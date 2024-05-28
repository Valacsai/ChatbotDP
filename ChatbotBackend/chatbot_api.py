from flask import Flask, request, jsonify, redirect
import json
from werkzeug.utils import secure_filename
from flask_cors import CORS
from chatbot_logic import ChatBot
from storage.database_functions import DatabaseFunctions
from logic.chatbot_train import ConversationTrainer
from helpers.constants import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, FILE_SIZE_LIMIT
import os

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = FILE_SIZE_LIMIT

adapter = DatabaseFunctions()
adapter.create_database()

bot = ChatBot('Chatbot', storage = adapter, chatbot_learn = True)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    bot_response = bot.find_answer(user_input)
    return jsonify({'response': str(bot_response)})

@app.route('/username', methods=['POST'])
def change_username():
    new_username = request.json.get('username')
    if not new_username:
        return jsonify({'error': 'Username is required'}), 400
    with open('helpers/settings.json', 'r') as file:
        settings = json.load(file)
    settings['username'] = new_username

    with open('helpers/settings.json', 'w') as file:
        json.dump(settings, file, indent=4)
    return jsonify({'username': new_username})

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return jsonify({'message': 'File uploaded successfully', 'file_path': file_path})
    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/username', methods=['GET'])
def get_username():
    try:
        with open('helpers/settings.json', 'r') as file:
            settings = json.load(file)
            return jsonify({'username': settings['username']})
    except FileNotFoundError:
        return jsonify({'username': "User"})
    
@app.route('/train', methods=['POST'])
def train_bot():
    trainer = ConversationTrainer(bot)
    try:
        trainer.train(trainer.process_files_in_folder())
        return jsonify({'message': 'successful'})
    except Exception:
        return jsonify({'message': 'training failed'})

@app.route('/clear', methods=['POST'])
def clear_bot_data():
    adapter.drop_tables()
    return jsonify({'message': 'data cleared'})


@app.route('/histories', methods=['GET'])
def get_histories():
    histories = adapter.get_all_histories()
    return jsonify({'histories': [history_record_to_dict(history) for history in histories]})

@app.route('/history/<int:history_id>', methods=['GET'])
def get_history_id(history_id):
    history = adapter.get_history(history_id)
    if history is None:
        return jsonify({'error': 'History not found'}), 404
    return jsonify({'history': history.to_dict()})

@app.route('/history', methods=['POST'])
def add_history():
    data = request.get_json()
    history_entries = data.get('history')
    history_id = adapter.create_history(history_entries)
    return jsonify({'message': 'History created successfully', 'id': history_id}), 201

@app.route('/history', methods=['PUT'])
def update_history():
    data = request.get_json()
    history_entries = data.get('history')
    history_id = data.get('id')
    if not history_entries or not isinstance(history_entries, list):
        return jsonify({'error': 'Invalid or missing history entries'}), 400
    success = adapter.update_history(history_id, history_entries)
    if (success): 
        return jsonify({'message': 'History updated successfully'}), 201
    else:
        return jsonify({'error': 'History update failed'}), 400

@app.route('/delete_history', methods=['POST'])
def delete_history():
    history_id = request.json.get('id')
    adapter.delete_history(history_id)
    return jsonify({'message': 'History deleted successfully'}), 202

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def history_record_to_dict(history_record):
    return {
        'id': history_record.id,
        'history': history_record.history,
        'created_at': history_record.created_at.isoformat() if history_record.created_at else None,
        'last_updated': history_record.last_updated.isoformat() if history_record.last_updated else None
    }

if __name__ == '__main__':
    app.run(debug=True, port=5000)