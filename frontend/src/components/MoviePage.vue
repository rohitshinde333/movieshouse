<template>
  <div class="movie-page">
    <h2>{{ movie.title }}</h2>
    <div class="movie-details">
      <div class="poster">
        <img :src="movie.image" :alt="movie.title" class="poster-image" />
      </div>
      <div class="movie-info">
        <p><strong>Genre:</strong> {{ movie.genre }}</p>
        <p><strong>Director:</strong> {{ movie.director }}</p>
        <p><strong>Release Date:</strong> {{ movie.release_date }}</p>
        <p><strong>Duration:</strong> {{ movie.duration }} minutes</p>
        <p><strong>Description:</strong> {{ movie.description }}</p>
        <div class="buttons">
            <button v-if="isAdmin" @click="editMovie(movie)" class="btn btn-warning">Edit</button><br>
            <button v-if="isAdmin" @click="deleteMovie(movie.id)" class="btn btn-danger">Delete</button>
        </div>
        
      </div>
    </div>
    <div v-if="editingMovie">
          <h4>Edit Movie</h4>
          <form @submit="updateMovie" >
            <div class="form-group-edit-movie">
              <label for="title">Title:</label>
              <input class="form-control form-control-sm" type="text" v-model="editingMovie.title" id="title">
            </div>
            <div class="form-group-edit-movie">
              <label for="genre">Genre</label>
              <select v-model="editingMovie.genre" class="form-control" id="genre" >
                <option value="" disabled>Select a genre</option>
                <option value="Romance">Romance</option>
                <option value="Comedy">Comedy</option>
                <option value="Drama">Drama</option>
                <option value="Drama">Action</option>
                <option value="Drama">Horror</option>
              </select>
              <div class="invalid-feedback">Please select a genre.</div>
            </div>
            <div class="form-group-edit-movie">
              <label for="director">Director</label>
              <input type="text" v-model="editingMovie.director" class="form-control" id="director" >
              <div class="invalid-feedback">Please enter a director.</div>
            </div>
            <div class="form-group-edit-movie">
              <label for="release_date">Release Date</label>
              <input type="date" v-model="editingMovie.release_date" class="form-control" id="release_date" >
              <div class="invalid-feedback">Please enter a release date.</div>
            </div>
            <div class="form-group-edit-movie">
              <label for="duration">Duration</label>
              <input type="number" v-model="editingMovie.duration" class="form-control" id="duration" >
              <div class="invalid-feedback">Please enter a valid duration.</div>
            </div>
            <div class="form-group-edit-movie">
              <label for="description">Description</label>
              <textarea v-model="editingMovie.description" class="form-control" id="description" rows="4" ></textarea>
              <div class="invalid-feedback">Please enter a description.</div>
            </div>
            <div class="form-group-edit-movie">
              <label for="image">Poster link</label>
              <textarea v-model="editingMovie.image" class="form-control" id="image"></textarea>
              <div class="invalid-feedback">Please enter a valid image link.</div>
            </div>
            
            <button type="submit" class="btn btn-success">Save</button>
            <button @click="closeForm()" class="btn btn-warning"> Cancel </button>
          </form>
        </div>
    <div class="section-buttons">
      <button @click="toggleSection('review')" :class="{ active: activeSection === 'review' }">Top Reviews</button>
      <button @click="toggleSection('write-review')" :class="{ active: activeSection === 'write-review' }">Write a Review</button>
    </div>
    <div v-if="activeSection === 'review'" class="reviews-section">
      <h3 class="reviews-heading">Top Reviews</h3>
      <ul class="reviews-list">
        <li v-for="review in topReviews" :key="review.id" class="review-item">
          <p class="review-content">{{ review.content }}</p>
          <p class="review-author">By: {{ review.user_id }}</p>
          <p class="review-likes">Likes: {{ review.likes }}</p>
          <button v-if="!review.liked_by_current_user" @click="likeReview(review.id)" class="like-button">Like</button>
          <button v-else @click="unlikeReview(review.id)" class="unlike-button">Unlike</button>
        </li>
      </ul>
    </div>
    <div v-if="activeSection === 'write-review'" class="write-review">
      <h3>Write a Review</h3>
      <form @submit.prevent="submitReview">
        <div class="form-group">
          <label for="reviewContent">Review:</label>
          <textarea v-model="newReview.content" class="form-control" id="reviewContent" rows="4" required></textarea>
        </div>
        <button type="submit" class="btn btn-primary">Submit Review</button>
      </form>
    </div>
    <div v-if="loadingShows" class="loading-spinner">
      <i class="fas fa-spinner fa-spin"></i>
      <p>Loading shows...</p>
    </div>
    <div v-else >
      <div v-if="!makeShowsInvisible && !isAdmin &&!isTheaterAdmin">
        <h3>Available Shows at your city: {{ userCity }}</h3>
        <ul>
          <li v-for="show in userCityShows" :key="show.id" class="show-item" >
            <div style="margin-right: 50px;" >
              <p>Theatre Name: {{ show.theater.name }}</p>
              <p>Date and Time: {{ show.show_datetime }}</p>
              <p>Ticket Price: {{ show.price }}</p>
              <button @click="openBooking(show)" class="btn btn-success"  >Book Show</button>

            </div>
            
          </li>
        </ul>
      </div>
      <div v-if="!makeShowsInvisible && !isAdmin &&isTheaterAdmin">
        
        <ul>
          <li v-for="show in userCityShows" :key="show.id">
            <div v-if="show.theater.id == theatre_id" class="show-timing" style="border-color: black;">
              <h3>Available Shows at your theatre: {{ show.theater.name }}</h3>
              <p>Date and Time: {{ show.show_datetime }}</p>
              <p>Ticket Price: {{ show.price }}</p>
            </div>
            <button @click="openBooking(show)" class="btn btn-primary">Look at bookings</button>
            
          </li>
        </ul>
      </div>
    </div>
    <div v-if="activeSection === 'book-show'" class="seat-selection">
      <h3>Select Seats for Show at {{ selectedShow.theater.name }} - {{ selectedShow.show_datetime }}</h3>
      <div class="seat-grid">
        <!-- Generate the seats dynamically based on the theater's capacity -->
        <div
          v-for="seatNumber in selectedShow.theater.capacity"
          :key="seatNumber"
          class="seat"
          :class="{ 'seat-booked': isSeatBooked(seatNumber), 'seat-selected': isSelected(seatNumber) }"
          @click="toggleSeatSelection(seatNumber)"
        >
          {{ seatNumber }}
        </div>
      </div>
      <div v-if="selectedSeats.length > 0">
        <h4>Selected Seats:</h4>
        <ul>
          <li v-for="seat in selectedSeats" :key="seat">
            {{ seat }}
          </li>
        </ul>
        <!-- Add payment options here -->
      </div>
      <button v-if="!isAdmin && !isTheaterAdmin" @click="confirmBooking()">Confirm Booking</button>
      <button @click="cancelBooking()">Close</button>
    </div>
     <!-- Theatre Admin Section -->
     <div v-if="isTheaterAdmin" class="form-group-edit-movie">
      
      <form @submit.prevent="submitShow">
        <h2>Add Show @ your theater</h2>
        <div class="form-group-edit-movie">
          <label for="showDatetime">Show Date and Time:</label>
          <input v-model="newShow.show_datetime" type="datetime-local" class="form-control" id="showDatetime" required>
        </div>
        
        <div class="form-group-edit-movie">
          <label for="price">Price:</label>
          <input v-model="newShow.price" type="number" class="form-control" id="price" required>
        </div>
        <button type="submit" class="btn btn-primary">Add Show</button>
      </form>
    </div>
   
    
        <Modal :title="modalTitle" :message="modalMessage" :isOpen="showModal" @close="closeModal" />
  </div>
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';
import Modal from './Modal.vue'
export default {
  components: {
    Modal
  },
  computed: {
    ...mapGetters(['accessToken']),
    ...mapGetters(['isTheaterAdmin']),
    ...mapGetters(['theatre_id']),
    ...mapGetters(['isAdmin'])
  },
  data() {
    return {
      showModal: false,
      modalTitle: '',
      modalMessage: '',
      movie: '',
      topReviews: [],
      newReview: {
        content: '',
        movie_id: '',
      },
      userId: '',
      
      theaters: [],
      selectedTheater: null,
      shows: [],
      newShow: {
        movie_id: this.$route.params.movieId,
        theater_id: this.theatre_id,
        show_datetime: '',
        price: '',
      },
      userCity: '',
      userEmail: '',
      userCityShows: [],
      activeSection: 'review',
      loadingShows: true,
      selectedShow: null,
      selectedSeats: [],
      makeShowsInvisible: false,
      bookedSeats: [],
      showAddShowForm: false,
      editingMovie: null,
    };
  },
  async mounted() {
    this.fetchMovie();
    this.fetchUsername();
    await this.fetchUserCity();
    this.fetchTopReviews();
    this.fetchUserCityShows();
  },
  
  methods: {
    closeForm() {
      this.editingMovie = null;
    },
    closeModal() {
      this.showModal = false;
      this.$router.push('/adminHome');
    },
    editMovie() {
      this.editingMovie = {
        title: '',
        genre: '', 
        

      };
    },
    updateMovie(event) {
      event.preventDefault();

      axios.put(`http://localhost:5000/movies/${this.movie.id}`, this.editingMovie, {
        headers: {
          Authorization: `Bearer ${this.accessToken}`,
          "Content-Type": "application/json" // Corrected content type
        },
      })
      .then(response => {
        console.log('Movie updated successfully:', response.data);
        this.editingMovie = null;
        this.showModal = true;
        this.modalTitle = 'Success';
        this.modalMessage = 'Movie updated successfully';
      })
      .catch(error => {
        this.showModal = true;
        this.modalTitle = 'Failure';
        this.modalMessage = 'Movie updation failed';
        console.error('Movie updation failed:', error); // Log the error for debugging
      });
    },

    deleteMovie(movieId) {
      axios.delete(`http://localhost:5000/movies/${movieId}`, {
        headers: {
          Authorization: `Bearer ${this.accessToken}`,
        },
      })
      .then(response => {
        this.fetchMovies();
        this.editingMovie = null;
        this.showModal = true;
        this.modalTitle = 'Success';
        this.modalMessage = 'Movie deleted successfully';

      })
      .catch(error => {
        this.showModal = true;
        this.modalTitle = 'Failure';
        this.modalMessage = 'Movie deletion failed';
      });
    },
    async fetchMovie() {
      const movieId = this.$route.params.movieId;
      await axios
        .get(`http://localhost:5000/movie/${movieId}`)
        .then((response) => {
          this.movie = response.data;
        })
        .catch((error) => {
          console.error('Failed to fetch movie:', error);
        });
    },
    async fetchTopReviews() {
      const movieId = this.$route.params.movieId;
      await axios
        .get(`http://localhost:5000/movie/${movieId}/reviews`, {
          headers: {
            Authorization: `Bearer ${this.accessToken}`,
          },
        })
        .then((response) => {
          this.topReviews = response.data.map((review) => {
            return {
              ...review,
              liked_by_current_user: this.userHasLiked(review),
            };
          });
        })
        .catch((error) => {
          console.error('Failed to fetch top reviews:', error);
        });
    },
    submitReview() {
      this.newReview.movie_id = this.$route.params.movieId;
      axios
        .post(`http://localhost:5000/movie/${this.$route.params.movieId}/reviews`, this.newReview, {
          headers: {
            Authorization: `Bearer ${this.accessToken}`,
          },
        })
        .then((response) => {
          alert(response.data.message);
          this.newReview.content = '';
          this.fetchTopReviews();
        })
        .catch((error) => {
          console.error('Failed to submit review:', error);
        });
    },
    async fetchUsername() {
      await axios
        .get('http://localhost:5000/protected', {
          headers: {
            Authorization: `Bearer ${this.accessToken}`,
          },
        })
        .then((response) => {
          this.userId = response.data.id;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    userHasLiked(review) {
      const currentUserId = this.userId;
      return review.liked_by && review.liked_by.some((user) => user.id === currentUserId);
    },
    async fetchUserCityShows() {
      await axios
        .post(`http://localhost:5000/showsAtCity/${this.$route.params.movieId}/${this.userCity}`, null, {
          headers: {
            Authorization: `Bearer ${this.accessToken}`,
          },
        })
        .then((response) => {
          this.userCityShows = response.data;
        })
        .catch((error) => {
          console.error('Failed to fetch user city shows:', error);
        });
      this.loadingShows = false;
    },
    async openBooking(show) {
      await this.fetchBookedSeats(show.id);
      this.selectedShow = show;
      this.makeShowsInvisible = true;
      this.activeSection = 'book-show';
    },
    cancelBooking() {
      this.selectedShow = null;
      this.selectedSeats = [];
      this.makeShowsInvisible = false;
      
      this.activeSection = 'review'
      
    },
    async fetchUserCity() {
      await axios
        .get(`http://localhost:5000/currentUserCity`, {
          headers: {
            Authorization: `Bearer ${this.accessToken}`,
          },
        })
        .then((response) => {
          this.userCity = response.data.address;
          this.userEmail = response.data.email;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    toggleSection(section) {
      this.activeSection = section;
    },
    isSeatBooked(seatNumber) {
      // Check if the seat is booked by looking at the bookedSeats array
      return this.bookedSeats.includes(seatNumber);
    },

    isSelected(seatNumber) {
      // Check if the seat is selected by looking at the selectedSeats array
      return this.selectedSeats.includes(seatNumber);
    },
    async fetchBookedSeats(showId) {
      try {
        const response = await axios.get(`http://localhost:5000/bookings/${showId}`, {
          headers: {
            Authorization: `Bearer ${this.accessToken}`,
          },
        });
        this.bookedSeats = response.data;
      } catch (error) {
        console.error('Failed to fetch booked seats:', error);
      }
    },
    toggleSeatSelection(seatNumber) {
      // Toggle seat selection based on its current state
      if (this.isSeatBooked(seatNumber)) {
        // If the seat is booked, do nothing
        return;
      }

      if (this.isSelected(seatNumber)) {
        // If the seat is already selected, remove it from the selectedSeats array
        this.selectedSeats = this.selectedSeats.filter((seat) => seat !== seatNumber);
      } else {
        // If the seat is not selected, add it to the selectedSeats array
        this.selectedSeats.push(seatNumber);
      }
    },

    async confirmBooking() {

      const selectedSeatsArray = [...this.selectedSeats];
      const data = {
        show_id: this.selectedShow.id,
        theater_id: this.selectedShow.theater.id,
        selected_seats: selectedSeatsArray,
      };
      console.log(data);
      try {
        const response = await axios.post('http://localhost:5000/bookings', data, {
          headers: {
            Authorization: `Bearer ${this.accessToken}`, // Include the accessToken in the headers
          },
        });
        // Handle the response from the server
        await this.fetchBookedSeats(this.selectedShow.id);
        this.cancelBooking();
        alert(response.data.message);
        //await this.sendTicketsEmail(this.selectedShow.id);
        // Perform any other actions as needed after successful booking
      } catch (error) {
        // Handle errors from the server
        console.error('Error while booking seats:', error.response.data.message);
        // Show an error message to the user or handle the error as per your requirements
      }
    },
    toggleAddShowForm() {
      this.showAddShowForm = !this.showAddShowForm;
      this.newShow.show_datetime = '';
      this.newShow.price = '';
    },

    // Submit the new show to the backend
    submitShow() {
      const payload = {
        movie_id: this.newShow.movie_id,
        theater_id: this.theatre_id,
        show_datetime: this.newShow.show_datetime,
        theater_id: this.theatre_id,
        price: this.newShow.price,
      };

      axios
        .post(`http://localhost:5000/showtimes`, payload, {
          headers: {
            Authorization: `Bearer ${this.accessToken}`,
          },
        })
        .then((response) => {
          alert(response.data.message);
          this.newShow = {
            show_datetime: '',
            theater_id: '',
            available_seats: 0,
            price: 0,
          };
          
        })
        .catch((error) => {
          console.error('Failed to add show:', error);
        });
    },
    async  sendTicketsEmail(selectedShowId) {
  const emailData = {
    recipient: "harishrivaidya@gmail.com",
    subject: "Show Booked/do-not reply",
    body: `Hello user. This is an autogenerated mail. Please do not reply to this mail. Thank you. Enjoy Movies!!!`,
  };

  try {
    const response = await axios.post('http://localhost:5000/email', emailData, {
      headers: {
        'Content-Type': 'application/json',
      },
    });

    console.log('Email sent:', response.data.message);
  } catch (error) {
    console.error('Failed to send email:', error);
  }
},
likeReview(reviewId) {
      axios.post(`http://localhost:5000/movies/${this.movie.id}/reviews/${reviewId}/like`, {}, {
        headers: {
          Authorization: `Bearer ${this.accessToken}`,
        },
      })
      .then(response => {
        this.review.likes = response.data.likes; // Update the local review object
        this.review.liked_by_current_user = true;
      })
      .catch(error => {
        console.error('Failed to like review:', error);
      });
    },

    unlikeReview(reviewId) {
      axios.delete(`http://localhost:5000/movies/${this.movie.id}/reviews/${reviewId}/like`, {
        headers: {
          Authorization: `Bearer ${this.accessToken}`,
        },
      })
      .then(response => {
        this.review.likes = response.data.likes; // Update the local review object
        this.review.liked_by_current_user = false;
      })
      .catch(error => {
        console.error('Failed to unlike review:', error);
      });
    },
  },
    

};
</script>


<style>
.form-group-edit-movie {
  margin: 10px 0;
  padding: 10px;
  width: 100%;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.reviews-section {
  margin-top: 20px;
}

.reviews-heading {
  font-size: 24px;
  margin-bottom: 10px;
}

.reviews-list {
  list-style: none;
  padding: 0;
}

.review-item {
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 15px;
  display: block; 
}

.review-content {
  font-size: 18px;
  margin-bottom: 5px;
}

.review-author {
  font-size: 14px;
  color: #666;
  margin-bottom: 5px;
}

.review-likes {
  font-size: 14px;
  color: #666;
  margin-bottom: 10px;
}

.like-button,
.unlike-button {
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 10px; /* Adjust the margin to separate buttons */
}

.like-button:hover,
.unlike-button:hover {
  background-color: #2ac92c;
}

.like-button:focus,
.unlike-button:focus {
  outline: none;
}

h2 {
  color: #333;
  margin-bottom: 10px;
}

.movie-details {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
}

.poster {
  flex: 0 0 200px;
  margin-right: 20px;
}

.poster-image {
  width: 100%;
  height: auto;
  border-radius: 8px;
}
.seat {
  display: inline-block;
  width: 30px;
  height: 30px;
  margin: 5px;
  text-align: center;
  line-height: 30px;
  cursor: pointer;
}


.seat-booked {
  background-color: red;
  color: white;
}


.seat-selected {
  background-color: green;
  color: white;
}

.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 200px; 
  font-size: 24px;
  color: #007bff;
}

.loading-spinner i {
  margin-bottom: 10px;
}

.movie-info {
  flex: 1;
}

.movie-details p {
  margin: 0 0 10px;
}

.movie-details strong {
  font-weight: bold;
}



.movie-page {
  background-color: #ffffff;
  padding: 20px;
  font-family: Arial, sans-serif;
  width:100%;
}

h2 {
  color: #333;
  font-size: 24px;
  margin-bottom: 20px;
}

.movie-details {
  background-color: #9790e4;
  
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  width:700px;
}

.poster {
  flex: 0 0 200px;
  margin-right: 20px;
}

.poster-image {
  width: 100%;
  height: auto;
  border-radius: 8px;
}

.movie-info {
  flex: 1;
}

.movie-details p {
  margin: 0 0 10px;
}

.movie-details strong {
  font-weight: bold;
}



.movie-page {
  max-width: 750px;
  margin: 0 auto;
}

.movie-details {
  font-size: 16px;
  line-height: 1.5;
}

.movie-details p {
  margin-bottom: 8px;
}

.reviews {
  margin-top: 20px;
}
.buttons {
  display: flex;
  justify-content: space-between;
}

.edit-button,
.delete-button {
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
}

.edit-button:hover,
.delete-button:hover {
  background-color: #0056b3;
}

.edit-button:focus,
.delete-button:focus {
  outline: none;
}

.reviews h3 {
  font-size: 18px;
  margin-bottom: 10px;
}

.reviews ul {
  list-style-type: none;
  padding: 0;
}

.reviews li {
  margin-bottom: 10px;
}

.reviews p {
  margin: 0;
}

.reviews p:first-child {
  font-weight: bold;
}









.theatre-admin-section {
  margin-top: 20px;
  margin: 0 auto;
  margin-left: 150px;
}

.theatre-admin-section h3 {
  font-size: 18px;
  margin-bottom: 10px;
}

.theatre-admin-section form {
  max-width: 400px;

}

.theatre-admin-section .form-group {
  margin-bottom: 20px;
}

.theatre-admin-section label {
  font-weight: bold;
}

.theatre-admin-section input {
  width: 100%;
  padding: 5px;
  font-size: 16px;
}

.show-item {
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 15px;
  width: 500px;
  margin-right:100px;
}

.theatre-admin-section button[type="submit"] {
  background-color: #007bff;
  color: #ffffff;
  border: none;
  padding: 8px 15px;
  border-radius: 4px;
  cursor: pointer;
}

.theatre-admin-section button[type="submit"]:hover {
  background-color: #0056b3;
}

.theatre-admin-section button[type="submit"]:focus {
  outline: none;
}

.show-list {
  margin-top: 20px;
}

.show-list h3 {
  font-size: 18px;
  margin-bottom: 10px;
}



.show-list li {
  font-size: 16px;
  margin-bottom: 10px;
}

.show-list li button {
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
}

.show-list li button:hover {
  background-color: #0056b3;
}

.show-list li button:focus {
  outline: none;
}

.show-list {
  margin-top: 20px;
  margin-left:100px;
}

.show-list h3 {
  font-size: 18px;
  margin-bottom: 10px;
}

.show-list ul {
  font-size: 16px;
  margin-bottom: 10px;
  margin-left:100px;
  display: flex;
  align-items: center;
}

.show-list li {
  font-size: 16px;
  margin-bottom: 10px;
  margin-left:100px;
  display: flex;
  align-items: center;
}


.show-list li button {
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
}

.show-list li button:hover {
  background-color: #0056b3;
}

.show-list li button:focus {
  outline: none;}
.section-buttons {
  display: flex;
  justify-content: center;
  margin: 20px 0;
}

.section-buttons button {
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 8px 15px;
  border-radius: 4px;
  cursor: pointer;
  margin: 0 10px;
}

.section-buttons button.active {
  background-color: #0056b3;
}


</style>
