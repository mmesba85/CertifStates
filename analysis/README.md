Public key collisions analysis
===

# `dig`: Get an IP address from a domain name and vice versa 

> nslookup and dnspython could work as well.

## Domain name to IP address

```
➜  /tmp dig -q google.com                        

; <<>> DiG 9.11.3-1ubuntu1.11-Ubuntu <<>> -q google.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 55123
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 65494
;; QUESTION SECTION:
;google.com.			IN	A

;; ANSWER SECTION:
google.com.		63	IN	A	216.58.209.238

;; Query time: 12 msec
;; SERVER: 127.0.0.53#53(127.0.0.53)
;; WHEN: Thu Mar 12 11:58:26 CET 2020
;; MSG SIZE  rcvd: 55

```

And we get an answer!

```
;; ANSWER SECTION:
google.com.		63	IN	A	216.58.209.238
```
## IP address to domain name

```
➜  /tmp dig -x 8.8.8.8

; <<>> DiG 9.11.3-1ubuntu1.11-Ubuntu <<>> -x 8.8.8.8
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 60616
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 65494
;; QUESTION SECTION:
;8.8.8.8.in-addr.arpa.		IN	PTR

;; ANSWER SECTION:
8.8.8.8.in-addr.arpa.	6567	IN	PTR	dns.google.

;; Query time: 0 msec
;; SERVER: 127.0.0.53#53(127.0.0.53)
;; WHEN: Thu Mar 12 11:57:14 CET 2020
;; MSG SIZE  rcvd: 73
```

And voila !

`8.8.8.8.in-addr.arpa.	6567	IN	PTR	dns.google.`

# `whois`: Get ASN (Autonomous System Number) from IP address

An ASN will tell us on which part of the Internet the website is located.

To get an ASN, we need the domain IP address though (previous section).

[How to find the ASN of an IP using “dig” command?](https://askubuntu.com/questions/595403/how-to-find-the-asn-of-an-ip-using-dig-command)

`whois -h whois.cymru.com " -v [IP_ADDR]"`

> It does not work if we do not include the `-h` part.
> `whois.cymru.com` is the _Team Cymru IP to ASN Lookup v1.0_ tool.
> It seems like `whois` uses their service.

Let's us it with `google.com` IP address.

```
➜  /tmp whois -h whois.cymru.com  " -v 216.58.213.174"
AS      | IP               | BGP Prefix          | CC | Registry | Allocated  | AS Name
15169   | 216.58.213.174   | 216.58.213.0/24     | US | arin     | 2012-01-27 | GOOGLE, US
```

`google.com` ASN number is `15169`.