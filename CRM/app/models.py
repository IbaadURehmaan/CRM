from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize the database object
db = SQLAlchemy()

# Users table for Admin, Agents, and Clients (Role-Based Access)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='agent') # admin, agent, or client

# Leads table for storing captured visitors
class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    location = db.Column(db.String(100)) # Auto-filled via IP
    source = db.Column(db.String(50), default='chatbot') 
    score = db.Column(db.Integer, default=0) # AI priority score
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Connect leads to their deals and activity timeline
    deals = db.relationship('Deal', backref='lead', lazy=True)
    activities = db.relationship('Activity', backref='lead', lazy=True)

# Deals table for the drag-and-drop Kanban Pipeline
class Deal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    amount = db.Column(db.Float, default=0.0)
    currency = db.Column(db.String(10), default='USD') # Multi-currency support
    stage = db.Column(db.String(50), default='New') # Stages: New, Proposal, Negotiation, Won, Lost
    
    lead_id = db.Column(db.Integer, db.ForeignKey('lead.id'), nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# Activity table for tracking calls, emails, and notes
class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action_type = db.Column(db.String(50)) # Call, Email, Note
    description = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    lead_id = db.Column(db.Integer, db.ForeignKey('lead.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# Ticket table for client support requests
class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Open') # Open, In-Progress, Resolved
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)