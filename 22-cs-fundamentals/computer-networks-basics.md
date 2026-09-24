# Computer Networks Basics

## 1. OSI Model (7 Layers)
```
7. Application   — HTTP, FTP, SMTP, DNS, WebSocket
6. Presentation  — SSL/TLS, encoding, compression
5. Session       — session management
4. Transport     — TCP, UDP (ports, reliability)
3. Network       — IP, ICMP, routing
2. Data Link     — Ethernet, MAC addresses, switches
1. Physical      — bits on wire, fiber, radio
```
Mnemonic: "All People Seem To Need Data Processing"

## 2. TCP vs UDP
| | TCP | UDP |
|--|-----|-----|
| Connection | Connection-oriented (3-way handshake) | Connectionless |
| Reliability | Guaranteed delivery, ordered | Best-effort, no ordering |
| Flow control | Yes (sliding window) | No |
| Congestion control | Yes | No |
| Overhead | Higher | Lower |
| Use cases | HTTP, email, FTP | DNS, video streaming, gaming |

## 3. TCP 3-Way Handshake
```
Client → SYN → Server
Client ← SYN-ACK ← Server
Client → ACK → Server
[Connection established]
```
Termination: 4-way FIN handshake.

## 4. HTTP vs HTTPS
- HTTP: plaintext, port 80.
- HTTPS: HTTP over TLS (Transport Layer Security), port 443.
- TLS handshake: negotiate cipher, exchange certificates, establish session key.
- Data encrypted end-to-end after handshake.

## 5. HTTP Methods
GET (read), POST (create), PUT (replace), PATCH (partial update), DELETE (remove), OPTIONS (CORS preflight).

## 6. HTTP Status Codes
```
2xx Success:   200 OK, 201 Created, 204 No Content
3xx Redirect:  301 Permanent, 302 Temporary, 304 Not Modified
4xx Client:    400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 429 Rate Limited
5xx Server:    500 Internal Error, 502 Bad Gateway, 503 Unavailable, 504 Timeout
```

## 7. DNS (Domain Name System)
Translates domain names → IP addresses.
```
Browser → Recursive Resolver → Root NS → TLD NS (.com) → Authoritative NS → IP
Result cached at each level (TTL-based).
```
Record types: A (IPv4), AAAA (IPv6), CNAME (alias), MX (mail), TXT (verification).

## 8. CDN (Content Delivery Network)
Distribute static assets to geographically distributed edge servers.
User routed to nearest PoP (Point of Presence) → lower latency.
Examples: Cloudflare, AWS CloudFront, Akamai.

## 9. Load Balancer
Distributes incoming requests across backend servers.
Algorithms: Round Robin, Least Connections, IP Hash, Weighted.
Operates at L4 (TCP) or L7 (HTTP — can route by URL/headers).

## 10. WebSockets
Full-duplex persistent connection between client and server.
Starts as HTTP, upgraded via `Upgrade: websocket` header.
Use for: chat, real-time notifications, live dashboards.

## 11. REST vs GraphQL
```
REST: GET /users/1, POST /orders — multiple endpoints, fixed response shape
GraphQL: single /graphql endpoint, client specifies exact fields needed
```

## 12. Latency Numbers
```
L1 cache: 1 ns           RAM: 100 ns
SSD: 100 µs              HDD: 10 ms
Same datacenter RTT: 0.5 ms
Cross-continent RTT: 150 ms
```

## 13. Subnet and CIDR
192.168.1.0/24 → 256 addresses, subnet mask 255.255.255.0.
Private ranges: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16.

## 14. Common Protocols Summary
| Protocol | Port | Layer | Purpose |
|----------|------|-------|---------|
| HTTP | 80 | 7 | Web |
| HTTPS | 443 | 7 | Secure web |
| DNS | 53 | 7 | Name resolution |
| SSH | 22 | 7 | Remote shell |
| SMTP | 25 | 7 | Email |
| TCP | — | 4 | Reliable transport |
| UDP | — | 4 | Fast transport |

## 15. Interview Tips
- TCP 3-way handshake: know SYN/SYN-ACK/ACK by heart.
- HTTPS: "HTTP + TLS encryption, port 443."
- DNS: resolver hierarchy, TTL caching.
- Know difference between L4 and L7 load balancers.
