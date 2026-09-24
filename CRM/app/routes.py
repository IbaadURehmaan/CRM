from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from . import db
from .models import User, Lead, Deal, Ticket, Activity  # Aapke exact models
from .utils import get_ai_response

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/dashboard')
def dashboard():
    try:
        total_leads = Lead.query.count()
        active_deals = Deal.query.count()
    except:
        total_leads = 0
        active_deals = 0
        
    return render_template('dashboard.html', total_leads=total_leads, active_deals=active_deals)

@bp.route('/leads')
def leads():
    try:
        all_leads = Lead.query.all()
    except:
        all_leads = []
    return render_template('leads.html', leads=all_leads)

@bp.route('/add_lead', methods=['POST'])
def add_lead():
    lead_name = request.form.get('name')
    lead_email = request.form.get('email')
    
    if lead_name and lead_email:
        new_lead = Lead(name=lead_name, email=lead_email, source='portal')
        db.session.add(new_lead)
        db.session.commit()
        
    return redirect(url_for('main.leads'))

@bp.route('/pipeline')
def pipeline():
    try:
        deals_data = Deal.query.all()
        # Database ke 'title' ko frontend ke liye 'name' mein map kar rahe hain
        all_deals = [{'name': d.title, 'amount': d.amount} for d in deals_data]
    except:
        all_deals = []
        
    return render_template('pipeline.html', deals=all_deals)

@bp.route('/add_deal', methods=['POST'])
def add_deal():
    deal_name = request.form.get('name')
    deal_amount = request.form.get('amount')
    
    if deal_name and deal_amount:
        # Aapki Deal ko lead_id chahiye. Hum default lead find ya create karenge
        first_lead = Lead.query.first()
        if not first_lead:
            first_lead = Lead(name="System Lead", email="system@wordbitx.com")
            db.session.add(first_lead)
            db.session.commit()

        # Deal ko title aur lead_id ke sath save kar rahe hain
        new_deal = Deal(title=deal_name, amount=float(deal_amount), stage='New', lead_id=first_lead.id)
        db.session.add(new_deal)
        db.session.commit()
        
    return redirect(url_for('main.pipeline'))

@bp.route('/support')
def support():
    try:
        tickets_data = Ticket.query.all()
        all_tickets = []
        for t in tickets_data:
            # Client ki ID se uska email nikal kar frontend par bhej rahe hain
            client = User.query.get(t.client_id)
            client_email = client.email if client else "unknown@example.com"
            all_tickets.append({
                'id': t.id,
                'description': t.subject,
                'status': t.status,
                'email': client_email
            })
    except:
        all_tickets = []
        
    return render_template('support.html', tickets=all_tickets)

@bp.route('/add_ticket', methods=['POST'])
def add_ticket():
    ticket_desc = request.form.get('description')
    ticket_email = request.form.get('email')
    
    if ticket_desc and ticket_email:
        # Ticket ko client_id chahiye. User find ya create karenge
        client = User.query.filter_by(email=ticket_email).first()
        if not client:
            client = User(name="Client", email=ticket_email, password="none", role="client")
            db.session.add(client)
            db.session.commit()

        # Form data ko 'subject' aur 'client_id' mein adjust kar ke save kar rahe hain
        new_ticket = Ticket(
            subject=ticket_desc, 
            description="Created via support modal.", 
            status='Open', 
            client_id=client.id
        )
        db.session.add(new_ticket)
        db.session.commit()
        
    return redirect(url_for('main.support'))

# --- Authentication Routes ---
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        if email:
            session['user_id'] = email
            return redirect(url_for('main.dashboard'))
    return render_template('login.html')

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login'))

# --- API Routes ---
@bp.route('/api/chat', methods=['POST'])
def chat_api():
    data = request.get_json()
    user_message = data.get('message', '')
    if not user_message:
        return jsonify({'reply': 'Please provide a message.'})
    bot_reply = get_ai_response(user_message)
    return jsonify({'reply': bot_reply})