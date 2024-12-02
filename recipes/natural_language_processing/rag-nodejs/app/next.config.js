/** @type {import('next').NextConfig} */
module.exports = {
  output: "standalone",

  // Indicate that these packages should not be bundled by webpack
  experimental: {
    serverComponentsExternalPackages: ['sharp', 'onnxruntime-node', 'chromadb' ],
  },
};
