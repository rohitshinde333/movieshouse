<template>
  <div>
    <div v-if="!searchQuery">
      
      <h1>Welcome to the Home Page</h1>
    <p v-if="isAuthenticated">Logged in as: {{ username }}</p>
    <p v-else>Please log in to see your username.</p>
    
    <button v-if="isAuthenticated" @click="theatre_admin_request" class="btn btn-primary">Request Theatre Admin Status</button>
    <button v-if="isAuthenticated" @click="delete_my_account" class="btn btn-danger">Delete My Account</button>
    <button v-if="isAuthenticated" @click="updateProfile" class="btn btn-warning">Update Profile</button>
    <button v-if="isAuthenticated" @click="callVerification" class="btn btn-warning">Face verification</button>

    <form v-if="editingProfile" @submit="submitProfile">
      <div>Edit Profile</div>
      <div>
        <label for="name">Phone:</label>
        <input type="text" v-model="editingProfile.phone" id="phone">
      </div>
      <div>
        <label for="email">Email:</label>
        <input type="email" v-model="editingProfile.email" id="email">
      </div>
      <div>
        <label for="address">Address:</label>
        <input type="text" v-model="editingProfile.address" id="address">
      </div>

      <button type="submit" class="btn btn-success">Save</button>
      <button type="button" @click="cancelEditProfile" class="btn btn-danger">Cancel</button>
    </form>
    <Modal :title="modalTitle" :message="modalMessage" :isOpen="showModal" @close="closeModal" />
    <div v-if="bookedShows.length > 0">
      <h1>
        Your Bookings are here
      </h1>
      <table class="current-shows-table">
        <thead class="th">
          <tr>
            <th>Booking Date and Time</th>
            <th>Theater Name</th>
            <th>City</th>
            <th>Show Date and Time</th>
            <th>Movie</th>
            <th>Seat Number</th>
            <th>Price</th>
            <th>Cancel Booking</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="show in bookedShows" :key="show.id" >
            <td>{{ show.booking_datetime }}</td>
            <td>{{ show.showtime.theater.name }}</td>
            <td>{{ show.showtime.theater.city }}</td>
            <td>{{ show.showtime.show_datetime}}</td>
            <td>{{ show.showtime.movie.title}}</td>
            <td>{{ show.seat_number }}</td>
            <td>{{ show.showtime.price }}</td>
            <td>
              <button class="btn btn-primary" @click="cancelBooking(show)">Delete</button>
            </td>
            
          </tr>
        </tbody>
      </table>
    </div>
    </div>
    

    
    
    
    
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import { mapActions } from 'vuex';
import axios from 'axios';
import Modal from './Modal.vue'
import { useStore } from 'vuex';
import MovieList from './MovieList.vue';
import startFaceVerification from '../index';
// const myLib = require('faceoauth');
// myLib.updateConfig({
//     apiUrl: 'http://localhost:3003/oauth/token',
//     clientId: 'OGIzZTEzNzAtZWZkMC00ZjM5LTk3MzMtMjA4YWMzZTU2N2UyOjhiM2UxMzcwLWVmZDAtNGYzOS05NzMzLTIwOGFjM2U1NjdlMi1ydnNoaW5kZTMzMzYzNTc=',
// });

export default {
  components: {
    Modal,
    MovieList
  },
  data() {
    return {
      isAuthenticated: false,
      editingProfile: null,
      username: '',
      userId: 0,
      message: '',
      showModal: false,
      bookedShows: [],
      searchQuery: '',
      searchMovies: [],
      searchShows: [],
      searchTheaters: [],
    };
  },
  
  computed: {
    ...mapGetters(['accessToken'])
  },
  mounted() {
  this.fetchUsername();
  this.fetchBookedShows(); 
},
  methods: {
    ...mapActions(['clearAccessToken']),
    async callVerification() {
      startFaceVerification(this.username);
      
    },
    
    performSearch() {
      if (this.searchQuery === '') {
        this.searchResults = [];
        return;
      }

      const accessToken = this.accessToken;

      axios
        .get(`http://localhost:5000/search?q=${this.searchQuery}`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        })
        .then((response) => {
          this.searchMovies = response.data.movies;
          this.searchShows = response.data.shows;
          this.searchTheaters = response.data.theaters;
          
        })
        .catch((error) => {
          console.error('Failed to perform search:', error);
        });
    },
  
    delete_my_account() {
      axios
        .delete('http://localhost:5000/users',{
          headers: {
            Authorization: `Bearer ${this.accessToken}`,
          },
        })
        .then((response)=> {
          alert(response.data.message);
          this.$router.push('/');
        })
        .catch((error)=>{
          console.error(error);
        })
    },
    fetchUsername() {
      const store = useStore();
      const accessToken = store.getters.accessToken;
      axios
        .get('http://localhost:5000/protected', {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        })
        .then((response) => {
          // Handle the response from the protected resource
          this.isAuthenticated = true;
          this.message = response.data.message;
          this.username = response.data.name;
          this.userId = response.data.id;
        })
        .catch((error) => {
          // Handle the error
          console.error(error);
        });
    },
    fetchBookedShows() {
    const accessToken = this.accessToken;
    axios
      .get('http://localhost:5000//userBookedShows', {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      })
      .then((response) => {
        // Handle the response and update the bookedShows array with the fetched data
        this.bookedShows = response.data;
      })
      .catch((error) => {
        console.error('Failed to fetch booked shows:', error);
      });
  },
    logout() {
      // Clear the access token from the store and perform any other necessary logout actions
      this.clearAccessToken();
      // Redirect the user to the login page or any other desired page
      this.$router.push('/');
    },
    updateProfile(event) {
      event.preventDefault();
      this.editingProfile = {
        phone: '',
        email: '', 
        address: '',

      };
    },
    cancelEditProfile() {
      this.editingProfile = null;
    },
    theatre_admin_request(){
      this.$router.push('/TheatreAdminRequest');
    },
    submitProfile(event) {
      event.preventDefault();

      
      const accessToken = this.accessToken;
      const userId = this.userId;
      axios
        .put(`http://localhost:5000/users/${userId}`, this.editingProfile, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        })
        .then((response) => {
          // Handling the successful profile update
          this.showModal = true;
          this.modalTitle = 'Success';
          this.modalMessage = 'Profile updated successfully';

          // Reseting the editingProfile and fetch the updated profile data
          this.editingProfile = null;
          this.fetchUsername();
        })
        .catch((error) => {
          // Handling the profile update error
          console.error('Failed to update profile:', error);
        });
    },
    closeModal() {
      this.showModal = false;
    },
    cancelBooking(show){
      
      axios
      .delete(`http://localhost:5000/bookings/${show.id}`, {
        headers: {
          Authorization: `Bearer ${this.accessToken}`,
        },
      })
      .then((response) => {
        // Handle the response and update the bookedShows array with the fetched data
        alert("Booking deleted Successfully!")
        this.fetchBookedShows();
      })
      .catch((error) => {
        console.error('Failed to Delete booked show:', error);
      });
    }
  },
};
</script>
<style scoped>
table {
  border-collapse: collapse;
  width: 100%;
  
}

th, td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

th {
  background-color: #e8b76d;
}
</style>
