# In Plain Sight
(Web, 70 points)

Gives a website address, which appears to be down.
The hint mentions "dig", which is a DNS tool. If we run a TXT query (ANY query not allowed :( ), we get the flag.

```
dig -t txt blockingthesky.com

; <<>> DiG 9.10.3-P4-Ubuntu <<>> -t txt blockingthesky.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 28521
;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 512
;; QUESTION SECTION:
;blockingthesky.com.		IN	TXT

;; ANSWER SECTION:
blockingthesky.com.	30	IN	TXT	"easyctf{betcha_wish_you_could_have_used_ANY}"
blockingthesky.com.	30	IN	TXT	"_globalsign-domain-verification=kXlECiyonFE_qsQR-8ki6BOIdVru3bzxpwMDZr334_"

;; Query time: 21 msec
;; SERVER: 127.0.1.1#53(127.0.1.1)
;; WHEN: Fri Feb 16 08:11:04 GMT 2018
;; MSG SIZE  rcvd: 191
```
