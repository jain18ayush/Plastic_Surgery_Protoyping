<template>
  <div>
    <h1>ONNX Runtime Web Example</h1>
    <button @click="runModel">Run Model</button>
  </div>
</template>

<script>
import * as ort from 'onnxruntime-web';

ort.env.wasm.wasmPaths = {
  'ort-wasm.wasm': 'https://cdn.jsdelivr.net/npm/onnxruntime-web/dist/ort-wasm.wasm',
  'ort-wasm-simd.wasm': 'https://cdn.jsdelivr.net/npm/onnxruntime-web/dist/ort-wasm-simd.wasm',
  'ort-wasm-threaded.wasm': 'https://cdn.jsdelivr.net/npm/onnxruntime-web/dist/ort-wasm-threaded.wasm',
};

export default {
  name: 'OnnxModel',
  methods: {
    async runModel() {
      try {
        // Load the ONNX model from the public directory
        const session = await ort.InferenceSession.create('/model.onnx');
        console.log(session)
        // Prepare input tensor
        // const inputTensor = new ort.Tensor('float32', new Float32Array([1.0, 2.0, 3.0]), [3]);

        // // Prepare feeds
        // const feeds = { input: inputTensor };

        // // Run the model
        // const output = await session.run(feeds);

        // // Log the output
        // console.log(output);
      } catch (error) {
        console.error('Error running the model:', error);
      }
    }
  }
};
</script>

<style>
/* Add your styles here */
</style>
