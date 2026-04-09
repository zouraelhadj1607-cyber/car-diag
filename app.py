from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# تحميل قاعدة بيانات أكواد الأعطال
def load_codes():
    path = os.path.join(os.path.dirname(__file__), 'data', 'codes.json')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

CODES = load_codes()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('code', '').strip().upper()
    
    if not query:
        return jsonify({'error': 'الرجاء إدخال كود العطل'})
    
    # البحث المباشر بالكود
    if query in CODES:
        return jsonify({'result': CODES[query]})
    
    # البحث الجزئي
    results = []
    for code, data in CODES.items():
        if query in code or query in data.get('titre', ''):
            results.append(data)
    
    if results:
        return jsonify({'results': results})
    
    return jsonify({'error': f'لم يتم العثور على كود "{query}" في قاعدة البيانات'})

@app.route('/all-codes')
def all_codes():
    return jsonify(list(CODES.keys()))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
