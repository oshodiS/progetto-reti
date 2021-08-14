import random
import socket
import time
from threading import Thread
from termcolor import colored
import datetime
import json


# Ogni device rappresenta 24 ore in 24 secondi.
# Ogni secondo vengono generati dei valori dal device, e ogni 24 secondi (che rappresentano 24 ore)
# vengono inviati al gateway


class Device(Thread):
    def __init__(self, device_ip_address, gateway_ip_address, server_port, frequency):
        # variable initialization
        self.device_ip_address = device_ip_address
        self.gateway_ip_address = gateway_ip_address
        self.server_port = server_port
        self.frequency = frequency
        self.data = []
        # Thread setting
        Thread.__init__(self)
        self.daemon = True
        # socket initialization
        self.send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_values(self, values):
        try:
            self.send.sendto(values.encode(), (self.gateway_ip_address, int(self.server_port)))
            print(colored(f"CLIENT --> Messaggio Inviato =  {values}", 'green'))
        except Exception as exc:
            print(colored(f"Client error = {exc}", 'red'))

    # ritorna una stringa nel formato oggetto json -> { id_address = "", ... }
    def __generate_random_measurements(self):
        return {
            "device_ip_address": self.device_ip_address,
            "time_of_measurement": datetime.datetime.now().isoformat(),
            "temperature": random.randint(18, 36),
            "humidity": random.randint(0, 100)
        }

    def run(self):
        print(colored(f"Device {self.server_ip_address}  created ", "yellow"))
        while True:
            # Esegue 24 misure in un giorno, la lunghezza del giorno è specificata fa frequency nel costruttore
            for i in range(24):
                # aggiunge all'array di dizionari il valore di una lettura
                self.data.append(self.__generate_random_measurements())
                time.sleep(self.frequency / 24)
            # Trasformazione dei dati in json per l'invio
            json_data = json.dumps(self.data)
            self.send_values(json.dumps(self.data))
            # Dopo l'invio dei dati vengono resettati
            self.data = []


if __name__ == "__main__":
    print("not executable as main")
