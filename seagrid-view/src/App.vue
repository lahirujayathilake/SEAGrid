<template>
  <div>
    <h3>Create Dummy Data</h3>
    <input v-model="dataProductId" type="text" placeholder="Data Product ID">
    <input v-model="dataProductName" type="text" placeholder="Data Product Name">
    <button @click="createDataProduct">Create Dummy Data</button>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      dataProductId: "",
      dataProductName: ""
    };
  },
  methods: {
    async createDataProduct() {
      try {
        const response = await axios.post("http://127.0.0.1:8000/seagrid-data/create/", JSON.stringify({
          data_product_id: this.dataProductId,
          name: this.dataProductName
        }), {
          headers: {
            "Content-Type": "application/json"
          }
        });
        console.log(response.data);
      } catch (error) {
        console.error(error);
      }
    }
  }
};
</script>
