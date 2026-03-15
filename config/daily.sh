#!/bin/bash

sudo port -d selfupdate
sudo port upgrade outdated
./kopia_sync


