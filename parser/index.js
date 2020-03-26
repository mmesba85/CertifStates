const fs = require('fs');
const { Certificate } = require('@fidm/x509');
const perf = require('execution-time')();
var forge = require('node-forge');

perf.start();

const pemDirectory = cleanDirname(process.argv[2]);

const json = {}
const doubleChecker = []

fs.readdir(pemDirectory, (err, files) => {
    var idCert = 1;
    files.forEach(file => {

        var pathFile = pemDirectory + "/" + file
        try {
            const issuer = Certificate.fromPEM(fs.readFileSync(pathFile));

            const parsedCert = {
                keyType: issuer.publicKey.algo,
                dnsNames: issuer.dnsNames.toString().split(','),
                ipAdressess: issuer.ipAddresses.toString().split(','),
                publicKeyRaw: Buffer.from(issuer.publicKey.toJSON().publicKey.toJSON().data).toString('hex'),
                commonName: issuer.issuer.commonName,
                countryName: issuer.issuer.countryName
            }

            if (!doubleChecker.includes(JSON.stringify(parsedCert))) {
                json[idCert] = parsedCert
                idCert++;
                doubleChecker.push(JSON.stringify(parsedCert))
            }
            
        }
        catch (err) {
            console.log(err)
        }

    });

    
    let data = JSON.stringify(json);
    fs.writeFileSync('certificat.json', data);

    const result_perf = perf.stop();

    console.log("Execution time: " + result_perf.words);

    return json;

});


function cleanDirname(dir) {
    if(dir[dir.length - 1] === '/') {
        return dir.slice(0, -1)
    }
    else {
        return dir;
    }
}