from flask import Flask, render_template, request, jsonify
import pandas as pd, os, warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)
CSV = 'Electricity Bill.csv'

def load_csv():
    df = pd.read_csv(CSV)
    df.columns = df.columns.str.strip()
    df = df.rename(columns={
        'Customer_ID':        'Customer ID',
        'Units_Consumed':     'Units Consumed',
        'Num_Appliances':     'No. of Appliances',
        'Hours_Used_Per_Day': 'Hours / Day',
        'Monthly_Bill_INR':   'Bill Amount (₹)'
    })
    return df

@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        d = request.get_json()
        u = float(d['units'])
        a = float(d['appliances'])
        h = float(d['hours'])
        bill = round(u * 3.5 + a * h * 12 + 50, 2)
        cat = "Low" if bill < 600 else "Medium" if bill < 1500 else "High"
        return jsonify({'success': True, 'bill': bill, 'category': cat})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/dataset')
def dataset():
    try:
        df = load_csv()
        return jsonify(df.to_dict(orient='records'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/dataset/<cid>')
def dataset_row(cid):
    try:
        df = load_csv()
        row = df[df['Customer ID'].astype(str) == str(cid)]
        if row.empty: 
            return jsonify({'error': 'Not found'}), 404
        return jsonify(row.iloc[0].to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    import webbrowser
    webbrowser.open('http://127.0.0.1:5000')
    app.run(debug=False)
