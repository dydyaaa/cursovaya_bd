<template>
    <div>
      <h1>Home Page</h1>
      <div v-if="error">Error connecting to server</div>
      <div v-else>
        <ul>
          <li v-for="item in data" :key="item.id">{{ item }}</li>
        </ul>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        data: [],
        error: false,
      };
    },
    created() {
      axios.get('http://localhost:5001/api/home')
        .then(response => {
          this.data = response.data.result;
        })
        .catch(() => {
          this.error = true;
        });
    }
  };
  </script>
  