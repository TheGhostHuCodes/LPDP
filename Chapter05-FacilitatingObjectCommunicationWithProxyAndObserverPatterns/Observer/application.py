#!/usr/bin/env python3
import time

from subject import Subject
from observer import USATimeObserver, EUTimeObserver

if __name__ == '__main__':
    subject = Subject()

    print("Adding usa_time_observer")
    observer1 = USATimeObserver('usa_time_observer')
    subject.register_observer(observer1)
    subject.notify_observers()

    time.sleep(2)
    print("Adding eu_time_observer")
    observer2 = EUTimeObserver('eu_time_observer')
    subject.register_observer(observer2)
    subject.notify_observers()

    time.sleep(2)
    print("Removing usa_time_observer")
    subject.unregister_observer(observer1)
    subject.notify_observers()
