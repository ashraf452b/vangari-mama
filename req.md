# ScrapMama - Trash Collection Marketplace

## Overview

ScrapMama is a Flask-based web application that serves as a marketplace connecting waste sellers with collectors. The platform allows users to post their recyclable items for sale with custom pricing (including negotiable options), and enables collectors to find and purchase items. The application promotes environmental sustainability by facilitating efficient waste collection and recycling while providing monetary incentives.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Flask
- **UI Framework**: Bootstrap 5 with dark theme support
- **Icons**: Font Awesome 6.0
- **JavaScript**: Vanilla JavaScript for enhanced user interactions
- **Responsive Design**: Mobile-first approach using Bootstrap grid system

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: Flask-Login for session management
- **Password Security**: Werkzeug for password hashing
- **Data Storage**: PostgreSQL database with persistent storage
- **Session Management**: Flask sessions with configurable secret key

### Application Structure
```
/
├── app.py              # Application factory and configuration
├── main.py             # Application entry point
├── models.py           # Data models (User, TrashPost)
├── routes.py           # URL routes and view functions
├── templates/          # Jinja2 HTML templates
│   ├── base.html       # Base template with navigation
│   ├── index.html      # Landing page
│   ├── login.html      # Authentication forms
│   ├── register.html   # User registration
│   ├── user_dashboard.html     # User interface
│   ├── collector_dashboard.html # Collector interface
│   ├── create_post.html        # Trash posting form
│   └── view_post.html         # Post details view
└── static/
    ├── css/custom.css  # Custom styling
    └── js/main.js      # Client-side functionality
```

## Key Components

### User Management System
- **Two User Types**: Regular users (waste generators) and collectors
- **Authentication**: Username/password with secure hashing
- **Session Management**: Flask-Login integration for persistent sessions
- **Pricing System**: Cash-based transactions with negotiable pricing options

### Trash Post Management
- **Post Creation**: Users can create posts with trash type, quantity, location, description, and price
- **Pricing Options**: Set fixed prices or mark items as negotiable
- **Status Tracking**: Posts progress through pending → accepted → completed states
- **Categorization**: Support for multiple trash types (plastic, glass, metal, paper, electronic, organic)
- **Location-Based**: Address-based pickup coordination

### Dashboard Systems
- **User Dashboard**: View posts, track earnings, manage account
- **Collector Dashboard**: Find available pickups, manage accepted jobs
- **Real-time Updates**: Auto-refresh functionality for collectors

## Data Flow

### User Registration & Authentication
1. User submits registration form with user type selection
2. System validates uniqueness of username/email
3. Password is hashed and stored securely
4. User can log in and access appropriate dashboard

### Trash Collection Workflow
1. User creates trash post with details, location, and price
2. Post appears in collector dashboard as available pickup
3. Collector accepts the post (status: pending → accepted)
4. Collector completes pickup (status: accepted → completed)
5. User receives payment based on their set price

### Database Schema
```sql
-- Users table with authentication and rewards
CREATE TABLE user (
    id SERIAL PRIMARY KEY,
    username VARCHAR(64) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    user_type VARCHAR(20) DEFAULT 'user' NOT NULL,
    total_earnings NUMERIC(10,2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Trash posts with collection workflow
CREATE TABLE trash_post (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES user(id) NOT NULL,
    trash_type VARCHAR(50) NOT NULL,
    quantity INTEGER NOT NULL,
    location VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'pending' NOT NULL,
    collector_id INTEGER REFERENCES user(id),
    price NUMERIC(10,2) NOT NULL,
    is_negotiable BOOLEAN DEFAULT FALSE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);
```

## External Dependencies

### Frontend Dependencies
- **Bootstrap 5**: UI framework and components (CDN)
- **Font Awesome 6**: Icon library (CDN)
- **Custom CSS**: Application-specific styling

### Backend Dependencies
- **Flask**: Core web framework
- **Flask-Login**: User session management
- **Werkzeug**: Password hashing and WSGI utilities
- **Gunicorn**: WSGI HTTP server for production deployment
- **Email-validator**: Email validation functionality

### Installed Packages
```
Flask==3.0.0
Flask-Login==0.6.3
Werkzeug==3.0.1
gunicorn==23.0.0
email-validator==2.1.0
```

### Browser Requirements
- Modern browsers supporting ES6+ JavaScript
- Bootstrap 5 compatibility
- Dark theme support (preferred)

## Deployment Strategy

### Current Configuration
- **Development Mode**: Debug enabled, in-memory storage
- **Host Configuration**: 0.0.0.0:5000 for external access
- **Proxy Support**: ProxyFix middleware for reverse proxy compatibility
- **Environment Variables**: SESSION_SECRET for production security

### Production Considerations
- **Database Migration**: Current in-memory storage needs persistent database
- **Session Security**: Environment-based secret key configuration
- **Static Assets**: CDN delivery for Bootstrap and Font Awesome
- **Auto-refresh**: 30-second intervals for collector dashboard updates

### Scaling Recommendations
- **Database**: Implement PostgreSQL or similar for data persistence
- **Caching**: Redis for session storage and frequently accessed data
- **File Storage**: Cloud storage for potential image uploads
- **Load Balancing**: Support for multiple Flask instances

## Changelog
- June 30, 2025: Initial setup with reward points system
- June 30, 2025: Migrated from reward points to pricing system with negotiable options

## User Preferences

Preferred communication style: Simple, everyday language.