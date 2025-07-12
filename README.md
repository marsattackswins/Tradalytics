# Trading Journal Analytics

A powerful Streamlit web application for interactive analysis and visualization of trading journal data. Gain deep insights into your trading performance with comprehensive analytics, equity curves, P&L breakdowns, and win/loss statistics.

## 🚀 Features

### Interactive Dashboards
- **W&L by Market:** Stacked bar chart showing wins and losses for each trading market
- **P&L by Market:** Color-coded bar chart displaying profit/loss per market (positive in light blue, negative in golden yellow)
- **P&L per Trade:** Line chart tracking individual trade performance over time
- **Equity Curve:** Interactive chart monitoring account equity growth from a $2,000 starting balance

### Key Analytics
- Real-time data processing and visualization
- Custom hover tooltips with formatted currency values
- Dark theme optimized for trading environments
- Responsive design that adapts to different screen sizes
- Optional raw data table for detailed inspection

## 📊 Data Requirements

Your CSV file should contain the following columns:
- `Date`: Trade date and time
- `Market`: Trading instrument/market name
- `P/L`: Profit/Loss amount (with $ symbol and commas)
- `W/L`: Win/Loss indicator ('W' for wins, 'L' for losses)

## 🛠️ Setup

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/marsattackswins/Demo.git
   cd Demo
   ```

2. **Install required dependencies:**
   ```bash
   pip install streamlit pandas plotly
   ```

3. **Prepare your data:**
   - Place your trading journal CSV file in the project directory
   - Update the filename in `interactive_trading_journal.py` if needed (currently set to `'Free Trading Journal DB 20a776d92d078137a4ccfeaa4b1081bd_all.csv'`)

## 🎯 Usage

1. **Start the application:**
   ```bash
   streamlit run interactive_trading_journal.py
   ```

2. **Access the dashboard:**
   - Open your web browser
   - Navigate to the URL provided by Streamlit (typically `http://localhost:8501`)

3. **Interact with the charts:**
   - Hover over data points for detailed information
   - Use the interactive features to explore your trading data
   - Toggle the "Show raw data table" checkbox to view underlying data

## 📁 File Structure

```
Demo/
├── interactive_trading_journal.py    # Main Streamlit application
├── analyze_trading_journal.py        # Additional analysis script
├── Free Trading Journal DB *.csv     # Trading journal data
├── README.md                         # This file
```

## 🎨 Customization

### Chart Colors
- **Positive P&L:** Light blue (`#90caf9`)
- **Negative P&L:** Golden yellow (`#F4BB44`)
- **Wins:** Light blue (`#90caf9`)
- **Losses:** Golden yellow (`#F4BB44`)

### Starting Balance
The equity curve calculation uses a $2,000 starting balance. You can modify this in the code:
```python
initial_equity = 2000  # Change this value as needed
```

## 🔧 Technical Details

### Dependencies
- **Streamlit:** Web application framework
- **Pandas:** Data manipulation and analysis
- **Plotly:** Interactive charting library

### Data Processing
- Automatic date parsing and sorting
- Currency formatting and cleaning
- Cumulative equity calculation
- Market-specific aggregations

## 📈 Sample Output

The application generates several key visualizations:
- Stacked bar charts for win/loss analysis
- Color-coded P&L charts by market
- Time-series equity curves
- Individual trade performance tracking

## 🤝 Contributing

Feel free to extend this application with additional features:
- Risk metrics and drawdown analysis
- Portfolio allocation charts
- Trading session analysis
- Export functionality for reports

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Credits

Built with:
- [Streamlit](https://streamlit.io/) - Web app framework
- [Plotly](https://plotly.com/python/) - Interactive charts
- [Pandas](https://pandas.pydata.org/) - Data analysis

---

**Happy Trading! 📈**
