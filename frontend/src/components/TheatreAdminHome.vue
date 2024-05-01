<template>
  <div style="margin-top: 65px;">
    <h1>Welcome, Theatre Admin!</h1>
    <button  @click="delete_my_account" class="btn btn-danger">Delete My Account</button>

    <div v-if="theatreInfo">
      <h2>Theatre Information</h2>
      <p><strong>Name:</strong> {{ theatreInfo.name }}</p>
      <p><strong>Seats:</strong> {{ theatreInfo.capacity }}</p>
      <p><strong>Location:</strong> {{ theatreInfo.address }}</p>
      <p><strong>City:</strong> {{ theatreInfo.city }}</p>
      <p><strong>Country:</strong> {{ theatreInfo.country }}</p>
    </div>

    <div>
      <h2>Current Shows</h2>
      <table class="table">
        <thead class="th">
          <tr>
            
            <th>Movie Name</th>
            <th>Show Date Time</th>
            <th>Total Bookings</th>
            <th>Price</th>
            <th>Edit</th>
            <th>Delete</th>
          </tr>
        </thead>
        <tbody class="td">
          <tr v-for="show in shows" :key="show.id" :class="{ 'filling-up-fast': isFillingUpFast(show), 'moderate': isModerate(show), 'Housefull': isHouseFull(show) }">
            
            <td>{{ show.movie }}</td>
            <td>{{ show.show_datetime }}</td>
            
            <td> {{ show.available_seats }}</td>
            <td>{{ show.price }}</td>
            <td>
              <button class="btn btn-primary" @click="openEditForm(show)">Edit</button>
            </td>
            <td>
              <button class="btn btn-primary" @click="Delete(show)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-if="showForm.show" class="form-group-edit-movie">
      <h2>Edit Show</h2>
      <form @submit.prevent="updateShow">
        <div class="form-group-edit-movie">
          <label for="editShowTime">Show Date Time:</label>
          <input v-model="showForm.show_datetime" type="datetime-local" id="editShowTime" required />
        </div>
        <div class="form-group-edit-movie">
          <label for="editShowPrice">Price:</label>
          <input v-model="showForm.price" type="number" step="0.01" id="editShowPrice" required />
        </div>
        <button type="submit" class="btn btn-primary">Update Show</button>
        <button @click="closeEditForm()" class="btn btn-primary">Close Form</button>
      </form>
    </div>
  </div>
    

    
    
</template>

<script>
import { mapGetters } from 'vuex';
import axios from 'axios';
import MovieList from './MovieList.vue';

export default {
  components: {
    MovieList,
  },
  data() {
    return {
      shows: [],
      movies: [],
      theatreInfo: null,
      showForm: {
        show: false,
        show_datetime: null,
        price: null,
        showId: null,
      },
    };
  },
  computed: {
    ...mapGetters(['accessToken', 'theatre_id']),
    
  },
  mounted() {
    if (this.accessToken) {
      this.fetchMovies();
      this.fetchTheatre();
      this.fetchShows();
    }
  },
  methods: {
    isFillingUpFast(show) {
      const bookedPercentage = (show.available_seats / this.theatreInfo.capacity) * 100;
      return bookedPercentage >= 75;
    },

    isModerate(show) {
      const bookedPercentage = (show.available_seats / this.theatreInfo.capacity) * 100;
      return bookedPercentage > 0 && bookedPercentage < 75;
    },

    isHouseFull(show) {
      const bookedPercentage = (show.available_seats / this.theatreInfo.capacity) * 100;
      return bookedPercentage == 100;
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
    Delete(show){
      axios
        .delete(`http://localhost:5000/showtimes/${show.id}`, {
          headers: {
            Authorization: `Bearer ${this.accessToken}`,
          },
        })
        .then((response) => {
          // Handle success, you may want to show a success message or refresh the shows
          console.log('Show deleted successfully');
          this.fetchShows(); // Refresh the shows to show updated data
        })
        .catch((error) => {
          // Handle error, show an error message or handle the error accordingly
          console.error('Failed to delete show:', error);
        });
    },
    openEditForm(show) {
      this.showForm = {
        show: true,
        show_datetime: show.show_datetime,
        price: show.price,
        showId: show.id,
      };
    },
    closeEditForm() {
      this.showForm.show = false;
      this.showForm.show_datetime = null;
      this.showForm.price = null;
      this.showForm.showId = null;
    },
    updateShow() {
      axios
        .put(`http://localhost:5000/showtimes/${this.showForm.showId}`, this.showForm, {
          headers: {
            Authorization: `Bearer ${this.accessToken}`,
          },
        })
        .then((response) => {
          this.closeEditForm();
          // Refresh the shows to show updated data
          this.fetchShows();
        })
        .catch((error) => {
          console.error('Failed to update show:', error);
        });
    },
    fetchMovies() {
      axios
        .get('http://localhost:5000/movies')
        .then((response) => {
          this.movies = response.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    async fetchTheatre() {
      axios
        .get(`http://localhost:5000/theatre/info/${this.theatre_id}`, {
          headers: {
            Authorization: `Bearer ${this.accessToken}`,
          },
        })
        .then((response) => {
          this.theatreInfo = response.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    async fetchShows() {
      axios
        .get(`http://localhost:5000/theatre/${this.theatre_id}/shows`, {
          headers: {
            Authorization: `Bearer ${this.accessToken}`,
          },
        })
        .then((response) => {
          this.shows = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    
  },
};
</script>

<style>
table {
  border-collapse: collapse;
  width: 100%;
  
}

th, td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
  background-color: rgb(236, 207, 115);
}

th {
  background-color: #f2f2f2;
}
.filling-up-fast {
  background-color: #e6eb62; 
  color: white;
}

.moderate {
  background-color: #96bc65; 
}

.housefull {
  background-color: rgb(244, 99, 99);
}
</style>
