# Rot13ItBot

This is the source for [@Rot13ItBot](https://telegram.me/Rot13ItBot) on
Telegram.

You can tag this bot from any chat to rot13 some text:

    @rot13itbot text to hide

The rot13'd message will show up as having been sent from "Your username via
@Rot13ItBot", and it will have a "show" button to conveniently show the
original text.

This was inspired by [@HideItBot](https://github.com/erpheus/hideit-bot), which
works the same but blanks text out with question marks or block characters
(e.g. ██████ ██ ███████) rather than using rot13.  This means that the *only*
way to recover the original text with HideItBot is with the "show" button, and
when the bot goes down, messages are simply inaccessible.

With Rot13ItBot, on the other hand, you can still decode the messages yourself
should the bot go down.


## Privacy

Once a message is sent, Telegram provides no way for the bot to retrieve the
message afterwards -- i.e. when you click the "show" button.  Therefore, all
messages sent through this bot are stored server-side.  This sucks, but I'm not
sure what else to do.
