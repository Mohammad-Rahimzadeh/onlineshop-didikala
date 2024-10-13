from rest_framework import serializers
from django.conf import settings
from app_blog.models import Blog , BlogCategory , BlogContent





class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ['id', 'title']



class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ['title', 'slug' , 'is_available']





# ===============================================================================================================
# ===============================================================================================================
# ===============================================================================================================



class BlogContentSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        if obj.image:
            return settings.DOMAIN + obj.image.url
        return None

    class Meta:
        model = BlogContent
        fields = ['sub_title', 'description', 'image_url']



class BlogContentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogContent
        fields = ['product' , 'sub_title' , 'description' , 'image']




# ===============================================================================================================
# ===============================================================================================================
# ===============================================================================================================



class BlogSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    blogcontents = BlogContentSerializer(many=True)

    def get_category(self, obj):
        return CategorySerializer(obj.category.all(), many=True).data
    
    thumbnail_url = serializers.SerializerMethodField()
    def get_thumbnail_url(self, obj):
        if obj.thumbnail:
            return settings.DOMAIN + obj.thumbnail.url
        return None
    
    author_username = serializers.SerializerMethodField()
    def get_author_username(self, obj):
        if obj.author:
            return obj.author.username
        return None

    class Meta:
        model = Blog
        fields = ['id' , 'author_username', 'category', 'title' , 'visit_count', 'thumbnail_url' , 'blogcontents' , 'created_date' , 'is_published' , 'rate']




class BlogCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['author', 'category', 'title' , 'slug' , 'is_published' , 'thumbnail' , 'rate']




class BlogUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['author', 'category', 'title' , 'slug' , 'is_published' , 'thumbnail' , 'rate']