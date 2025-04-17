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
## launch

4. Run the app
   ```bash
   chainlit run src/app.py
   ```

## TODO next

- [x] Mettre tout ça dans un git
- [x] Refactoring du cde pcq ça devient n'importe quoi
- [x] Ajoute du contexte de la conv
- [x] Clean up the mess
- [] Store des infos fixes (albums)
- [] vectorstore pour la bio de Tay 
- [] Debug Trace Error 2025-04-17 10:57:46 - Error in callback coroutine: TracerException('No indexed run ID e671b05a-e901-474c-9e7f-f64f55c35fbe.')
