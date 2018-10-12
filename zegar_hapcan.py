import threading, csv, socket, happroc, zegar_astro
from datetime import date, datetime, time
import configparser
import time
# czasowo na testy
import binascii

KOMENDY_ZEGARA = {}
DZIEN = {}


def wyslij(id_komunikatu, dane):
    try:
        config = configparser.ConfigParser()
        config.read('hapcan.ini')
        # pobiera dane z sekcji [IP] pliku .INI
        sock_ip = (config.get('IP', 'adres'))
        sock_port = int(config.get('IP','port'))
        proto = socket.getprotobyname('tcp')
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto)
        print(sock_ip,type(sock_ip),(sock_port), type(sock_port))
        #sock.connect(("192.168.1.201", 1001))
        #sock_port = 1001
        sock.connect((sock_ip,sock_port))
        msg = bytearray()
        msg.append(0xAA)

        b2 = (id_komunikatu >> 8) & 0xFF;
        msg.append(b2)

        b1 = (id_komunikatu) & 0xFF;
        msg.append(b1)

        for val in dane:
            #print('val 1',val)
            msg.append(val)
        msg.append(happroc.hap_crc(msg))
        msg.append(0xA5)

        #print(msg)

        sock.sendall(msg)
        print('wyslano =', binascii.hexlify(msg))

    except socket.error:
        pass
    finally:
        sock.close()



def setInterval(interval):
    def decorator(function):
        def wrapper(*args, **kwargs):
            stopped = threading.Event()

            def loop():
                while not stopped.wait(interval):
                    function(*args, **kwargs)

            t = threading.Thread(target=loop)
            t.daemon = True
            t.start()
            return stopped

        return wrapper

    return decorator

@setInterval(10)  # Wysylanie zapytania do 100 sekund
def komendy_zegara():
    # procedura wykonywana cyklicznie co 3 sek - docelowo 1 minuta
    data_obecna = datetime.now()
    if DZIEN[1] == int((data_obecna.strftime('%d'))):
        data_int = int((data_obecna.timestamp())/60)
        #print(data_int)
        ks = list(KOMENDY_ZEGARA.keys())
        for key in ks:
            komendy = KOMENDY_ZEGARA.get(key, None)
            if data_int < komendy[1]:
                print('Jescze do zrobienia')
            else:
                print('Już czas zrobić')
                #a=KOMENDY_ZEGARA.
                print(komendy[3], komendy[4])
                wyslij(komendy[3], komendy[4])
                odczyt_komend()
    else:
        print("Mamy nowy dzień :)")
        nowy_dzien()
        odczyt_komend()


def nowy_dzien():
    DZIEN[1] = int((datetime.now().strftime('%d')))

def odczyt_komend():
    try:
        indeks = 0
        data_obecna = datetime.now()

        with open('komendy_zegara.csv', 'r') as  f:
            f_csv = csv.reader(f, delimiter=';')
            next(f_csv)
            for row in f_csv:
                dane = [0xF0, 0xF0, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0xFF]
                dzien_tyg = False
                # sprawdza dzień tygodnia jeśli nie jest do zrobienia dziś to pomija
                a=row[2]
                if (datetime.now().weekday() == 6) and row[2].count('N'): # Niedziela
                    print('Jest i w niedziele')
                    dzien_tyg = True
                elif (datetime.now().weekday() == 0) and row[2].count('P'): # Poniedziałek
                    print('Jest i w pon')
                    dzien_tyg = True
                elif (datetime.now().weekday() == 1) and row[2].count('W'):  # Wtorek
                    print('Jest i w wt')
                    dzien_tyg = True
                elif (datetime.now().weekday() == 2) and row[2].count('R'):  # Środa
                    print('Jest i w sr')
                    dzien_tyg = True
                elif (datetime.now().weekday() == 3) and row[2].count('C'):  # Czwartek
                    print('Jest i w cz')
                    dzien_tyg = True
                elif (datetime.now().weekday() == 4) and row[2].count('T'):  # Piątek
                    print('Jest i w pt')
                    dzien_tyg = True
                elif (datetime.now().weekday() == 5) and row[2].count('S'):  # Sobota
                    print('Jest i w sobota')
                    dzien_tyg = True
                if not(dzien_tyg):
                    print('to inny dzien')
                    continue
                # odczyt z pliku ini lokalizacji
                config = configparser.ConfigParser()
                config.read('hapcan.ini')
                # pobiera dane z sekcji [geoloc] pliku .INI
                latgeo = float(config.get('geoloc', 'latgeo'))
                longgeo = float(config.get('geoloc', 'longgeo'))
                #a = calendar.weekday(data_obecna.strftime('%Y'),data_obecna.strftime('%m'),data_obecna.strftime('%d'))
                # row[0] - rodzaj oznaczenia czasu H- godzina, W- czas względem wschodu Z-czas względem zachodu słońca
                print (row[0])
                if row[0]=='W':
                    x = zegar_astro.int_wsch(latgeo,longgeo,int(row[1]))
                elif row[0]=='Z':
                    x = zegar_astro.int_zach(latgeo, longgeo, int(row[1]))
                elif row[0]=='H':
                    x1 = data_obecna.strftime('%Y-%m-%d') + " " + row[1] + ":00"
                    x2 = datetime.strptime(x1, '%Y-%m-%d %H:%M:%S')
                    x=int((x2.timestamp())/60)
                else:
                    print('Brak właściwego zaprogramwania czasu !!!')
                if x < int((data_obecna.timestamp())/60):
                    print('To już było')
                    continue
                else:
                    row[1] = x

                # typ Hapcan obsługiwany P-przekaźnik
                if row[3] == 'P':
                    row[3] =  0x10A0
                    # odczyt modułu, grupy i nr kanału
                    dane[4] = int(row[5])
                    dane[5] = int(row[6])
                    dane[3] = 2 ** (int(row[7]) - 1)
                    #if row[6] == "":
                    #    dane[6] = 0
                    #else:
                    dane[6] = int(row[9])
                    #
                    #
                else:
                    print('Brak właściwego zaprogramwania modułu !!!')
                # oczyt komendy ON/OFF
                if row[8] == 'ON':
                    dane[2] = 1
                elif row[8] == 'OFF':
                    dane[2] = 0
                else:
                    print('Brak komendy !!!')
                row[4]=dane
                print(row)
                # map_temp2.update(hex(key[0]))
                KOMENDY_ZEGARA[indeks] = row
                indeks = indeks + 1
            print("Komendy zegara", KOMENDY_ZEGARA)
            print(DZIEN)
    except socket.error:
        print('ERROR')
        pass
    finally:
        #print('no to pa')
        f.close()


def wisielec():
    print('ee')
    while True:
       time.sleep(5)


if __name__ == "__main__":
    print("Start")
    nowy_dzien()
    odczyt_komend()
    komendy_zegara()
    while True:
       time.sleep(1)
    #wisielec()
    print('nnn')
