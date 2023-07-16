from bot import bots
from utils import create_logs


def main(bot_type, bot_name):

    create_logs()

    bot = bots.get(bot_type)

    bot(bot_name=bot_name)


if __name__ == "__main__":

    main(bot_type="repeat_bot", bot_name="EfrenReyes")
