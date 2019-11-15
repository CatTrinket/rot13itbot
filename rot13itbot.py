import asyncio
import collections
import configparser
import functools
import hashlib
import logging
import shelve
import sys

import telethon


rot13_table = str.maketrans(
    'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
    'nopqrstuvwxyzabcdefghijklmNOPQRSTUVWXYZABCDEFGHIJKLM5678901234'
)


Config = collections.namedtuple(
    'Config',
    ('api_id', 'api_hash', 'bot_token', 'session_file', 'message_file')
)


def rot13(text):
    """Translate the text through rot13.

    This will work on ASCII letters and will also rot5 ASCII digits.  Anything
    else will be left alone; it doesn't try to do anything clever with accented
    letters or anything.
    """

    return text.translate(rot13_table)

async def new_rot13_message(event, messages):
    """Deal with an incoming message @-ing the bot.

    We can't get the message back later so we have to store it locally for the
    "Show" button to work!  Great!

    Also, this event fires periodically as the user types!  There's no way to
    determine when the user actually *sends* the message, so we end up storing
    a few unfinished messages for each actual message!  Great!!!!
    """

    # Skip empty messages
    if not event.text:
        await event.answer()
        return

    # Store the message
    sha = hashlib.sha256(event.text.encode('UTF-8'))
    messages[sha.hexdigest()] = event.text

    # Reply with the single "Send" option for the user to click
    result = rot13(event.text)
    await event.answer([
        event.builder.article(
            id=str(event.id),
            title='Send',
            description=result,
            text=result,
            buttons=telethon.Button.inline('Show', sha.digest())
        )
    ])

async def show_rot13_message(event, messages):
    """Show a previous message upon clicking the "Show" button."""

    key = event.data.hex()

    try:
        message = messages[key]
    except KeyError:
        await event.answer("Message no longer in Rot13ItBot's database")
    else:
        if len(message) > 200:
            message = '{}…'.format(message[:199])

        await event.answer(message, alert=True)

def get_config():
    """Read the config file named on the command line and return the results as
    a Config namedtuple.
    """

    # Read config
    if len(sys.argv) != 2:
        exit('Usage: {} config_file'.format(sys.argv[0]))

    config = configparser.ConfigParser()

    with open(sys.argv[1]) as config_file:
        result = config.read_file(config_file)

    # Map keys to required Config fields
    kwargs = {}

    for field in Config._fields:
        if field not in config['DEFAULT']:
            exit('Missing required config key: {}'.format(field))

        kwargs[field] = config['DEFAULT'][field]

    return Config(**kwargs)

async def main():
    """Run the bot from the command line."""

    logging.basicConfig(level=logging.WARNING)
    config = get_config()

    client = telethon.TelegramClient(
        config.session_file, config.api_id, config.api_hash)

    with shelve.open(config.message_file) as messages:
        client.add_event_handler(
            functools.partial(new_rot13_message, messages=messages),
            telethon.events.InlineQuery
        )

        client.add_event_handler(
            functools.partial(show_rot13_message, messages=messages),
            telethon.events.CallbackQuery
        )

        await client.start(bot_token=config.bot_token)
        await client.run_until_disconnected()


if __name__ == '__main__':
    # TODO: use asyncio.run once we're on Python 3.7
    asyncio.get_event_loop().run_until_complete(main())
