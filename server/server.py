from flask import Flask, request, jsonify
from files import FilesQueue
from tqdm import tqdm
import multiprocessing

hostName = "localhost"
serverPort = 8080

filesQueue: FilesQueue = FilesQueue()


app = Flask(__name__)


@app.route('/getFile', methods=['GET'])
def get_file():
    return jsonify({'fileName': filesQueue.getElement(request.remote_addr).__str__()})

@app.route('/setFinished', methods=['POST'])
def set_finished():
    # Simulate marking a file as finished
    finishedFile = request.json.get('fileName')
    if finishedFile is None:
        return jsonify({'error': 'Missing file ID'}), 400
      
    filesQueue.setFinished(finishedFile)
    
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True, port=serverPort, host='192.168.1.140')
