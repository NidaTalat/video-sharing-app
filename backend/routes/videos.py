from flask import request, jsonify
from flask_restful import Resource
import cloudinary
import cloudinary.uploader
from azure.cosmos import CosmosClient, PartitionKey
from config import Config
import uuid
from datetime import datetime

# Initialize Cloudinary
cloudinary.config(
    cloud_name=Config.CLOUDINARY_CLOUD_NAME,
    api_key=Config.CLOUDINARY_API_KEY,
    api_secret=Config.CLOUDINARY_API_SECRET,
)

# Initialize Cosmos DB client
cosmos_client = CosmosClient(Config.COSMOS_URI, credential=Config.COSMOS_KEY)
database = cosmos_client.get_database_client(Config.COSMOS_DB_NAME)
videos_container = database.get_container_client("videos")
comments_container = database.get_container_client("comments")

class Videos(Resource):
    def post(self):

        print(request.files)  # Check what files are in the request

        
        if "file" not in request.files:
            return {"message": "No video file provided"}, 400

        video_file = request.files["file"]
        title = request.form.get("title", "Untitled")
        uploaded_by = request.form.get("uploaded_by")

        # Upload video to Cloudinary
        upload_result = cloudinary.uploader.upload(video_file, resource_type="video")
        video_url = upload_result.get("url")

        # Add video metadata to Cosmos DB
        video = {
            "id": upload_result.get("public_id"),
            "title": title,
            "video_url": video_url,
            "uploaded_by": uploaded_by,
        }
        videos_container.create_item(video)

        return {"message": "Video uploaded successfully", "video": video}, 201

    def get(self):
        videos = list(videos_container.read_all_items())
        return {"videos": videos}, 200

class Comments(Resource):
    def post(self):
        """Add a new comment."""
        data = request.json
        video_id = data.get("video_id")
        user = data.get("user")
        comment = data.get("comment")

        if not video_id or not user or not comment:
            return {"message": "All fields (video_id, user, comment) are required."}, 400

        comment_data = {
            "id": str(uuid.uuid4()),
            "video_id": video_id,
            "user": user,
            "comment": comment,
            "timestamp": datetime.utcnow().isoformat()
        }

        comments_container.create_item(comment_data)
        return {"message": "Comment added successfully"}, 201

    def get(self):
        """Retrieve comments for a specific video."""
        video_id = request.args.get("video_id")
        if not video_id:
            return {"message": "video_id is required as a query parameter."}, 400

        query = f"SELECT * FROM c WHERE c.video_id = @video_id"
        parameters = [{"name": "@video_id", "value": video_id}]
        comments = list(comments_container.query_items(query=query, parameters=parameters, enable_cross_partition_query=True))

        return {"comments": comments}, 200