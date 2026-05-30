KEY=$(openssl rand -base64 32 | tr '+/' '-_' | tr -d '=')
FILE=".env.docker"

touch "$FILE"

if grep -q "^FIELD_ENCRYPTION_KEY=" "$FILE"; then
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then    
        sed -i "s/^FIELD_ENCRYPTION_KEY=.*/FIELD_ENCRYPTION_KEY=$KEY/" "$FILE"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i "" "s/^FIELD_ENCRYPTION_KEY=.*/FIELD_ENCRYPTION_KEY=$KEY/" "$FILE"
    elif [[ "$OSTYPE" == "msys"* ]] || [[ "$OSTYPE" == "cygwin"* ]]; then
        sed -i "s/^FIELD_ENCRYPTION_KEY=.*/FIELD_ENCRYPTION_KEY=$KEY/" "$FILE"
    else
        grep -v "^FIELD_ENCRYPTION_KEY=" "$FILE" > "$FILE.tmp"
        echo "FIELD_ENCRYPTION_KEY=$KEY" >> "$FILE.tmp"
        mv "$FILE.tmp" "$FILE"
    fi
else
    MONGODB_INITDB_ROOT_USERNAME=user
    MONGODB_INITDB_ROOT_PASSWORD=pass
    echo """###
API_ADDR=127.0.0.1
API_PORT=8090

# Do not touch this line unless you are sure of what you are doing, safely rerun setup to update
FIELD_ENCRYPTION_KEY=$KEY
###
MONGODB_INITDB_ROOT_USERNAME=user
MONGODB_INITDB_ROOT_PASSWORD=pass
MONGOT_LOG_FILE=/dev/stderr
RUNNER_LOG_FILE=/dev/stderr

# Do not touch this line, as it is generated from above values
MONGODB_URI=mongodb://\${MONGODB_INITDB_ROOT_USERNAME}:\${MONGODB_INITDB_ROOT_PASSWORD}@mongodb:27017/flux_db?authSource=admin
###
TRAGGO_DEFAULT_USER_NAME="user"
TRAGGO_DEFAULT_USER_PASS="pass"
TRAGGO_SERVER_BASE_PATH="/traggo"
###""" >> "$FILE"
fi