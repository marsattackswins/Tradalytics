import streamlit as st
import pandas as pd
import plotly.graph_objs as go

# Title
st.set_page_config(page_title="Trading Journal Analytics", layout="wide")
st.title("Trading Journal Analytics (Interactive)")

# Load CSV
df = pd.read_csv('Free Trading Journal DB 20a776d92d078137a4ccfeaa4b1081bd_all.csv')

# Clean and preprocess
df['Date'] = pd.to_datetime(df['Date (GMT+1)'].str.replace(' - ', ' ', regex=False), errors='coerce')
df = df.sort_values('Date')
df['P/L'] = df['P/L'].replace({r'\$':'', ',':''}, regex=True).astype(float)
df['W/L'] = df['W/L'].str.strip()

# Calculate equity from $2,000 starting balance
initial_equity = 2000
df['Equity'] = initial_equity + df['P/L'].cumsum()

# --- Summary Stats Block ---
# Calculate stats
wins = (df['W/L'] == 'W').sum()
losses = (df['W/L'] == 'L').sum()
total_trades = wins + losses
win_pct = (wins / total_trades * 100) if total_trades > 0 else 0
loss_pct = (losses / total_trades * 100) if total_trades > 0 else 0
avg_win = df.loc[df['W/L'] == 'W', 'P/L'].mean() if wins > 0 else 0
avg_loss = df.loc[df['W/L'] == 'L', 'P/L'].mean() if losses > 0 else 0

# Custom CSS for stat blocks (no vw units, just for color/rounded look)
st.markdown('''
    <style>
    .summary-block {
        background: #23272e;
        border-radius: 20px;
        padding: 18px 40px 18px 40px;
        margin-bottom: 10px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        font-family: 'Segoe UI', sans-serif;
        color: #b0b3c2;
        font-weight: 500;
        min-width: 180px;
        width: 100%;
        text-align: center;
    }
    .summary-label {
        color: #b0b3c2;
        font-size: 18px;
        letter-spacing: 1px;
    }
    .summary-value-win {
        color: #3fffa8;
        font-size: 26px;
        font-weight: 600;
        margin-left: 8px;
    }
    .summary-value-loss {
        color: #ff4b5c;
        font-size: 26px;
        font-weight: 600;
        margin-left: 8px;
    }
    .summary-value-neutral {
        color: #3fffa8;
        font-size: 26px;
        font-weight: 600;
        margin-left: 8px;
    }
    .summary-value-avg-loss {
        color: #ff4b5c;
        font-size: 26px;
        font-weight: 600;
        margin-left: 8px;
    }
    .winrate-label, .winrate-value {
        width: 100%;
        text-align: center;
        display: block;
    }
    .winrate-label {
        color: #b0b3c2;
        font-size: 22px;
        font-weight: 500;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    .winrate-value {
        color: #b0b3c2;
        font-size: 32px;
        font-weight: 600;
        letter-spacing: 1px;
        width: 100%;
        text-align: center;
        display: block;
    }
    .summary-block-winrate {
        background: #23272e;
        border-radius: 20px;
        padding: 40px 40px 50px 40px;
        margin-bottom: 10px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        font-family: 'Segoe UI', sans-serif;
        color: #b0b3c2;
        font-weight: 500;
        min-width: 180px;
        width: 100%;
        text-align: center;
    }
    .circle-percentage {
        width: 90px;
        height: 90px;
        border-radius: 50%;
        border: 8px solid #90caf9;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #23272e;
        margin: 0 auto;
    }
    </style>
''', unsafe_allow_html=True)

# Use Streamlit columns for layout
col_left, col_winrate, col_right = st.columns([2,1.2,2])

with col_left:
    st.markdown(f'''<div class="summary-block"><span class="summary-label">WINS</span> <span class="summary-value-win">{wins}</span></div>''', unsafe_allow_html=True)
    st.markdown(f'''<div class="summary-block"><span class="summary-label">LOSSES</span> <span class="summary-value-loss">{losses}</span></div>''', unsafe_allow_html=True)

with col_winrate:
    winrate_display = f"{win_pct:.0f}%" if total_trades > 0 else "-"
    st.markdown(f'''
        <div class="summary-block-winrate">
            <span class="winrate-label">WIN RATE</span>
            <div class="circle-percentage"><span class="winrate-value">{winrate_display}</span></div>
        </div>
    ''', unsafe_allow_html=True)

with col_right:
    st.markdown(f'''<div class="summary-block"><span class="summary-label">AVG W</span> <span class="summary-value-neutral">{int(avg_win) if avg_win else 0}</span></div>''', unsafe_allow_html=True)
    st.markdown(f'''<div class="summary-block"><span class="summary-label">AVG L</span> <span class="summary-value-avg-loss">{int(avg_loss) if avg_loss else 0}</span></div>''', unsafe_allow_html=True)

# --- Wins and Losses by Market (Grouped Bar Chart) ---
st.subheader("W&L by Market")
market_stats = df.groupby('Market').agg(
    Wins = ('W/L', lambda x: (x == 'W').sum()),
    Losses = ('W/L', lambda x: (x == 'L').sum()),
).sort_values('Wins', ascending=False)
markets = market_stats.index.tolist()
fig_bar = go.Figure()
fig_bar.add_trace(go.Bar(
    x=markets,
    y=market_stats['Wins'],
    name='Wins',
    marker_color='#90caf9',
    offsetgroup=0,
    hovertemplate='%{y} wins<extra></extra>'
))
fig_bar.add_trace(go.Bar(
    x=markets,
    y=market_stats['Losses'],
    name='Losses',
    marker_color='#F4BB44',
    offsetgroup=1,
    hovertemplate='%{y} losses<extra></extra>'
))
fig_bar.update_layout(
    barmode='relative',
    xaxis_title='',
    yaxis_title='Number of Trades',
    template='plotly_dark',
    plot_bgcolor='#23272e',
    paper_bgcolor='#23272e',
    font=dict(color='#e0e0e0'),
    margin=dict(l=40, r=40, t=60, b=40),
    height=500,
)
fig_bar.update_yaxes(separatethousands=True)
st.plotly_chart(fig_bar, use_container_width=True)

# --- P&L by Market (Positive/Negative Bar Chart) ---
st.subheader("P&L by Market")
pnl_by_market_bar = df.groupby('Market')["P/L"].sum().reset_index()
pnl_by_market_bar = pnl_by_market_bar.sort_values('P/L', ascending=False)
bar_colors_market = [
    '#90caf9' if v >= 0 else '#F4BB44' for v in pnl_by_market_bar['P/L']
]
fig_market_bar = go.Figure()
fig_market_bar.add_trace(go.Bar(
    x=pnl_by_market_bar['Market'],
    y=pnl_by_market_bar['P/L'],
    marker_color=bar_colors_market,
    text=pnl_by_market_bar['Market'],
    textposition='outside',
    hovertemplate='$%{y:,.2f}<extra></extra>',
))
fig_market_bar.update_layout(
    xaxis_title='',
    yaxis_title='P&L',
    template='plotly_dark',
    plot_bgcolor='#23272e',
    paper_bgcolor='#23272e',
    font=dict(color='#e0e0e0'),
    margin=dict(l=40, r=40, t=60, b=40),
    height=600,
    showlegend=False,
)
fig_market_bar.update_xaxes(showticklabels=False)
fig_market_bar.update_yaxes(tickprefix="$", separatethousands=True, zeroline=True)
st.plotly_chart(fig_market_bar, use_container_width=True)

# --- P&L per Trade (Line Chart) ---
st.subheader("P&L per Trade")
fig_pnl = go.Figure()
fig_pnl.add_trace(go.Scatter(
    x=list(range(1, len(df['P/L'])+1)),
    y=df['P/L'],
    mode='lines',
    name='P&L per Trade',
    line=dict(color='#90caf9', width=2),
    line_shape='spline',
    hovertemplate='<b>Trade #%{x}</b><br>P&L: $%{y:,.0f}<extra></extra>'
))
fig_pnl.add_shape(type="line", x0=1, x1=len(df['P/L']), y0=0, y1=0, line=dict(color="white", width=1.5, dash="dash"))
fig_pnl.update_layout(
    xaxis_title='Trade #',
    yaxis_title='P/L',
    template='plotly_dark',
    plot_bgcolor='#23272e',
    paper_bgcolor='#23272e',
    font=dict(color='#e0e0e0'),
    margin=dict(l=40, r=40, t=60, b=40),
    height=500,
    showlegend=False,
)
fig_pnl.update_yaxes(tickprefix="$", separatethousands=True)
st.plotly_chart(fig_pnl, use_container_width=True)

# --- Interactive Equity Curve ---
st.subheader("Equity Curve")
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=list(range(1, len(df['Equity'])+1)),
    y=df['Equity'],
    mode='lines',
    name='Equity Curve',
    line=dict(color='#90caf9', width=2),
    line_shape='spline',
    hovertemplate='<b>Trade #%{x}</b><br>Equity: $%{y:,.0f}<extra></extra>'
))
fig.update_layout(
    xaxis_title='Trade #',
    yaxis_title='Equity',
    template='plotly_dark',
    plot_bgcolor='#23272e',
    paper_bgcolor='#23272e',
    font=dict(color='#e0e0e0'),
    margin=dict(l=40, r=40, t=60, b=40),
    height=500,
    showlegend=False,
)
fig.update_yaxes(tickprefix="$", separatethousands=True)
st.plotly_chart(fig, use_container_width=True)

# Optionally, show the raw data table
toggle = st.checkbox("Show raw data table")
if toggle:
    st.dataframe(df[['Date', 'Market', 'P/L', 'Equity']])

st.markdown("---")
st.markdown("Made with Streamlit & Plotly. Extend this app for more analytics!") 