import os
import requests
import xml.etree.ElementTree as ET
import streamlit as st
import streamlit.components.v1 as components
from crewai import Agent, Task, Crew

# Environment Configuration for API Access
os.environ["OPENAI_API_BASE"] = 'https://api.groq.com/openai/v1'
os.environ["OPENAI_MODEL_NAME"] = "llama3-70b-8192"
os.environ["OPENAI_API_KEY"] = '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'
NOTION_TOKEN = 'secret_F9clIJWRa6SPzqBpsM27zOKQ4QC4FjmBVBWty0zAgHt'

# Function to Get News Titles from Google News RSS Feed
def get_news_titles(keyword):
    url = f'https://news.google.com/rss/search?q={keyword}'
    response = requests.get(url)

    if response.status_code == 200:
        root = ET.fromstring(response.content)
        titles = [item.text for item in root.findall('.//item/title')]
        display_in_toggle("News Headlines", "\n=>".join(titles))
        return "\n".join(titles)
    else:
        st.error("Failed to retrieve the RSS feed")
        return ""

# Function to Display Extracted Output
def display_extracted_output(task_output):
    output = str(task_output)
    start_index = output.find("exported_output=") + len("exported_output=") + 1
    extracted_output = output[start_index:-1]
    display_in_toggle("Agent's Processing", extracted_output)

# Function to Display Text in Toggle Expander with Custom CSS
def display_in_toggle(title, raw_text):
    with st.expander(title):
        css = """
        <style>
        .code-block {
            white-space: pre-wrap;
            word-wrap: break-word;
            background-color: #333333;
            color: #f0f0f0;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #ccc;
            font-family: monospace;
            overflow: auto;
        }
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
        st.markdown(f"<div class='code-block'><pre>{raw_text}</pre></div>", unsafe_allow_html=True)

# Function to Setup Sidebar in Streamlit
def setup_sidebar():
    st.sidebar.title("AI Stock Assistant")
    st.sidebar.subheader("Search from Ticker")
    st.sidebar.text_input("Enter Ticker Symbol", "", on_change=analyze_stock, key='ticker_input')
    
    st.sidebar.subheader("Search from Portfolio")
    manage_portfolio()
    add_new_stock()

    st.sidebar.subheader("About the Project")
    st.sidebar.info("AI Stock Assistant analyzes stock market data and provides insights through advanced AI-driven models.")

    st.sidebar.subheader("Enter API Key")
    st.sidebar.text_input("API Key", type="password", key='api_key')

# Function to Manage Portfolio in Session State
def manage_portfolio():
    if 'portfolio' not in st.session_state:
        st.session_state.portfolio = ["AAPL", "TSLA"]

    for index, stock in enumerate(st.session_state.portfolio):
        col1, col2, col3 = st.sidebar.columns([2, 1, 1])
        col1.write(stock)
        if col2.button("Remove", key=f"remove_{index}"):
            st.session_state.portfolio.pop(index)
        if col3.button("Search", key=f"search_{index}"):
            analyze_stock(stock)

# Function to Add New Stock to Portfolio
def add_new_stock():
    new_stock = st.sidebar.text_input("Add New Stock to Portfolio", "")
    if st.sidebar.button("Add Stock", key='add_new_stock'):
        if new_stock and new_stock not in st.session_state.portfolio:
            st.session_state.portfolio.append(new_stock)

# Function to Analyze Stock Data
def analyze_stock(stock=None):
    ticker_input = stock if stock else st.session_state.get('ticker_input', '')
    if not ticker_input:
        st.error("Please enter a valid ticker symbol.")
        return

    st.subheader(f"Stock Chart for {ticker_input}")
    col1, col2 = st.columns([2, 1])

    with col1:
        sub_col1, sub_col2 = st.columns([1, 2])
        with sub_col1:
            show_current_price(ticker_input)
        with sub_col2:
            trading_view(ticker_input)

    with col2:
        show_news(ticker_input)

    st.write(f"Analyzing stock data for: {ticker_input}")

    stock_analysis_agent = Agent(
        role='Stock Analyst',
        goal=f'Analyze stock data and identify factors that could influence stock price of {ticker_input} by understanding the news headlines.',
        backstory="""You are a seasoned stock analyst equipped with deep market knowledge.
                    Your expertise lies in examining market data and trends to forecast stock movements by understanding news headlines about the stock.""",
        verbose=True,
        allow_delegation=False
    )

    stock_prediction_agent = Agent(
        role='Stock Predictor',
        goal=f'Predict the direction of stock price movement of {ticker_input} based on analysis.',
        backstory="""You are a financial predictor with a knack for quantitative analysis.
                    You specialize in using statistical models to forecast future stock price movements.""",
        verbose=True,
        allow_delegation=False
    )

    analyze_stock_task = Task(
        description=f"Analyze the {ticker_input} stock data and outline key factors that might influence its price in bullet points by understanding these headlines:\n{get_news_titles(ticker_input)}",
        agent=stock_analysis_agent,
        expected_output="Bullet points outlining key factors with reasons that may influence the stock price."
    )

    predict_stock_task = Task(
        description="Based on the analysis, predict the likelihood of the stock price moving up or down on a scale from -10 to +10.",
        agent=stock_prediction_agent,
        expected_output="""Prediction of stock price movement (range from -10 to +10) with a detailed summary in a markdown format,
                        explaining the reasoning behind the prediction, crafted like an expert's analysis."""
    )

    crew = Crew(
        agents=[stock_analysis_agent, stock_prediction_agent],
        tasks=[analyze_stock_task, predict_stock_task],
        verbose=2,
        full_output=True
    )

    result = crew.kickoff()
    display_extracted_output(result['tasks_outputs'][0])
    display_extracted_output(result['tasks_outputs'][1])

    with col1:
        st.markdown(result['final_output'])

# Function to Display TradingView Chart
def trading_view(symbol):
    html_code = f"""
    <div class="tradingview-widget-container">
    <div class="tradingview-widget-container__widget"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>
    {{
    "width": "600",
    "height": "300",
    "symbol": "NASDAQ:{symbol}",
    "interval": "D",
    "timezone": "Etc/UTC",
    "theme": "dark",
    "style": "2",
    "locale": "en",
    "backgroundColor": "rgba(0, 0, 0, 1)",
    "hide_top_toolbar": true,
    "allow_symbol_change": false,
    "save_image": false,
    "calendar": false,
    "support_host": "https://www.tradingview.com"
    }}
    </script>
    </div>
    """
    components.html(html_code, height=300)

# Function to Display Current Price Widget
def show_current_price(symbol):
    html_code = f"""
    <div class="tradingview-widget-container">
    <div class="tradingview-widget-container__widget"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-single-quote.js" async>
    {{
    "symbol": "NASDAQ:{symbol}",
    "width": "300",
    "isTransparent": true,
    "colorTheme": "dark",
    "locale": "en"
    }}
    </script>
    </div>
    """
    components.html(html_code, height=300)

# Function to Display News Timeline Widget
def show_news(symbol):
    html_code = f"""
    <div class="tradingview-widget-container">
    <div class="tradingview-widget-container__widget"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-timeline.js" async>
    {{
    "feedMode": "symbol",
    "symbol": "NASDAQ:{symbol}",
    "isTransparent": true,
    "displayMode": "regular",
    "width": 300,
    "height": 700,
    "colorTheme": "dark",
    "locale": "en"
    }}
    </script>
    </div>
    """
    components.html(html_code, height=700)

# Main Function to Setup Streamlit App
def main():
    st.set_page_config(page_title="AI Stock Assistant", layout="wide")
    setup_sidebar()
    st.header("Welcome to AI Stock Assistant")

if __name__ == "__main__":
    main()
