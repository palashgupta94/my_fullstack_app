export MONGODB_ATLAS_URI="mongodb+srv://palashgupta94:har23071990@cluster0.qrhlii4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
export MONGODB_DB_NAME="mydatabase"
export MONGODB_COLLECTION_NAME="mycollection"

docker run --network host --name backend -v ./backend/data:/data -e MONGODB_ATLAS_URI=$MONGODB_ATLAS_URI -e MONGODB_DB_NAME=$MONGODB_DB_NAME -e MONGODB_COLLECTION_NAME=$MONGODB_COLLECTION_NAME backend:v1.0.0
