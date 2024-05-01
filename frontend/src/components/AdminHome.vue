<template>
  <div >
    <div>
      <h1>Welcome, Admin!     </h1>
      <button v-if="isAuthenticated" @click="delete_my_account" class="btn btn-danger mt-3">Delete My Account</button>
      <br>
      <button v-if="isAuthenticated" @click="updateProfile()" class="btn btn-warning mt-3">Update Profile</button>

    <form v-if="editingProfile" @submit="submitProfile" class="add-movie-form">
      <div>Edit Profile</div>
      <div class="form-group">
        <label for="name">Phone:</label>
        <input type="text" v-model="editingProfile.phone" id="phone">
      </div>
      <div class="form-group">
        <label for="email">Email:</label>
        <input type="email" v-model="editingProfile.email" id="email">
      </div>
      <div class="form-group">
        <label for="address">Address:</label>
        <input type="text" v-model="editingProfile.address" id="address">
      </div>

      <button type="submit" class="btn btn-success">Save</button>
      <button type="button" @click="cancelEditProfile" class="btn btn-danger">Cancel</button>
    </form>
    </div>
      <MovieList :movies="movies" />
      <br>
      <button v-if="isAuthenticated" @click="showAddMovieForm" class="btn btn-primary mt-3">Add Movie</button>
    <br>
    <div v-if="showForm" class="add-movie-form" >
      <h2>Add Movie</h2>
      <form @submit="addMovie" class="needs-validation" novalidate>
        <div class="form-group">
          <label for="title">Title</label>
          <input type="text" v-model="movieData.title" class="form-control" id="title" required>
          <div class="invalid-feedback">Please enter a title.</div>
        </div>
        <div class="form-group">
          <label for="genre">Genre</label>
          <select v-model="movieData.genre" class="form-control" id="genre" required>
            <option value="" disabled>Select a genre</option>
            <option value="Romance">Romance</option>
            <option value="Comedy">Comedy</option>
            <option value="Drama">Drama</option>
            <option value="Drama">Action</option>
            <option value="Drama">Horror</option>
          </select>
          <div class="invalid-feedback">Please select a genre.</div>
        </div>
        <div class="form-group">
          <label for="director">Director</label>
          <input type="text" v-model="movieData.director" class="form-control" id="director" required>
          <div class="invalid-feedback">Please enter a director.</div>
        </div>
        <div class="form-group">
          <label for="release_date">Release Date</label>
          <input type="date" v-model="movieData.release_date" class="form-control" id="release_date" required>
          <div class="invalid-feedback">Please enter a release date.</div>
        </div>
        <div class="form-group">
          <label for="duration">Duration</label>
          <input type="number" v-model="movieData.duration" class="form-control" id="duration" required>
          <div class="invalid-feedback">Please enter a valid duration.</div>
        </div>
        <div class="form-group">
          <label for="description">Description</label>
          <textarea v-model="movieData.description" class="form-control" id="description" rows="4" required></textarea>
          <div class="invalid-feedback">Please enter a description.</div>
        </div>
        <div class="form-group">
          <label for="image">Poster link</label>
          <textarea v-model="movieData.image" class="form-control" id="image" required></textarea>
          <div class="invalid-feedback">Please enter a valid image link.</div>
        </div>
        <div class="form-group">
          <label for="casts">Casts</label>
          <select multiple v-model="selectedCasts" class="form-control" id="casts">
            <option v-for="cast in casts" :key="cast.id" :value="cast.id">{{ cast.name }}</option>
          </select>
          <div class="invalid-feedback">Please select at least one cast.</div>
        </div>
        <div class="buttons">
          <button type="submit" class="btn btn-primary">Submit</button>
          <button type="button" @click="closeForm" class="btn btn-danger">Close</button>
        </div>
      </form>
    </div>
    
    <br>
    <div v-if="casts.length > 0" >
      <h1>
        List of cast in your system
      </h1>
      <table class="table table-bordered">
        <thead class="th" >
          <tr>
            <th> Name</th>
            <th> About</th>
            <th> Delete</th>
            <th> Edit</th>
          </tr>
        </thead >
        <tbody class="td">
          <tr v-for="cast in casts" :key="cast.id" >
            <td>{{ cast.name }}</td>
            <td>{{ cast.about }}</td>
            

            
            <td>
              <button class="btn btn-primary" @click="deleteCast(cast)">Delete</button>
            </td>
            <td>
              <button class="btn btn-warning" @click="editCast(cast)">Edit</button>
            </td>
            
          </tr>
        </tbody>
      </table>
      <div v-if="editingCast" class="edit-cast-form">
        <h2>Edit Cast</h2>
        <form @submit.prevent="saveEditedCast" class="needs-validation" novalidate>
          <div class="form-group">
            <label for="editedCastName">Name</label>
            <input type="text" v-model="editingCast.name" class="form-control" id="editedCastName" required>
            <div class="invalid-feedback">Please enter a cast name.</div>
          </div>
          <div class="form-group">
            <label for="editedCastAbout">About</label>
            <input type="text" v-model="editingCast.about" class="form-control" id="editedCastAbout" required>
            <div class="invalid-feedback">Please enter about the cast.</div>
          </div>
          <div class="buttons">
            <button type="submit" class="btn btn-primary">Save</button>
            <button type="button" @click="cancelEditCast" class="btn btn-danger">Cancel</button>
          </div>
        </form>
      </div>
      
    </div>
    
    <button v-if="isAuthenticated" @click="showAddCastForm" class="btn btn-primary mt-3">Add Cast</button>
    <div v-if="showCastForm" class="add-cast-form">
      <h2>Add Cast</h2>
      <form @submit.prevent="addCast" class="needs-validation" novalidate>
        <div class="form-group">
          <label for="newCast">New Cast Name</label>
          <input type="text" v-model="newCastName" class="form-control" id="newCast" required>
          <div class="invalid-feedback">Please enter a new cast name.</div>
        </div>
        <div class="form-group">
          <label for="newCast">New Cast About</label>
          <input type="text" v-model="newCastAbout" class="form-control" id="newCastAbout" required>
          <div class="invalid-feedback">Please enter about new cast.</div>
        </div>

        <div class="buttons">
          <button type="submit" class="btn btn-primary">Submit</button>
          <button type="button" @click="closeCastForm" class="btn btn-danger">Close</button>
        </div>
      </form>
    </div>
    
    
    
    
    <br>
    <div v-if="allTheatres.length > 0"  style="margin-top: 100px;">
      <h1>
        List of theatres in your system
      </h1>
      <table class="table table-bordered">
        <thead class="th">
          <tr>
            <th> Name</th>
            <th> Address</th>
            <th> City</th>
            <th> State</th>
            <th> Country</th>
            <th> Capacity</th>
            <th> Report</th>
            <th> Delete</th>
            <th> Edit</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="theatre in allTheatres" :key="theatre.id" >
            <td>{{ theatre.name }}</td>
            <td>{{ theatre.address }}</td>
            <td>{{ theatre.city }}</td>
            <td>{{ theatre.state }}</td>
            <td>{{ theatre.country }}</td>
            <td>{{ theatre.capacity}}</td>
            <td>
              <button  class="btn btn-success" @click="generateReport(theatre)">Report</button>
              
            </td>
            
            <td>
              <button class="btn btn-primary" @click="deleteTheatre(theatre)">Delete</button>
            </td>
            <td>
              <button class="btn btn-warning" @click="editTheatre(theatre)">Edit</button>
            </td>
            
          </tr>
        </tbody>
        <a :href="downloadLink" download v-if="downloadLink">Download generated report</a>
      </table>
      <br>
      <div v-if="editingTheatre" class="add-theatre-form">
        <h2>Edit Theatre</h2>
        <form @submit.prevent="saveEditedTheatre" class="needs-validation" novalidate>
          <div class="form-group">
          <label for="name">Theatre Name</label>
          <input type="text" v-model="editingTheatre.name" class="form-control" id="name" >
          <div class="invalid-feedback">Please enter a theatre name.</div>
        </div>
        <div class="form-group">
          <label for="address">Address</label>
          <input type="text" v-model="editingTheatre.address" class="form-control" id="address" >
          <div class="invalid-feedback">Please enter an address.</div>
        </div>
        <div class="form-group">
        <select v-model="editingTheatre.city" required >
          <option disabled value="">Select a city</option>
          <option v-for="city in cities" :key="city.id" :value="city.name">{{ city.name }}</option>
        </select>
        </div>
        <div class="form-group">
          <label for="state">State</label>
          <input type="text" v-model="editingTheatre.state" class="form-control" id="state" >
          <div class="invalid-feedback">Please enter a state.</div>
        </div>
        <div class="form-group">
          <label for="country">Country</label>
          <input type="text" v-model="editingTheatre.country" class="form-control" id="country" >
          <div class="invalid-feedback">Please enter a country.</div>
        </div>
        <div class="form-group">
          <label for="capacity">Capacity</label>
          <input type="number" v-model="editingTheatre.capacity" class="form-control" id="capacity" >
          <div class="invalid-feedback">Please enter a valid capacity.</div>
        </div>

          
          <div class="buttons">
            <button type="submit" class="btn btn-primary">Save</button>
            <button type="button" @click="cancelEditTheatre" class="btn btn-danger">Cancel</button>
          </div>
        </form>
      </div>
    </div>
    <button v-if="isAuthenticated" @click="showAddTheatreForm" class="btn btn-primary mt-3">Add Theatre</button>

      <div v-if="showTheatreForm" class="add-theatre-form">
      <h2>Add Theatre</h2>
      <form @submit.prevent="addTheatre" class="needs-validation" novalidate>
        <div class="form-group">
          <label for="name">Theatre Name</label>
          <input type="text" v-model="theatreData.name" class="form-control" id="name" required>
          <div class="invalid-feedback">Please enter a theatre name.</div>
        </div>
        <div class="form-group">
          <label for="address">Address</label>
          <input type="text" v-model="theatreData.address" class="form-control" id="address" required>
          <div class="invalid-feedback">Please enter an address.</div>
        </div>
        <div class="form-group">
        <select v-model="theatreData.city" required >
          <option disabled value="">Select a city</option>
          <option v-for="city in cities" :key="city.id" :value="city.name">{{ city.name }}</option>
        </select>
        </div>
        <div class="form-group">
          <label for="state">State</label>
          <input type="text" v-model="theatreData.state" class="form-control" id="state" required>
          <div class="invalid-feedback">Please enter a state.</div>
        </div>
        <div class="form-group">
          <label for="country">Country</label>
          <input type="text" v-model="theatreData.country" class="form-control" id="country" required>
          <div class="invalid-feedback">Please enter a country.</div>
        </div>
        <div class="form-group">
          <label for="capacity">Capacity</label>
          <input type="number" v-model="theatreData.capacity" class="form-control" id="capacity" required>
          <div class="invalid-feedback">Please enter a valid capacity.</div>
        </div>

        <div class="buttons">
          <button type="submit" class="btn btn-primary">Submit</button>
          <button type="button" @click="closeTheatreForm" class="btn btn-danger">Close</button>
        </div>
      </form>
    </div>

    

    
    
    <Modal :title="modalTitle" :message="modalMessage" :isOpen="showModal" @close="closeModal" />

  </div>
</template>
  
  <script>
  import { mapGetters, mapActions } from 'vuex';
  import axios from 'axios';
  import { useStore } from 'vuex';
  import MovieList from './MovieList.vue';
  export default {
    components: {
    MovieList,
  },
    data() {
      return {
        downloadLink: '',
        taskComplete: false,
        isAuthenticated: false,
        showForm: false,
        showCastForm: false,
        movieData: {
          title: '',
          genre: '',
          director: '',
          release_date: '',
          duration: 0,
          description: '',
          image: '',
          cast: null,
        },
        selectedCasts: [],
        casts: '',
        newCastName: '',
        newCastAbout: '',
        showTheatreForm: false,
        theatreData: {
          name: '',
          address: '',
          city: '',
          state: '',
          country: '',
          capacity: 0,
        },
        showModal: false,
        editingProfile: null,
        userId: 0,
        allTheatres: [],
        allCast: [],
        editingCast: null,
        editingTheatre: null,
        cities: [
      
        { id: 1, name: 'Mumbai' },
        { id: 2, name: 'Delhi' },
        { id: 3, name: 'Bangalore' },
        { id: 4, name: 'Chennai' },
        { id: 5, name: 'Kolkata' },
        { id: 6, name: 'Hyderabad' },
        { id: 7, name: 'Pune' },
        { id: 8, name: 'Ahmedabad' },
        { id: 9, name: 'Jaipur' },
        { id: 10, name: 'Lucknow' },
        { id: 11, name: 'Kanpur' },
        { id: 12, name: 'Nagpur' },
        { id: 13, name: 'Indore' },
        { id: 14, name: 'Chandigarh' },
        { id: 15, name: 'Coimbatore' },
        { id: 16, name: 'Kochi' },
        { id: 17, name: 'Bhopal' },
        { id: 18, name: 'Vadodara' },
        { id: 19, name: 'Visakhapatnam' },
        { id: 20, name: 'Surat' },
        { id: 21, name: 'Patna' },
        { id: 22, name: 'Ludhiana' },
        { id: 23, name: 'Agra' },
        { id: 24, name: 'Varanasi' },
        { id: 25, name: 'Sangli' }
      
      ],
      };
    },
    mounted() {
      if (this.accessToken) {
        this.isAuthenticated = true;
        
        this.fetchUsername();
        this.fetchTheatres();
        this.fetchCasts();
      }
    },
    computed: {
      ...mapGetters(['accessToken'])
    },
    methods: {
      ...mapActions(['clearAccessToken']),
      generateReport(theatre) {
        
        axios
          .post(`http://localhost:5000/generate_report/${theatre.id}`,{
            headers: {
              Authorization: `Bearer ${this.accessToken}`,
            },
          })
          .then((response)=> {
            alert(response.data.message);
            
            this.checkTaskStatus(response.data.task_id);
            
          })
          .catch((error)=>{
            console.error(error);
          })
      },
      async checkTaskStatus(taskId) {
        const response = await fetch(`http://localhost:5000/check_task_status/${taskId}`);
        const data = await response.json();

        if (data.status === 'SUCCESS') {
          this.downloadLink = data.download_url;
          this.taskComplete = true;
        } else if (data.status === 'PENDING' || data.status === 'STARTED') {
          setTimeout(() => this.checkTaskStatus(taskId), 2000); 
        }
        
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
      deleteTheatre(theatre) {
        axios
          .delete(`http://localhost:5000/theaters/${theatre.id}/720305`,{
            headers: {
              Authorization: `Bearer ${this.accessToken}`,
            },
          })
          .then((response)=> {
            alert(response.data);
          })
          .catch((error)=> {
            console.error(error);
          });
      },
      deleteCast(cast) {
        axios
          .delete(`http://localhost:5000/casts/${cast.id}`,{
            headers: {
              Authorization: `Bearer ${this.accessToken}`,
            },
          })
          .then((response)=> {
            alert(response.data);
          })
          .catch((error)=> {
            console.error(error);
          });
      },
      fetchTheatres() {
        axios
          .get('http://localhost:5000/theaters',{
            headers: {
              Authorization: `Bearer ${this.accessToken}`,
            },
          })
          .then((response) => {
            this.allTheatres = response.data;
          })
          .catch((error)=> {
            console.error(error);
          });
      },
      fetchUsername() {
      
      axios
        .get('http://localhost:5000/protected', {
          headers: {
            Authorization: `Bearer ${this.accessToken}`,
          },
        })
        .then((response) => {
          // Handle the response from the protected resource
          
          this.userId = response.data.id;
        })
        .catch((error) => {
          // Handle the error
          console.error(error);
        });
    },
      updateProfile() {
      
      this.editingProfile = {
        phone: '',
        email: '', 
        address: '',

      };
    },
    cancelEditProfile() {
      this.editingProfile = null;
    },
      showAddMovieForm() {
        this.showForm = true;
      },
      closeForm(event){
        event.preventDefault();
        event.target.classList.add('was-validated');
        if (!event.target.checkValidity()) {
            return;
        }
        this.showForm = false;
      },
      addMovie(event) {
          event.preventDefault();
          event.target.classList.add('was-validated');
          if (!event.target.checkValidity()) {
            return;
          }

          const formattedReleaseDate = new Date(this.movieData.release_date).toISOString().split('T')[0];

          axios
            .post('http://localhost:5000/movies', {
              ...this.movieData,
              release_date: formattedReleaseDate,
              cast_ids: this.selectedCasts, // Add selected cast IDs to the request payload
            }, {
              headers: {
                Authorization: `Bearer ${this.accessToken}`,
              },
            })
            .then((response) => {
              alert(response.data.message);
              console.log('Movie added successfully:', response.data);
              this.movieData = {
                title: '',
                genre: '',
                director: '',
                release_date: '',
                duration: 0,
                description: '',
                image: '',
              };
              this.selectedCasts = []; // Clear the selected casts
              this.showForm = false;
              this.$router.push('/adminHome')
              
            })
            .catch((error) => {
              console.error('Failed to add movie:', error);
              this.$router.push('/');
            });
        },

        showAddCastForm() {
          this.showCastForm = true;
        },
        closeCastForm(event) {
          event.preventDefault();
          event.target.classList.add('was-validated');
          if (!event.target.checkValidity()) {
            return;
          }
          this.showCastForm = false;
        },
        addCast(event) {
          event.preventDefault();
          event.target.classList.add('was-validated');
          if (!event.target.checkValidity()) {
            return;
          }

          axios
            .post('http://localhost:5000/casts', {
              name: this.newCastName,
              about: this.newCastAbout,
            }, {
              headers: {
                Authorization: `Bearer ${this.accessToken}`,
              },
            })
            .then((response) => {
              alert(response.data.message);
              console.log('Cast added successfully:', response.data);
              this.newCastName = '';
              this.newCastAbout = '';
              this.fetchCasts(); // Refresh casts data after adding a new cast
              this.showCastForm = false;
            })
            .catch((error) => {
              console.error('Failed to add cast:', error);
              this.$router.push('/');
            });
        },
        fetchCasts() {
          axios.get('http://localhost:5000/casts')
            .then(response => {
              this.casts = (response.data);
            })
            .catch(error => {
              console.error('Failed to fetch casts:', error);
            });
        },
        showAddTheatreForm() {
          this.showTheatreForm = true;
        },

        closeTheatreForm() {
          this.showTheatreForm = false;
          this.resetTheatreData();
        },

        resetTheatreData() {
          this.theatreData = {
            name: '',
            address: '',
            city: '',
            state: '',
            country: '',
            capacity: 0,
          };
        },
        addTheatre(event) {
          event.preventDefault();
          event.target.classList.add('was-validated');
          if (!event.target.checkValidity()) {
            return;
          }

          axios
            .post('http://localhost:5000/theaters', this.theatreData, {
              headers: {
                Authorization: `Bearer ${this.accessToken}`,
              },
            })
            .then((response) => {
              alert(response.data.message);
              console.log('Theatre added successfully:', response.data);
              this.closeTheatreForm();
              this.fetchTheatres();
            })
            .catch((error) => {
              console.error('Failed to add theatre:', error);
              this.$router.push('/');
            });
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
          // Handle the successful profile update
          this.showModal = true;
          this.modalTitle = 'Success';
          this.modalMessage = 'Profile updated successfully';

          // Reset the editingProfile and fetch the updated profile data
          this.editingProfile = null;
          this.fetchUsername();
        })
        .catch((error) => {
          // Handle the profile update error
          console.error('Failed to update profile:', error);
        });
    },
    closeModal() {
      this.showModal = false;
    },
    editCast(cast) {
      this.editingCast = { ...cast };
    },
    saveEditedCast() {
      const editedCast = this.editingCast;
      axios
        .put(`http://localhost:5000/casts/${editedCast.id}`, editedCast, {
          headers: {
            Authorization: `Bearer ${this.accessToken}`,
          },
        })
        .then((response) => {
          alert(response.data.message);
          console.log('Cast updated successfully:', response.data);
          this.editingCast = null;
          this.fetchCasts(); // Refresh the cast data
        })
        .catch((error) => {
          console.error('Failed to update cast:', error);
        });
    },
    cancelEditCast() {
      this.editingCast = null;
    },
    editTheatre(theatre) {
      this.editingTheatre = { ...theatre };
    },
    saveEditedTheatre() {
      const editedTheatre = this.editingTheatre;
      axios
        .patch(`http://localhost:5000/theaterEditing/${editedTheatre.id}`, editedTheatre, {
          headers: {
            Authorization: `Bearer ${this.accessToken}`,
          },
        })
        .then((response) => {
          alert(response.data.message);
          console.log('Theatre updated successfully:', response.data);
          this.editingTheatre = null;
          this.fetchTheatres(); 
        })
        .catch((error) => {
          console.error('Failed to update theatre:', error);
        });
    },
    cancelEditTheatre() {
      this.editingTheatre = null;
    },
  

    },
  };
  </script>

<style>
.add-movie-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 900px;
  margin: 0 auto;
}

.add-theatre-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 900px;
  margin: 0 auto;
}

.add-cast-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 900px;
  margin: 0 auto;
}

.form-group {
  margin: 10px 0;
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
  margin-top: 5px;
}

.buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}
.table {
  border-collapse: collapse;
  width: 100%;
  border-color: #000000;
  
}
.th {
  background-color: rgb(224, 182, 126);
}
.td {
  border: 1px solid #000000;
  padding: 8px;
  text-align: left;
  background-color: #ffffff;
}


</style>