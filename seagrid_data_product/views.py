import json

import grpc
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import DataCatalogAPI_pb2
import DataCatalogAPI_pb2_grpc
from seagrid_data_product.models import SEAGridDataProduct


@csrf_exempt
def create_seagrid_data_product(request):
    # Connect to the gRPC service (DataCatalogAPI gRPC Server)
    channel = grpc.insecure_channel('localhost:6565')
    stub = DataCatalogAPI_pb2_grpc.DataCatalogAPIServiceStub(channel)

    data_product = DataCatalogAPI_pb2.DataProduct()
    seagrid_data_product = create_computational_product(request)

    data_product.data_product_id = seagrid_data_product.data_product_id
    data_product.name = seagrid_data_product.name
    data_product.metadata = seagrid_data_product.metadata

    # Call Data Catalog API
    create_request = DataCatalogAPI_pb2.DataProductCreateRequest()
    create_request.data_product.CopyFrom(data_product)

    create_response = stub.createDataProduct(create_request)
    print(create_response.data_product)

    # Return a response to the client
    return JsonResponse({'data_product_id': create_response.data_product_id}, status=201)


def create_computational_product(request):
    # Get data from request body
    data = json.loads(request.body)

    seagrid_data_product = SEAGridDataProduct(data_product_id=data.get('data_product_id'), name=data.get('name'),
                                              mw=87.0)
    seagrid_data_product.metadata = json.dumps({"mw": seagrid_data_product.mw, "absorb": 834})
    return seagrid_data_product
