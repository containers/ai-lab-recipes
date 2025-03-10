import { z } from 'zod';
import { tool } from '@langchain/core/tools';

const weatherSchema = z.object({
  latitude: z.number().describe('The latitude of a place'),
  longitude: z.number().describe('The longitude of a place')
});

const weather = tool(
  async function ({ latitude, longitude }) {
    const response = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&hourly=temperature_2m`);
    const json = await response.json();
    return json;
  },
  {
    name: 'weather',
    description: 'Get the current weather in a given latitude and longitude.',
    schema: weatherSchema
  }
);

export default weather;
