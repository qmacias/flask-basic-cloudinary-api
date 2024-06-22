# Getting Started

We're using Python v3.10.0 and Flask v3.0.3

## Cloudinary Routes

Here the client interacts with the provided Flask API endpoints.

| Method | Url                                                             | Description            |
|--------|-----------------------------------------------------------------|------------------------|
| GET    | https://flask-basic-cloudinary-api.vercel.app                   | Index path             |
| GET    | https://flask-basic-cloudinary-api.vercel.app/images            | Search all images      |
| PUT    | https://flask-basic-cloudinary-api.vercel.app/images/{image_id} | Upload a new image     |
| GET    | https://flask-basic-cloudinary-api.vercel.app/images/{image_id} | Get a current image    |
| DELETE | https://flask-basic-cloudinary-api.vercel.app/images/{image_id} | Delete a current image |
