import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

def format_currency_compact(value):
    abs_value = abs(value)
    if abs_value >= 1_000_000:
        return f"${value/1_000_000:.1f}M"
    elif abs_value >= 1_000:
        return f"${value/1_000:.0f}k"
    else:
        return f"${int(value)}"

# Title
st.set_page_config(page_title="Trading Journal Analytics", layout="wide", page_icon="favicon.png")

# Set Streamlit page background to match dark theme
st.markdown(
    """
    <style>
    body, .stApp {
        background-color: #181818 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state
if 'data_uploaded' not in st.session_state:
    st.session_state.data_uploaded = False
if 'df' not in st.session_state:
    st.session_state.df = None

def show_upload_page():
    """Show the upload page"""
    # Streamlit-native header with logo and title
    header_col1, header_col2, header_col3 = st.columns([1, 6, 1])
    with header_col1:
        st.image("tradalytics_logo.png")
    # header_col3 is now unused
    
    # Center the content
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("## 📊 Welcome to Tradalytics")
        st.markdown("<div style='margin-bottom: 48px;'></div>", unsafe_allow_html=True)
        st.markdown(
            "Upload your CSV file with trading data to get comprehensive analytics and insights. Required columns: Date/Time, Market, Setup, P/L, W/L.")
        
        # File upload section
        uploaded_file = st.file_uploader(
            "Upload CSV",  # Non-empty label for accessibility
            type=['csv'],
            help="Upload a CSV file with columns: Date/Time column, Market, Setup, P/L, W/L",
            label_visibility="collapsed"
        )
        
        # Load CSV based on upload
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.success("✅ File uploaded successfully!")
                
                # Display data preview
                with st.expander("📋 Data Preview (click to expand)"):
                    st.write("First 5 rows of your data:")
                    st.dataframe(df.head())
                    st.write(f"Total rows: {len(df)}")
                    st.write("Columns:", list(df.columns))
                
                # Store data in session state and proceed to analysis
                st.session_state.df = df
                st.session_state.data_uploaded = True
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error reading file: {e}")
                st.info("Please check your CSV format and try again.")
        else:
            pass

def show_analysis_page():
    """Show the analysis page with all charts and metrics"""
    df = st.session_state.df
    
    # Streamlit-native header with logo and title
    header_col1, header_col2, header_col3, header_col4 = st.columns([1, 6, 1, 0.5])
    with header_col1:
        st.image("tradalytics_logo.png")
    # Position upload button at the far right edge
    with header_col4:
        if st.button("Upload"):
            st.session_state.data_uploaded = False
            st.session_state.df = None
            st.rerun()
    # header_col3 is now unused
    
    # Clean and preprocess
    # Find date column (flexible detection)
    date_columns = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
    if date_columns:
        date_col = date_columns[0]  # Use the first date column found
    else:
        date_col = 'Date (GMT+1)'  # Fallback to original column name
    
    df['Date'] = pd.to_datetime(
        df[date_col].str.replace(' \(GMT\+1\)', '', regex=True),
        errors='coerce',
        format="%B %d, %Y %I:%M %p"  # Matches 'June 4, 2025 9:41 PM' after removing timezone
    )
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

    # Calculate profit factor for summary block
    gross_profit = df.loc[df['P/L'] > 0, 'P/L'].sum()
    gross_loss = abs(df.loc[df['P/L'] < 0, 'P/L'].sum())
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0

    # Calculate risk-reward for summary block
    avg_win_abs = abs(avg_win) if avg_win else 0
    avg_loss_abs = abs(avg_loss) if avg_loss else 0
    risk_reward_ratio = avg_win_abs / avg_loss_abs if avg_loss_abs > 0 else 0

    # Calculate average trades per day
    trades_per_day = df.groupby(df['Date'].dt.date).size()
    avg_trades_per_day = trades_per_day.mean() if len(trades_per_day) > 0 else 0
    
    # Fallback calculation if the above doesn't work
    if avg_trades_per_day == 0 or pd.isna(avg_trades_per_day):
        # Calculate total trades divided by number of unique trading days
        unique_days = df['Date'].dt.date.nunique()
        avg_trades_per_day = len(df) / unique_days if unique_days > 0 else 0

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
        .summary-block-winrate {
            background: #23272e;
            border-radius: 20px;
            padding: 40px 40px 36px 40px;
            margin-bottom: 10px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
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
            font-size: 18px;
            font-weight: 400;
            margin-left: 8px;
        }
        .summary-value-loss {
            color: #ff4b5c;
            font-size: 18px;
            font-weight: 400;
            margin-left: 8px;
        }
        .summary-value-neutral {
            color: #3fffa8;
            font-size: 18px;
            font-weight: 400;
            margin-left: 8px;
        }
        .summary-value-avg-loss {
            color: #ff4b5c;
            font-size: 18px;
            font-weight: 400;
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
            margin-bottom: 0;
            margin-top: 0;
        }
        .winrate-value {
            color: #b0b3c2;
            font-size: 18px;
            font-weight: 400;
            letter-spacing: 1px;
            width: 100%;
            text-align: center;
            display: block;
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

    # Calculate streaks for the summary blocks
    def calculate_streaks(series):
        streaks = []
        current_streak = 1
        current_value = series.iloc[0]
        
        for value in series.iloc[1:]:
            if value == current_value:
                current_streak += 1
            else:
                streaks.append((current_value, current_streak))
                current_streak = 1
                current_value = value
        
        # Add the last streak
        streaks.append((current_value, current_streak))
        return streaks

    # Calculate win and loss streaks
    win_loss_series = (df['W/L'] == 'W').astype(int)
    streaks = calculate_streaks(win_loss_series)

    win_streaks = [length for value, length in streaks if value == 1]
    loss_streaks = [length for value, length in streaks if value == 0]

    # Calculate highest streaks
    highest_win_streak = max(win_streaks) if win_streaks else 0
    highest_loss_streak = max(loss_streaks) if loss_streaks else 0

    # Calculate highest win and loss
    highest_win = df.loc[df['W/L'] == 'W', 'P/L'].max() if wins > 0 else 0
    highest_loss = df.loc[df['W/L'] == 'L', 'P/L'].min() if losses > 0 else 0

    # Calculate best market for summary blocks
    best_market_row = df.groupby('Market')["P/L"].sum().sort_values(ascending=False).head(1)
    best_market = best_market_row.index[0] if not best_market_row.empty else "-"
    expectancy = (win_pct * avg_win + loss_pct * avg_loss) / 100 if total_trades > 0 else 0
    
    # Calculate drawdown for summary blocks
    df['Running Max'] = df['Equity'].expanding().max()
    df['Drawdown'] = df['Equity'] - df['Running Max']
    max_drawdown = df['Drawdown'].min()

    # Calculate recovery periods (when drawdown goes from negative to 0)
    df_sorted = df.sort_values('Date').reset_index(drop=True)
    df_sorted['DateShort'] = df_sorted['Date'].dt.strftime('%B %d')
    df_sorted['Drawdown %'] = (df_sorted['Drawdown'] / df_sorted['Running Max']) * 100
    recovery_periods = []
    current_drawdown_start = None
    for i, drawdown in enumerate(df_sorted['Drawdown']):
        if drawdown < 0 and current_drawdown_start is None:
            current_drawdown_start = i
        elif drawdown >= 0 and current_drawdown_start is not None:
            recovery_periods.append(i - current_drawdown_start)
            current_drawdown_start = None
    avg_recovery_period = sum(recovery_periods) / len(recovery_periods) if recovery_periods else 0

    # Use Streamlit columns for layout - First Row
    col_left, col_winrate, col_pnl, col_avg_trades, col_right = st.columns([2,1.2,1.2,1.2,2])

    with col_left:
        st.markdown(f'''<div class="summary-block" style="display: flex; flex-direction: row; align-items: center; justify-content: space-between; gap: 12px;"><span class="summary-label">WINS</span> <span class="summary-value-win">{wins}</span></div>''', unsafe_allow_html=True)
        st.markdown(f'''<div class="summary-block" style="display: flex; flex-direction: row; align-items: center; justify-content: space-between; gap: 12px;"><span class="summary-label">AVG WIN</span> <span class="summary-value-neutral">${int(avg_win) if avg_win else 0}</span></div>''', unsafe_allow_html=True)

    with col_winrate:
        winrate_display = f"{win_pct:.0f}%" if total_trades > 0 else "-"
        winrate_color = '#3fffa8' if win_pct > 55 else '#ff4b5c'
        st.markdown(f'''
            <div class="summary-block-winrate">
                <span class="winrate-label">WIN RATE</span>
                <span class="winrate-value" style="color: {winrate_color};">{winrate_display}</span>
            </div>
        ''', unsafe_allow_html=True)

    with col_pnl:
        total_pnl = df['P/L'].sum()
        pnl_color = '#3fffa8' if total_pnl >= 0 else '#ff4b5c'
        formatted_pnl = f"${total_pnl:,.0f}"
        st.markdown(f'''
            <div class="summary-block-winrate">
                <span class="winrate-label">TOTAL P&amp;L</span>
                <span class="winrate-value" style="color: {pnl_color}; font-size:18px;">{formatted_pnl}</span>
            </div>
        ''', unsafe_allow_html=True)

    with col_avg_trades:
        # Debug: Check if avg_trades_per_day is valid
        if pd.isna(avg_trades_per_day) or avg_trades_per_day == 0:
            avg_trades_display = "0"
            avg_trades_color = '#b0b3c2'  # default/gray
        else:
            if avg_trades_per_day < 3:
                avg_trades_color = '#3fffa8'  # green
            elif 3.1 <= avg_trades_per_day <= 4:
                avg_trades_color = '#90caf9'  # blue
            elif avg_trades_per_day > 4.1:
                avg_trades_color = '#ff4b5c'  # red
            else:
                avg_trades_color = '#b0b3c2'  # default/gray
            
            # Format to show decimal only when needed
            avg_trades_display = f"{avg_trades_per_day:.0f}" if avg_trades_per_day.is_integer() else f"{avg_trades_per_day:.1f}"
        
        st.markdown(f'''
            <div class="summary-block-winrate" style="padding-bottom: 40px;">
                <span class="winrate-label">AVG TRADES</span>
                <span class="winrate-value" style="color: {avg_trades_color};">{avg_trades_display}</span>
            </div>
        ''', unsafe_allow_html=True)

    with col_right:
        st.markdown(f'''<div class="summary-block" style="display: flex; flex-direction: row; align-items: center; justify-content: space-between; gap: 12px;"><span class="summary-label">LOSSES</span> <span class="summary-value-loss">{losses}</span></div>''', unsafe_allow_html=True)
        st.markdown(f'''<div class="summary-block" style="display: flex; flex-direction: row; align-items: center; justify-content: space-between; gap: 12px;"><span class="summary-label">AVG LOSS</span> <span class="summary-value-avg-loss">${int(avg_loss) if avg_loss else 0}</span></div>''', unsafe_allow_html=True)

    # Second Row - Aligned with first row
    col_left2, col_winrate2, col_pnl2, col_avg_trades2, col_right2 = st.columns([2,1.2,1.2,1.2,2])

    with col_left2:
        st.markdown(f'''<div class="summary-block" style="display: flex; flex-direction: row; align-items: center; justify-content: space-between; gap: 12px;"><span class="summary-label">HIGHEST WIN</span> <span class="summary-value-win">${int(highest_win) if highest_win else 0}</span></div>''', unsafe_allow_html=True)
        st.markdown(f'''<div class="summary-block" style="display: flex; flex-direction: row; align-items: center; justify-content: space-between; gap: 12px;"><span class="summary-label">WIN STREAK</span> <span class="summary-value-win">{highest_win_streak}</span></div>''', unsafe_allow_html=True)

    with col_winrate2:
        expectancy_color = '#3fffa8' if expectancy >= 50 else '#ff4b5c'  # green if >= $50, red if < $50
        st.markdown(f'''
            <div class="summary-block-winrate">
                <span class="winrate-label">EXPECTANCY</span>
                <span class="winrate-value" style="color: {expectancy_color};">${expectancy:,.2f}</span>
            </div>
        ''', unsafe_allow_html=True)

    with col_pnl2:
        rrr_color = '#3fffa8' if risk_reward_ratio >= 1.5 else '#ff4b5c'
        st.markdown(f'''
            <div class="summary-block-winrate">
                <span class="winrate-label">RRR</span>
                <span class="winrate-value" style="color: {rrr_color};">{risk_reward_ratio:.2f}</span>
            </div>
        ''', unsafe_allow_html=True)

    with col_avg_trades2:
        st.markdown(f'''
            <div class="summary-block-winrate">
                <span class="winrate-label">PROFIT FACTOR</span>
                <span class="winrate-value" style="color: #3fffa8;">{profit_factor:.2f}</span>
            </div>
        ''', unsafe_allow_html=True)

    with col_right2:
        st.markdown(f'''<div class="summary-block" style="display: flex; flex-direction: row; align-items: center; justify-content: space-between; gap: 12px;"><span class="summary-label">HIGHEST LOSS</span> <span class="summary-value-loss">${int(highest_loss) if highest_loss else 0}</span></div>''', unsafe_allow_html=True)
        st.markdown(f'''<div class="summary-block" style="display: flex; flex-direction: row; align-items: center; justify-content: space-between; gap: 12px;"><span class="summary-label">LOSS STREAK</span> <span class="summary-value-loss">{highest_loss_streak}</span></div>''', unsafe_allow_html=True)

    # Add space between summary blocks and charts
    st.markdown("<br><br>", unsafe_allow_html=True)

    # --- Wins and Losses by Market (Stacked Bar Chart) ---
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
        marker_color='#3CB371',  # medium sea green
        hovertemplate='%{y} wins<extra></extra>'
    ))
    fig_bar.add_trace(go.Bar(
        x=markets,
        y=market_stats['Losses'],
        name='Losses',
        marker_color='#ff4b5c',  # red
        hovertemplate='%{y} losses<extra></extra>'
    ))
    fig_bar.update_layout(
        barmode='stack',
        xaxis_title='',
        yaxis_title='',  # Remove y-axis label
        template='plotly_dark',
        plot_bgcolor='#181818',
        paper_bgcolor='#181818',
        font=dict(color='#e0e0e0'),
        margin=dict(l=40, r=40, t=60, b=40),
        height=500,
        bargap=0.6,  # makes bars thinner
        showlegend=False,
        hoverlabel=dict(font_size=15),
    )
    fig_bar.update_yaxes(separatethousands=True)
    fig_bar.update_xaxes(showticklabels=True, tickfont=dict(size=14))  # show labels and make them bigger
    st.plotly_chart(fig_bar, use_container_width=True)

    # --- P&L by Market (Positive/Negative Bar Chart) ---
    st.subheader("P&L by Market")
    pnl_by_market_bar = df.groupby('Market')["P/L"].sum().reset_index()
    pnl_by_market_bar = pnl_by_market_bar.sort_values('P/L', ascending=False)
    bar_colors_market = [
        '#3CB371' if v >= 0 else '#ff4b5c' for v in pnl_by_market_bar['P/L']
    ]
    fig_market_bar = go.Figure()
    fig_market_bar.add_trace(go.Bar(
        x=pnl_by_market_bar['Market'],
        y=pnl_by_market_bar['P/L'],
        marker_color=bar_colors_market,
        hovertemplate='$%{y:,.0f}<extra></extra>'
    ))
    fig_market_bar.update_layout(
        xaxis_title='',
        yaxis_title='',  # Remove y-axis label
        template='plotly_dark',
        plot_bgcolor='#181818',
        paper_bgcolor='#181818',
        font=dict(color='#e0e0e0'),
        margin=dict(l=40, r=40, t=60, b=40),
        height=600,
        showlegend=False,
        bargap=0.6,  # makes bars thinner
        hoverlabel=dict(font_size=15),
    )
    fig_market_bar.update_xaxes(showticklabels=True, tickfont=dict(size=14))  # show labels and make them bigger
    fig_market_bar.update_yaxes(tickprefix="$", separatethousands=True, zeroline=True, tickformat=",.0f")
    st.plotly_chart(fig_market_bar, use_container_width=True)

    # --- P&L by Setup (Bar Chart) ---
    if 'Setup' in df.columns:
        st.subheader("P&L by Setup")
        setup_pnl = df.groupby('Setup')['P/L'].sum().sort_values(ascending=False)
        # Filter out setups with P&L between -400 and 400 (inclusive)
        setup_pnl = setup_pnl[(setup_pnl < -400) | (setup_pnl > 400)]
        # Set bar colors: green for positive, red for negative
        bar_colors_setup = ['#3CB371' if v > 0 else '#ff4b5c' for v in setup_pnl.values]
        fig_setup = go.Figure([go.Bar(x=setup_pnl.index, y=setup_pnl.values, marker_color=bar_colors_setup)])
        fig_setup.update_layout(
            xaxis_title='',
            yaxis_title='',
            template='plotly_dark',
            plot_bgcolor='#181818',
            paper_bgcolor='#181818',
            font=dict(color='#e0e0e0'),
            margin=dict(l=40, r=40, t=60, b=40),
            height=500,
            showlegend=False,
            bargap=0.6,
            hoverlabel=dict(font_size=15),
        )
        fig_setup.update_xaxes(showticklabels=True, tickfont=dict(size=14))
        fig_setup.update_yaxes(tickprefix="$", separatethousands=True, zeroline=True, tickformat=",.0f")
        st.plotly_chart(fig_setup, use_container_width=True)

    # --- P&L per Trade (Line Chart) ---
    st.subheader("P&L per Trade")
    if 'DateShort' not in df.columns:
        df['DateShort'] = df['Date'].dt.strftime('%B %d')
    fig_pnl = go.Figure()
    fig_pnl.add_trace(go.Scatter(
        x=list(range(1, len(df['P/L'])+1)),
        y=df['P/L'],
        mode='lines',
        name='P&L per Trade',
        line=dict(color='white', width=2, shape='spline', smoothing=1.3),
        customdata=np.stack([df['DateShort'], [i+1 for i in range(len(df))]], axis=-1),
        hovertemplate='<b>Date:</b> %{customdata[0]}<br><b>Trade # %{customdata[1]}</b><br>P&L: $%{y:,.0f}<extra></extra>'
    ))
    fig_pnl.add_shape(type="line", x0=1, x1=len(df['P/L']), y0=0, y1=0, line=dict(color="white", width=1.5, dash="dash"))
    fig_pnl.update_layout(
        xaxis_title='',
        yaxis_title='',  # Remove y-axis label
        template='plotly_dark',
        plot_bgcolor='#181818',
        paper_bgcolor='#181818',
        font=dict(color='#e0e0e0'),
        margin=dict(l=40, r=40, t=60, b=40),
        height=500,
        showlegend=False,
        hoverlabel=dict(font_size=15),
    )
    fig_pnl.update_yaxes(tickprefix="$", separatethousands=True)
    st.plotly_chart(fig_pnl, use_container_width=True)

    # Ensure data is sorted by date and all columns are present
    df_sorted = df.sort_values('Date').reset_index(drop=True)
    df_sorted['DateShort'] = df_sorted['Date'].dt.strftime('%B %d')
    df_sorted['Drawdown %'] = (df_sorted['Drawdown'] / df_sorted['Running Max']) * 100

    # --- Interactive Equity Curve ---
    st.subheader("Equity Curve")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(range(1, len(df_sorted)+1)),
        y=df_sorted['Equity'],
        mode='lines',
        name='Equity Curve',
        line=dict(color='#90EE90', width=2),  # light green line
        fill='tonexty',
        fillcolor='rgba(144, 238, 144, 0.2)',  # more transparent light green fill
        customdata=np.stack([df_sorted['DateShort'], df_sorted['Trade #']], axis=-1),
        hovertemplate='<b>Date:</b> %{customdata[0]}<br><b>Trade # %{customdata[1]}</b><br><b>Equity:</b> $%{y:,.0f}<extra></extra>'
    ))
    fig.update_layout(
        xaxis_title='',  # Remove Trade # label
        yaxis_title='',  # Remove y-axis label
        template='plotly_dark',
        plot_bgcolor='#181818',
        paper_bgcolor='#181818',
        font=dict(color='#e0e0e0'),
        margin=dict(l=40, r=40, t=60, b=40),
        height=500,
        showlegend=False,
        hoverlabel=dict(font_size=15),
    )
    fig.update_yaxes(tickprefix="$", separatethousands=True)
    st.plotly_chart(fig, use_container_width=True)

    # --- Cumulative Win/Loss Count ---
    st.subheader("Cumulative W&L")
    trade_numbers = list(range(1, len(df_sorted) + 1))
    # Calculate cumulative wins and losses
    df_sorted['Cumulative Wins'] = (df_sorted['W/L'] == 'W').cumsum()
    df_sorted['Cumulative Losses'] = (df_sorted['W/L'] == 'L').cumsum()
    customdata = np.stack([df_sorted['DateShort'], df_sorted['Trade #']], axis=-1)
    fig_cum = go.Figure()
    fig_cum.add_trace(go.Scatter(
        x=trade_numbers,
        y=df_sorted['Cumulative Wins'],
        mode='lines',
        name='Cumulative Wins',
        line=dict(color='#3fffa8', width=2, shape='spline', smoothing=1.3),
        customdata=customdata,
        hovertemplate='<b>Date:</b> %{customdata[0]}<br><b>Trade # %{customdata[1]}</b><br><b>Wins:</b> %{y}<extra></extra>'
    ))
    fig_cum.add_trace(go.Scatter(
        x=trade_numbers,
        y=df_sorted['Cumulative Losses'],
        mode='lines',
        name='Cumulative Losses',
        line=dict(color='#ff4b5c', width=2, shape='spline', smoothing=1.3),
        customdata=customdata,
        hovertemplate='<b>Date:</b> %{customdata[0]}<br><b>Trade # %{customdata[1]}</b><br><b>Losses:</b> %{y}<extra></extra>'
    ))
    fig_cum.update_layout(
        xaxis_title='',
        yaxis_title='',  # Remove y-axis label
        template='plotly_dark',
        plot_bgcolor='#181818',
        paper_bgcolor='#181818',
        font=dict(color='#e0e0e0'),
        margin=dict(l=40, r=40, t=60, b=40),
        height=500,
        showlegend=False,  # Hide the legend
        hoverlabel=dict(font_size=15),
    )
    st.plotly_chart(fig_cum, use_container_width=True)

    # --- Drawdown Analysis ---
    st.subheader("Drawdown")
    # Calculate additional drawdown statistics
    max_drawdown_pct = df_sorted['Drawdown %'].min()
    avg_drawdown = df_sorted['Drawdown'].mean()
    avg_drawdown_pct = df_sorted['Drawdown %'].mean()
    # Create drawdown line chart
    fig_drawdown = go.Figure()
    fig_drawdown.add_trace(go.Scatter(
        x=list(range(1, len(df_sorted)+1)),
        y=df_sorted['Drawdown %'],
        mode='lines',
        name='Drawdown %',
        line=dict(color='#ff4b5c', width=2, shape='spline', smoothing=1.3),
        fill='tonexty',
        fillcolor='rgba(255, 75, 92, 0.3)',
        customdata=np.stack([df_sorted['DateShort'], [i+1 for i in range(len(df_sorted))], df_sorted['Drawdown']], axis=-1),
        hovertemplate='<b>Date:</b> %{customdata[0]}<br><b>Trade # %{customdata[1]}</b><br>Drawdown: $%{customdata[2]:,.0f}<extra></extra>'
    ))
    fig_drawdown.update_layout(
        xaxis_title='',  # Remove Trade # label
        yaxis_title='',  # Remove y-axis label
        template='plotly_dark',
        plot_bgcolor='#181818',
        paper_bgcolor='#181818',
        font=dict(color='#e0e0e0'),
        margin=dict(l=40, r=40, t=60, b=40),
        height=500,
        showlegend=False,
        hoverlabel=dict(font_size=15),
    )
    fig_drawdown.update_yaxes(tickformat=".1f", ticksuffix="%")
    st.plotly_chart(fig_drawdown, use_container_width=True)

    # Display drawdown statistics (moved below the chart)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'''
            <div class="summary-block-winrate">
                <span class="winrate-label">MAX DRAWDOWN</span>
                <span class="winrate-value" style="color: #ff4b5c;">${max_drawdown:,.0f}</span>
            </div>
        ''', unsafe_allow_html=True)
    with col2:
        st.markdown(f'''
            <div class="summary-block-winrate">
                <span class="winrate-label">MAX DRAWDOWN %</span>
                <span class="winrate-value" style="color: #ff4b5c;">{max_drawdown_pct:.1f}%</span>
            </div>
        ''', unsafe_allow_html=True)
    with col3:
        st.markdown(f'''
            <div class="summary-block-winrate">
                <span class="winrate-label">AVG DRAWDOWN</span>
                <span class="winrate-value" style="color: #ff4b5c;">${avg_drawdown:,.0f}</span>
            </div>
        ''', unsafe_allow_html=True)
    with col4:
        st.markdown(f'''
            <div class="summary-block-winrate">
                <span class="winrate-label">AVG RECOVERY</span>
                <span class="winrate-value" style="color: #3fffa8;">{avg_recovery_period:.0f} trades</span>
            </div>
        ''', unsafe_allow_html=True)

    # Optionally, show the raw data table
    toggle = st.checkbox("Show raw data table")
    if toggle:
        st.dataframe(df[['Date', 'Market', 'P/L', 'Equity']])

    st.markdown("---")
    st.markdown("Made with Streamlit & Plotly. Extend this app for more analytics!")

# Main app logic
if st.session_state.data_uploaded and st.session_state.df is not None:
    show_analysis_page()
else:
    show_upload_page() 