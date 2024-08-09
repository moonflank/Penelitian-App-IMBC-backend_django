import os
import logging
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
from ultralytics import YOLO
from PIL import Image

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class ImageAnalysisView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        if 'image' not in request.FILES or 'selectedFruit' not in request.data:
            return Response({"error": "No image file or selected fruit provided."}, 
                            status=status.HTTP_400_BAD_REQUEST)

        image = request.FILES['image']
        selected_fruit = request.data['selectedFruit']

        model_paths = {
            'Dragon Fruit': 'models/dragon_fruit_yolo.pt',
            'Papaya': 'models/papaya_yolo.pt',
            'Banana': 'models/banana_yolo.pt',
        }

        if selected_fruit not in model_paths:
            return Response({"error": "Invalid fruit selection."}, status=status.HTTP_400_BAD_REQUEST)

        model_path = model_paths[selected_fruit]
        temp_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        image_path = os.path.join(temp_dir, image.name)
        
        # Ensure the temp directory exists
        os.makedirs(temp_dir, exist_ok=True)
        
        try:
            # Save the image to the specified directory
            with open(image_path, 'wb+') as f:
                for chunk in image.chunks():
                    f.write(chunk)

            # Load YOLO model based on selected fruit
            model = YOLO(model_path)
            
            # Run inference
            results = model(image_path)
            logger.info(f"Results: {results}")

            # Get image dimensions
            with Image.open(image_path) as img:
                image_width, image_height = img.size

            # Process detections
            detections = []
            for result in results:
                if len(result.boxes) == 0:
                    logger.info("No detections found.")
                    continue
                for box in result.boxes:
                    label = model.names[int(box.cls)]
                    confidence = box.conf.item()  # Use .item() to convert single-element tensor to scalar
                    xyxy = box.xyxy.tolist()  # Convert tensor to list
                    detections.append({
                        'label': label,
                        'confidence': confidence,
                        'box': [int(x) for x in xyxy[0]]
                    })

            response_data = {
                "detections": detections,
                "imageWidth": image_width,
                "imageHeight": image_height
            }

            if not detections:
                return Response({"message": "No detections found.", **response_data}, status=status.HTTP_200_OK)
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error during image analysis: {e}")
            return Response({"error": "Something went wrong while analyzing the image."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
