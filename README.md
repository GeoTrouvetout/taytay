# taytay
taytay is a AI bot specialized in in-depth analysis of Taylor Swift career and song. 

## Setup

1. Set up the environment variable

   ```bash
   export OPENAI_API_KEY='your_api_key_here'
   ```
2. Create the chromadb with utils/create_vdb.py
   ```bash
   python utils/create_vdb.py
   ```
3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
4. Run the app
   ```bash
   chainlit run src/app.py
   ```
