import lib.triggers.features.nudity_detection as nudity
from lib.loader import Config

FEATURES = []

if Config.get("NUDITY_DETECTION.ENABLED", False):
    FEATURES.append(nudity.handler)


def features_handler(bot, update):

    # features controlled here
    for feature_handler in FEATURES:
        feature_handler(bot, update)
