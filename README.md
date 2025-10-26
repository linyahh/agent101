# Smart Travel Assistant

An intelligent travel assistant based on large language models that can query weather and recommend corresponding tourist attractions.

## Project Structure

```
├── custom_tools/           # Custom tools modules
│   ├── __init__.py
│   ├── weather_tools.py    # Weather query tools
│   ├── attraction_tools.py # Attraction recommendation tools
│   └── budget_tools.py     # Budget calculation tools
├── config/                 # Configuration files
│   ├── __init__.py
│   ├── agent_system_prompt.py  # Agent system prompts
│   ├── api_keys.py         # API key configuration (not committed to git)
│   └── api_keys.example.py # API key configuration example
├── utils/                  # Utility classes
│   ├── __init__.py
│   ├── llm_client.py       # LLM client wrapper
│   └── output_manager.py   # Output manager
├── output/                 # Output folder (not committed to git)
│   └── README.md          # Output description file
├── main.py                 # Main program entry
├── requirements.txt        # Dependency list
├── .gitignore             # Git ignore file
└── README.md              # Project description
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## API Key Configuration

1. Copy configuration file template:
```bash
cp config/api_keys.example.py config/api_keys.py
```

2. Edit `config/api_keys.py` file and fill in your real API keys:
   - `MODELSCOPE_API_KEY`: ModelScope API key
   - `TAVILY_API_KEY`: Tavily search API key

## Run Program

```bash
python main.py
```

## Features

- 🌤️ Real-time weather query (based on wttr.in API)
- 🏛️ Intelligent attraction recommendations (based on Tavily search API)
- 💰 Travel budget calculation (tickets and transport costs)
- 📊 Budget allocation suggestions
- 💾 Automatically save query results to files
- 🔄 Support multi-turn dialogue and reasoning
- 🏗️ Modular design, easy to extend
- 🔐 Secure API key management

## Output File Management

The program automatically saves each query result to the `output/` folder:

- 📁 File naming: `YYYYMMDD_HHMMSS_CityName.txt`
- 📄 Contains complete query process and final answer
- 🎯 Supports Chinese and international city name recognition
- 📈 Automatically generates query statistics

## Security Notes

- `config/api_keys.py` file has been added to `.gitignore` and will not be committed to version control
- Please keep your API keys safe and do not share them in public places