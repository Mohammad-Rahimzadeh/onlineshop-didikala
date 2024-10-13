from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from app_blog.models import Blog , BlogCategory , BlogContent
from app_blog.api import serializers





@api_view(['GET'])
def blogcategoryListView(request):
    blog_categor_list = BlogCategory.objects.all()

    if blog_categor_list:
        data = serializers.CategorySerializer(blog_categor_list, many=True).data
        return Response(data , status=status.HTTP_200_OK)
    else:
        return Response({'massage':'0 category'} , status=status.HTTP_204_NO_CONTENT)
    



class BlogCategoryCreateSerializer(generics.CreateAPIView):
    queryset = BlogCategory.objects.all()
    serializer_class = serializers.CategoryCreateSerializer
    permission_classes = [IsAuthenticated] 



# ========================================================================================================================
# ========================================================================================================================
# ========================================================================================================================



@api_view(['GET'])
def blogListView(request):
    blog_list = Blog.objects.all()

    if blog_list:
        data = serializers.BlogSerializer(blog_list, many=True).data
        return Response(data , status=status.HTTP_200_OK)
    else:
        return Response({'massage':'0 blog'} , status=status.HTTP_204_NO_CONTENT)




@api_view(['GET'])
def blogDetailView(request , id):
    try:
        blog = Blog.objects.get(id=id)

        if blog:
            blog.visit_count += 1
            blog.save()
            data = serializers.BlogSerializer(blog).data
            return Response(data , status=status.HTTP_200_OK)
        else:
            return Response({'massage':'blog not found!'} , status=status.HTTP_204_NO_CONTENT)
    except:
        return Response({'massage':'unknown id'} , status=status.HTTP_404_NOT_FOUND)




@api_view(['DELETE'])
def blogDeleteView(request):
    pk = request.POST.get('pk', None)

    if pk is not None:
        try:
            blog = Blog.objects.get(id=pk)
            blog.delete()
            return Response({'message': 'Deleted successfully!'}, status.HTTP_204_NO_CONTENT)
        except (ValueError, Blog.DoesNotExist) as err:
            return Response({'message': str(err)}, status.HTTP_400_BAD_REQUEST)
        
    return Response({'message': 'pk required!'}, status.HTTP_400_BAD_REQUEST)




class blogCreateView(generics.CreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = serializers.BlogCreateSerializer
    permission_classes = [IsAuthenticated] 




class blogUpdateView(generics.UpdateAPIView):
    queryset = Blog.objects.all()
    serializer_class = serializers.BlogUpdateSerializer





# ========================================================================================================================
# ========================================================================================================================
# ========================================================================================================================


class blogContentCreateView(generics.CreateAPIView):
    queryset = BlogContent.objects.all()
    serializer_class = serializers.BlogContentCreateSerializer
    permission_classes = [IsAuthenticated] 