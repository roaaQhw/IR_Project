import json

from flask import Flask, request, jsonify

app = Flask(__name__)

with open('lifestyle_suggestions.json', 'r') as file:
    data = file.readlines()

available_queries = []

for line in data:
    suggestion = json.loads(line)
    available_queries.append(suggestion['query'])

print(available_queries)



@app.route('/suggest_lifestyle', methods=['POST'])
def suggest_query():
    query = request.json.get('query', '')
    suggested_queries = [q for q in available_queries if query.lower() in q.lower()]
    return jsonify(suggested_queries)

if __name__ == '__main__':
    app.run(port=5001)


