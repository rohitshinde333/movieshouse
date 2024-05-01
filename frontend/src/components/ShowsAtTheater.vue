<template>
  <div>
    <div class="tabs">
      <div
        class="tab"
        v-for="(tab, index) in tabs"
        :key="index"
        :class="{ active: activeTabIndex === index }"
        @click="changeTab(index)"
      >
        {{ tab }}
      </div>
    </div>
    <div v-for="show in filteredShows" :key="show.id" >
      <div v-if="show.theater.id == theatreId" class="show-timing">
        <p >Movie Name: {{ show.movie.title }}</p>
        <p>Date and Time: {{ show.show_datetime }}</p>
        <p>Ticket Price: {{ show.price }}</p>
        <button @click="openBooking(show)" class="btn btn-success">Book Show</button>
      </div>
    </div>
    <div v-if="selectedShow" class="seat-selection">
      <h3>Select Seats for Show at {{ selectedShow.theater.name }} - {{ selectedShow.show_datetime }}</h3>
      <div class="seat-grid">
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
        <button @click="confirmBooking" class="btn btn-success">Confirm Booking</button>
        <button @click="cancelBooking" class="btn btn-danger">Cancel</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';

export default {
  name: 'TheaterShow',
  data() {
    return {
      userCityShows: [],
      userCity: '',
      userEmail: '',
      theatreId: this.$route.params.theaterId,
      tabs: ['Today', 'Tomorrow', 'Day After Tomorrow'],
      activeTabIndex: 0,
      filteredShows: [],
      selectedShow: null,
      selectedSeats: [],
      bookedSeats: [], 
    };
  },
  computed: {
    ...mapGetters(['accessToken']),
    ...mapGetters(['isTheaterAdmin']),
    ...mapGetters(['theatre_id']),
    ...mapGetters(['isAdmin']),
  },
  async mounted() {
    await this.fetchUserCity();
    this.fetchUserCityShows();
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
    async fetchUserCityShows() {
      await axios
        .post(`http://localhost:5000/showsAtCity/1/${this.userCity}`, null, {
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
      
    },
    changeTab(index) {
      this.activeTabIndex = index;
    },
    filterShowsByDate(date) {
      return this.userCityShows.filter(
        (show) => show.show_datetime.split('T')[0] === date
      );
    },
    openBooking(show) {
      this.selectedShow = show;
    },
    cancelBooking() {
      this.selectedShow = null;
      this.selectedSeats = [];
    },
    isSeatBooked(seatNumber) {
      return this.bookedSeats.includes(seatNumber);
    },
    isSelected(seatNumber) {
      return this.selectedSeats.includes(seatNumber);
    },
    toggleSeatSelection(seatNumber) {
      if (this.isSeatBooked(seatNumber)) {
        return;
      }

      if (this.isSelected(seatNumber)) {
        this.selectedSeats = this.selectedSeats.filter((seat) => seat !== seatNumber);
      } else {
        this.selectedSeats.push(seatNumber);
      }
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
    async confirmBooking() {
      const selectedSeatsArray = [...this.selectedSeats];
      const data = {
        show_id: this.selectedShow.id,
        theater_id: this.selectedShow.theater.id,
        selected_seats: selectedSeatsArray,
      };

      try {
        const response = await axios.post('http://localhost:5000/bookings', data, {
          headers: {
            Authorization: `Bearer ${this.accessToken}`,
          },
        });
        await this.fetchBookedSeats(this.selectedShow.id);
        this.cancelBooking();
        alert(response.data.message);
      } catch (error) {
        console.error('Error while booking seats:', error.response.data.message);
      }
    },
  
  },
  watch: {
    activeTabIndex(newValue) {
      const today = new Date();
      const tomorrow = new Date(today);
      tomorrow.setDate(today.getDate() + 1);
      const dayAfterTomorrow = new Date(today);
      dayAfterTomorrow.setDate(today.getDate() + 2);

      const selectedDate = [
        today.toISOString().split('T')[0],
        tomorrow.toISOString().split('T')[0],
        dayAfterTomorrow.toISOString().split('T')[0],
      ][newValue];

      this.filteredShows = this.filterShowsByDate(selectedDate);
    },
  },
  
};
</script>

<style>
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
.show-timing {
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 15px;
  width: 500px;
  margin-right:100px;
  margin-left: 485px;
  
}
.tabs {
  display: flex;
  margin-bottom: 10px;
  display: flex;
  justify-content: center;
}

.tab {
  cursor: pointer;
  padding: 8px 16px;
  border: 1px solid #ccc;
  margin-right: 10px;
  border-radius: 4px 4px 0 0;
}

.tab.active {
  background-color: #ef6666;
  border-bottom-color: transparent;
}

</style>
