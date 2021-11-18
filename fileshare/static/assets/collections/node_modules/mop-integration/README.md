[![Build Status](https://travis-ci.org/montagejs/mop-integration.png?branch=master)](http://travis-ci.org/montagejs/mop-integration)

Mop integration
===============

Tests integration between Mop, Montage and Mr.

Requires PhantomJS to be installed.

## Example

```bash
$ MOP_VERSION="#master" MR_VERSION="#master" ./integration.js
Testing mop and mr
Using mop #master in /var/folders/3j/c5plsfss7c965m4lmqvb08_c0000gn/T/mop113626-36934-1ilejy5/node_modules/mop
Using mr #master in /var/folders/3j/c5plsfss7c965m4lmqvb08_c0000gn/T/mr113626-36934-1jetamr/node_modules/mr
Running Mop on module
module passed

Running Mop on simple
simple passed
```

## Environment variables

These can be set by a CI system to vary the combination of projects that is tested.

`MR_VERSION` and `MONTAGE_VERSION` may not be both set at the same time.

### MOP_VERSION, MR_VERSION, MONTAGE_VERSION

 - `#` + hash-or-ref. To use a ref from the respective git repository.
   e.g. `#master`, or `#fb0b642`.
 - npm tag. To use a published version in npm.
   e.g. `latest` to use the most recent version, or `0.13.0`.
 - `.` + path. To use a directory relative to the current directory. For
   testing while developing. e.g. `.`, `../mop`, `./dir/mop`.

### DEBUG=true

Enables extra debug output.
