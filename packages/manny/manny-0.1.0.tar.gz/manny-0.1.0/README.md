# Manny
Django cli add-on for generating apps, models, serializers, views, urls
## Installation
Install with pip: 
```
$ pip install manny
```
Then add it to your INSTALLED_APPS.
```python
INSTALLED_APPS = (
    ...
    'scaffold',
    ...
)
```
## Usage
To create multiple apps at once, run the following command, where args are future app names:
```python
$ python manage.py scaffold-app app1 app2 ...
```
To create models, serializers, views, urls, run the following command:
```python
$ python manage.py scaffold {app_name} {options}
```
| Option |  |
| ------ | ------ |
| -m, --model {fields} | Add a model with specific fields. Default fields: update_date, create_date|
| -s, --serializers {model_names} | Add a new serializer for the specific model; by default for all models |
| -vi, -views | Add a view for the specific model; by default for all models  |
| -u | Add urls for all models |

To create models, use following syntax:
```python
$ python manage.py scaffold {app_name} -m {model_name} title:Char:255 books:Foreign::CASCADE
```
To specify a field, you must pass the arguments in this order: 
```
NAME:FIELD_TYPE:FIELD_OPTIONS(only required)
```
Field options are optional because there are default values.  
Result:  
```python
class Book(models.Model):
    title = models.CharField(max_length=255)
    books = models.ForeignKey("self", on_delete=models.CASCADE)
    update_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]
```