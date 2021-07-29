import multiprocessing
import time

NULL_CHAR = chr(0x00)

class KeyboardProcess:
    keyboard = {
      "a": 0x04,
      "esc": 0x29
    }
    service = None
    
    def press_key(self, id):
      self.write_report(NULL_CHAR*2+chr(id)+NULL_CHAR*5)
      # Release keys
      self.write_report(NULL_CHAR*8)
    
    def write_report(self, report):
      with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())
            
    def pressEscForever(self, key, timespan):
      while(True):
          self.press_key(self.keyboard[key])
          time.sleep(timespan)
    
    def stop(self):
      if self.service is not None:
        self.service.terminate()
    def start(self, key="esc", timespan=300):
      self.stop()
      self.service = multiprocessing.Process(name='fake-keyboard-service', target=self.pressEscForever, args=(key,timespan,))
      self.service.start()
    def status(self):
      if self.service is None:
        return "STOP"
      return "RUN" if self.service.is_alive() else "STOP"
