from django.db import models
import json


class SEAGridDataProduct(models.Model):
    managed = False
    data_product_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    mw = models.CharField(max_length=255)
    metadata = models.TextField()

    def set_json_data(self, data):
        self.metadata = json.dumps(data)

    def get_json_data(self):
        return json.loads(self.metadata)
