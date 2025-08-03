// Test file to verify that the client can be imported correctly
import { ApiClient, GPUListingDTO, GPUModelDTO } from '@repo/client';

// Log the type of ApiClient to verify it's imported correctly
console.log('ApiClient type:', typeof ApiClient);

// Create a new instance of ApiClient
const client = new ApiClient('http://localhost:8000');

// Log some properties to verify the client is working correctly
console.log('Client has forecast API:', !!client.forecast);
console.log('Client has health API:', !!client.health);
console.log('Client has import API:', !!client.import);
console.log('Client has listings API:', !!client.listings);
console.log('Client has ml API:', !!client.ml);
console.log('Client has models API:', !!client.models);
console.log('Client has persist API:', !!client.persist);
console.log('Client has report API:', !!client.report);
console.log('Client has schema API:', !!client.schema);
console.log('Client has validation API:', !!client.validation);

// Test type imports
const listing: GPUListingDTO = {
  id: '1',
  title: 'Test GPU',
  price: 100,
  model: 'Test Model',
  url: 'http://example.com'
};

const model: GPUModelDTO = {
  id: '1',
  name: 'Test Model',
  manufacturer: 'Test Manufacturer',
  memoryGB: 8,
  releaseDate: '2023-01-01'
};

console.log('Listing:', listing);
console.log('Model:', model);

// This file is just for testing imports and won't be used in the application
export {};