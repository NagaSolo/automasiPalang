#!/bin/bash

echo ""
echo "Removing containers, images, volumes, network"
echo ""
docker compose down --rmi local -v
echo ""
echo "Finish"
echo ""