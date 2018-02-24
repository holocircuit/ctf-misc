# Digging For Soup
(Web, 150 points)

Another DNS challenge.

Doing a text query gives you a message:
`"Close, but no cigar... where else could it be? hint: the nameserver's IP is 159.65.43.62"`

Then doing a zone transfer with that nameserver gives you the flag:
```$ dig @159.65.43.62 nicebowlofsoup.com axfr

; <<>> DiG 9.10.3-P4-Ubuntu <<>> @159.65.43.62 nicebowlofsoup.com axfr
; (1 server found)
;; global options: +cmd
nicebowlofsoup.com.	86400	IN	SOA	ns1.nicebowlofsoup.com. hostmaster.nicebowlofsoup.com. 2018021205 28800 7200 604800 86400
easyctf.nicebowlofsoup.com. 10	IN	TXT	"easyctf{why_do_i_even_have_this_domain}"
nicebowlofsoup.com.	100	IN	TXT	"Close, but no cigar... where else could it be? hint: the nameserver's IP is 159.65.43.62"
nicebowlofsoup.com.	86400	IN	SOA	ns1.nicebowlofsoup.com. hostmaster.nicebowlofsoup.com. 2018021205 28800 7200 604800 86400
;; Query time: 177 msec
;; SERVER: 159.65.43.62#53(159.65.43.62)
;; WHEN: Sat Feb 17 00:53:14 GMT 2018
;; XFR size: 4 records (messages 3, bytes 404)
```
