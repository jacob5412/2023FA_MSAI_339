const { MongoClient, ServerApiVersion } = require('mongodb');
const fs = require('fs');

const dbCreds = JSON.parse(fs.readFileSync('db_creds.json'));

const uri = `mongodb+srv://${dbCreds.username}:${dbCreds.password}@${dbCreds.url}/?retryWrites=true&w=majority`;
const database = `${dbCreds.database}`;
const query = { year: { $gt: 1975, $lt: 1980 } };
const projection = { title: true, year: true, runtime: true, _id: false };
const sort = { runtime: 1 };
const outputFilePath = 'output.json';

const client = new MongoClient(uri, {
    serverApi: {
        version: ServerApiVersion.v1,
        strict: true,
        deprecationErrors: true,
    }
});

async function run() {
    try {
        // Connect the client to the server	(optional starting in v4.7)
        await client.connect();

        // Send a ping to confirm a successful connection
        const pingResult = await client.db(database).command({ ping: 1 })
        console.log('Ping result:', pingResult);

        // Create a cursor to read query
        const cursor = await client.db(database).collection('movies').find(query, { projection }).sort(sort);

        // write to file through a write stream
        const fileStream = fs.createWriteStream(outputFilePath, { flags: 'w' });
        let isFirst = true;
        fileStream.write('[');
        await cursor.forEach(document => {
            if (!isFirst) {
                fileStream.write(',');
            }
            isFirst = false;
            fileStream.write(JSON.stringify(document) + '\n');
        });
        fileStream.write(']');

        console.log(`Query result saved to ${outputFilePath}`);
    } finally {
        client.close();
    }
}
run().catch(console.dir);
