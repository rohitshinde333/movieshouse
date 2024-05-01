<template>
  <div style="background-color: rgb(255, 255, 255);">
    <input v-model="searchQuery" @input="performSearch" placeholder="Search...">

    <h2>Movie List</h2>
    <div class="movie-container">
      <button class="navigation-button" @click="previousPage">&#60;</button>
      <div v-for="movie in visibleMovies" :key="movie.id" class="movie-card" @click="openMoviePage(movie.id)">
        <div class="movie-image">
          <img :src="movie.image" :alt="movie.title" />
        </div>
        <div class="movie-details-list">
          <h3 class="movie-title">Title : {{ movie.title }}</h3><br>
          <h4 class="movie-genre">Genre :{{ movie.genre }}</h4><br>

          <br>
          
        </div>
        
        
      </div>
      <button class="navigation-button" @click="nextPage">&#62;</button>
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
  data() {
    return {
      movies: [],
      searchQuery: '',
      showModal: false,
      modalTitle: '',
      modalMessage: '',
      currentPage: 0,
      moviesPerPage: 4
    };
  },
  computed: {
    ...mapGetters(['isAdmin']),
    ...mapGetters(['accessToken']),
    visibleMovies() {
      const startIndex = this.currentPage * this.moviesPerPage;
      const endIndex = startIndex + this.moviesPerPage;
      return this.movies.slice(startIndex, endIndex);
    }
  },
  mounted() {
    this.fetchMovies();
  },
  methods: {
    performSearch() {
      if (this.searchQuery === '') {
        this.searchResults = [];
        return;
      }

      // Make an API request to perform the search
      const accessToken = this.accessToken;

      axios
        .get(`http://localhost:5000/search?q=${this.searchQuery}`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        })
        .then((response) => {
          this.movies = response.data.movies;
          
          
        })
        .catch((error) => {
          console.error('Failed to perform search:', error);
        });
    },
    fetchMovies() {
      axios.get('http://localhost:5000/movies')
        .then(response => {
          this.movies = response.data;
        })
        .catch(error => {
          console.error(error);
        });
    },
    closeModal() {
      this.showModal = false;
    },
    closeForm() {
      this.editingMovie = null;
    },
    previousPage() {
      if (this.currentPage > 0) {
        this.currentPage--;
      }
    },
    nextPage() {
      if (this.currentPage < Math.ceil(this.movies.length / this.moviesPerPage) - 1) {
        this.currentPage++;
      }
    },
    openMoviePage(movieId) {
      this.$router.push(`/MoviePage/${movieId}`);
      console.log(`${movieId}`);
    },
  },
  
};
</script>


<style>
.movie-container {
  display: flex;
  flex-wrap: nowrap;
  overflow-x: auto;
  justify-content:center;
  gap: 20px;
  padding: 10px;
}

.navigation-button {
  background-color: #b6b7b9;
  color: #fff;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
}

.navigation-button:hover {
  background-color: #0056b3;
}

.movie-card {
  width: 250px;
  
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.movie-image img {
  width: 100%;
  height: 200px;
  border-radius: 8px 8px 0 0;
}

.movie-details-list {
  padding: 10px;
}

.movie-title {
  margin: 0;
  font-size: 18px;
  font-weight: bold;
}

.movie-genre {
  margin: 5px 0;
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
</style>
