from datetime import datetime
from config.Config import Config

def is_within_grace_period():
    current_time = datetime.now(Config.TIMEZONE)
    return Config.GRACE_PERIOD_START <= current_time.hour < Config.GRACE_PERIOD_END
