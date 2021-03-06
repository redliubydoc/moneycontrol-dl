# do not edit this file
import os
from colorama import init, Fore, Back, Style


class Console:
    circular_cursor = ['|', '/', '-', '\\']
    console_width = os.get_terminal_size()[0]
    padding = 16

    def __init__(self):
        init(autoreset=False, convert=None, strip=None, wrap=True)
        print(Back.BLACK)
        print(Style.BRIGHT)
        self.print_ascii_art()

    @staticmethod
    def print_ascii_art():
        os.system('cls || clear')
        print(Fore.GREEN)
        text_art_part_1 = "█▀▄▀█ █▀▀█ █▀▀▄ █▀▀ █░░█ █▀▀ █▀▀█ █▀▀▄ ▀▀█▀▀ █▀▀█ █▀▀█ █░░ ░░ █▀▀▄ █░░"
        text_art_part_2 = "█░▀░█ █░░█ █░░█ █▀▀ █▄▄█ █░░ █░░█ █░░█ ░░█░░ █▄▄▀ █░░█ █░░ ▀▀ █░░█ █░░"
        text_art_part_3 = "▀░░░▀ ▀▀▀▀ ▀░░▀ ▀▀▀ ▄▄▄█ ▀▀▀ ▀▀▀▀ ▀░░▀ ░░▀░░ ▀░▀▀ ▀▀▀▀ ▀▀▀ ░░ ▀▀▀░ ▀▀▀"

        print('\n\n' +
              text_art_part_1.center(Console.console_width) + '\n' +
              text_art_part_2.center(Console.console_width) + '\n' +
              text_art_part_3.center(Console.console_width) + '\n\n\n'
              )

    @staticmethod
    def print_left_aligned(msg, end='\n'):
        left_padding = int(Console.padding / 2)
        print(Fore.CYAN + " " * left_padding + msg, end=end)

    @staticmethod
    def print_centre_aligned(msg, end='\n'):
        msg = msg.center(Console.console_width)
        print(Fore.CYAN + msg, end=end)

    @staticmethod
    def print_right_aligned(msg, end="\n"):
        left_padding = Console.console_width - int(Console.padding / 2) - len(msg)
        print(Fore.CYAN + " " * left_padding + msg, end=end)

    @staticmethod
    def print_verbose(lmsg, rmsg='', end='\n', level='INFO'):
        display_string = lmsg + '.' * (Console.console_width - Console.padding - len(lmsg) - len(rmsg)) + rmsg

        if level == 'INFO':
            print(Fore.YELLOW + display_string.center(Console.console_width), end=end)
        elif level == 'SUCCESS':
            print(Fore.GREEN + display_string.center(Console.console_width), end=end)
        elif level == 'DANGER':
            print(Fore.RED + display_string.center(Console.console_width), end=end)
        elif level == "EXCEPTION":
            print(Fore.LIGHTMAGENTA_EX + display_string.center(Console.console_width), end=end)

    @staticmethod
    def print_table(table):
        lines = table.to_string(index=False).split("\n")
        n = len(lines)
        m = len(lines[0])

        print('\n')
        for i in range(n):
            line = lines[i]

            if i == 0:
                x = m - 10

                index = "%5s" % "INDEX"
                name = line[:x - 1].upper()
                price = line[x:]
                row = index + " | " + name + " | " + price

                print(Fore.CYAN + ("+" + '-' * (len(line) + 12) + "+").center(Console.console_width))
                print(Fore.CYAN + ("| " + row + " |").center(Console.console_width))
                print(Fore.CYAN + ("+" + '-' * (len(line) + 12) + "+").center(Console.console_width))

            else:
                index = "%5s" % str(i)
                name = line[:x - 1].lower().capitalize()
                price = line[x:]
                row = index + " | " + name + " | " + price

                if i == n - 1:
                    if n % 2 == 0:
                        print(Fore.CYAN + ("| " + row + " |").center(Console.console_width))
                        print(Fore.CYAN + ("+" + '-' * (len(line) + 12) + "+").center(Console.console_width))
                    else:
                        print(Fore.CYAN + ("| " + row + " |").center(Console.console_width))
                        print(Fore.CYAN + ("+" + '-' * (len(line) + 12) + "+").center(Console.console_width))

                else:
                    if n % 2 == 0:
                        print(Fore.CYAN + ("| " + row + " |").center(Console.console_width))
                        print(Fore.CYAN + ("|" + '-' * (len(line) + 12) + "|").center(Console.console_width))
                    else:
                        print(Fore.CYAN + ("| " + row + " |").center(Console.console_width))
                        print(Fore.CYAN + ("|" + '-' * (len(line) + 12) + "|").center(Console.console_width))
                i += 1
        print("\n")
