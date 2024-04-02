import ast
import json
import os
import shutil
from utils.paths import Data, Defaults

# Loads settings from the config file or generates / updates it from the default
# configuration
def load_settings(logging):
    logging.info('loading config settings...')
    default_settings = {}
    settings = {}

    # Checking if config file exists and then writing the default config settings
    # to a new file if it doesn't
    if not os.path.exists(Data.CONFIG):
        shutil.copyfile(Defaults.CONFIG, Data.CONFIG)
        logging.warning('could not find config.cfg, wrote new file from default config values.')

    with open(Defaults.CONFIG, 'r') as f:
        default_settings = json.loads(f.read())
        logging.info('read in settings from config_default.json')

    with open(Data.CONFIG, 'r') as f:
        settings = json.loads(f.read())
        logging.info('read in settings from config.cfg')

    # If the length of the settings are different, attempt to add any missing
    # settings from the defaults to the actual config
    if len(settings) != len(default_settings):
        logging.warning('setting JSON len mismatch, regenerating new settings with missing keys...')
        for key in default_settings:
            if key not in settings:
                settings[key] = default_settings[key]
        settings['versionplusplus'] = default_settings['versionplusplus']
        with open(Data.CONFIG, 'w') as f:
            f.write(json.dumps(settings))
            logging.info('wrote updated config to config.cfg')

    # TODO: Wallpapers should be stored as JSON objects
    try:
        settings['wallpaperDat'] = ast.literal_eval(settings['wallpaperDat'])
    except Exception as e:
        logging.warning(f'failed to parse wallpaper from string\n\tReason: {e}')

    return settings
