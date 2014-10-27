import logging
import yaml
import jasperpath


logger = logging.getLogger(__name__)
new_configfile = jasperpath.config('profile.yml')

try:
    with open(new_configfile, "r") as f:
        profile = yaml.safe_load(f)
except OSError:
    logger.error("Can't open config file: '%s'", new_configfile)
    raise
