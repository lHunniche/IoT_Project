import time

class LongPolling:
    def __init__(self):
        polling_addresses = []

    def is_polling(self, poller):
        for element in self.polling_addresses:
            if element[0] == poller:
                return True
        return False

    def remove_expired_polling_addresses(self):
        new_pollers = []
        for poller in self.polling_addresses:
            if poller[1] > time.time():
                new_pollers.append(poller)
        polling_addresses = new_pollers

    def add_poller(self, poller):
        self.polling_addresses.append((poller, time.time()+30))