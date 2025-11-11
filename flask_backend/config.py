#!/usr/bin/env python3
"""
Configuration file for Flask backend
"""

import os

class Config:
    """Flask application configuration"""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'leaksense-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    PORT = int(os.getenv('FLASK_PORT', 5000))
    
    # Database settings
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'leaksense')
    DB_USER = os.getenv('DB_USER', 'leaksense_user')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'leaksense_pass')
    
    # CORS settings
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')
    
    # API settings
    MAX_RECORDS_PER_REQUEST = 1000
    DEFAULT_RECORDS_LIMIT = 50
    MAX_TIME_RANGE_HOURS = 168  # 7 days
