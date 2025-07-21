# Tradalytics: Interactive Trading Journal Analytics

A powerful Streamlit web app for interactive analysis and visualization of your trading journal. Gain deep insights into your trading performance with comprehensive analytics, equity curves, P&L breakdowns, and win/loss statistics.

## 🚀 Features

- **Wins & Losses by Market:** Stacked bar chart showing wins and losses for each trading market
- **P&L by Market:** Color-coded bar chart displaying profit/loss per market (positive in light blue, negative in golden yellow)
- **P&L per Trade:** Line chart tracking individual trade performance over time
- **Equity Curve:** Interactive chart monitoring account equity growth from a customizable starting balance
- Real-time data processing and visualization
- Custom hover tooltips with formatted currency values
- Dark theme optimized for trading environments
- Responsive design for all screen sizes
- Optional raw data table for detailed inspection

## 📊 Data Requirements

Your CSV file should include the following columns:
- `Date`: Trade date and time
- `Market`: Trading instrument/market name
- `P/L`: Profit/Loss amount (with $ symbol and commas)
- `W/L`: Win/Loss indicator ('W' for wins, 'L' for losses)

## 🛠️ Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/marsattackswins/Demo.git
   cd Tradalytics
   ```
2. **Install dependencies:**
   ```bash
   pip install streamlit pandas plotly
   ```
3. **Prepare your data:**
   - Place your trading journal CSV file in the project directory.
   - Update the filename in `interactive_trading_journal.py` if needed (default: `'Free Trading Journal DB 20a776d92d078137a4ccfeaa4b1081bd_all.csv'`).

## 🎯 Usage

1. **Start the application:**
   ```bash
   streamlit run interactive_trading_journal.py
   ```
2. **Open the dashboard:**
   - In your browser, go to the URL provided by Streamlit (usually `http://localhost:8501`).
3. **Explore your data:**
   - Hover over charts for details
   - Use interactive features to analyze your trading performance
   - Toggle "Show raw data table" to view the underlying data

## 📁 File Structure

```
Tradalytics/
├── interactive_trading_journal.py    # Main Streamlit application
├── README.md                         # Project documentation
├── requirements.txt                  # Python dependencies
├── tradalytics_logo.png              # Project logo
├── favicon.png                       # Favicon for the app
├── Free Trading Journal DB *.csv     # Your trading journal data
```

## 🎨 Customization

- **Chart Colors:**
  - Positive P&L / Wins: Light blue (`#90caf9`)
  - Negative P&L / Losses: Golden yellow (`#F4BB44`)
- **Starting Balance:**
  - The equity curve uses a $2,000 starting balance by default. Change this in the code:
    ```python
    initial_equity = 2000  # Edit as needed
    ```

## 🔧 Technical Details

- **Streamlit:** Web application framework
- **Pandas:** Data manipulation and analysis
- **Plotly:** Interactive charting library
- Automatic date parsing, currency formatting, and cumulative equity calculation
- Market-specific aggregations for detailed insights

## 📈 Sample Output

- Stacked bar charts for win/loss analysis
- Color-coded P&L charts by market
- Time-series equity curves
- Individual trade performance tracking

## 🤝 Contributing

Contributions are welcome! Ideas for new features include:
- Risk metrics and drawdown analysis
- Portfolio allocation charts
- Trading session analysis
- Export functionality for reports

## 📝 License

This project is open source under the MIT License.

## 🙏 Credits

Built with:
- [Streamlit](https://streamlit.io/) – Web app framework
- [Plotly](https://plotly.com/python/) – Interactive charts
- [Pandas](https://pandas.pydata.org/) – Data analysis

---

**Happy Trading! 📈**
