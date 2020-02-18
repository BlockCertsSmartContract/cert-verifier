[![Build Status](https://travis-ci.org/blockchain-certificates/cert-verifier.svg?branch=master)](https://travis-ci.org/blockchain-certificates/cert-verifier)
[![PyPI version](https://badge.fury.io/py/cert-verifier.svg)](https://badge.fury.io/py/cert-verifier)

# cert-verifier
Library for verifying blockchain certificates.

## Using the pypi package

The most common way to use this is to add the [latest cert-verifier pypi package](https://badge.fury.io/py/cert-verifier) to your project dependencies. 

## Configuration

Set the ethereum node you want to use in the verification processes in ``` cert-verifier/cert_verifier/config.ini ```.

The Provided ones can also be used and should work out of the box, but keep in mind that they are only recommendations.

If you want to change the ens nodes as well you can use the ```conf_sample.ini``` schema as a structure guideline.
## Verify a certificate by command line

1. Ensure you have an python environment. [Recommendations](https://github.com/blockchain-certificates/cert-issuer/blob/master/docs/virtualenv.md)

2. Ensure you have installed [solc](https://solidity.readthedocs.io/en/v0.5.3/installing-solidity.html)

3. Git clone the repository and change to the directory 
``` bash git clone https://github.com/blockchain-certificates/cert-verifier.git && cd cert-verifier ```

4. Run cert-viewer setup ```bash pip install . ```

5. Run the main program
  ```bash
  cd cert_verifier
  python verifier.py
  ```
  
## Verification process

[Read about how Blockcerts verification works](https://github.com/blockchain-certificates/cert-verifier-js#verification-process)

## Unit tests

This project uses tox to validate against several python environments.

1. Ensure you have an python environment. [Recommendations](https://github.com/blockchain-certificates/cert-issuer/blob/master/docs/virtualenv.md)

2. Run tests
    ```
    ./run_tests.sh
    ```

## Contact

Contact us at [the Blockcerts community forum](http://community.blockcerts.org/).
