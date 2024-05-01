<template>
  <div id="app" >
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    
    <nav :class="{ hidden: isNavbarHidden }" id="navbar">
      <ul>
        <li v-if="isAuthenticated">
          <!-- Display admin-specific navigation links -->
          <router-link to="/adminHome" v-if="isAdmin">Admin Home</router-link> 
          <router-link to="/TheatreAdminHome" v-else-if="isTheaterAdmin" >Admin Home</router-link> 
          <router-link to="/home" v-else>User Home</router-link> |
          <router-link to="/about">About</router-link> |
          <router-link to="/movies">Movies</router-link> |
          <router-link to="/Theaters">Theaters</router-link>

          <button v-if="isAuthenticated" @click="logout" class="btn btn-danger" style="margin-left: 60ch">Logout</button>
        </li>
        <li v-else>
          <!-- Display non-admin navigation links -->
          <router-link to="/">Login Signup</router-link> |
          <router-link to="/Theaters">Theaters</router-link> |
          <router-link to="/movies">Movies</router-link>
        </li>
      </ul>
    </nav>
    
      <router-view style="margin-top: 100px; "></router-view>
      
      <footer class="app-footer" style="margin-top: 100px; margin-bottom: 0%;">
        <div class="footer-content">
          <div class="footer-section">
            <h3>About Us</h3>
            <p>One of the most trusted ticket booking platform of all time. You are right ! I am bluffing : |</p>
          </div>
          <div class="footer-section">
            <h3>Contact Us</h3>
            <p>Email: contact@example.com</p>
            <p>Phone: +123 456 7890</p>
            <p>Address: 123 Street, City, Country</p>
          </div>
          <div class="footer-section">
            <h3>Follow Us</h3>
            <div class="social-icons">
              <a href="#"><i class="fab fa-facebook"></i></a>
              <a href="#"><i class="fab fa-twitter"></i></a>
              <a href="#"><i class="fab fa-instagram"></i></a>
            </div>
          </div>
        </div>
        <div class="footer-bottom">
          <p>&copy; 2023 MoviesHouse. All rights reserved.</p>
        </div>
      </footer>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
  data() {
    return {
      isAuthenticated: false,
      prevScrollPos: window.scrollY,
      isNavbarHidden: false,
    };
  },
  computed: {
    ...mapGetters(['isAdmin', 'accessToken','isTheaterAdmin']),
  },
  mounted() {
    this.checkAuthentication();
    window.addEventListener('scroll', this.handleScroll);
  },
  beforeDestroy() {
    window.removeEventListener('scroll', this.handleScroll);
  },
  watch: {
    accessToken() {
      this.checkAuthentication();
    },
    
  },

  methods: {
    ...mapActions(['clearAccessToken']),
    checkAuthentication() {
      if (this.accessToken) {
        this.isAuthenticated = true;
      } else {
        this.isAuthenticated = false;
      }
    },
    logout() {
        this.clearAccessToken();
        this.$router.push('/');
      },
      handleScroll() {
      const currentScrollY = window.scrollY;

      // Scroll down
      if (this.prevScrollY < currentScrollY) {
        this.isNavbarHidden = true;
      }
      // Scroll up
      else {
        this.isNavbarHidden = false;
      }

      this.prevScrollY = currentScrollY;
    },
  
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  font-size: larger;
}

/* Navbar Styles */


ul {
  list-style: none;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  margin: 0;
  padding: 0;
}

li {
  margin-right: 20px;
}

/* Navigation Link Styles */
router-link {
  color: #fff;
  text-decoration: none;
  font-weight: bold;
  transition: color 0.3s;
}

router-link:hover {
  color: #ddd;
}
#navbar {
  position: fixed;
  top: 0;
  left: 0;
  height: 10%;
  width: 100%;
  background-color: #ffffff; /* Facebook's blue color */
  padding: 10px 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease-in-out, opacity 0.3s ease-in-out;
}

#navbar.hidden {
  transform: translateY(-100%);
  opacity: 0;
}
/* Logout Button Styles */
.btn-danger {
  background-color: #f02849; /* Facebook's red color */
  color: #fff;
  border: none;
  
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s;
}
.container {
  margin-top: 100px; 
  height: 200vh;
  width: 50vw;
}

.btn-danger:hover {
  background-color: #d4263f;
}

.app-footer {
  background-color: #222;
  color: #fff;
  padding: 30px 0;
}

.footer-content {
  display: flex;
  justify-content: space-around;
  max-width: 1200px;
  margin: 0 auto;
}

.footer-section {
  flex: 1;
  padding: 0 20px;
}

.footer-section h3 {
  margin-bottom: 10px;
}

.social-icons a {
  color: #fff;
  font-size: 24px;
  margin-right: 10px;
  transition: color 0.3s;
}

.social-icons a:hover {
  color: #ffc107; /* Change to your preferred hover color */
}

.footer-bottom {
  text-align: center;
  margin-top: 20px;
}

.footer-bottom p {
  font-size: 14px;
}

</style>
