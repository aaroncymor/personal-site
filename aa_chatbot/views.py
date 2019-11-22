import json
import logging

from django.shortcuts import render

from rest_framework import (viewsets, mixins, 
                            authentication, status)
from rest_framework.decorators import action
from rest_framework.response import Response

from myportfolioapi.authentication import CsrfExemptSessionAuthentication

logger = logging.getLogger(__name__)

# Create your views here.
class FacebookChatbotViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['GET', 'POST'], 
    authentication_classes=())
    def webhook(self, request, pk=None, *args, **kwargs):
        if request.method == 'POST':
            _data = request.data.copy()
            
            if 'body' not in _data:
                return Response({
                    'error': "The 'body' parameter is required."
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                # if body is not a dictionary, we load it with json
                body = _data['body']
            except Exception:
                body = json.loads(_data['body'])
            
            if 'object' not in body:
                return Response({'error': "Key 'object' not found in body."},
                            status=status.HTTP_400_BAD_REQUEST)
            obj = body['object']
            
            if 'entry' not in body:
                return Response({'error': "Key 'entry' not found in body."},
                            status=status.HTTP_400_BAD_REQUEST)
            entries = body['entry']
            if not isinstance(entries, list):
                return Response({'error': "Entries not an instance of list."},
                                status=status.HTTP_400_BAD_REQUEST)

            if obj == 'page':
                for entry in entries: 
                    if not isinstance(entry, dict):
                        return Response({'error': "Entry not an instance of dictionary."},
                                        status=status.HTTP_400_BAD_REQUEST)

                    try:
                        print("Entry", entry)
                        messaging = entry['messaging']
                        if not isinstance(messaging, list):
                            return Resonse({'error': "Entry messaging not a list."},
                                    status=status.HTTP_400_BAD_REQUEST)
                        try:  
                            print("Messaging first index", entry['messaging'][0])
                        except IndexError:
                            print("Entry messaging is empty")
                    except KeyError:
                        print("No 'messaging' key for this entry.")

                return Response("EVENT RECEIVED", status=status.HTTP_200_OK,
                                content_type="text/html")
            
            return Response(None, status=status.HTTP_403_FORBIDDEN)

        elif request.method == 'GET':
            verify_token = "C75D9C4588648645EDBF24987D32713368806AB2"
            
            mode = request.query_params.get('hub.mode', None)
            token = request.query_params.get('hub.verify_token', None)
            challenge = request.query_params.get('hub.challenge')

            if token and verify_token == token:
                return Response(challenge, status=status.HTTP_200_OK, 
                                content_type="text/html")
     
        return Response({
                    'error': "Access to this service not allowed."
                }, status=status.HTTP_403_FORBIDDEN)

