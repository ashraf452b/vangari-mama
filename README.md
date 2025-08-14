# ScrapMama - Trash Collection Marketplace

A web application connecting waste generators with collectors, featuring a reward point system to encourage sustainable waste management.

## Features

- **User Registration**: Sign up as either a User (waste generator) or Collector
- **Trash Posting**: Users can post trash details with location for collection
- **Collection Management**: Collectors can browse, accept, and complete pickups
- **Reward System**: Earn points based on trash type and quantity
- **Real-time Dashboard**: Track posts, earnings, and collection status
- **Responsive Design**: Works on desktop and mobile devices

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: PostgreSQL with SQLAlchemy
- **Frontend**: Bootstrap 5 with dark theme
- **Authentication**: Flask-Login
- **Icons**: Font Awesome 6

## Local Development Setup (VS Code)

### Prerequisites

- Python 3.11+
- PostgreSQL
- VS Code

### Installation

1. Clone the repository and navigate to the project directory

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements_for_vscode.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

5. Create PostgreSQL database:
```sql
CREATE DATABASE scrapmama;
```

6. Initialize the database:
```bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

7. Run the application:
```bash
python main.py
```

The application will be available at `http://localhost:5000`

## Usage

1. **Register**: Create an account as User or Collector
2. **Users**: Post trash details with pickup location
3. **Collectors**: Browse available pickups and accept them
4. **Complete**: Mark pickups as completed to award reward points

## Trash Types & Rewards

- **Electronic**: 5 points per unit
- **Metal**: 4 points per unit
- **Glass**: 3 points per unit
- **Plastic**: 2 points per unit
- **Paper**: 1 point per unit
- **Organic**: 1 point per unit

## Project Structure

```
/
├── app.py              # Flask app configuration
├── main.py             # Application entry point
├── models.py           # Database models (User, TrashPost)
├── routes.py           # URL routes and view functions
├── templates/          # HTML templates
├── static/            # CSS, JS, and assets
├── requirements_for_vscode.txt  # Python dependencies
└── .env.example       # Environment variables template
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License."# Vangari-Mama" 
