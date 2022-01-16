from bots.bot import Bott
import threading

if __name__ == '__main__':
    bot = Bott()
    boot = bot.run()
    thread_two = threading.Thread(target=boot)
    thread_two.start()
