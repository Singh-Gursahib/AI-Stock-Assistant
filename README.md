# AI Stock Assistant

AI Stock Assistant is a Streamlit web application designed to assist investors by analyzing stock market data and providing insights through advanced AI-driven models.

## Features

- **Search by Ticker**: Analyze stock data for a specific ticker symbol.
- **Manage Portfolio**: Add, remove, and analyze stocks in your portfolio.
- **AI Analysis**: Utilizes CrewAI to perform stock analysis and prediction based on news headlines.
- **Interactive Charts**: Visualize stock prices and news using TradingView widgets.
- **Secure API Key Entry**: Enter API keys securely through Streamlit's password input.

## Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-username/ai-stock-assistant.git
   cd ai-stock-assistant
   ```

2. **Create and activate a virtual environment** (optional but recommended):

   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

   Activating the virtual environment isolates your project's dependencies from other Python projects.

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Environment Variables**:

   Make sure to set the following environment variables before running the application:

   ```bash
   export OPENAI_API_BASE='https://api.groq.com/openai/v1'
   export OPENAI_MODEL_NAME='llama3-70b-8192'
   export OPENAI_API_KEY='your_openai_api_key'
   ```

   Replace `your_openai_api_key` with your actual OpenAI API key. You can obtain a free API key from [here](https://console.groq.com/keys) (currently free).

5. **Run the application**:

   ```bash
   streamlit run app.py
   ```

   The application will start running on `localhost` by default. Open your web browser and navigate to `http://localhost:8501` to view the AI Stock Assistant.

## Usage

- **Search by Ticker**: Enter a ticker symbol in the sidebar to analyze its stock data.
- **Manage Portfolio**: Add new stocks to your portfolio, remove existing ones, and analyze each stock's data individually.
- **View Analysis**: Explore the analysis and predictions provided by AI models based on the latest news headlines.

## Screenshots

![Screenshot 1](/screenshots/screenshot1.png)
![Screenshot 2](/screenshots/screenshot2.png)
