## PUBLICKEY INFRASTRUCTURE:

Public Key Infrastructure (PKI) is a set of roles, policies, hardware, software and procedures needed to  
create, manage, distribute, use, store and revoke digital certificates and manage public-key encryption.  
It consists of three entities that assure you can communicate securely over an insecure network like the public internet.  


## KEY-TERMS:

* SSL = Secure Socket Layer
* TLS = Transport Layer Security

## ASSIGNMENT:

* Create a self-signed certificate on your VM.  
* Analyze some certification paths of known websites (ex. techgrounds.nl / google.com / ing.nl).  
* Find the list of trusted certificate roots on your system (bonus points if you also find it in your VM).  



## USED RESOURCES:

[installing-ssl](https://www.atlantic.net/dedicated-server-hosting/how-to-create-and-install-a-self-signed-ssl-certificate-on-ubuntu-20-04/)

[openssl-quick-ref](https://www.digicert.com/kb/ssl-support/openssl-quick-reference-guide.htm)

[self-signed-certificate-for-apache](https://www.digitalocean.com/community/tutorials/how-to-create-a-self-signed-ssl-certificate-for-apache-in-ubuntu-20-04)
## DIFFICULTIES:

* creating the certificate, it took a while before i found the right manual for apache.

## RESULT:

### Create a self-signed certificate:  

#### Open in VM ufw firewall ports 80 and 443.  
![enable-ports80/443](../00_includes/Security/SEC7.0_80-443.png)  

## Step 1 - Enabling mod_ssl:  

#### Before we can use any SSL certificates, we first have to enable mod_ssl, an Apache module that provides support for SSL encryption.  
#### (Because i ssh into the VM i have no password and therefore created another user with sudo priviliges.)  
![enable-mod_ssl](../00_includes/Security/SEC7.1_enable-mod_ssl.png) 
#### The mod_ssl module is now enabled and ready for use.

## Step 2 - Creating the SSL Certificate:    

#### We can create the SSL key and certificate files with the openssl command:  
![ssl_key](../00_includes/Security/SEC7.3_ssl-key.png)  
#### Both of the files you created will be placed in the appropriate subdirectories under /etc/ssl.  
![crt_key-files](../00_includes/Security/SEC7.4_crt-key-files.png)

## Step 3 – Configuring Apache to Use SSL:  
#### VirtualHost config.      
![virt-host-conf](../00_includes/Security/SEC7.5_virthost-conf.png)

#### Enable config file and do a config test.  
![conf-test](../00_includes/Security/SEC7.6-config-test.png)  

![selfsigned-certificate](../00_includes/SCREENSHOTS/Security/SEC-06-1.1_creating_certificate.png)


![verification-CSR](../00_includes/SCREENSHOTS/Security/SEC-06-1.2_certificate.png)

![certificate-key](../00_includes/SCREENSHOTS/Security/SEC-06-1.3_certificate.key.png)

#### Trusted certificate roots list.

![trusted-certificate-roots-list](../00_includes/Security/SEC7.4-VM-trusted-crt-list.png)



