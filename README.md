# flask_template
Template project for Flask Python  
  
Link assets: https://drive.google.com/drive/folders/1GuKRGeDuS1i5cusF68VWgUQ13NWcpRtJ?usp=sharing  
Put the static folder at same level with: controllers, dao, models, others and templates  
Put .env at same level with: main.py 
  
To migrate database from flask model:  
1. flask db init
2. flask db migrate -m "migrate message"  
3. flask db upgrade  