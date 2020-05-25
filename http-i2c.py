import time
import BaseHTTPServer
import smbus2

bus=smbus2.SMBus(2)
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
<style>
a.thumbutton{
  display:inline-block;
  padding:0.35em 1.2em;
  border:0.1em solid #FFFFFF;
  margin:0 0.3em 0.3em 0;
  border-radius:0.12em;
  box-sizing: border-box;
  text-decoration:none;
  font-weight:300;
  color:#FFFFFF;
  text-align:center;
  transition: all 0.2s;
}
a.thumbutton.hover{
  color:#000000;
  background-color:#FFFFFF;
}
@media all and (max-width:30em){
  a.button1{
    display:block;
    margin:0.4em auto;
  }
}
</style>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
<script>
$(document).ready(function(){
  $("a.thumbutton").click(function(){
    $.get("/" + this.id, function(data, status){});
    return false;
  });
});
</script>
</head>
<body bgcolor=#000000;>

<table border=0>
<tr>
  <td></td>
  <td><a href="#" id="up" class="thumbutton">&nbsp;</a></td>
  <td></td>
</tr>

<tr>
  <td><a href="#" id="left" class="thumbutton">&nbsp;</a</td>
  <td></td>
  <td><a href="#" id="right" class="thumbutton">&nbsp;</a</td>
</tr>

<tr>
  <td></td>
  <td><a href="#" id="down" class="thumbutton">&nbsp;</a></td>
  <td></td>
</tr>
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
      s.send_response(200)
    elif s.path == "/right":
      bus.write_i2c_block_data(address, 0, StringToBytes("r"))
      s.send_response(200)
    elif s.path == "/up":
      bus.write_i2c_block_data(address, 0, StringToBytes("u"))
      s.send_response(200)
    elif s.path == "/down":
      bus.write_i2c_block_data(address, 0, StringToBytes("d"))
      s.send_response(200)
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


