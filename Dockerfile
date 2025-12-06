# Step 1: Use official Nginx image (Alpine for minimal size)
FROM public.ecr.aws/nginx/nginx:alpine

# Step 2: Copy static files from dist folder to Nginx html directory
COPY dist /usr/share/nginx/html

# Step 3: Expose port 80 (default HTTP port)
EXPOSE 80

# Step 4: Start Nginx server in foreground
CMD ["nginx", "-g", "daemon off;"]
