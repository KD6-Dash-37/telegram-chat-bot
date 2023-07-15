# repeat_bot.py
from dotenv import load_dotenv


from telegram import Update
from telegram.ext import (Application, ApplicationHandlerStop, CommandHandler,
                          ContextTypes)
from utils import load_config
from common import verify_user
from data_model import BotConfig


load_dotenv()


class PostHelp:

    def __init__(self, cfg: BotConfig):

        self.cfg = cfg

    async def send_hello(self, update: Update, context: ContextTypes.DEFAULT_TYPE): # pylint: disable=W0613

        if await verify_user(update=update, auth_users=self.cfg.auth.users):

            await update.message.reply_text("Hello")

class RepeatMessage:

    def __init__(self, cfg: BotConfig):

        self.cfg = cfg

    async def alarm(self, context: ContextTypes.DEFAULT_TYPE):

        job = context.job

        await context.bot.send_message(
            job.chat_id,
            message_thread_id=self.cfg.chat.message_thread_id,
            text="beep!"
            )

class StopRepeatMessage:

    def __init__(self, cfg: BotConfig):

        self.cfg = cfg

    async def stop(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        current_jobs = context.job_queue.get_jobs_by_name(self.cfg.name)

        if len(current_jobs) > 0:

            for job in current_jobs:

                job.schedule_removal()

            await update.effective_message.reply_text(
                "succesfully stopped repeat message"
                )

            return

        await update.effective_message.reply_text(
            "there are no repeating message jobs to stop"
            )


class SetTimer:

    def __init__(self, cfg: BotConfig):

        self.cfg = cfg

    async def set_timer(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        if await verify_user(update=update, auth_users=self.cfg.auth.users):

            try:

                interval = float(context.args[0])

                if interval < 0:

                    await update.effective_message.reply_text(
                        "interval must be numeric and greater than zero"
                    )

                    return

                message_function = RepeatMessage(cfg=self.cfg)

                context.job_queue.run_repeating(
                    message_function.alarm,
                    interval=interval,
                    chat_id=self.cfg.chat.chat_id,
                    name=self.cfg.name,
                    data=interval
                )

                text = f"repeating message every {interval} seconds"

                await update.effective_message.reply_text(text)

            except (IndexError, ValueError):

                await update.effective_message.reply_text(
                "The interval has to be a number, interpreted as seconds"
                )


def repeat_bot(bot_name: str):

    cfg = load_config(bot_name=bot_name)

    post_help = PostHelp(cfg=cfg)

    set_timer = SetTimer(cfg=cfg)

    stop_message = StopRepeatMessage(cfg=cfg)

    application = Application.builder().token(cfg.auth.token).build()

    application.add_handler(CommandHandler("help", post_help.send_hello))

    application.add_handler(CommandHandler("set", set_timer.set_timer))

    application.add_handler(CommandHandler("stop", stop_message.stop))

    application.run_polling()


if __name__ == "__main__":

    repeat_bot("bot1")
