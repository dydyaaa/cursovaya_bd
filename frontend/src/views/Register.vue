<template>
    <div>
      <h1>Register</h1>
      <form @submit.prevent="register">
        <input v-model="user_login" placeholder="Username" />
        <input v-model="password" type="password" placeholder="Password" />
        <button type="submit">Register</button>
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
      register() {
        axios.post('http://localhost:5001/api/register', {
          user_login: this.user_login,
          password: this.password,
        })
        .then(response => {
          document.cookie = `token=${response.data.token}; max-age=3600; httponly`;
          this.$router.push('/');
        })
        .catch(err => {
          this.error = err.response.data.result || 'Registration failed';
        });
      }
    }
  };
  </script>
  