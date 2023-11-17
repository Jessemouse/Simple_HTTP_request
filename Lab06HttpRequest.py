#Task: 
# 1. Server opens connection 
# 2. Client connects with text message
# 3. Server prints to terminal window 
# 4. Connection is shut down
# 5. Server remains open

# Hints: Use port 80, server receives byte-arrays, transform into string using decode ('ASCII')
# ---- IMPORTS ---- # 
import socket

# ---- FUNCTIONS ---- # 
#Establish a socket with specified ip and port
def init_connection(port: int, ip: str, timeout: int):
    #AF_INET is IPv4, enter AF_INET6 for IPv6. SOCK_STREAM specifies socket type of TCP. Enter SOCK_DGRAM for UDP. 
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((ip, port))
    server_sock.settimeout(timeout)
    server_sock.listen(1)
    return server_sock

#Establish new connection
def new_connection(timeout: int, sock):
    try:
        client, address = sock.accept()
    except TimeoutError:
        return TimeoutError
    client.settimeout(timeout)
    return client, address

#Creates the HTML content 
def make_html_res(html_req):
    # f""" used for multi-line string literal
    html_content = f"""
    <html>
    <head><title>Browser request</title></head>
    <body><h1>Your browser sent the following request:</h1><br>
    <pre>{html_req}</pre>
    </body>
    </html>
    """
    return html_content

# Send an HTML response
def send_html_res(html_content, client_sock):
    #Start with response to open connection for HTML content 
    response = 'HTTP/1.1 200 OK \r\n'
    response += 'Content-Type: text/html; charset=utf-8\r\n'
    response += 'Content-Length: ' + str(len(html_content.encode('utf-8'))) + '\r\n'
    response += html_content
    client_sock.sendall(response.encode('utf-8'))
    
# ----- Program ----- #
server_sock = init_connection(80, "127.0.0.1", 15)

while True:
    timeout = 15
    try:
        client_sock, address = new_connection(timeout, server_sock)
    except:
        print(f"Could not establish connection within the timelimit {timeout} seconds")
        break
    if client_sock:
        print(f"Connection established with... \nsocket: [{client_sock}]\naddress: [{address}]")
    try:
        data = client_sock.recv(4096) #Buffer size 4096
        if data:
            html_content = make_html_res(data.decode('utf-8'))
            send_html_res(html_content, client_sock)
    except TimeoutError:
        print("Connection timeout while communicating with client")
    finally:
        client_sock.close()