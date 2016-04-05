# jays-wp-htaccess

![](http://i.imgur.com/uqqPJPb.jpg)

An .htaccess file that I use for various Wordpress websites to improve performance, security, and functionality.
*Some* informal tests on *some* sites have seen them *appear* to double in speed instantly just by uploading this file to the website's root folder. **Your results may vary**. Heavy emphasis has been placed on blocking malicious IPs and Bots.

:warning: Caution |
------------ |
The .htaccess is a powerful file. One wrong move in the .htaccess file can make a website inaccessible. Make sure you have a backup of any original .htaccess file to restore via FTP if that happens.|

This file is a mish-mash of content pulled from various sources. It's divided into a couple sections.

* **Tweaks**
  * **Show The Admin’s Email Address In Apache Error Messages**
  * **Remove Server Signature Completely**
  * **Block Access To Directories Without A Default Document**
  * **Prevent Image Hotlinking**
  * **Allow Cross-Origin Requests**
  * **Send The Cors Header For Images When Browsers Request It**
  * **Cross-Origin Web Fonts**
  * **Custom Error Pages**
  * **Prevents Overzealous 404 Errors From Apache**
  * **Turn Off Directory Indexing**
  * **Increase Maximum Upload File Size (Optional)**
  * **Add Support For Svg And Htc**
  * **Redirect All Wordpress Feeds To Feedburner**
  * **Block Access To Any Source Files**
  * **Force Internet Explorer 8/9/10 To Render Pages In The Highest Mode**
  * **Change URL**
  * **Force SSL**
  * **Serve Resources With The Proper Media Types (Mime Types)**
  * **Character Encodings As UTF-8**
* **Performance**
  * **Compress With Gzip**
  * **Mod_Deflate**
  * **Force Compression For Mangled Accept-Encoding Request Headers**
  * **Compress Media Types**
  * **Google's Mod_Pagespeed**
  * **Expire Headers**
  * **Begin Cache-Control Headers**
  * **Enable Keep-Alive**
  * **Disable Etag**
* **Security**
  * **Block Individual Ip Addresses**
  * **Strong Htaccess Protection**
  * **Remove The X-Powered-By Response Header**
  * **Recognize Ssl When Set At A Load Balancer/Proxy Level (For Cloudflare)**
  * **Prevent Wordpress Version Exposure In Readme.Html**
  * **Disable Http Trace**
  * **Block Access To Hidden Files & Directories**
  * **Block Access To Files That Can Expose Sensitive Information**
  * **Disable Access To Wordpress Wp-Config File**
  * **Disable Access To Sftp-Config.Json**
  * **Disable Access To Includes.**
  * **Pass The Default Character Set**
  * **Redirect Spammer Attacks To Bogus Site**
  * **Deny No Referer Requests** - http://www.wprecipes.com/how-to-deny-comment-posting-to-no-referrer-requests
  * **Block Browser Access To Log Files**
  * **Stop Wordpress Username Enumeration Vulnerability**
  * **Wp Hardening Security Headers**
  * **Block Common Malicious Bot Queries**
  * **Abuse User Agents Blocking** - Blocking User Agents Stops Traffic From The Named Bots Below
  * **2014 Micro Blacklist Plus Malicious Bots And Search Spiders.**
  * **Start Bad Bot Prevention**
  * **Block Specific Sites From Stealing Bandwidth By Hotlinking To Images**
  * **Abuse Http Referrer Blocking** - Blocking Referrer Domains Stops Traffic Originating From The Specified Domains
  * **Block China** - http://www.ip2location.com/free/visitor-blocker
* **301 Redirects**

## The various sources of all this goodness
* [HTML5 Boilerplate](https://github.com/h5bp/html5-boilerplate)
* [2014 Micro Blacklist](http://perishablepress.com/2014-micro-blacklist/)
* [2016 Bad Bots .htaccess List from HackRepair.com](http://pastebin.com/BPRv4TDd)
* [Htaccess Security and The Largest Block Bots List On The Web](http://www.allthingsdemocrat.com/block-bad-bots-in-htaccess.txt)
* [ip2location.com](http://www.ip2location.com/free/visitor-blocker)
* [Crunchify](http://crunchify.com/how-to-speed-up-wordpress-leveraging-browser-caching-via-htaccess/)
* [Ventureharbour](https://www.ventureharbour.com/improving-site-speed/)
* [Ducea](http://www.ducea.com/2007/10/22/apache-tips-disable-the-http-trace-method/)
* [wprecipes](http://www.wprecipes.com/how-to-deny-comment-posting-to-no-referrer-requests)
* [6G Beta](https://perishablepress.com/6g-beta/)
* [Hardening Wordpress](http://codex.wordpress.org/Hardening_WordPress)
* [WpMuDev](http://premium.wpmudev.org/blog/5-simple-htaccess-tips-to-tighten-your-sites-security/)
* [WpExplorer](http://www.wpexplorer.com/htaccess-wordpress-security/)
* [Creare](https://github.com/Creare)/[WP-htaccess](https://github.com/Creare/WP-htaccess)
