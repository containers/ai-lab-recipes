import Fastify from 'fastify';
import fastifyStatic from '@fastify/static';
import path from 'node:path';
import { fileURLToPath } from 'url';
import fs from 'node:fs';
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

import temperatureRoute from './routes/temperatures.mjs';

// Setup Logging
const fastify = Fastify({
  logger: true
});

// WebUI related setup and serving
const webuiLocation = './public';

fastify.register(fastifyStatic, {
  wildcard: false,
  root: path.join(__dirname, webuiLocation)
});

fastify.get('/*', (req, res) => {
  res.send(fs.createReadStream(path.join(__dirname, webuiLocation, 'index.html')));
});

fastify.register(temperatureRoute);

/**
 * Run the server!
 */
const start = async () => {
  try {
    await fastify.listen({ port: process.env.PORT || 8005, host: process.env.HOSTNAME })
  } catch (err) {
    fastify.log.error(err)
    process.exit(1)
  }
};
start();