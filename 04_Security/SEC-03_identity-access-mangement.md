## IDENTITY and ACCESS MANAGEMENT:

Identity and access management (IAM) is the practice of making sure that people and entities with digital  
identities have the right level of access to enterprise resources like networks and databases. User roles  
and access privileges are defined and managed through an IAM system.

## KEY-TERMS:

* IAM = Identity and Access Management
* Authentication = The purpose of authentication is to verify that someone or something is who or what they claim to be.  
* Authorization = Authorization is the security process that determines a user or service's level of access.  

## ASSIGNMENT:

Study:
* The difference between authentication and authorization.
* The three factors of authentication and how MFA improves security.
* What the principle of least privilege is and how it improves security.



## USED RESOURCES:

[authentication-authorization](https://www.onelogin.com/learn/authentication-vs-authorization)

[multifactor-authentication](https://www.techtarget.com/searchsecurity/definition/multifactor-authentication-MFA)

[PoLP](https://www.paloaltonetworks.com/cyberpedia/what-is-the-principle-of-least-privilege)

## DIFFICULTIES:

None

## RESULT:

## Authentication
### To verify that you are who you say you are, authentication processes use: 
* something you know; password, security questions  
* something you have; mobile phone (OTP one time pin send to you by sms or app) or USB security tokens
* something you are ; biometric authentication, fingerprints or other physical features such as face recognition.  

## Authorization
### Common Types of Authorization:
* an ACL (access control list) e.g. sudoers file in linux
* data access; public data (website), internal data (for employees) or confidential data (data on a need to know basis)

## The difference between authentication and authorization respectively;
* Authentication verifies the identity of a user or service before granting them access, while authorization determines what they can do once they have access.  

### The similarity is: _They both provide access._

## MFA (multi factor authentication)
Multifactor authentication is a core component of an identity and access management framework.
It uses 2 or more factors of the 3 factors of authentication described above.  

A fourth factor of authentication often suggested is: location, e.g. you can use the GPS on a mobile phone to check if the requesting person is  
actually on premisses instead of somewhere in Russia.

## The principal of least priviliges and how it improves security
The principle of least privilege (PoLP) is an information security concept which maintains that a user or entity should only  
have access to the specific data, resources and applications needed to complete a required task. Organizations that follow  
the principle of least privilege can improve their security posture by significantly reducing their attack surface and risk of malware spread.  

