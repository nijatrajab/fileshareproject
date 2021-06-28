# FileShare

## Description

Welcome to File Share App

## Getting Started

### Dependencies

* [Docker](https://www.docker.com/get-started)

### Installing

* Clone the repo
```
git clone https://github.com/nijatrajab/fileshareproject.git
```
* Create `.env` file on cloned directory and define your passwords
```
DSK='Django Secret key'
DP=Your DB password
PGP=Your POSTGRES password
PGDP=Your PGADMIN password
```
* Open `cmd` on cloned directory then follow commands:
```
docker build .
docker-compose build
```

### Executing program

After creating docker images you can start containers for a service with 2 options
* On Docker Desktop start your containers using GUI or open `cmd` on cloned directory then follow commands:
```
docker-compose up
```
_Make sure Docker is running as an administrator. For the first time it may take a few minutes to start because of creating containers_

## Version History

* See [commit change](https://github.com/nijatrajab/fileshareproject/commits/main)
