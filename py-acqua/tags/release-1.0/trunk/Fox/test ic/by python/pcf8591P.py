from i2c import *
 
def main ():
        i2c_fixed = 0x09
        i2c_addr  = 0x01
 
        print "Reading from 4 ch 8 bit A/D converter PCF8591"
 
        if i2c_open () < 0:
                print "i2c open error"
                return 1
 
        ch = 0
 
        while "azz":
                i2c_start ()
 
                if i2c_outbyte ((i2c_fixed<<4)|(i2c_addr<<1)|0) == 0:
                        print "NACK received"
                        i2c_stop ()
                        continue
 
                if i2c_outbyte (ch) == 0:
                        print "NACK received"
                        i2c_stop ()
                        continue
 
                i2c_stop ()
                i2c_start ()
 
                if i2c_outbyte((i2c_fixed<<4)|(i2c_addr<<1)|1) == 0:
                        print "NACK received"
                        i2c_stop ()
                        continue
 
                i2c_inbyte (0)
                value = i2c_inbyte (1)
                i2c_stop ()
 
                print "CH%d = %.4fv (%.4f hex/n)" % (ch,value*0.012941,value)
 
                ch += 1
 
                if ch == 4:
                        break;
 
        i2c_close ()
        return 0
main()
