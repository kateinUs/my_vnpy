# flake8: noqa
import sys
sys.path.append('../../')
from vnpy.event import EventEngine, Event
from vnpy.gateway.ctp import CtpGateway

from vnpy.trader.engine import MainEngine
from vnpy.trader.ui import MainWindow, create_qapp
from vnpy.trader.event import EVENT_TICK, EVENT_CONTRACT
from vnpy.trader.object import SubscribeRequest

class TickCountManager:

    def __init__(self, main_engine):
        """"""
        self.tick_count: int = 0
        self.main_engine = main_engine
    
    def process_contract(self, event: Event):
        """"""
        contract = event.data

        req = SubscribeRequest(contract.symbol, contract.exchange, )
        self.main_engine.subscribe(req, contract.gateway_name)

    def process_tick_event(self, event: Event):
        """"""
        self.tick_count += 1

        tick = event.data
        print(self.tick_count, tick.vt_symbol, tick.last_price, tick.datetime)
    
    

def main():
    """"""
    qapp = create_qapp()

    event_engine = EventEngine()

    main_engine = MainEngine(event_engine)

    main_engine.add_gateway(CtpGateway)

    manager = TickCountManager(main_engine)
    event_engine.register(EVENT_TICK, manager.process_tick_event);
    event_engine.register(EVENT_CONTRACT, manager.process_contract);
    
    main_window = MainWindow(main_engine, event_engine)
    main_window.showMaximized()

    qapp.exec()


if __name__ == "__main__":
    main()