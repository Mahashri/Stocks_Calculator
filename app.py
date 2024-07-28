from flask import Flask, render_template, request, jsonify
import yfinance as yf
import pandas as pd
import numpy as np
import numpy_financial as npf
import warnings
import json

warnings.filterwarnings('ignore', category=UserWarning, module='yfinance')

app = Flask(__name__)

def fetch_stock_data(stock_symbol, start_date, end_date):
    stock = yf.Ticker(stock_symbol)
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date)
    return stock_data['Close']

def get_stock_price_on_date(stock_symbol, date):
    try:
        stock_data = yf.download(stock_symbol, start=date, end=pd.to_datetime(date) + pd.DateOffset(1))
        if not stock_data.empty:
            return stock_data['Close'].iloc[0]
        else:
            return np.nan
    except Exception as e:
        print(f"Error fetching stock price on {date}: {e}")
        return np.nan

def calculate_sip_returns(stock_symbol, sip_amount, start_date, end_date):
    try:
        stock_data = fetch_stock_data(stock_symbol, start_date, end_date)
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan
    
    start_price = get_stock_price_on_date(stock_symbol, start_date)
    end_price = get_stock_price_on_date(stock_symbol, end_date)
    
    if pd.isna(start_price) or pd.isna(end_price):
        print(f"Error: Unable to retrieve stock prices for {start_date} or {end_date}.")
        return np.nan, np.nan, np.nan, np.nan, np.nan, start_price, end_price

    sip_dates = pd.date_range(start=start_date, end=end_date, freq='MS')  # Monthly SIP
    stock_data.index = stock_data.index.tz_localize(None)
    sip_dates = sip_dates.tz_localize(None)
    
    sip_df = pd.DataFrame(index=sip_dates)
    sip_df['Stock Price'] = stock_data.reindex(sip_dates, method='ffill')
    sip_df['Investment Amount'] = sip_amount
    sip_df['Shares Bought'] = sip_df['Investment Amount'] / sip_df['Stock Price']
    sip_df['Total Shares'] = sip_df['Shares Bought'].cumsum()
    
    current_value = sip_df['Total Shares'].iloc[-1] * stock_data.iloc[-1]
    total_invested = sip_df['Investment Amount'].sum()
    
    cash_flows = [-sip_amount] * len(sip_df)
    cash_flows.append(current_value)
    cash_flow_dates = sip_df.index.tolist()
    cash_flow_dates.append(stock_data.index[-1])
    
    xirr = npf.irr(cash_flows) * 100  # Annualized return percentage
    
    overall_return_percentage = ((end_price - start_price) / start_price) * 100
    overall_return_amount = current_value - total_invested
    
    return current_value, total_invested, xirr, overall_return_percentage, overall_return_amount, start_price, end_price

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/results', methods=['POST'])
def results():
    stock_symbol = request.form.get('stock_symbol').upper()
    sip_amount = float(request.form.get('sip_amount', 1000))  # Default value of 1000 if not provided
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')

    # Automatically append .NS if not present
    if not stock_symbol.endswith('.NS'):
        stock_symbol += '.NS'

    current_value, total_invested, xirr, overall_return_percentage, overall_return_amount, start_price, end_price = calculate_sip_returns(stock_symbol, sip_amount, start_date, end_date)
    
    # Format values to two decimal places
    formatted_start_price = f"{start_price:.2f}" if not pd.isna(start_price) else "N/A"
    formatted_end_price = f"{end_price:.2f}" if not pd.isna(end_price) else "N/A"
    formatted_total_invested = f"{total_invested:.2f}"
    formatted_current_value = f"{current_value:.2f}"
    formatted_xirr = f"{xirr:.2f}"
    formatted_overall_return_percentage = f"{overall_return_percentage:.2f}"
    formatted_overall_return_amount = f"{overall_return_amount:.2f}"

    return render_template('index.html', 
                          stock_symbol=stock_symbol,
                          start_date=start_date,
                          end_date=end_date,
                          start_price=formatted_start_price,
                          end_price=formatted_end_price,
                          total_invested=formatted_total_invested,
                          current_value=formatted_current_value,
                          xirr=formatted_xirr,
                          overall_return_percentage=formatted_overall_return_percentage,
                          overall_return_amount=formatted_overall_return_amount)

@app.route('/nse_stocks')
def nse_stocks():
    with open('nse_stocks.json') as f:
        stock_data = json.load(f)
    return jsonify(stock_data)

if __name__ == '__main__':
    app.run(debug=True)
