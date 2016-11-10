from telegram.ext import Updater, MessageHandler, Filters
from random import randint

import enchant

active_game = False
used_words = set([])
players = []
current_player = 0

words = enchant.Dict("en_US")
last_word = None

def reply(user, txt):
  global active_game
  global used_words
  global players
  global current_player
  global last_word

  user = user.lower().strip()
  txt = txt.lower()

  start = "start"
  quit = "quit"
  check = "check"
  turn = "turn"
  current = "current"
  
  if txt[:len(start)] == start:
    if active_game:
      return "Sorry, there is already an active game!"
    else:
      current_player = 0
      active_game = True
      used_words = set([])
      players = map(lambda name: name.lower().strip(), txt[len(start):].strip().split(","))
      return "Game started with players: " + ','.join(players) + ". Current it's %s's turn." % players[current_player]
  elif txt[:len(quit)] == quit:
    if not active_game:
      return "Sorry, no game to quit..."
    elif user not in players:
      return "Looks like you're not in the game."
    else:
      del players[players.index(user)]
      current_player = current_player % len(players)

      return "The remaining players are: " + ",".join(players) + ". Currently it's %s's turn." % players[current_player]
  elif txt[:len(check)] == check:
    return ["Not a real word!", "Real word!"][int(words.check(txt[len(check):].strip()))]
  elif txt[:len(current)] == current:
    return "Current word is " + last_word
  elif txt[:len(turn)] == turn:
    return "It is %s's turn." % players[current_player]
  else:
    if players[current_player] != user:
      return "Not your turn. Patience is a virtue."
    elif len(txt.split()) != 1:
      del players[players.index(user)]
      current_player = current_player % len(players)

      if len(players) == 1:
        active_game = False
        return "More than one word. The winner is %s" % players[0] + ". Everyone else is trash."

      current_player = current_player % len(players)

      return "You're out! Need to specify a single word. How hard is it to follow basic rules..."
    elif last_word and last_word[-1] != txt[0]:
      del players[players.index(user)]
      current_player = current_player % len(players)

      if len(players) == 1:
        active_game = False
        return "Doesn't follow rules. The winner is %s" % players[0] + ". Everyone else is trash."

      current_player = current_player % len(players)

      return "Doesn't follow rules! How hard is it to follow basic rules..."
    elif txt in used_words:
      del players[players.index(user)]

      if len(players) == 1:
        active_game = False
        return "Word used! The winner is %s" % players[0] + ". Everyone else is trash."

      current_player = current_player % len(players)

      return "Word already used! You're out!"
    elif not words.check(txt.strip()):
      del players[players.index(user)]
      current_player = current_player % len(players)

      if len(players) == 1:
        active_game = False
        return "Not a real word! The winner is %s" % players[0] + ". Everyone else is trash."

      current_player = current_player % len(players)

      return "You're out! Word doesn't exist in the dictionary. Learn english pls."
    else:
      used_words.add(txt)
      current_player = (current_player + 1) % len(players)
      return_val = ["Good work!", "Ok!", "Nice job!", "Well done."][0] + " Next is %s." % players[current_player]
      last_word = txt
      return return_val

def respond(bot, update):
  cmd = '@'
  txt = update.message.text
  user = update.to_dict()['message']['from']['first_name']

  if txt[:len(cmd)] == cmd:
    bot.sendMessage(chat_id=update.message.chat_id,
                    text=reply(user, txt[len(cmd):].strip().lower()))


if __name__ == '__main__':
  updater = Updater(token='232010029:AAHRVcKHvbyLgRTdjfpGfC8RsyGhEUfKTeg')
  dispatcher = updater.dispatcher
  dispatcher.add_handler(MessageHandler([Filters.text], respond))
  updater.start_polling()
