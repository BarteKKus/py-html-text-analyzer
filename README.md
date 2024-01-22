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

Short workflow description:
1. Module requires urls and plugins configuration,
2. Urls json config are loaded by urls loader,
3. Plugins json config is loaded by plugins loader,
4. According to --scenario flag - specific scenario is launched,
5. Scenario import urls and plugins cfg,
6. Scenario launch plugins loading process with importlib when (if provided) configuration is beeing passed to selected plugins,
7. Next scenario in async way gets html content form provided url(s),
8. When content is loaded - scenario applies text conversion plugins on scraped html text,
9. When text is processed by plugins -> text_postprocessors going to be used (depending on the specific plugin),
10. In case of html_words_counter - selection of specific words is applied,
11. At the end word interpreters are launched - in case of html_words_counter - scenario prints results to the console and saves results to txt file,
12. Job is done.

Project is oriented to use plain python as much as possible.

In case of (the only existing) html word counting scenario - module is able to return quite accurate results (compared with beautifulsoup4 for same task) but with better performance.

Unit tests with pytest are provided for most crucial functionality.
