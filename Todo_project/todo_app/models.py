from django.db import models

# Create your models here.
class user_registry(models.Model):
    id=models.AutoField(primary_key=True)
    First_name=models.CharField(max_length=200,null=False)
    Last_name=models.CharField(max_length=200,null=False)
    Email=models.CharField(max_length=200,null=False,unique=True)
    Password=models.CharField(max_length=255,null=False)
    created_at=models.DateTimeField()
    class Meta:
        managed=False
        db_table="User_registry"
        
class todo(models.Model):
    id=models.AutoField(primary_key=True)
    user_id=models.ForeignKey(user_registry,on_delete=models.CASCADE,db_column='user_id')
    Title=models.CharField(max_length=200)
    category=models.CharField(max_length=200)
    Descbribe=models.TextField()
    Status=models.CharField(max_length=200)
    class Meta:
        managed=False
        db_table="Todo"
        
class custom_token(models.Model):
    id=models.AutoField(primary_key=True)
    User_id=models.ForeignKey(user_registry,on_delete=models.CASCADE,db_column='User_id')
    Jwt_token=models.CharField(max_length=255)
    Sign_in=models.DateTimeField()
    sign_out=models.DateTimeField()
    class Meta:
        managed=False
        db_table="Custom_token"