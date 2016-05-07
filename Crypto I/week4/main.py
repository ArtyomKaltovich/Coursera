import urllib2
import sys

URL = 'http://crypto-class.appspot.com/po?er='
TARGET = 'f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4'
#--------------------------------------------------------------
# padding oracle
#--------------------------------------------------------------
class PaddingOracle(object):
    def query(self, q):
        target = URL + urllib2.quote(q)    # Create query URL
        req = urllib2.Request(target)         # Send HTTP request to server
        try:
            f = urllib2.urlopen(req)          # Wait for response
        except urllib2.HTTPError, e:          
            if e.code == 404:
                return True # good padding
            return False # bad padding


def gen_padding(number):
    s = '00' * (16 - number) + format(number, '02x') * number
    #print(hex(int(s, 16)))
    return int(s, 16)


blocks = ()
ct = TARGET
while ct:
    blocks = blocks + (ct[:32],)
    ct = ct[32:]

#print '\n'.join(blocks)
possible_values = [ord(' '),] +  range(ord('a'),ord('z')+1) + range(ord('A'),ord('Z')+1) + range(0, 17)
po = PaddingOracle()

#it does not work for byte before real padding :(   
iv = blocks[0]
cif = TARGET[32:]
cur_cif = "".join(blocks[1:3]) # change here to "".join(blocks[1:3]) to get all
                     # blocks but last and then just google it for wiki page :)
msg_int = int(iv + cur_cif, 16)
message = ''
for i in xrange(1, len(cur_cif) + 1):
    #print format(msg_int, 'x')
    cur_symbol = '?'
    #for j in possible_values:
    for j in range(0,257):
        last_bytes = (gen_padding(i) ^ j << 8*(i - 1))
        last_bytes <<= 8 * 16
        #print hex(last_bytes)
        query_str = format(msg_int ^ last_bytes, 'x')
        #print query_str
        if po.query(query_str) == True:
            cur_symbol = chr(j)
            msg_int ^= j << 8 * (15 + i)
            break
    message = cur_symbol + message
    print "'" + message + "'", "".join("{:02x}".format(ord(c)) for c in message)
        