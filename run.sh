backend_dir="h2overlord-python/src/h2overlord_python/"
frontend_dir="web-build/"


cleanup() {
    echo "Received interrupt signal. Stopping the h2overlord."
    if [ -n "${webserver_pid:-}" ] && kill -0 "$webserver_pid" 2>/dev/null; then
        kill "$webserver_pid"           # send SIGTERM
        wait "$webserver_pid" 2>/dev/null   # reap it
    fi
        if [ -n "${backend_pid:-}" ] && kill -0 "$backend_pid" 2>/dev/null; then
        kill "$backend_pid"           # send SIGTERM
        wait "$backend_pid" 2>/dev/null   # reap it
    fi
    exit 130   # 128 + 2  (script was interrupted)
}

trap cleanup INT TERM
trap cleanup EXIT

echo "STARTING THE H2OVERLORD!"
echo "1. Starting the webserver"
cd $frontend_dir 
python3 -m http.server 9000 > frontend.log &
webserver_pid=$!

echo "Started web server at localhost:9000 with PID ${webserver_pid}"

cd ..
echo "2. Starting the backend"
cd $backend_dir

poetry run python3 main.py > backend.log &
backend_pid=$!
echo "Started the backend at localhost:8080 with PID ${backend_pid}"


wait "$backend_pid"
