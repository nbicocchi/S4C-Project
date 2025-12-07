FROM nginx:alpine

# Pulizia cartella html
RUN rm -rf /usr/share/nginx/html/*

# Copia il frontend
COPY public/ /usr/share/nginx/html/

# Copia il file di root di nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Copia la configurazione del server
COPY default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
