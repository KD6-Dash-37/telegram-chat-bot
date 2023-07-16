# main.py
import sys
from bot import bots
from utils import create_logs, load_config


def main(bot_name):

    create_logs()

    cfg = load_config(bot_name=bot_name)

    bot = bots.get(cfg.bot_type)

    bot(cfg=cfg)


if __name__ == "__main__":

    main(sys.argv[1])
