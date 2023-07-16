# repeat_bot.py

from bot.common import verify_user, job_name
from dotenv import load_dotenv
from bot.messages import account_summary
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from data_model import BotConfig
from utils import load_config


load_dotenv()


class PostHelp:

    def __init__(self, cfg: BotConfig):

        self.cfg = cfg

    async def post_help_info(self, update: Update, context: ContextTypes.DEFAULT_TYPE): # pylint: disable=W0613

        if await verify_user(update=update, auth_users=self.cfg.auth.telegram.users):

            text = [
                "/help to view this text",
                "/set [number] to set how often the message should be posted",
                "/stop to stop the repeating message",
                "/jobs to see what repeating message is currently working",
            ]

            text = "\n".join(text)

            await update.message.reply_text(text)

class RepeatMessage:

    def __init__(self, cfg: BotConfig):

        self.cfg = cfg

    async def send_message(self, context: ContextTypes.DEFAULT_TYPE):

        job = context.job

        text = await account_summary(cfg=self.cfg)

        await context.bot.send_message(
            job.chat_id,
            message_thread_id=self.cfg.chat.message_thread_id,
            text=text
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

        if await verify_user(update=update, auth_users=self.cfg.auth.telegram.users):

            try:

                interval = float(context.args[0])

                if interval < 0:

                    await update.effective_message.reply_text(
                        "interval must be numeric and greater than zero"
                    )

                    return

                message_function = RepeatMessage(cfg=self.cfg)

                context.job_queue.run_repeating(
                    message_function.send_message,
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

class Jobs:

    def __init__(self, cfg: BotConfig):

        self.cfg = cfg

    async def post_job_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        if await verify_user(update=update, auth_users=self.cfg.auth.telegram.users):

            current_jobs = context.job_queue.get_jobs_by_name(self.cfg.name)

            if len(current_jobs) > 0:

                text = job_name(cfg=self.cfg)

                await update.effective_message.reply_text(text=text)

                return

            text = "idle, no jobs"

            await update.effective_message.reply_text(text=text)


def repeat_bot(cfg: BotConfig):

    # cfg = load_config(bot_name=bot_name)

    post_help = PostHelp(cfg=cfg)

    set_timer = SetTimer(cfg=cfg)

    jobs = Jobs(cfg=cfg)

    stop_message = StopRepeatMessage(cfg=cfg)

    application = Application.builder().token(cfg.auth.telegram.token).build()

    application.add_handler(CommandHandler("help", post_help.post_help_info))

    application.add_handler(CommandHandler("set", set_timer.set_timer))

    application.add_handler(CommandHandler("stop", stop_message.stop))

    application.add_handler(CommandHandler("jobs", jobs.post_job_status))

    application.run_polling()
