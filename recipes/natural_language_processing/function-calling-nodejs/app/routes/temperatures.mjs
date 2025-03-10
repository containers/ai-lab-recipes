import { askQuestion } from '../ai/weather-prompt.mjs';

async function temperatureRoutes (fastify, options) {
  fastify.post('/api/temperatures', async (request, reply) => {
    const city = request.body.city;

    // Call the AI stuff
    const response = await askQuestion(city);

    return {
      result: response
    }
  });
}

export default temperatureRoutes;