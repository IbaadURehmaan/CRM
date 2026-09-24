import os

class Config:
    # Flask security key session aur cookies ke liye
    SECRET_KEY = 'wordbitx_secure_key_123'
    
    # SQLite database connection
    SQLALCHEMY_DATABASE_URI = 'sqlite:///wordbitx_crm.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Free APIs keys (Jab apke paas keys hon toh yahan update kar lein)
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY') or 'AQ.Ab8RN6Jl9AGfhzRGJ8Yw-9Sv8KxC7lZcU-YbGuJQF2-g810Yrw'
    EXCHANGE_RATE_API_KEY = os.environ.get('EXCHANGE_RATE_API_KEY') or '10db581514ed624a0cdedaf5'