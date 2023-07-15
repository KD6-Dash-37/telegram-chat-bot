from bot import repeat_bot
from utils import create_logs


def main(bot_name):

    create_logs()

    repeat_bot(bot_name=bot_name)


if __name__ == "__main__":

    main(bot_name="bot1")
