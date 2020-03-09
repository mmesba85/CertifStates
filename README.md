Certificates State
===

# Get `n` certificates from a 7GB certificates directory

Opening such a huge directory might make your file explorer crash/freeze.

![](https://i.imgur.com/H4EICAS.png)

```shell script
# copy_certificates.sh

for i in $(cat certificate_filenames.txt); do
    echo $i
    cp ../cert/$i ./sample_certificates/
done
```

This script copies 500 certificates from `../cert/` to `./sample_certificates/`.