import modlib

c = modlib.ModbusServerContext(
	coils_address=1, coils_count=3,
	holding_registers_address=30,
	holding_registers_count=3)
c.setHoldingRegisterValues(address=30, values=[20])
c.setCoilValues(address=1, values=[True])
s = modlib.ModbusTCPServer(context=c)
try:
	print "Partito...."
	print "Ctrl+C pressed - exiting..."
	s.serve_forever()
except KeyboardInterrupt:
	print "Ctrl+C pressed - exiting..."
s.server_close()
