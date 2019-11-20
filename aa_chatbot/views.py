import json

from django.shortcuts import render

from rest_framework import (viewsets, mixins, 
                            authentication, status)
from rest_framework.decorators import action
from rest_framework.response import Response

from myportfolioapi.authentication import CsrfExemptSessionAuthentication


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
                return Response({'success': True, 'message': "EVENT RECEIVED"}, 
                        status=status.HTTP_200_OK)
            return Response({'success': True}, status=status.HTTP_200_OK)

        elif request.method == 'GET':
            verify_token = "aaron"
            required_qparams = ['hub.mode', 'hub.verify_token', 'hub.challenge']
            param_keys = request.query_params.keys()

            # compare count required query parameters
            if len(param_keys) != len(required_qparams):
                return Response({
                    'error': "Parameters passed incomplete."
                }, status=status.HTTP_400_BAD_REQUEST)

            # check for query parameter keys
            for query_param in request.query_params.keys():
                if query_param not in required_qparams:
                    return Response({
                        'error': "Parameters passed incomplete."
                    }, status=status.HTTP_400_BAD_REQUEST)

            mode = request.query_params['hub.mode']
            token = request.query_params['hub.verify_token']
            challenge = request.query_params['hub.challenge']

            if mode != 'subscribe' or token != verify_token:
                return Response({'error': "Token does not match."},
                                status=status.HTTP_400_BAD_REQUEST)

            return Response({'challenge': challenge}, status.HTTP_200_OK)

        return Response({
                    'error': "Unknown error occured."
                }, status=status.HTTP_404_NOT_FOUND)

