import time
import BaseHTTPServer
import smbus

bus=smbus.SMBus(2)
address=0x05

HOST_NAME = 'chip'
PORT_NUMBER = 8000

def StringToBytes(val):
    retVal = []
    for c in val:
            retVal.append(ord(c))
    return retVal

indexPage = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, user-scalable=no">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
<script>
$(document).ready(function(){
  $("button").click(function(){
    $.get("/" + this.id, function(data, status){});
  });
});
</script>
</head>
<body>

<table border=0>
<tr>
<td><button id="left"> &lt;-- </button></td>
<td><button id="rotate"> @ </button></td>
<td><button id="right"> --&gt; </button></td>
</tr>
<tr><td></td>
<td><button id="down">|<br/>v</td>
<td></td></tr>
</table>

</body>
</html>
"""

count=0

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
  def do_HEAD(s):
    print "HEAD " + s.path
    s.send_response(200)
    s.end_headers()
  def do_GET(s):
    global count
    count=count+1
    print str(count) + " GET " + s.path
    if s.path == "/left":
      bus.write_i2c_block_data(address, 0, StringToBytes("l"))
    elif s.path == "/right":
      bus.write_i2c_block_data(address, 0, StringToBytes("r"))
    elif s.path == "/rotate":
      bus.write_i2c_block_data(address, 0, StringToBytes("u"))
    elif s.path == "/down":
      bus.write_i2c_block_data(address, 0, StringToBytes("d"))
    else:
      s.send_response(200)
      s.send_header("Content-type", "text/html")
      s.end_headers()
      s.wfile.write(indexPage)
    

if __name__ == '__main__':
  server_class = BaseHTTPServer.HTTPServer
  httpd = server_class(("", PORT_NUMBER), MyHandler)
  print "start"
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    pass
  httpd.server_close()
  print "stop"


