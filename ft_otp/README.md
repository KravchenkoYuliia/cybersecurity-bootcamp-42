# Implementation of a TOTP (Time-based One-Time Password) system

In this project, the aim is to implement a TOTP (Time-based One-Time Password) system, which will be capable of generating ephemeral passwords from a master key using the HOTP algorithm (RFC 4226).
The program must repeat the behaviour of:
```
oathtool --totp $(cat key.txt)
```


#### Usage
to activate/deactivate a virtual python environment
```
source .venv/bin/activate
deactivate
```

make the python file executable
```
chmod +x ft_otp
```

run the program
usage
```
./ft_otp -g key.txt
./ft_otp -k ft_otp.key
```
`-g`: the program receives as argument a hexadecimal key of at least 64 characters. The program stores this key safely in a file called ft_otp.key, which is encrypted
`-k`: the program generates a new temporary password based on the key given as argument and prints it on the standard output

The content of `key.txt` can be modified
