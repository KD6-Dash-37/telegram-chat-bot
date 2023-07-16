# job.py
from data_model import BotConfig


def job_name(cfg: BotConfig) -> str:

    bot_name = cfg.name

    account = cfg.auth.deribit.account_name

    message_type = cfg.message_type.name

    job_name = ":".join([bot_name, account, message_type])

    return job_name
