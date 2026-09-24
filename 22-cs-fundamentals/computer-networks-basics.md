# Computer Networks Basics

## 1. Definition
Computer networking is the interconnection of multiple devices to share resources and exchange data, governed by standardized protocols, primarily the OSI model and the TCP/IP suite.

## 2. Intuition
Think of sending a letter. 
- Application (writing the letter).
- Transport (choosing Certified Mail for guaranteed delivery, or Standard Mail for speed).
- Network (the postal addressing system, ZIP codes).
- Data Link (the mail trucks moving between local post offices).
- Physical (the road).

## 3. Why it exists
To allow isolated computers to communicate globally. The rigid layered models ensure that a Python web server (Application) doesn't need to know if the user is on WiFi or Ethernet (Physical); the layers abstract away the complexity below them.

## 4. Mechanics
**TCP/IP (and OSI) Layers:**
- **L7 Application:** HTTP, DNS, WebSockets. Data formatting.
- **L4 Transport:** 
  - **TCP:** Connection-oriented, reliable, guarantees order (Handshake, ACKs). Used for Web/Email.
  - **UDP:** Connectionless, fast, unreliable (drops packets). Used for Video Streaming/Gaming.
- **L3 Network:** IP (Internet Protocol), Routers. Routing packets across the globe using IP addresses.
- **L2 Data Link:** MAC addresses, Switches. Moving frames within a local network (LAN).
- **L1 Physical:** Cables, Radio waves, Bits.

## 5. Complexity (Time & Space)
- **Latency Numbers:** L1 cache (0.5 ns) -> Main Memory (100 ns) -> SSD (15,000 ns) -> Network Ping inside datacenter (500,000 ns) -> Network Ping CA to Europe (150,000,000 ns). *Network calls are incredibly slow compared to CPU operations.*

## 6. Tiny worked example
User types `google.com`.
1. **DNS (L7):** Queries a DNS server to translate `google.com` to IP `142.250.190.46`.
2. **TCP (L4):** Performs 3-way handshake (`SYN`, `SYN-ACK`, `ACK`) with the IP on port 443.
3. **TLS (L7/L6):** Handshake to establish encryption keys (HTTPS).
4. **HTTP (L7):** Sends `GET / HTTP/1.1`.

## 7. Code (Python)
```python
import socket

# A basic TCP client
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("google.com", 80)) # DNS resolution and TCP handshake
s.sendall(b"GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")

response = s.recv(4096)
print(response.decode().split('\n')[0]) # HTTP/1.1 200 OK
s.close()
```

## 8. Common mistakes
- **HTTP status code ignorance:** Assuming a 200 OK means the API call succeeded logically. An API might return 200 OK with `{"error": "invalid user"}`.
- **Ignoring network latency in design:** Making 100 sequential API calls in a loop instead of sending a single batch request. Sequential network calls compound the speed of light delay.

## 9. 30-second interview answer
"Computer networks rely on layered protocol models, primarily TCP/IP. The Application layer handles protocols like HTTP and DNS. The Transport layer ensures data delivery, utilizing TCP for reliable, ordered communication via handshakes, or UDP for fast, connectionless streaming. The Network layer uses IP addresses and routers to navigate the global internet, while the Data Link layer uses MAC addresses and switches for local delivery."

## 10. 2-minute interview answer
"Understanding networks requires understanding the OSI or TCP/IP layered abstractions, where each layer solves a specific problem without worrying about the layers below it. At the Application layer (L7), we deal with HTTP, REST APIs, and DNS (which acts as the internet's phonebook, translating domain names to IP addresses). When an app sends data, it passes to the Transport layer (L4). Here, we choose between TCP and UDP. TCP is connection-oriented; it uses a 3-way handshake, acknowledges received packets, and retransmits lost ones, making it essential for web traffic and file transfers. UDP just blasts packets into the void—it's lossy but very fast, perfect for video calls or real-time gaming. This segment is wrapped in an IP packet at the Network Layer (L3), which routers use to find the best path across the internet. Finally, the Data Link layer (L2) uses MAC addresses to hop the packet across individual physical links (like from your laptop to the WiFi router). In system design, knowing these limits is crucial—specifically the latency overhead of establishing TCP and TLS connections, which is why we use connection pooling and Keep-Alive headers in production."

## 11. Follow-ups
- "What happens during a TCP 3-way handshake?" (Client sends SYN (synchronize). Server replies with SYN-ACK. Client replies with ACK (acknowledge). Connection is established. Takes 1.5 round trips).

## 12. Deeper questions
- "What is a NAT (Network Address Translation)?" (IPv4 only has 4 billion addresses, which isn't enough for every device. Your home router has one public IP. All devices inside your home have private IPs (like 192.168.x.x). The router translates private IPs to its public IP and vice versa using port mapping).

## 13. Related concepts
- **System Design**: Networking is the foundation of distributed systems.
- **Processes vs Threads**: Using async/threads to handle slow network I/O.

## 14. When it breaks / Edge cases
- Packet Loss and TCP Congestion: If a network link gets saturated, routers drop packets. TCP detects this (missing ACKs), assumes the network is congested, and drastically cuts its sending speed (TCP Congestion Control window), ruining throughput.

## 15. Comparison with alternative approaches
- **HTTP/1.1 vs HTTP/2 vs HTTP/3:** HTTP/1.1 requires a new TCP connection (or blocked sequential requests) for each file. HTTP/2 multiplexes over a single TCP connection. HTTP/3 replaces TCP with QUIC (built on UDP) to eliminate Head-of-Line blocking.

---
*Where this shows up in ML:*
Distributed training (NCCL, InfiniBand vs Ethernet), serving models via REST/gRPC APIs.
