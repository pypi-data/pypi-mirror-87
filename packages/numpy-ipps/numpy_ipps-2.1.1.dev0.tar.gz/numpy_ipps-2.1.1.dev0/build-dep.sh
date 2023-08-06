#!/usr/bin/env bash
apt-get update -y
apt-get install -y apt-transport-https
apt-get update -y
eval apt-get install -y $(cat "pkglist")
