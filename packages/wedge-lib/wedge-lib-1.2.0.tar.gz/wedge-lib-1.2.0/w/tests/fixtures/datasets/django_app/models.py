from django.db import models


class Example(models.Model):
    attribute_one = models.CharField(max_length=50)
    attribute_two = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.attribute_one}/{self.attribute_two}"


class InternalDependencyOne(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


class InternalDependencyTwo(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


class ExampleWithInternalDependencies(models.Model):
    name = models.CharField(max_length=50)
    internal_one = models.ForeignKey(InternalDependencyOne, on_delete=models.CASCADE)
    internal_two = models.ForeignKey(InternalDependencyTwo, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.internal_one}/{self.internal_two})"
