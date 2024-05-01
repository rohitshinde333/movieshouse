<template>
  <div>
    <div>
      <button v-if="!showLogin" @click="toggleForm('login')" class="btn btn-primary" style="margin-right: 1.5ch;width: 10ch;">Login</button>
      <button v-if="!showSignup" @click="toggleForm('signup')" class="btn btn-warning" style="margin-left: 1.5ch; width: 10ch; ">Signup</button>
    </div>

    <div v-if="showLogin">
      
      <div class="d-flex justify-content-center align-items-center" style="height: 60vh;">
        <form @submit="login">
          <div class="form-group-login" >
            <label for="exampleInputEmail1" style="font-size:x-large;">Username</label>
            <input type="text" v-model="loginData.name" class="form-control" placeholder="Username" >
            <small id="emailHelp" class="form-text text-muted">We'll never share your Username with anyone else.</small>
          </div>
          <div class="form-group-login">
            <label for="exampleInputPassword1" style="font-size:x-large;">Password</label>
            <input type="password"  v-model="loginData.password" class="form-control" id="exampleInputPassword1" placeholder="Password" required>
          </div>
          <div class="form-check">
            <input type="checkbox"  class="form-check-input" id="exampleCheck1" required>
            <label class="form-check-label" for="exampleCheck1">Check me out</label>
          </div>
          <button type="submit" class="btn btn-primary">Submit</button>
          <br>
        </form>
      </div>
      
    </div>

    <div v-if="showSignup">
      <h2>Signup</h2>
      <form @submit="signup" class="signup-form">
        <input type="text" v-model="signupData.name" placeholder="Username" required>
        <input type="password" v-model="signupData.password" placeholder="Password" required>
        <input type="text" v-model="signupData.email" placeholder="Email" required>
        <select v-model="signupData.address" required>
          <option disabled value="">Select a city</option>
          <option v-for="city in cities" :key="city.id" :value="city.name">{{ city.name }}</option>
        </select>
        <input type="text" v-model="signupData.phone" placeholder="Phone" required>
        <div class="admin-checkbox">
          <label for="admin">Admin:</label>
          <input type="checkbox" v-model="signupData.is_admin" id="admin">
        </div>
        <input type="password" v-if="signupData.is_admin" v-model="signupData.key" placeholder="Enter Admin Verification">
        <button type="submit" class="btn btn-success mt-3">Signup</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import AdminHome from './AdminHome.vue';
import UserHome from './UserHome.vue';

export default {
  components: {
    AdminHome,
    UserHome,
  },
  data() {
    return {
      showLogin: false,
      showSignup: false,
      loginData: {
        name: '',
        password: '',
      },
      signupData: {
        name: '',
        password: '',
        email: '',
        address: '',
        phone: '',
        is_admin: false,
        key: '',
      },
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
      isAuthenticated: false,
      isAdmin: false,
      isTheatreAdmin: false,
    };
  },
  methods: {
    toggleForm(form) {
      if (form === 'login') {
        this.showLogin = true;
        this.showSignup = false;
      } else if (form === 'signup') {
        this.showLogin = false;
        this.showSignup = true;
      }
    },
    login(event) {
      event.preventDefault();

      // Make API request to login endpoint
      axios
        .post('http://localhost:5000/login', this.loginData)
        .then(response => {
          // Handle successful login
          console.log('Logged in successfully');

          this.isAuthenticated = true;
          this.isAdmin = response.data.is_admin;
          this.isTheatreAdmin = response.data.is_theatre_admin;
          this.$store.dispatch('setAccessToken', {
            token: response.data.access_token
            
          });

          this.$store.dispatch('setIsAdmin', {
            is_admin: response.data.is_admin
            
          });

          this.$store.dispatch('setIsTheaterAdmin',{
            is_theater_admin: response.data.is_theatre_admin

          })
          this.$store.dispatch('setTheatreId',{
            theatre_id: response.data.theatre_id
          })

          if (this.isAdmin) {
            this.$router.push('/AdminHome');
          } else if (this.isTheatreAdmin) {
            this.$router.push('/TheatreAdminHome');
          } else {
            this.$router.push('/home')
          }
        })
        .catch(error => {
          // Handle login error
          alert(error.response.data.message);
          console.error('Login failed:', error.response.data.message);
          this.loginData.name = '';
          this.loginData.password = '';
        });
    },

    async signup(event) {
      event.preventDefault();

      // Make API request to signup endpoint
      axios
        .post('http://localhost:5000/users', this.signupData)
        .then(response => {
          // Handle successful signup
          alert(response.data.message);
          console.log('Signed up successfully');
          this.sendEmail();
        })
        .catch(error => {
          // Handle signup error
          console.error('Signup failed:', error);
          alert("Something went wrong. Email ID in use")
        });
    },
    async sendEmail() {
      const emailData = {
        recipient: this.signupData.email,
        subject: "welcome / do-not reply",
        body: "Hello user, Welcome to MoviesHouse. This is an autogenerated mail. Please do not reply to this mail. Thank you. Enjoy Movies!!!",
      };

      axios({
        method: 'post',
        url: 'http://localhost:5000/email',
        data: emailData,
        headers: {
          'Content-Type': 'application/json',
        },
      })
        .then(response => {
          console.log('Email sent:', response.data.message);
        })
        .catch(error => {
          console.error('Failed to send email:', error);
        });
    },
    
  },
};
</script>
<style scoped>
.signup-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 600px;
  margin: 0 auto;
}

.signup-form input {
  margin: 10px 0;
  padding: 10px;
  width: 100%;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.signup-form select {
  margin: 10px 0;
  padding: 10px;
  width: 100%;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.admin-checkbox {
  display: flex;
  align-items: center;
  margin: 10px 0;
}

.admin-checkbox label {
  margin-right: 10px;
}

.btn-success {
  background-color: #28a745;
  color: #fff;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-success:hover {
  background-color: #218838;
}

.form-group-login {
  margin: 10px 0;
  padding: 10px;
  width: 100%;
  border: 1px solid #ccc;
  border-radius: 4px;
}

</style>
