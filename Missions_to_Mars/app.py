#!/usr/bin/env python
# coding: utf-8

# In[3]:


from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars 


# In[4]:


# Create an instance of Flask app
app = Flask(__name__)


# In[ ]:


mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

