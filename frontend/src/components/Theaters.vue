<template>
  <div>
    <input v-model="searchQuery" @input="performSearch" placeholder="Search...">
          
    <h2 class="section-title">Theater List</h2>
    <div class="theater-container">
      <div v-for="theater in theaters" :key="theater.id" class="theater-card">
        <div v-if="theater.city === userCity">
          <h3 class="theater-name">{{ theater.name }}</h3>
          <p class="theater-address">{{ theater.address }}</p>
          <p class="theater-city">{{ theater.city }}</p>
          <h4>{{ theater.state }}</h4>
          <h4>{{ theater.country }}</h4>
          
          <!-- Add a link to TheaterShow.vue with theater id as parameter -->
          <router-link :to="{ name: 'theater-show', params: { theaterId: theater.id } }">
            View Shows
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

  
  <script>
  import axios from 'axios';
  import { mapGetters } from 'vuex';

  export default {
    data (){
        return {
            theaters: [],
            searchQuery: '',
            userCity: '',
            userEmail: '',
        };
    },
    async mounted (){
        await this.fetchUserCity();
        this.fetchTheaters();
    },
    computed: {
    ...mapGetters(['accessToken']),
  },
    methods: {
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
        
            fetchTheaters() {
            axios
                .get('http://localhost:5000/theaters') 
                .then(response => {
                this.theaters = response.data; 
                })
                .catch(error => {
                console.error('Error fetching theaters:', error);
                });
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
                  
                  this.theaters = response.data.theaters;
                  
                })
                .catch((error) => {
                  console.error('Failed to perform search:', error);
                });
            },
    }
  };
  </script>
  
  <style>
.section-title {
  font-size: 24px;
  margin-bottom: 20px;
  color: #333;
}

.theater-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
}

.theater-card {
  background-color: #f5f5f5;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  width: 300px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;

  /* Hover effect */
  cursor: pointer;
}

.theater-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  background-color: rgb(118, 219, 118);
}

.theater-name {
  margin: 0;
  font-size: 18px;
  font-weight: bold;
}

.theater-address,
.theater-city {
  margin: 5px 0;
  font-size: 14px;
}

/* Add more styling as needed */
</style>
  