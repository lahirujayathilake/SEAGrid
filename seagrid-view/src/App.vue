<template>
  <div>
    <h3>Create Dummy Data</h3>
    <input v-model="dataProductId" type="text" placeholder="Data Product ID">
    <input v-model="dataProductName" type="text" placeholder="Data Product Name">
    <button @click="createComputationalDataProduct">Create Dummy Data</button>
  </div>
</template>

<script>
import grpc from '@grpc/grpc-js';
import { root } from '../ComputationalDataAPI_pb';

export default {
  data() {
    return {
      response: ''
    };
  },
  methods: {
    async createComputationalDataProduct() {
      const client = new root.ComputationalDataAPIService(
        'localhost:50051',
        grpc.credentials.createInsecure()
      );
      const request = new root.ComputationalDataProduct();
      request.setMw('test data');

      client.createComputationalDataProduct(request, (err, response) => {
        if (err) {
          this.response = `Error: ${err}`;
        } else {
          this.response = `Response: ${response.getCompDataProductId()}`;
        }
      });
    }
  }
};
</script>
