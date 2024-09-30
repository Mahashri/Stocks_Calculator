import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import numpy_financial as npf
import warnings
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta




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
        return np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, None
    
    start_price = get_stock_price_on_date(stock_symbol, start_date)
    end_price = get_stock_price_on_date(stock_symbol, end_date)
    
    if pd.isna(start_price) or pd.isna(end_price):
        print(f"Error: Unable to retrieve stock prices for {start_date} or {end_date}.")
        return np.nan, np.nan, np.nan, np.nan, np.nan, start_price, end_price, np.nan, None

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
    
    xirr =((currentValue - totalInvested) / totalInvested) * 100; # Annualized return percentage
    
    overall_return_percentage = ((end_price - start_price) / start_price) * 100
    sip_returns_profit = current_value - total_invested
    overall_profit_amount = end_price - start_price
    
    # Calculate duration
    start_date_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_dt = datetime.strptime(end_date, '%Y-%m-%d')
    duration = relativedelta(end_date_dt, start_date_dt)

    duration_str = f"{duration.years} years, {duration.months} months, {duration.days} days"

    return current_value, total_invested, xirr, overall_return_percentage, start_price, end_price, sip_returns_profit, overall_profit_amount, duration_str

@app.route('/')
def form():
    today = datetime.today()
    start_date = today.replace(year=today.year - 1).strftime('%Y-%m-%d')
    end_date = today.strftime('%Y-%m-%d')
    return render_template('form.html', start_date=start_date, end_date=end_date)

@app.route('/results', methods=['POST'])
def results():
    stock_symbol = request.form.get('stock_symbol').upper()
    sip_amount = float(request.form.get('sip_amount', 1000))  # Default value of 1000 if not provided
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')

    # Automatically append .NS if not present
    if not stock_symbol.endswith('.NS'):
        stock_symbol += '.NS'

     # Generate logo URL based on stock symbol
    if stock_symbol.startswith('DIVISLAB'):
        logo_url = "https://cdn.freelogovectors.net/wp-content/uploads/2020/09/divis-laboratories-logo.png"
    elif stock_symbol.startswith('DRREDDY'):
        logo_url = "https://cdn.freelogovectors.net/wp-content/uploads/2020/09/dr-reddys-laboratories-logo.png"
    elif stock_symbol.startswith('TMB'):
        logo_url = "https://moneyorbit.in/wp-content/uploads/2022/09/Tamilnad-Merc-Bank-IPO-1.jpg"    
    elif stock_symbol.startswith('TITAN'):
        logo_url = "  https://cdn.freelogovectors.net/wp-content/uploads/2023/10/titan-company_logo_freelogovectors.net_-640x474.png"  

    elif stock_symbol.startswith('AMBUJACEM'):
        logo_url = " https://c.ndtvimg.com/2023-05/kkabrsqg_ambuja-cement_625x300_02_May_23.jpg"
    elif stock_symbol.startswith('SHREECEM'):
        logo_url = " https://cdn.freelogovectors.net/wp-content/uploads/2020/08/shree_cement_logo.png"    
    elif stock_symbol.startswith('ULTRACEMCO'):
        logo_url = " https://cdn.freelogovectors.net/wp-content/uploads/2020/09/ultratech-cement-logo-180x175.png"
    elif stock_symbol.startswith('ACC'):
        logo_url = "   https://cdn.freelogovectors.net/wp-content/uploads/2020/09/acc-limited-logo-180x62.png"
        
    elif stock_symbol.startswith('GLENMARK'):
        logo_url = "  https://cdn.freelogovectors.net/wp-content/uploads/2020/09/glenmark-logo-180x85.png"   
    
    elif stock_symbol.startswith('SUNPHARMA'):
        logo_url = " https://cdn.freelogovectors.net/wp-content/uploads/2020/08/sun-pharma-logo-180x180.png"  
    elif stock_symbol.startswith('NATCOPHARM'):
        logo_url = "  https://cdn.freelogovectors.net/wp-content/uploads/2020/09/natco-pharma-logo-180x79.png" 
        
    elif stock_symbol.startswith('GOLDBEES'):
        logo_url = "https://th.bing.com/th/id/OIP.e1MsY9sKoXTFxvXMoYAf0wAAAA?rs=1&pid=ImgDetMain"
    elif stock_symbol.startswith('GOLD1'):
        logo_url = "https://th.bing.com/th/id/OIP.u212LfA11ebqafh_hd9F3QAAAA?rs=1&pid=ImgDetMain"
        
    elif stock_symbol.startswith('TATAGOLD'):
        logo_url = "https://i.pinimg.com/originals/70/ad/d5/70add5912c3cdb2a4a7179598768ad4f.jpg"    
        
    elif stock_symbol.startswith('TATASTEEL'):
        logo_url = "   https://cdn.freelogovectors.net/wp-content/uploads/2020/09/tata_steel_logo-180x23.png"
    elif stock_symbol.startswith('TATACONSUM'):
        logo_url = " https://cdn.freelogovectors.net/wp-content/uploads/2022/12/tata_consumer_products_logo-freelogovectors.net_-180x19.png"   
    elif stock_symbol.startswith('CANBK'):
        logo_url = "https://clipground.com/images/canara-bank-logo-clipart-5.png"
        
    elif stock_symbol.startswith('VBL'):
        logo_url = "https://www.stockgro.club/blogs/wp-content/uploads/2023/11/Varun-Baverages-1024x516.png"
    elif stock_symbol.startswith('TRENT'):
        logo_url = " https://imgnew.outlookindia.com/public/uploads/articles/2021/11/3/trent-ltd.jpg"
    elif stock_symbol.startswith('HEROMOTOCO'):
        logo_url = "https://cdn.freelogovectors.net/wp-content/uploads/2023/05/hero_motors_logo-freelogovectors.net_-180x113.png"
    elif stock_symbol.startswith('SBIN'):
        logo_url = "  https://cdn.freelogovectors.net/wp-content/uploads/2023/08/sbi-logo-freelogovectors.net_-180x113.png"
        
    elif stock_symbol.startswith('ITC'):
        logo_url = " https://cdn.freelogovectors.net/wp-content/uploads/2020/08/itc-logo.png"
    elif stock_symbol.startswith('VEDL'):
        logo_url = "https://cdn.freelogovectors.net/wp-content/uploads/2020/09/vedanta_logo-180x37.png"



    
    else:
        logo_url = f"https://logo.clearbit.com/{stock_symbol[:-3].lower()}.com"  # Removing .NS

    current_value, total_invested, xirr, overall_return_percentage, start_price, end_price, sip_returns_profit, overall_profit_amount, duration_str = calculate_sip_returns(stock_symbol, sip_amount, start_date, end_date)
    
    # Format values to two decimal places
    formatted_start_price = f"{start_price:.2f}" if not pd.isna(start_price) else "N/A"
    formatted_end_price = f"{end_price:.2f}" if not pd.isna(end_price) else "N/A"
    formatted_total_invested = f"{total_invested:.2f}"
    formatted_current_value = f"{current_value:.2f}"
    formatted_xirr = f"{xirr:.2f}"
    formatted_overall_return_percentage = f"{overall_return_percentage:.2f}"
    formatted_sip_returns_profit = f"{sip_returns_profit:.2f}"
    formatted_overall_profit_amount = f"{overall_profit_amount:.2f}"

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
                          sip_returns_profit=formatted_sip_returns_profit,
                          overall_profit_amount=formatted_overall_profit_amount,
                          duration=duration_str,
                          logo_url=logo_url)

@app.route('/nse_stocks')
def nse_stocks():
    with open('nse_stocks.json') as f:
        stock_data = json.load(f)
    return jsonify(stock_data)

if __name__ == '__main__':
    app.run(debug=True)
