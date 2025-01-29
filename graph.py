from flask import Flask, render_template, Response
import pandas as pd
import matplotlib.pyplot as plt
import io

app = Flask(__name__)

# Load the Excel file
def load_data():
    file_path = "/funds.csv"
    df = pd.read_excel('funds.csv')
    return df.head(5)  # Select first five funds

# SIP Calculation function
def calculate_sip(principal, rate, time):
    rate = rate / 100  # Convert percentage to decimal
    return principal * (((1 + rate) ** time) - 1) / rate

@app.route('/')
def index():
    return render_template('mutual_funds.html')

@app.route('/plot')
def plot():
    df = load_data()
    time_intervals = [1, 2, 3, 5, 10]  # Years
    sip_principal = 1000  # ₹1000 monthly investment
    
    plt.figure(figsize=(10, 6))
    for _, row in df.iterrows():
        fund_name = row["Scheme Name"]
        rates = [row["1Y"], row["2Y"], row["3Y"], row["5Y"], row["10Y"]]
        
        if all(pd.notna(rates)):
            gains = [calculate_sip(sip_principal, r, t * 12) for r, t in zip(rates, time_intervals)]
            plt.plot(time_intervals, gains, label=fund_name)
    
    plt.xlabel("Years")
    plt.ylabel("Total Amount Gained (₹)")
    plt.title("SIP Growth Over Time")
    plt.legend()
    
    # Save plot to an in-memory file
    img = io.BytesIO()
    plt.savefig('/img.png')
    img.seek(0)
    plt.close()
    
    return Response(img.getvalue(), mimetype='image/png')

if __name__ == '_main_':
    app.run(debug=True)