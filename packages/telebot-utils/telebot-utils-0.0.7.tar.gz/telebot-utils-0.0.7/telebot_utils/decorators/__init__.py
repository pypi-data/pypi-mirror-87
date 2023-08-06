import telebot
import traceback
from typing import Union
from logging import getLogger


logger = getLogger('telebot-utils')


def auto_answer(bot: telebot.TeleBot, exception_message: Union[None, str]=None, verbose=False):
    def _decorator(_handler):
        def _callback_query_handler(call_or_message: [telebot.types.CallbackQuery, telebot.types.Message], *args, **kwargs):
            try:
                res = _handler(call_or_message, *args, **kwargs)
                return res
            except Exception as e:
                if exception_message is not None:
                    if isinstance(call_or_message, telebot.types.CallbackQuery):
                        bot.send_message(call_or_message.message.chat.id, exception_message)
                    elif isinstance(call_or_message, telebot.types.Message):
                        bot.send_message(call_or_message.chat.id, exception_message)
                    else:
                        logger.error(exception_message)

                    if verbose:
                        traceback.print_exc()
            finally:
                if isinstance(call_or_message, telebot.types.CallbackQuery):
                    bot.answer_callback_query(call_or_message.id)
        return _callback_query_handler
    return _decorator
