# Movie Ticket Booking System

## Introduction
The Movie Ticket Booking System is a project aimed at streamlining the process of booking movie tickets. It provides users with a user-friendly platform to explore available movies, view showtimes, select seats, and make reservations. Additionally, it offers an administration interface for managing movies, theaters, and showtimes, ensuring efficient operations.
[![Watch the video for demo]](https://drive.google.com/file/d/1R8GdCYRw8Byn17ZBN_ij39ahQ5dGH9vM/view)


## System Overview
The Movie Ticket Booking System allows users to search for movies, view showtimes, select seats, and book tickets. It includes features for both users and administrators. Users can browse movies, view showtimes, choose seats, and make reservations. Administrators, on the other hand, can manage movies, theaters, and showtimes. The system also utilizes Celery, a distributed task queue, to automate background tasks such as sending reminder emails and generating reports.

## System Architecture
The system follows a client-server architecture. The backend, built using Flask, hosts the application logic and data and communicates with the frontend, which is built with Vue.js, using RESTful APIs. Celery is used for background job automation, enhancing the system's functionality.

## Data Models
The system comprises several data models, including User, Theatre, Movie, Showtime, and Reservation, to manage users, theaters, movies, showtimes, and reservations, respectively.

## Use Cases
- **User Registration:** Users can sign up with their personal details.
- **Browse Movies and Showtimes:** Users can search for movies and view available showtimes.
- **Select Seats and Make Reservation:** Users can select desired seats for a specific showtime and make reservations.

## Security Considerations
- Authentication and authorization mechanisms are implemented to ensure secure access to user and administrator functionalities.
- Passwords are securely hashed using Bcrypt before storage.
- Access to administrator functionalities is restricted to authorized users.

## Technology Stack
- **Backend:** Flask (Python), SQLAlchemy (Database ORM), Flask-JWT-Extended (Authentication)
- **Frontend:** Vue.js, Axios (HTTP requests)
- **Database:** SQLite (Development), PostgreSQL (Production)
- **Additional Tools:** Celery (Scheduled Tasks), Redis (Message Broker)

## Contributors
- **Rohit Shinde** (github.com/rohitshinde333)
## Conclusion
The Movie Ticket Booking System offers a well-designed architecture and data models to support seamless movie ticket booking for users. Its intuitive interface and efficient data management provide a user-friendly experience for both users and administrators. The modular design ensures flexibility for future enhancements and improvements.

[Watch the video presentation](https://drive.google.com/file/d/1R8GdCYRw8Byn17ZBN_ij39ahQ5dGH9vM/view?usp=drive_link)
