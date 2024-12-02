import { ChromaClient } from 'chromadb';

const vectorDBHost = process.env.VECTORDB_HOST || '0.0.0.0';
const vectorDBPort = process.env.VECTORDB_PORT || 8000;
const vectorDBName = process.env.VECTORDB_NAME || 'nodejs_test_collection';

const url =  `http://${vectorDBHost}:${vectorDBPort}`;
const client = new ChromaClient({path: url});

/////////////////////////////////////////////////////
// delete and recreate the collection in Chroma when
// requested by the front end
const HANDLER = async (req, res) => {
  try {
    const collection = await client.getOrCreateCollection({name: vectorDBName});
    const result = await collection.get({include: []});
    if (result && result.ids && (result.ids.length > 0)) {
      await collection.delete({ids: result.ids});
    }
    res.statusCode = 200;
    res.statusMessage = 'Success';
    res.end("Deleted succesfully, count is:" + await collection.count());
  } catch (error) {
    res.statusCode = 500;
    res.statusMessage = 'Deletion failed';
    res.end(error.toString());
  }
};

export default HANDLER;
