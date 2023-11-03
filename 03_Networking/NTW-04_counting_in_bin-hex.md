## COUNTING IN BINARY AND HEX:

* Binary numbers are important because using them instead of the decimal system simplifies the design of computers and related technologies.  

* The main advantage of a Hexadecimal Number is that it is very compact and by using a base of 16 means that the number of digits used   
  to represent a given number is usually less than in binary or decimal.  

## KEY-TERMS:

* binary = a base 2 number  
* decimal = a base 10 number  
* hexadecimal = a base 16 number

## ASSIGNMENT:

### Study:  
* Counting in base 2 and base 16  

* View tables and explanation given under RESULT.


## USED RESOURCES:

[decimal-to-binary](https://www.youtube.com/watch?v=RrJXLdv1i74)

[hex-to-decimal](https://www.youtube.com/watch?v=pg-HEGBpCQk)

[decimal-to-hex](https://www.youtube.com/watch?v=QJW6qnfhC70)

## DIFFICULTIES:

None  

## RESULT:

### Binary -> Decimal 


|   |   |   |   |  |  |  |  |  
|:-:|:-:|:--|:-:|:-:|:-:|:-:|:-:|    
|128| 64| 32| 16| 8| 4| 2| 1|  
| 1  |0  |0  |1 |1 |0 |0 |0 |    
|+128|0|0|+16|+8|0|0|0|  

### Binary 10011000 is 152 Decimal

### For decimal to binary: 154 in binary:

* Start subtracting the highest number in the decimal line above from 154 and work your way to the right.  
* **If you can subtract notate a 1, if not notate a 0.**  

|decimal calc      |bin output|
|:-----------------|:---------|  
|154 - 128 = 26    | 1        |  
| 26 - 64 = not pos| 10       |  
| 26 - 32 = np     | 100      |  
| 26 - 16 = 10     | 1001     |  
| 10 - 8 = 2       | 10011    |  
| 2 - 4 = np       | 100110   | 
| 2 - 2 = 0        | 1001101  |  
| 0 -1 = np        | 10011010 |    

So, 154 in binary is: 10011010  

* Smallest 8 bit binary: 0000 0000 = 0  
* Largest 8 bit binary: 1111 1111 = 255  

### Convert the following decimals into binary.  
|Decimal   |Binary     |  
|:-------- |:--------: |  
|16        |10000      |  
|128       |1000 0000  |  
|228       |1110 0100  |  
|112       |1110000   |  
|73        |1001001    |    

### Convert the following binary number into decimal.
|Binary |Decimal |  
|:---------|:--------|  
|1010 1010 |170      |  
|1111 0000 |240      |  
|1101 1011 |219      |  
|1010 0000 |160      |  
|0011 1010 |58       |  


## HEXADECIMAL base 16.

### The hexadecimal digit is expanded to multiply each digit with the power of 16.  
### The power starts at 0 from the right moving forward towards the left with the increase in power.  

### |16^7|16^6|16^5|16^4|16^3|16^2|16^1|16^0|  

**Hexa = 6 + decimal = 10  --> Hexadecimal = 16**  

0 -> 0 | 10 -> A  
1 -> 1 | 11 -> B  
2 -> 2 | 12 -> C    
3 -> 3 | 13 -> D  
4 -> 4 | 14 -> E  
5 -> 5 | 15 -> F  
6 -> 6  
7 -> 7  
8 -> 8  
9 -> 9  


### How to calculate from decimal to hexadecimal.
479 -> hex  

479 : 16 = 29.9375  
this leaves an integer of 29 and a remainder of .9375  
16 * .9375 = 15

29 : 16 = 1.8125 
this leaves an integer of 1 and a remainder of .8125  
16 * .8125 = 13

1 : 16 = 0.0625 
this leaves 0 and a remainder of .0625  
16 * .0625 = 1  
when you get to 0 you stop  

To form the hexadecimal you start with the 'most significant number' which is 1 (the last remainder)  
Then go up to the 'least significant number', which is 15 (the first remainder)  
So this comes down to 1 which is equivalent to 1 in hex, then 13 which is equivalent to d in hex  
then 15 which is equivalent to f in hex.  

### decimal 479 == hex 1df  

### Translate the following decimals into hexadecimal.
|Decimal   | Hex     |  
|:---------|:--------|  
|15        |f        |  
|37        |25       |  
|246       |f6       |  
|125       |9c       |  
|209       |d1       |  

### How to calculate from hex to decimal.
88 hex -> decimal  

|8       |8    |    
|:------:|:---:|  
|16^1    |16^0 |  
|8 * 16  |8 * 1|  
|128     |8    |   

**128 + 8 = 136**    
### 88 hex == decimal 136   


### Translate the following hexadecimals to decimal.
|Hex       |Decimal  |  
|:---------|:--------|  
|88        |136      |  
|e0        |224      |  
|cb        |203      |    
|2f        |47       |    
|d8        |216      |  

