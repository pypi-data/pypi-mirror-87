#pyModSlave

pyModSlave is a free python-based implementation of a ModBus slave application for simulation purposes and is based on [modbus-tk] (http://code.google.com/p/modbus-tk/), [pySerial] (http://pyserial.sourceforge.net/) and [pyQt5] (http://www.riverbankcomputing.co.uk).

It starts a TCP/RTU ModBus Slave.Builds 4 data blocks (coils,discrete inputs,input registers,holding registers) and sets random values. You can also set values for individual registers.

To configure the logging level set the 'LoggingLevel' in 'pyModSlave.ini' file
- CRITICAL : 50
- ERROR : 40
- WARNING : 30 [default]
- INFO : 20
- DEBUG : 10
- NOTSET : 0

