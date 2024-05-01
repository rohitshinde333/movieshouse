<template>
  <h2 style="margin-top: 100px;">Send Theater Admin Request</h2>
    <div class="container mt-4">
      
      <form @submit.prevent="sendRequest" >
        <div class="form-group-request">
          <label for="theater">Select Theater:</label>
          <select v-model="selectedTheater" class="form-control" id="theater" required>
            <option disabled value="">Please select a theater</option>
            <option v-for="theater in theaters" :key="theater.id" :value="theater.id">{{ theater.name }}</option>
          </select>
          <div class="invalid-feedback">Please select a theater.</div>
        </div>
        <div class="form-group-request">
          <label for="secureKey">Secure Key:</label>
          <input v-model="secureKey" type="password" class="form-control" id="secureKey" required>
          <div class="invalid-feedback">Please enter a secure key.</div>
        </div>
        <button type="submit" class="btn btn-primary">Send Request</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { mapGetters } from 'vuex';

  export default {
    data() {
      return {
        theaters: [],
        selectedTheater: null,
        secureKey: '',
      };
    },
    mounted() {
      // Fetch the list of theaters from the backend API
      this.fetchTheaters();
    },
    computed: {
    ...mapGetters(['accessToken'])
    },
    methods: {
      fetchTheaters() {
        axios
          .get(`http://localhost:5000/theaters`)
          .then((response) => {
            this.theaters = response.data;
          })
          .catch((error) => {
            console.error('Failed to fetch theaters:', error);
          });
      },
      sendRequest() {
        // Check if the form is valid before submitting the request
        
  
        // Send the theater admin request with the secure key to the backend API
        axios
          .post(`http://localhost:5000/theaters/${this.selectedTheater}/${this.secureKey}`,null,{
            headers: {
                Authorization: `Bearer ${this.accessToken}`,
                'Content-Type': 'application/json',
            },
          })
          .then((response) => {
            alert('Theater admin request sent successfully!');
            // Clear the form after successful request submission
            this.selectedTheater = null;
            this.secureKey = '';
            this.$router.push('/')
            
          })
          .catch((error) => {
            console.error('Failed to send theater admin request:', error);
            alert('Failed to send theater admin request. Please try again later.');
          });
      },
    },
  };
  </script>
  
  <style>
  .container {
    max-width: 500px;
    margin-top:  300px;
  }
  
  .form-group-request {
    margin: 100px 100px;
  padding: 10px;
  width: 900px;
  border: 1px solid #ccc;
  border-radius: 4px;
  }
  
  label {
    font-weight: bold;
  }
  
  .invalid-feedback {
    color: red;
  }
  
  /* Add any additional styles here as needed */
  </style>
  