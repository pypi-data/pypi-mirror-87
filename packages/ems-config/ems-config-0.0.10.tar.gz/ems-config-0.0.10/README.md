Create a `config.py` file in your repository with contents like this,

    from ems_config import parse_config
    
    config = parse_config()
    # Parse config into python variables (optional).
    URL = config["DEFAULT"]["URL"]
    
along with an example file `config.ini.example` that contains an example of the configuration,

    [DEFAULT]
    URL = http://google.com
    
You can then use the configuration in other python files like this,

    from config import URL
    print(URL)  # do stuff with the URL