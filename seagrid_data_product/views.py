import json

import grpc
import concurrent.futures as futures
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import DataCatalogAPI_pb2
import DataCatalogAPI_pb2_grpc
import ComputationalDataAPI_pb2_grpc
from seagrid_data_product.models import SEAGridDataProduct


@csrf_exempt
def create_seagrid_data_product(request):
    # Connect to the gRPC service (DataCatalogAPI gRPC Server)
    channel = grpc.insecure_channel('localhost:6565')
    stub = DataCatalogAPI_pb2_grpc.DataCatalogAPIServiceStub(channel)

    parent_data_product = DataCatalogAPI_pb2.DataProduct()
    parent_data_product.name = "parent dp"
    parent_dp_result = create_data_product(parent_data_product, stub)

    data_product = DataCatalogAPI_pb2.DataProduct()
    seagrid_data_product = create_computational_product(request)

    # Common data assignments for Computational, Experimental, and Literature Data Products
    data_product.data_product_id = seagrid_data_product.data_product_id
    data_product.name = seagrid_data_product.name
    data_product.metadata = seagrid_data_product.metadata
    data_product.parent_data_product_id = parent_dp_result.data_product_id

    # Call Data Catalog API to create DP
    result_dp = create_data_product(data_product, stub)
    print(result_dp)

    # Return a response to the client
    return JsonResponse({'data_product_id': result_dp.data_product_id}, status=201)


def create_computational_product(request):
    # Get data from request body
    data = json.loads(request.body)

    seagrid_data_product = SEAGridDataProduct(data_product_id=data.get('data_product_id'), name=data.get('name'),
                                              mw=87.0)
    seagrid_data_product.metadata = json.dumps({"mw": seagrid_data_product.mw, "absorb": 834})
    return seagrid_data_product


def create_data_product(data_product, stub):
    create_request = DataCatalogAPI_pb2.DataProductCreateRequest()
    create_request.data_product.CopyFrom(data_product)
    create_response = stub.createDataProduct(create_request)
    return create_response.data_product


class ComputationalDataAPIServer(ComputationalDataAPI_pb2_grpc.ComputationalDataAPIServiceServicer):
    @csrf_exempt
    def createComputationalDataProduct(self, request, context):
        comp_data_product_id = "some_id"
        return ComputationalDataAPI_pb2_grpc.CompDataProductCreateResponse(comp_data_product_id=comp_data_product_id)


server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
ComputationalDataAPI_pb2_grpc.add_ComputationalDataAPIServiceServicer_to_server(
    ComputationalDataAPIServer(), server)
server.add_insecure_port('[::]:50051')
server.start()
