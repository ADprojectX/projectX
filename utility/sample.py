import tempfile
from tempfile import NamedTemporaryFile
import os
custom_tmp_dir = '/Users/ad_demon/Documents/GitHub/projectX/tmp'

# Check if the custom temporary directory exists, and create it if not
if not os.path.exists(custom_tmp_dir):
    os.makedirs(custom_tmp_dir)

# Set the custom temporary directory as the tempdir
tempfile.tempdir = custom_tmp_dir
with NamedTemporaryFile(suffix=".txt", dir=custom_tmp_dir, delete=False) as temp_file:
    # Your code to work with the temporary file goes here
    temp_file.write(b"Hello, World!")

# server {
#     server_name nextgenvideo.info www.nextgenvideo.info;

#     location = /favicon.ico { access_log off; log_not_found off; }
#     location /static/ {
#         root /home/ubuntu/projectX;
#     }

#     location / {
#         include proxy_params;
#         proxy_pass http://unix:/run/gunicorn.sock;
#         if ($request_method = 'OPTIONS') {
#                 add_header 'Access-Control-Allow-Origin' 'https://www.magiclips.ai';
#                 add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
#                 add_header 'Access-Control-Allow-Credentials' 'true';
#                 add_header 'Access-Control-Allow-Headers' 'DNT, User-Agent, X-Requested-With, If-Modified-Since, Cache-Control, Content-Type, Range, x-csrftoken';
#                 #add_header Access-Control-Allow-Headers Origin, X-Requested-With, Content-Type, Accept';
#                 add_header 'Access-Control-Expose-Headers' 'Content-Length, Content-Range';
#                 add_header 'Access-Control-Max-Age' 1728000;
#                 add_header 'Content-Type' 'text/plain charset=UTF-8';
#                 add_header 'Content-Length' 0;
#                 return 204;
#         }
#         proxy_ssl_server_name on; # Add this line
#     }

#     listen 443 ssl; # managed by Certbot
#     ssl_certificate /etc/letsencrypt/live/nextgenvideo.info/fullchain.pem; # managed by Certbot
#     ssl_certificate_key /etc/letsencrypt/live/nextgenvideo.info/privkey.pem; # managed by Certbot
#     include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
#     ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot


# }
# server {
#     if ($host = www.nextgenvideo.info) {
#         return 301 https://$host$request_uri;
#     } # managed by Certbot


#     if ($host = nextgenvideo.info) {
#                 return 301 https://$host$request_uri;
#     } # managed by Certbot


#     if ($host = nextgenvideo.info) {
#         return 301 https://$host$request_uri;
#     } # managed by Certbot


#     listen 80;
#     server_name nextgenvideo.info www.nextgenvideo.info;
#     return 404; # managed by Certbot




# }



