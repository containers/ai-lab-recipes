import process from 'process';
import { NextResponse } from 'next/server';
import { MarkdownTextSplitter, RecursiveCharacterTextSplitter } from 'langchain/text_splitter';
import { PDFLoader } from "@langchain/community/document_loaders/fs/pdf";
import { Document } from 'langchain/document';
import { HuggingFaceTransformersEmbeddings } from '@langchain/community/embeddings/hf_transformers';
import { Chroma } from '@langchain/community/vectorstores/chroma';

const vectorDBHost = process.env.VECTORDB_HOST || '0.0.0.0';
const vectorDBPort = process.env.VECTORDB_PORT || 8000;
const vectorDBName = process.env.VECTORDB_NAME || 'nodejs_test_collection';

export async function POST(req, res) {

  /////////////////////////////////////////
  // Create the connection to the Chroma vector database
  // We use the HuggingFace transformers as since it does not need a remote
  // connect and seems to work pretty well
  const url =  `http://${vectorDBHost}:${vectorDBPort}`;
  const vectorStore = new Chroma(new HuggingFaceTransformersEmbeddings(), {
    collectionName: vectorDBName,
    url: url,
  });

  /////////////////////////////////////////
  // add files reveived to the Chroma database


  // get  the the files passed from the front end
  const fileFormData = await req.formData();
  const fileContents = fileFormData.getAll('file');
  if (!fileContents) {
    return NextResponse.json({ error: "no file received" }, { status: 400 });
  }

  // for each file load the file based on its type and use the appropriate
  // text splitter to split it up. Once split add to the vector database
  try {
    for (let i = 0; i < fileContents.length; i ++) {
      let splitDocs;
      if (fileContents[i].type === 'application/pdf') {
        const rawPDFContent = new Blob([await fileContents[i].arrayBuffer()]);
        const pdfLoader = new PDFLoader(rawPDFContent);
        const pdfContent = await pdfLoader.load();
        const splitter = await new RecursiveCharacterTextSplitter({
          chunkSize: 500,
          chunkOverlap: 50
        });
        splitDocs = await splitter.splitDocuments(pdfContent);
      } else if (fileContents[i].type === 'text/markdown') {
        const buffer = Buffer.from(await fileContents[i].arrayBuffer());
        const doc = new Document({ pageContent: buffer.toString() });
        const splitter = await new MarkdownTextSplitter({
          chunkSize: 500,
          chunkOverlap: 50
        });
        splitDocs = await splitter.splitDocuments([doc]);
      } else if (fileContents[i].type === 'text/plain') {
        const buffer = Buffer.from(await fileContents[i].arrayBuffer());
        const doc = new Document({ pageContent: buffer.toString() });
        const splitter = await new RecursiveCharacterTextSplitter({
          chunkSize: 500,
          chunkOverlap: 50
        });
        splitDocs = await splitter.splitDocuments([doc]);
      }
      if (splitDocs) {
        // it was one of the supported document type so add it to the datase
        // Otherwise we will ignore the file
        await vectorStore.addDocuments(splitDocs);
      }
    }

    return NextResponse.json({ Message: "Success", status: 201 });
  } catch (error) {
    console.log("upload failed", error);
    return NextResponse.json({ Message: "Failed", status: 500 });
  }
};
