from modlib import *
cn = TCPMasterConnection("127.0.0.1")

# Read Coils
reqb = ReadCoilsRequest(address=1, count=3)
trb = cn.createTransaction(reqb)
trb.setRequest(reqb)
resb = trb.execute()

# Read Discrete Inputs
#req = ReadDiscreteInputsRequest(address=0, count=1)
#tr.setRequest(req)
#res = tr.execute()

#Read Holding Registers
#req = WriteSingleRegisterRequest(address=30, value=15)
#req = setHoldingRegisterValues(address=30, values=10)

req = ReadHoldingRegistersRequest(address=30, count=1)
tr = cn.createTransaction(req)
tr.setRequest(req)
res = tr.execute()
print "Valore letto: " ,res.registers[0]
print "Valore letto bits: ",resb.bits[0]
