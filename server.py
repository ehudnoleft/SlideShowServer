import http.server 
import socketserver
import os

class SlideShow(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # self.BuildHtml()
        self.send_response(200)
        if self.path == '/':
            self.path = 'index.html'

        # self.send_header("Content-type", "text/html")
        # self.end_headers()
        # html = self.BuildHtml()
        # self.wfile.write(bytes(html, "utf8"))
        return http.server.SimpleHTTPRequestHandler.do_GET(self)
        # return

    def BuildHtml(self):
        images = self.FindImageLocations()
        html = f"<html><head><title>SlideShow</title><link rel='stylesheet' href='/assets/stylesheet.css'></head>"
        html = html + f"<body><div class='imgbox'><img id='image' class='center-fit' src='/{imageDir}{images[0]}' alt='picture' />{self.BuildScript(images)}</div>"
        html = html + f"</body></html>"
        f = open('index.html', "w")
        f.write(html)
        f.close()
        return html
    
    def BuildScript(self, images):
        script = f" <script type = 'text/javascript'>"
        script = script + "var image=document.getElementById('image');"
        imageListString = "["
        for i in images:
            imageListString = imageListString + f"'/assets/pics/{i}',"
        
        imageListString += "]"

        script += f"const imageArray = {imageListString}; var currPos = 0;"
        script= script + "function volgendefoto() {"
        
        script += "if (++currPos >= imageArray.length) {currPos = 0;} image.src = imageArray[currPos];} "

        script += "function timer(){setInterval(volgendefoto, 3000);}       </script>"
        return script

    def FindImageLocations(self):
        images = os.listdir(imageDir)
        return images

imageDir = 'assets/pics/'

handler = SlideShow

hostName = "localhost"
serverPort = 8081

webServer = socketserver.TCPServer((hostName, serverPort), SlideShow)
print("Server started http://%s:%s" % (hostName, serverPort))

try:
    webServer.serve_forever()
except KeyboardInterrupt:
    pass
    webServer.server_close()
    print("Server stopped.")


    