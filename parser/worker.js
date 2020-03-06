const fs = require('fs');
const { Certificate } = require('@fidm/x509');
const perf = require('execution-time')();

perf.start();

const pemDirectory = cleanDirname(process.argv[2]);

const json = {
    certificat: [],
}



fs.readdir(pemDirectory, (err, files) => {
    var idCert = 1;
    files.forEach(file => {

        var pathFile = pemDirectory + "/" + file
        const issuer = Certificate.fromPEM(fs.readFileSync(pathFile));
        const parsedCert = {
            id: idCert,
            keyType: issuer.publicKey.algo,
            dnsNames: issuer.dnsNames.toString(),
            ipAdressess: issuer.ipAddresses.toString(),
            publicKeyRaw: issuer.publicKeyRaw,
            commonName: issuer.issuer.commonName,
            countryName: issuer.issuer.countryName
        }
        
        json.certificat.push(parsedCert)
        idCert++;
    });

    console.log(json);

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