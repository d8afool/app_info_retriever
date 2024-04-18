# App Info Retriever
Easily retrieve all available information about apps matching a list of given search queries from Apple App Store and 
Google Play Store. In order to use this tool, you need a valid API key from SerpApi (https://serpapi.com). For up to 
100 searches per month the usage of SerpApi is free. However, SerpApi also provides different plans that allow
exceeding this limit.

Results will be saved as JSON files to the **data** directory. For each search query and app provider (engine) there 
will be written a separate file.

## Requirements
1. Register at https://serpapi.com/users/sign_up
2. Retrieve your API key at https://serpapi.com/manage-api-key
3. Save you API key to environment variables using  `export SERP_API_KEY=<your_key>` (or use the command line argument 
`--serpapikey`)
4. Install Python 3.x

## Usage
Run `python main.py --queries <QUERY_1>, <QUERY_2>, ...`, where  `<QUERY_1>`, `<QUERY_2>` (and so on) are your search 
queries. You can specify other search parameters as well. For a complete list of available parameters run 
`python main.py --help`.

Alternatively you can run the Jupyter notebook using `jupyter lab` and opening up `AppInfoRetriever.ipynb`. 

## Contact
Feedback and bug reports are appreciated: datafool@proton.me
