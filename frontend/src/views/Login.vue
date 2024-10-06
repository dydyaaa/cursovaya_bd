<template>
    <div>
      <h1>Login</h1>
      <form @submit.prevent="login">
        <input v-model="user_login" placeholder="Username" />
        <input v-model="password" type="password" placeholder="Password" />
        <button type="submit">Login</button>
      </form>
      <div v-if="error">{{ error }}</div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        user_login: '',
        password: '',
        error: null,
      };
    },
    methods: {
      login() {
        axios.post('http://localhost:5001/api/login', {
          user_login: this.user_login,
          password: this.password,
        })
        .then(response => {
          document.cookie = `token=${response.data.token}; max-age=3600; httponly`;
          this.$router.push('/');
        })
        .catch(err => {
          this.error = err.response.data.result || 'Login failed';
        });
      }
    }
  };
  </script>
  