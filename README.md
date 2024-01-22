# py-html-text-analyzer

> Analyze html text content from web and local files by using existing or creating new analyze scenarios with custom text conversion plugins!

Project requirements:
- Python 3.8 or higher
- aiohttp
- pytest
- aiofiles

Module is designed to be launched form command line. To run simply type <code>python3 main.py</code> and use existing configuration or provide your own - to do this use command line arguments:

> --urls_cfg_file | allows to override default path and use any custom urls config file. This configuration file describes what html's (in form of http/s link or local html file) should be used for analysis.
See example: *./configuration/default/configuration_files/urls.json*

> --text_conversion_plugins_cfg_file | allows to override default path and use any custom text converting plugins setup. This configuration file describes what kind of plugins should be loaded and how they should be configured. Order of specyfing plugins will be the order of text analyze. 
See example: *./configuration/default/configuration_files/text_converter_plugins.json*

> --scenario | allows to override default scenario. Scenario describes how plugins are used to analyze text and what exactly the module is doing. For example scenario *html_word_counting* tries to return in form of console log and txt file the most x number of words that are visible when html page is opened by webbrowser (human-readable text)

Project is oriented to use plain python as much as possible.

In case of (the only existing) html word counting scenario - module is able to return quite accurate results (compared with beautifulsoup4 for same task) but with better performance.

Unit tests with pytest are provided for most crucial functionality.
