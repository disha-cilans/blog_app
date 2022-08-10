from gc import get_objects
from django.http import Http404
from rest_framework.views import APIView
from blogs.models import Blog
from blogs.serializers import BlogSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'blogs': reverse('blog-list', request=request, format=format)
    })

class BlogList(APIView):
    """
    List all snippets, or create a new blogs.
    """
    def get(self,request,format = None):
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs,many=True)
        return Response(serializer.data)

    def post(self,request,format = None):
        serializer = BlogSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class BlogDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get_object(self,pk):
        try:
            return Blog.objects.get(pk=pk)
        except Blog.DoesNotExist:
            raise Http404
    
    def get(self,request,pk,format = None):
        blog = self.get_object(pk)
        serializer = BlogSerializer(blog)
        return Response(serializer.data)

    def post(self,request,pk,format = None):
        blog =  self.get_object(pk)
        serializer = BlogSerializer(blog , data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk,format=None):
        blog = self.get_object(pk)
        blog.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)



