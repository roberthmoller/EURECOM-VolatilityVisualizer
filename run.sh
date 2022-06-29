#!/bin/bash
source .venv/bin/activate

gitServerPort=8888
browserServerPort=80
browserServerAddress="$CODESPACE_NAME"-"$gitServerPort".githubpreview.dev

streamlit run --server.port $gitServerPort --browser.serverPort $browserServerPort --browser.serverAddress $browserServerAddress *Home*