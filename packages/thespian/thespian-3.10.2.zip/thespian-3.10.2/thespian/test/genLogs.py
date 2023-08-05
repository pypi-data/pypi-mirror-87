from thespian.actors import *

class LoggingActor(Actor):
    def receiveMessage(self, msg, sender):
        if msg == "Logs?":
            for ii in range(2):
                # self.logger().setLevel((ii)*20)
                logging.getLogger().setLevel(ii*20)
                self.logger().critical('Set log level to %d', (ii)*20)
                self.logger().debug("Debug message %d", ii)
                self.logger().info("Info message %d", ii)
                self.logger().warning("Warning message %d", ii)
                self.logger().error("Error message %d", ii)
            self.requestor = sender
            self.wakeupAfter(1)
        elif isinstance(msg, WakeupMessage) and getattr(self, 'requestor', None):
            self.send(self.requestor, 4 * 2)
            
if __name__ == "__main__":
    import sys
    print(sys.argv)
    asys = ActorSystem(systemBase=sys.argv[1] if len(sys.argv) > 1 else "simpleSystemBase",
                       logDefs={
                           'version' : 1,
                           'handlers': { 'testStream': { 'class': 'logging.StreamHandler',
                                                         'stream': sys.stdout,
                                                         'level': logging.WARNING,
                           },
                           },
                           'root': { 'handlers': ['testStream'], 'level': logging.INFO, },
                           'disable_existing_loggers': False,
                       })
    la = asys.createActor(LoggingActor)
    num = asys.ask(la, 'Logs?', 10)
    asys.shutdown()
    print(num)
    assert num == 8
