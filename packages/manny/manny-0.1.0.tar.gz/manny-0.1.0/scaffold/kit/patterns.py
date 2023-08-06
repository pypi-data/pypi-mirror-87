FIELD_TEMPLATE = "{{ name }} = models.{{ type|title }}Field()"

DECIMAL_FIELD_TEMPLATE = (
    "{{ name }} = models.{{ type }}Field(max_digits={{ max|default:'5' }}, decimal_places={{ "
    "places|default:'2' }}) "
)

CHAR_FIELD_TEMPLATE = (
    "{{ name }} = models.{{ type }}Field(max_length={{max|default:'255'}})"
)

FOREIGN_KEY_TEMPLATE = (
    "{{ name }} = models.{{ type }}Key({{ model|default:\"'self'\" }}, on_delete=models.{{ "
    'delete|default:"CASCADE" }}) '
)

ONE_TO_ONE_FIELD_TEMPLATE = (
    "{{ name }} = models.{{ type }}Field({{ model|default:\"'self'\" }}, on_delete=models.{{ "
    'delete|default:"CASCADE" }}) '
)

MANY_TO_MANY_FIELD_TEMPLATE = (
    "{{ name }} = models.{{ type }}Field({{ model|default:\"'self'\" }})"
)

MODEL_TEMPLATE = """
class {{ name }}(models.Model):{% for field in fields %}
    {{field}} {% endfor %}
    update_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-id']
"""

SERIALIZER_TEMPLATE = """{% for key, value  in imports.items %}from {{ key }} import {{ value|join:", " }} 
{% endfor %}
{% for model in models %}
class {{ model }}Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.{{ model }}
        fields = '__all__'
        
{% endfor %}
"""

VIEW_SET_URL_TEMPLATE = """from rest_framework.routers import SimpleRouter
from {{ app }} import views


router = SimpleRouter()
{% for model in models %}
router.register(r'{{ model | lower }}', views.{{ model }}ViewSet, '{{model}}'){% endfor %}
urlpatterns = router.urls
"""

VIEW_SET_VIEW_TEMPLATE = """{% for key, value  in imports.items %}from {{ key }} import {{ value|join:", " }} 
{% endfor %}
{% for model in models %}
class {{ model }}ViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = models.{{ model }}.objects.order_by('pk')
        serializer = serializers.{{ model }}Serializer(queryset, many=True)
        return response.Response(serializer.data)
    
    def create(self, request):
        serializer = serializers.{{ model }}Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=201)
        return response.Response(serializer.errors, status=400)
    
    def retrieve(self, request, pk=None):
        queryset = models.{{ model }}.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = serializers.{{ model }}Serializer(item)
        return response.Response(serializer.data)
    
    def update(self, request, pk=None):
        try:
            item = models.{{ model }}.objects.get(pk=pk)
        except models.{{ model }}.DoesNotExist:
            return response.Response(status=404)
        serializer = serializers.{{ model }}Serializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors, status=400)
    
    def destroy(self, request, pk=None):
        try:
            item = models.{{ model }}.objects.get(pk=pk)
        except models.{{ model }}.DoesNotExist:
            return response.Response(status=404)
        item.delete()
        return response.Response(status=204)
        
{% endfor %}
"""
