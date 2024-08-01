
import json
import logging
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status, exceptions
from rest_framework.response import Response
from Store.models import DMStore
from utils.generic import caching_key,update_key
from Layout.models import (CategoryLayoutMapping, Layout,ProductTypeLayoutMapping,
                          ProductLayoutMapping)
from Layout.v2.layout_serializer import (CategoryMappingSerializer,
                                        LayoutSerializer,
                                        LayoutUpdateSerializer,
                                        ProductMappingSerializer,
                                        ProductTypeMappingSerializer)
from utils.auth import validate_authorized_to_accesstoken, validate_token_using_introspect
from utils.global_serializers import (BadRequest_400, Conflict_409,
                                      InternalServerError_500,
                                      NoDetailsFound_204, NotFound_404,
                                      Unauthorised_401)
from utils.logger import api_debug_logs, api_error_logs
from product_management_services.settings import client

with open('config/logger.json', encoding="utf-8") as json_config:
    config_data = json.load(json_config)
    log_level = config_data['LOG_LEVEL']
LOGGER = logging.getLogger(log_level)


class LayoutAPIView(generics.GenericAPIView):
    '''
        class for the Layout
    '''
    layout_id = openapi.Parameter('layout_id',
                                 in_=openapi.IN_QUERY,
                                 type=openapi.TYPE_INTEGER,
                                 required=False
                                 )
    page_number = openapi.Parameter('page-number',
                                    in_=openapi.IN_QUERY,
                                    type=openapi.TYPE_INTEGER,
                                    default=1,
        description="This is used to retrieve list of data for a specific page number")
    page_limit = openapi.Parameter('page-limit',
                                   in_=openapi.IN_QUERY,
                                   type=openapi.TYPE_INTEGER,
                                   minimum=1,
                                   exclusiveMinimum=True,
                                   default=20,
            description="This is used to retrieve the number of data per page")
    
    serializer_class = LayoutSerializer
    #Create
    @method_decorator(validate_token_using_introspect('create-layout'), name='dispatch')
    @swagger_auto_schema(auto_schema = None)
        # tags=['Layout'],
        #                  operation_id='create-layout',
        #                  request_body=LayoutSerializer,
        #                  responses={
        # 201: openapi.Response("Success", LayoutSerializer),
        # 409: openapi.Response("Already Exists", Conflict_409),
        # 400: openapi.Response("Bad Request", BadRequest_400),
        # 401: openapi.Response("Unauthorized", Unauthorised_401),
        # 404: openapi.Response("Not Found", NotFound_404),
        # 500: openapi.Response("Internal Server Error", InternalServerError_500),
        # 204: openapi.Response("No Details Found", NoDetailsFound_204)})
    def post(self,request):
        '''
            Create layout

            This is used for the layout of the product
        '''
        try:
            user_id = request.data.get('user')
            serializer = LayoutSerializer(data=request.data)
            store_id = request.data.get('store')
            name = request.data.get('name').strip()
            description = request.data.get('description')
            display_name = request.data.get('display_name')
            statuss = request.data.get('status')
            if statuss is None:
                statuss = 1
            type = request.data.get('type')

            store_obj = DMStore.validate_store(store_id)
            api_debug_logs(request, message="Validating store_id "+str(store_id))
            if store_obj:
                if serializer.is_valid():
                    if Layout.objects.filter(name=name,store_id=store_id).exists():
                        result = {"message": "Name already exists"}
                        api_debug_logs(request,message="Store already exists with name= "+str(name))
                        return Response(result, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        layout_obj = Layout.objects.create(store_id=store_id,
                                                        name=name, description=description,display_name=display_name, status=statuss,
                                                        type=type,
                                                        created_by=user_id)
                        api_debug_logs(request, message="layout obj is created "+str(layout_obj))
                        layout_obj.save()
                        result = {
                            "id":layout_obj.id,
                            "store_id":store_id,
                            "name":layout_obj.name,
                            "description":layout_obj.description,
                            'display_name':layout_obj.display_name,
                            "status":layout_obj.status,
                            "type":layout_obj.type
                        }
                        #cache_update = update_key('list-of-layout')
                        return Response(result, status=status.HTTP_201_CREATED)     
                else:
                    result = serializer.errors
                    api_debug_logs(request, message="Serilaizer Error "+str(result))
                    return Response(result, status=status.HTTP_400_BAD_REQUEST)        
        except Exception as ex:
            api_error_logs(
                request=request,
                error=ex,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
            return Response({"message": str(ex)},
                            status=status.HTTP_400_BAD_REQUEST)
        except DMStore.DoesNotExist:
            return Response({'message': "Store_id Does not Exist."},
                            status=status.HTTP_400_BAD_REQUEST)

#retrive
    @method_decorator(validate_token_using_introspect('list-of-layout'), name='dispatch')
    #@method_decorator(caching_key('list-of-layout'))
    @swagger_auto_schema(auto_schema = None)
        # tags=['Layout'],
        #                  operation_id='list-of-layout',
        #                  manual_parameters=[layout_id,page_number,page_limit],
        #                  responses={
        #                      200: openapi.Response("Success",),
        #                      409: openapi.Response("Already Exists", Conflict_409),
        #                      400: openapi.Response("Bad Request", BadRequest_400),
        #                      401: openapi.Response("Unauthorized", Unauthorised_401),
        #                      404: openapi.Response("Not Found", NotFound_404),
        #                      500: openapi.Response("Internal Server Error", InternalServerError_500),
        #                      204: openapi.Response("No Details Found", NoDetailsFound_204)})
    def get(self, request):
        '''
            API to list all Layout

            This method is used to retrive all the layout.
        '''
        try:
            page = self.request.GET.get('page-number', 1)
            limit = self.request.GET.get('page-limit', 20)
            store_id = request.data.get('store')
            layout_id = self.request.GET.get('layout_id')
            queryset = Layout.objects.filter(store_id=store_id)
            count = queryset.count()
            if store_id:
                if isinstance(store_id,int):
                    pass
                else:
                    result = ({"message": 'The provided Store ID is invalid'})
                    return Response(result, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "store_id not in token"},status=status.HTTP_400_BAD_REQUEST)                
            
            if layout_id is not None:
                queryset=queryset.filter(id=layout_id).values()
                api_debug_logs(request, message="Data is retrived for the layout_id "+str(layout_id))

            
            response = get_response_structurelay(store_id=store_id,
                data=queryset,page=page,limit=limit,count=count)
            #client.set((request.data.get('cache_key')),json.dumps(response))
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            api_error_logs(
                request=request,
                error=ex,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
            return Response({"message": str(ex)},
                            status=status.HTTP_400_BAD_REQUEST)
#update
    def get_object(self, layout_id):
        try:
            return Layout.objects.get(id = layout_id)
        except Layout.DoesNotExist:
            return None
    @method_decorator(validate_token_using_introspect('update-layout'), name='dispatch')
    @swagger_auto_schema(auto_schema = None)
        # tags=['Layout'],
        # operation_id='update-layout',
        # manual_parameters=[layout_id],
        # request_body=LayoutUpdateSerializer,
        # responses={
        #     200: openapi.Response("Success",LayoutUpdateSerializer),
        #     409: openapi.Response("Already Exists",Conflict_409),
        #     400: openapi.Response("Bad Request",BadRequest_400),
        #     401: openapi.Response("Unauthorized",Unauthorised_401),
        #     404: openapi.Response("Not Found",NotFound_404),
        #     500: openapi.Response("Internal Server Error",InternalServerError_500),
        #     204: openapi.Response("No Details Found",NoDetailsFound_204)})
    def put(self, request):
        '''
            API to update the Layout

            This method is used to update the Layout
        '''
        try:
            serializer = LayoutUpdateSerializer(data = request.data)
            layout_id = self.request.GET.get('layout_id')
            layout = Layout.objects.get(id=layout_id )
            if not layout:
                return Response({"message":"object with layout_id doesnot exist"},
                status=status.HTTP_404_NOT_FOUND)
            store = request.data.get('store')
            name = request.data.get('name')
            description = request.data.get('description')
            display_name = request.data.get('display_name')
            statuss = request.data.get('status')
            if statuss is None:
                statuss = 1
            type = request.data.get('type')
            lay_obj = Layout.objects.filter(id = layout_id)
            if serializer.is_valid():
                if lay_obj:
                        if DMStore.validate_store(store):
                            api_debug_logs(request, message="Store_id is validate ")
                            lay_obj = Layout.objects.filter(id = layout_id).last()
                            if Layout.objects.filter(name=name,store_id=store).exclude(id = lay_obj.id).exists():
                                result = {"message": "Name already exists"}
                                api_debug_logs(request,message="Store already exists with name= "+str(name))
                                return Response(result, status=status.HTTP_400_BAD_REQUEST)    
                            else:
                                lay_obj.name=name
                                lay_obj.description=description
                                lay_obj.display_name=display_name
                                lay_obj.status=statuss
                                lay_obj.type=type
                                lay_obj.store_id = store
                                lay_obj.save()
                                result={"message":'Data updated successfully'}
                                #cache_update = update_key('list-of-layout')
                                return Response(result, status=status.HTTP_200_OK)
                        else:
                            api_debug_logs(request, message="Store_id does not exist")
                            result = ({'message': "store_id Doesn't exist"})
                            return Response(result, status=status.HTTP_400_BAD_REQUEST)
                else:
                    result = ({'message': "Object with id Doesn't exist"})
                    return Response(result, status=status.HTTP_400_BAD_REQUEST)
            result = serializer.errors
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        except Layout.DoesNotExist:
            result={'message':'Layout object does not exist'}
            return Response(result,status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            api_error_logs(
                request=request,
                error=ex,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
            return Response({"message": str(ex)},
                            status=status.HTTP_400_BAD_REQUEST)
#delete  
    @method_decorator(validate_token_using_introspect('delete-layout'), name='dispatch')                                  
    @swagger_auto_schema(auto_schema = None)
        # tags=['Layout'],
        # operation_id='delete-layout',
        # manual_parameters=[layout_id],
        # responses={
        #     200: openapi.Response("Success",),
        #     409: openapi.Response("Already Exists", Conflict_409),
        #     400: openapi.Response("Bad Request", BadRequest_400),
        #     401: openapi.Response("Unauthorized", Unauthorised_401),
        #     404: openapi.Response("Not Found", NotFound_404),
        #     500: openapi.Response("Internal Server Error",
        #                           InternalServerError_500),
        #     204: openapi.Response("No Details Found", NoDetailsFound_204)})
    def delete(self, request):
        '''
            API to delete-Layout

            This api is used to delete the Layout Data

        '''
        try:
            
            layout_id = self.request.GET.get('layout_id')
            layout_obj = Layout.objects.get(id=layout_id)
            layout_obj.delete()
            #cache_update = update_key('list-of-layout')
            api_debug_logs(request, message="Delete successfully mapping_id "+str(layout_id))
            return Response({"message": "Delete Successfully"},
                            status=status.HTTP_202_ACCEPTED)
        except Layout.DoesNotExist:
            return Response({'message': "layout_id Does not Exist."},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response({'message': "Internal server error"},
                            status=status.HTTP_400_BAD_REQUEST)


class ProductLayoutMappingAPIView(generics.GenericAPIView):
    '''class for the ProductlayourMapping'''
    serializer_class = ProductMappingSerializer

    layout_id = openapi.Parameter('layout_id',
                                 in_=openapi.IN_QUERY,
                                 type=openapi.TYPE_INTEGER,
                                 required=False)
    product_id = openapi.Parameter('product_id',
                                 in_=openapi.IN_QUERY,
                                 type=openapi.TYPE_INTEGER,
                                 required=False)
    mapping_id = openapi.Parameter('mapping_id',
                                        in_=openapi.IN_QUERY,
                                        type=openapi.TYPE_INTEGER,
                                        required=True)
    page_number = openapi.Parameter(
        'page-number',
        in_=openapi.IN_QUERY,
        type=openapi.TYPE_INTEGER,
        minimum=1,
        exclusiveMinimum=True,
        description="This is used to retrieve the number of data per page")
    page_limit = openapi.Parameter(
        'page-limit',
        in_=openapi.IN_QUERY,
        type=openapi.TYPE_INTEGER,
        minimum=1,
        exclusiveMinimum=True,
        description="This is used to retrieve list of data for a specific page number")
#get
    @method_decorator(validate_token_using_introspect('list-product-layout'), name='dispatch')
    #@method_decorator(caching_key('list-product-layout'))
    @swagger_auto_schema(auto_schema = None)
        # tags=['Layout'],
        #                  operation_id='list-product-layout',
        #                  manual_parameters=[layout_id, product_id, page_number,page_limit],
        #                  responses={
        #                      200: openapi.Response("Success",ProductMappingSerializer),
        #                      409: openapi.Response("Already Exists", Conflict_409),
        #                      400: openapi.Response("Bad Request", BadRequest_400),
        #                      401: openapi.Response("Unauthorized", Unauthorised_401),
        #                      404: openapi.Response("Not Found", NotFound_404),
        #                      500: openapi.Response("Internal Server Error", InternalServerError_500),
        #                      204: openapi.Response("No Details Found", NoDetailsFound_204)})
    def get(self, request):
        '''
           List of all the Product Layout Mapping 

           This API lists all the Product Layout Mapping
        '''

        try:
            page = self.request.GET.get('page-number', 1)
            limit = self.request.GET.get('page-limit', 20)
            layout_id = self.request.GET.get('layout_id')
            product_id = self.request.GET.get('product_id')
            queryset = ProductLayoutMapping.objects.all().values('id', 'layout_id', 'product_id')
            count = len(queryset)
            api_debug_logs(request, message="Data is retrived")
            if layout_id is not None:
                queryset=queryset.filter(layout_id_id=layout_id).values('id', 'layout_id', 'product_id')
                api_debug_logs(request, message="Data is retrived for the layout_id "+str(layout_id))

            if product_id is not None:
                queryset=queryset.filter(product_id_id=product_id).values('id', 'layout_id', 'product_id')

            response = get_response_structure2(
                data=queryset,page=page,limit=limit,count=count)
            #client.set((request.data.get('cache_key')),json.dumps(response))
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            api_error_logs(
                request=request,
                error=ex,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
            return Response({"message": str(ex)},
                            status=status.HTTP_400_BAD_REQUEST)
#Post 
    @method_decorator(validate_token_using_introspect('create-product-layout-mapping'), name='dispatch')  
    @swagger_auto_schema(auto_schema = None)
        # tags=['Layout'],
        #                  operation_id='create-product-layout-mapping',
        #                  manual_parameters=[],
        #                  responses={
        # 200: openapi.Response("Success", ProductMappingSerializer),
        # 409: openapi.Response("Already Exists", Conflict_409),
        # 400: openapi.Response("Bad Request", BadRequest_400),
        # 401: openapi.Response("Unauthorized", Unauthorised_401),
        # 404: openapi.Response("Not Found", NotFound_404),
        # 500: openapi.Response("Internal Server Error", InternalServerError_500),
        # 204: openapi.Response("No Details Found", NoDetailsFound_204)})
    def post(self,request):
        '''
            Create Product Layout  

            This is used for the create Product Layout
        '''
        try:
            user_id = request.data.get('user')
            serializer = ProductMappingSerializer(data=request.data)
            product_id = request.data.get('product_id')
            layout_id = request.data.get('layout_id')
            if ProductLayoutMapping.objects.filter(product_id_id = product_id,layout_id_id=layout_id):
                return Response({"message":"This product has been associated to the same layout"},status=status.HTTP_400_BAD_REQUEST)
            if serializer.is_valid():
                if not ProductLayoutMapping.objects.filter(product_id_id = product_id):
                    api_debug_logs(request, message="Unique Mapping Validated")
                    if Layout.objects.filter(id=layout_id,type='detailspage').exists():
                        api_debug_logs(request, message="Layout Type  Validated")
                        serializer.save(created_by=user_id)
                        result = serializer.data
                        #cache_update = update_key('list-product-layout')
                        return Response(result, status=status.HTTP_201_CREATED)
                    result= {"message":'Layout must belong to detailspage type'}
                    return Response(result, status=status.HTTP_400_BAD_REQUEST)
                cache_update = update_key('get-all-published-products')
                cache_update = update_key('get-all-published-products-with-version-number')
                cache_update = update_key('products-description')
                result= {"message":'Layout Mapping Already exits for Product'}
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
            else:
                result = serializer.errors
                return Response(result, status=status.HTTP_400_BAD_REQUEST)        
        except Exception as ex:
            api_error_logs(
                request=request,
                error=ex,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
            return Response({"message": str(ex)},
                            status=status.HTTP_400_BAD_REQUEST) 
    @method_decorator(validate_token_using_introspect('update-product-layout-mapping'), name='dispatch')
    @swagger_auto_schema(auto_schema = None)
        # tags=['Layout'],
        #                  operation_id='update-product-layout-mapping',
        #                  manual_parameters = [mapping_id],
        #                  responses={
        # 200: openapi.Response("Success",ProductTypeMappingSerializer),
        # 409: openapi.Response("Already Exists", Conflict_409),
        # 400: openapi.Response("Bad Request", BadRequest_400),
        # 401: openapi.Response("Unauthorized", Unauthorised_401),
        # 404: openapi.Response("Not Found", NotFound_404),
        # 500: openapi.Response("Internal Server Error", InternalServerError_500),
        # 204: openapi.Response("No Details Found", NoDetailsFound_204)})
    def put(self,request):
        '''
            Update Product Type Layout

            This is used for the Update Product Layout
        '''
        try:
            mapping_id = self.request.GET.get('mapping_id')
            product_id = request.data.get('product_id')
            layout_id = request.data.get('layout_id')
            if ProductLayoutMapping.objects.filter(product_id_id = product_id,layout_id_id=layout_id):
                return Response({"message":"This product has been associated to the same layout"},status=status.HTTP_400_BAD_REQUEST)
            serializer = ProductMappingSerializer(data=request.data)
            if serializer.is_valid():
                if not ProductLayoutMapping.objects.filter(id = mapping_id,
                                                           product_id_id=product_id):
                    result= {"message":"Product mapping with product id = "+str(product_id)+" does not exists"}
                    return Response(result, status=status.HTTP_400_BAD_REQUEST)
                obj = ProductLayoutMapping.objects.filter(id = mapping_id)
                etc = obj[0].layout_id
                if Layout.objects.filter(id=layout_id,type='detailspage').exists():
                    if layout_id != etc:
                        obj.update(product_id_id = product_id, layout_id_id = layout_id)
                        typeobj = obj.values('id', 'product_id', 'layout_id')
                        #cache_update = update_key('list-product-layout')
                        cache_update = update_key('get-all-published-products')
                        cache_update = update_key('get-all-published-products-with-version-number')
                        cache_update = update_key('products-description')
                        return Response(typeobj, status=status.HTTP_200_OK)
                    result= {"message":'Product Type mapping with same layout exists'}
                    return Response(result, status=status.HTTP_400_BAD_REQUEST)
                result= {"message":'Layout must belong to detailspage type'}
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
            else:
                result = serializer.errors
                return Response(result, status=status.HTTP_400_BAD_REQUEST)        
        except Exception as ex:
            api_error_logs(
                request=request,
                error=ex,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
            return Response({"message": str(ex)},
                            status=status.HTTP_400_BAD_REQUEST)

    #delete                                   
    @method_decorator(validate_token_using_introspect('delete-product-mapping-id'), name='dispatch')
    @swagger_auto_schema(auto_schema = None)
        # tags=['Layout'],
        # operation_id='delete-product-mapping-id',
        # manual_parameters=[mapping_id],
        # responses={
        #     200: openapi.Response("Success",),
        #     409: openapi.Response("Already Exists", Conflict_409),
        #     400: openapi.Response("Bad Request", BadRequest_400),
        #     401: openapi.Response("Unauthorized", Unauthorised_401),
        #     404: openapi.Response("Not Found", NotFound_404),
        #     500: openapi.Response("Internal Server Error",
        #                           InternalServerError_500),
        #     204: openapi.Response("No Details Found", NoDetailsFound_204)})
    def delete(self, request):
        '''
            API to delete Product Layout Mapping

            This api is used to delete the Product Layout Mapping Id

        '''
        try:
            
            mapping_id = self.request.GET.get('mapping_id')
            mapping_obj = ProductLayoutMapping.objects.get(id=mapping_id)
            mapping_obj.delete()
            api_debug_logs(request, message="Deleted mapping_id "+str(mapping_id))
            #cache_update = update_key('list-product-layout')
            cache_update = update_key('get-all-published-products')
            cache_update = update_key('get-all-published-products-with-version-number')
            cache_update = update_key('products-description')
            return Response({"message": "Delete Successfully"},
                            status=status.HTTP_202_ACCEPTED)
        except ProductLayoutMapping.DoesNotExist:
            api_debug_logs(request, message="mapping_id is does not exist"+str(mapping_id))
            return Response({'message': "ProductLayoutMapping_id Does not Exist."},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response({'message': "Internal server error"},
                            status=status.HTTP_400_BAD_REQUEST)

#CategoryMapping
class CategoryLayoutMappingAPIView(generics.GenericAPIView):
    '''class for the CategorylayourMapping'''
    serializer_class = CategoryMappingSerializer

    mapping_id = openapi.Parameter('mapping_id',
                                        in_=openapi.IN_QUERY,
                                        type=openapi.TYPE_INTEGER,
                                        required=True)
    category_id = openapi.Parameter('category_id',
                                 in_=openapi.IN_QUERY,
                                 type=openapi.TYPE_INTEGER,
                                 required=False
                                 )
    layout_id = openapi.Parameter('layout_id',
                                 in_=openapi.IN_QUERY,
                                 type=openapi.TYPE_INTEGER,
                                 required=False)
    page_number = openapi.Parameter(
                                    'page-number',
                                    in_=openapi.IN_QUERY,
                                    type=openapi.TYPE_INTEGER,
                                    minimum=1,
                                    exclusiveMinimum=True,
                                    description="This is used to retrieve the number of data per page")
    page_limit = openapi.Parameter(
                                'page-limit',
                                in_=openapi.IN_QUERY,
                                type=openapi.TYPE_INTEGER,
                                minimum=1,
                                exclusiveMinimum=True,
                                description="This is used to retrieve list of data for a specific page number")
#get
    @method_decorator(validate_token_using_introspect('list-category-layout'), name='dispatch')
    #@method_decorator(caching_key('list-category-layout'))
    @swagger_auto_schema(auto_schema = None)
        # tags=['Layout'],
        #                  operation_id='list-category-layout',
        #                  manual_parameters=[layout_id, category_id, page_number,page_limit],
        #                  responses={
        #                      200: openapi.Response("Success",CategoryMappingSerializer),
        #                      409: openapi.Response("Already Exists", Conflict_409),
        #                      400: openapi.Response("Bad Request", BadRequest_400),
        #                      401: openapi.Response("Unauthorized", Unauthorised_401),
        #                      404: openapi.Response("Not Found", NotFound_404),
        #                      500: openapi.Response("Internal Server Error", InternalServerError_500),
        #                      204: openapi.Response("No Details Found", NoDetailsFound_204)})
    def get(self, request):
        '''
           List of all the Category Layout Mapping 

           This API lists all the Category Layout Mapping
        '''
        try:
            page = self.request.GET.get('page-number', 1)
            limit = self.request.GET.get('page-limit', 20)
            layout_id = self.request.GET.get('layout_id')
            category_id = self.request.GET.get('category_id')
            queryset = CategoryLayoutMapping.objects.all().values('id', 'layout_id', 'category_id')
            count = len(queryset)
            api_debug_logs(request, message="Data is retrived")    
            
            if layout_id is not None:
                queryset=queryset.filter(layout_id_id=layout_id).values('id', 'layout_id', 'category_id')
                api_debug_logs(request, message="Data is retrived for the layout_id "+str(layout_id))

            if category_id is not None:
                queryset=queryset.filter(category_id_id=category_id).values('id', 'layout_id', 'category_id')

            response = get_response_structure1(
                data=queryset,page=page,limit=limit,count=count)
            #client.set((request.data.get('cache_key')),json.dumps(response))
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            api_error_logs(
                request=request,
                error=ex,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
            return Response({"message": str(ex)},
                            status=status.HTTP_400_BAD_REQUEST)
#Post   
    @method_decorator(validate_token_using_introspect('create-category-layout-mapping'), name='dispatch')
    @swagger_auto_schema(auto_schema = None)
        # tags=['Layout'],
        #                  operation_id='create-category-layout-mapping',
        #                  responses={
        # 200: openapi.Response("Success", CategoryMappingSerializer),
        # 409: openapi.Response("Already Exists", Conflict_409),
        # 400: openapi.Response("Bad Request", BadRequest_400),
        # 401: openapi.Response("Unauthorized", Unauthorised_401),
        # 404: openapi.Response("Not Found", NotFound_404),
        # 500: openapi.Response("Internal Server Error", InternalServerError_500),
        # 204: openapi.Response("No Details Found", NoDetailsFound_204)})
    def post(self,request):
        '''
            Create Category Layout

            This is used for the create Category Layout
        '''
        try:
            user_id = request.data.get('user')
            category_id = request.data.get('category_id')
            layout_id = request.data.get('layout_id')
            serializer = CategoryMappingSerializer(data=request.data)
            if CategoryLayoutMapping.objects.filter(category_id_id = category_id,layout_id_id=layout_id):
                return Response({"message":"This category has been associated to the same layout"},status=status.HTTP_400_BAD_REQUEST)
            if serializer.is_valid():
                if not CategoryLayoutMapping.objects.filter(
                    category_id_id=category_id):
                    api_debug_logs(request, message="Unique Mapping Validated")
                    if Layout.objects.filter(id=layout_id,type='listpage').exists():
                        api_debug_logs(request, message="Layout Type  Validated")
                        serializer.save(created_by=user_id)
                        result = serializer.data
                        #cache_update = update_key('list-category-layout')
                        cache_update = update_key('products-description')
                        cache_update = update_key('list-category-DisplayName')
                        cache_update = update_key('get_categories_values')
                        cache_update = update_key('get_children_categories')
                        return Response(result, status=status.HTTP_201_CREATED)
                    result= {"message":'Layout must belong to listpage type'}
                    return Response(result, status=status.HTTP_400_BAD_REQUEST)
                result= {"message":'Layout Mapping Already exits for Category '+str(category_id)}
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
            else:
                result = serializer.errors
                return Response(result, status=status.HTTP_400_BAD_REQUEST)        
        except Exception as ex:
            api_error_logs(
                request=request,
                error=ex,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
            return Response({"message": str(ex)},
                            status=status.HTTP_400_BAD_REQUEST)
    @method_decorator(validate_token_using_introspect('update-category-layout-mapping'), name='dispatch')
    @swagger_auto_schema(auto_schema = None)
        # tags=['Layout'],
        #                  operation_id='update-category-layout-mapping',
        #                  manual_parameters = [mapping_id],
        #                  responses={
        # 200: openapi.Response("Success",ProductTypeMappingSerializer),
        # 409: openapi.Response("Already Exists", Conflict_409),
        # 400: openapi.Response("Bad Request", BadRequest_400),
        # 401: openapi.Response("Unauthorized", Unauthorised_401),
        # 404: openapi.Response("Not Found", NotFound_404),
        # 500: openapi.Response("Internal Server Error", InternalServerError_500),
        # 204: openapi.Response("No Details Found", NoDetailsFound_204)})
    def put(self,request):
        '''
            Update Product Type Layout

            This is used for the Update Product Layout
        '''
        try:
            mapping_id = self.request.GET.get('mapping_id')
            category_id = request.data.get('category_id')
            layout_id = request.data.get('layout_id')
            serializer = CategoryMappingSerializer(data=request.data)
            if CategoryLayoutMapping.objects.filter(category_id_id = category_id,layout_id_id=layout_id):
                return Response({"message":"This category has been associated to the same layout"},status=status.HTTP_400_BAD_REQUEST)
            if serializer.is_valid():
                if not CategoryLayoutMapping.objects.filter(id = mapping_id,
                                                           category_id_id=category_id):
                    result= {"message":"Category mapping with category id = "+str(category_id)+" does not exists"}
                    return Response(result, status=status.HTTP_400_BAD_REQUEST)
                obj = CategoryLayoutMapping.objects.filter(id = mapping_id)
                etc = obj[0].layout_id
                if Layout.objects.filter(id=layout_id,type='listpage').exists():
                    if layout_id != etc:
                        obj.update(category_id_id = category_id, layout_id_id = layout_id)
                        typeobj = obj.values('id', 'category_id', 'layout_id')
                        #cache_update = update_key('list-category-layout')
                        cache_update = update_key('products-description')
                        cache_update = update_key('list-category-DisplayName')
                        cache_update = update_key('get_categories_values')
                        cache_update = update_key('get_children_categories')
                        return Response(typeobj, status=status.HTTP_200_OK)
                    result= {"message":'Category Type mapping with same layout exists'}
                    return Response(result, status=status.HTTP_400_BAD_REQUEST)
                result= {"message":'Layout must belong to listpage type'}
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
            else:
                result = serializer.errors
                return Response(result, status=status.HTTP_400_BAD_REQUEST)        
        except Exception as ex:
            api_error_logs(
                request=request,
                error=ex,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
            return Response({"message": str(ex)},
                            status=status.HTTP_400_BAD_REQUEST)

    #delete                                        
    @method_decorator(validate_token_using_introspect('delete-category-mapping-id'), name='dispatch')
    @swagger_auto_schema(auto_schema = None)
        # tags=['Layout'],
        # operation_id='delete-category-mapping-id',
        # manual_parameters=[mapping_id],
        # responses={
        #     200: openapi.Response("Success",),
        #     409: openapi.Response("Already Exists", Conflict_409),
        #     400: openapi.Response("Bad Request", BadRequest_400),
        #     401: openapi.Response("Unauthorized", Unauthorised_401),
        #     404: openapi.Response("Not Found", NotFound_404),
        #     500: openapi.Response("Internal Server Error",
        #                           InternalServerError_500),
        #     204: openapi.Response("No Details Found", NoDetailsFound_204)})
    def delete(self, request):
        '''
            API to delete Category Layout Mapping

            This api is used to delete the Category Layout Mapping Id

        '''
        try:
            
            mapping_id = self.request.GET.get('mapping_id')
            mapping_obj = CategoryLayoutMapping.objects.get(id=mapping_id)
            mapping_obj.delete()
            cache_update = update_key('products-description')
            cache_update = update_key('list-category-DisplayName')
            cache_update = update_key('get_categories_values')
            cache_update = update_key('get_children_categories')
            api_debug_logs(request, message='Deleted successfully mapping_id '+str(mapping_id))
            return Response({"message": "Delete Successfully"},
                            status=status.HTTP_202_ACCEPTED)
        except CategoryLayoutMapping.DoesNotExist:
            return Response({'message': "Categorylayout_id Does not Exist."},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response({'message': "Internal server error"},
                            status=status.HTTP_400_BAD_REQUEST)

#ProductTypeLayoutMapping
class ProductTypeLayoutMappingAPIView(generics.GenericAPIView):
    serializer_class = ProductTypeMappingSerializer
    
    layout_id = openapi.Parameter('layout_id',
                                 in_=openapi.IN_QUERY,
                                 type=openapi.TYPE_INTEGER,
                                 required=False)
    product_type_id = openapi.Parameter('product_type_id',
                                 in_=openapi.IN_QUERY,
                                 type=openapi.TYPE_INTEGER,
                                 required=False)
    page_number = openapi.Parameter('page-number', in_=openapi.IN_QUERY,
                             type=openapi.TYPE_INTEGER,
                            default=1,
                            description="This is used to retrieve list of data for a specific page number")
    mapping_id = openapi.Parameter('mapping_id',
                                        in_=openapi.IN_QUERY,
                                        type=openapi.TYPE_INTEGER,
                                        required=True)
    page_limit = openapi.Parameter('page-limit',
                              in_=openapi.IN_QUERY,
                              type=openapi.TYPE_INTEGER,
                              minimum=1,
                              default=20,
                            exclusiveMinimum=True,
                            description="This is used to retrieve the number of data per page")
#get 
    @method_decorator(validate_token_using_introspect('list-product-type-layout'), name='dispatch')
    #@method_decorator(caching_key('list-product-type-layout'))
    @swagger_auto_schema(auto_schema = None)
        # tags=['Layout'],
        #                  operation_id='list-product-type-layout',
        #                  manual_parameters=[layout_id,product_type_id,
        #                                     page_number,page_limit],
        #                  responses={
        #                      200: openapi.Response("Success",ProductTypeMappingSerializer),
        #                      409: openapi.Response("Already Exists", Conflict_409),
        #                      400: openapi.Response("Bad Request", BadRequest_400),
        #                      401: openapi.Response("Unauthorized", Unauthorised_401),
        #                      404: openapi.Response("Not Found", NotFound_404),
        #                      500: openapi.Response("Internal Server Error", InternalServerError_500),
        #                      204: openapi.Response("No Details Found", NoDetailsFound_204)})
    def get(self, request):
        '''
           List of all the Product Type Layout Mapping 

           This API lists all the Product Type Layout Mapping
        '''

        try:
            page = self.request.GET.get('page-number', 1)
            limit = self.request.GET.get('page-limit', 20)
            layout_id = self.request.GET.get('layout_id')
            store_id = request.data.get('store')
            product_type_id = self.request.GET.get('product_type_id')
            queryset = ProductTypeLayoutMapping.objects.filter(layout_id__store_id = store_id).values('id', 'layout_id', 'product_type_id')
            count = len(queryset)
            api_debug_logs(request, message="Data is retrived")
            if layout_id is not None:
                queryset=queryset.filter(layout_id_id=layout_id).values('id', 'layout_id', 'product_type_id')
                api_debug_logs(request, message="Data is retrived for the layout_id "+str(layout_id))

            if product_type_id is not None:
                queryset=queryset.filter(product_type_id_id=product_type_id).values('id', 'layout_id', 'product_type_id')

            response = get_response_structure(
                data=queryset,page=page,limit=limit,count=count)
            #client.set((request.data.get('cache_key')),json.dumps(response))
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            api_error_logs(
                request=request,
                error=ex,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
            return Response({"message": str(ex)},
                            status=status.HTTP_400_BAD_REQUEST)
#Post
    @method_decorator(validate_token_using_introspect('create-product-type-layout-mapping'), name='dispatch')
    @swagger_auto_schema(auto_schema = None)
        # tags=['Layout'],
        #                  operation_id='create-product-type-layout-mapping',
        #                  responses={
        # 200: openapi.Response("Success", ProductTypeMappingSerializer),
        # 409: openapi.Response("Already Exists", Conflict_409),
        # 400: openapi.Response("Bad Request", BadRequest_400),
        # 401: openapi.Response("Unauthorized", Unauthorised_401),
        # 404: openapi.Response("Not Found", NotFound_404),
        # 500: openapi.Response("Internal Server Error", InternalServerError_500),
        # 204: openapi.Response("No Details Found", NoDetailsFound_204)})
    def post(self,request):
        '''
            Create Product Type Layout

            This is used for the Product Type Layout
        '''
        try:
            user_id = request.data.get('user')
            product_type_id = request.data.get('product_type_id')
            layout_id = request.data.get('layout_id')
            store_id = request.data.get('store')
            serializer = ProductTypeMappingSerializer(data=request.data)
            if ProductTypeLayoutMapping.objects.filter(product_type_id_id = product_type_id,layout_id_id=layout_id):
                return Response({"message":"This product type has been associated to the same layout"},status=status.HTTP_400_BAD_REQUEST)
            if serializer.is_valid():
                if not ProductTypeLayoutMapping.objects.filter(
                    product_type_id_id=product_type_id,layout_id__store_id = store_id):
                    if Layout.objects.filter(id=layout_id,type='detailspage').exists():
                        serializer.save(created_by=user_id)
                        result = serializer.data
                        api_debug_logs(request, message="Data created successfully "+str(result))
                        #cache_update = update_key('list-product-type-layout')
                        cache_update = update_key('products-description')
                        return Response(result, status=status.HTTP_201_CREATED)
                    result= {"message":'Layout must belong to detailspage type'}
                    return Response(result, status=status.HTTP_400_BAD_REQUEST)
                result= {"message":'Layout Mapping Already exits for ProductType '+str(product_type_id)}
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
            else:
                result = serializer.errors
                return Response(result, status=status.HTTP_400_BAD_REQUEST)        
        except Exception as ex:
            api_error_logs(
                request=request,
                error=ex,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
            return Response({"message": str(ex)},
                            status=status.HTTP_400_BAD_REQUEST)
    #update
    @method_decorator(validate_token_using_introspect('update-product-type-layout-mapping'), name='dispatch')
    @swagger_auto_schema(auto_schema = None)
        # tags=['Layout'],
        #                  operation_id='update-product-type-layout-mapping',
        #                  manual_parameters = [mapping_id],
        #                  responses={
        # 200: openapi.Response("Success",ProductTypeMappingSerializer),
        # 409: openapi.Response("Already Exists", Conflict_409),
        # 400: openapi.Response("Bad Request", BadRequest_400),
        # 401: openapi.Response("Unauthorized", Unauthorised_401),
        # 404: openapi.Response("Not Found", NotFound_404),
        # 500: openapi.Response("Internal Server Error", InternalServerError_500),
        # 204: openapi.Response("No Details Found", NoDetailsFound_204)})
    def put(self,request):
        '''
            Update Product Type Layout

            This is used for the Update Product Type Layout
        '''
        try:
            serializer = ProductTypeMappingSerializer(data=request.data)
            mapping_id = self.request.GET.get('mapping_id')
            product_type_id = request.data.get('product_type_id')
            layout_id = request.data.get('layout_id')
            store_id = request.data.get('store')
            if ProductTypeLayoutMapping.objects.filter(layout_id = layout_id,
                                                           product_type_id_id=product_type_id).exists():
                result= {"message":"This product type has been associated to the same layout"}
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
            else:
                pass
            if serializer.is_valid():
                if not ProductTypeLayoutMapping.objects.filter(id = mapping_id,
                                                           product_type_id_id=product_type_id,layout_id__store_id = store_id):
                    result= {"message":"Product Type mapping with product type id = "+str(product_type_id)+" does not exists"}
                    return Response(result, status=status.HTTP_400_BAD_REQUEST)
                obj = ProductTypeLayoutMapping.objects.filter(id = mapping_id)
                etc = obj[0].layout_id
                if Layout.objects.filter(id=layout_id,type='detailspage').exists():
                    if layout_id != etc:
                        obj.update(product_type_id_id = product_type_id, layout_id_id = layout_id)
                        typeobj = obj.values('id', 'product_type_id', 'layout_id')
                        #cache_update = update_key('list-product-type-layout')
                        cache_update = update_key('products-description')
                        return Response(typeobj, status=status.HTTP_200_OK)
                    result= {"message":'Product Type mapping with same layout exists'}
                    return Response(result, status=status.HTTP_400_BAD_REQUEST)
                result= {"message":'Layout must belong to detailspage type'}
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
            else:
                result = serializer.errors
                return Response(result, status=status.HTTP_400_BAD_REQUEST)        
        
        except Exception as ex:
            api_error_logs(
                request=request,
                error=ex,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
            return Response({"message": str(ex)},
                            status=status.HTTP_400_BAD_REQUEST)
    #delete                                    
    @method_decorator(validate_token_using_introspect('delete-product-type-layout-mapping'), name='dispatch')
    @swagger_auto_schema(auto_schema = None)
        # tags=['Layout'],
        #                 operation_id='delete-product-type-mapping-id',
        #                 manual_parameters=[mapping_id],
        #                 responses={
        # 200: openapi.Response("Success",),
        # 409: openapi.Response("Already Exists", Conflict_409),
        # 400: openapi.Response("Bad Request", BadRequest_400),
        # 401: openapi.Response("Unauthorized", Unauthorised_401),
        # 404: openapi.Response("Not Found", NotFound_404),
        # 500: openapi.Response("Internal Server Error",
        #                         InternalServerError_500),
        # 204: openapi.Response("No Details Found", NoDetailsFound_204)})
    def delete(self, request):
        '''
            API to delete Product Type Layout Mapping

            This api is used to Product Type Layout Mapping Id
        '''
        try:
            mapping_id = self.request.GET.get('mapping_id')
            mapping_obj = ProductTypeLayoutMapping.objects.get(id=mapping_id)
            mapping_obj.delete()
            api_debug_logs(request, message='Deleted successfully mapping_id '+str(mapping_id))
            #cache_update = update_key('list-product-type-layout')
            cache_update = update_key('products-description')
            return Response({"message": "Delete Successfully"},
                            status=status.HTTP_202_ACCEPTED)
        except ProductTypeLayoutMapping.DoesNotExist:
            return Response({'message': "Product Type Layout Does not Exist."},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            api_error_logs(
                request=request,
                error=ex,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
            return Response({"message": str(ex)},
                            status=status.HTTP_400_BAD_REQUEST)

def get_response_structure2(data,page,limit,count):
    page1=page
    if int(page) == -1:
       page=0
    if (page) and (limit) is not None:
        total_data = Paginator(data, limit)
        try:
            page_number = total_data.page(page)
        except PageNotAnInteger:
            page_number = total_data.page(page)
        except EmptyPage:
            page_number = total_data.page(page) not in range(
                total_data.num_pages)
        data = page_number.object_list
    result = {"count":count,"page_limit":int(limit),"page_number":int(page),
    "product_layout_data": data}

    return result

def get_response_structure1(data,page,limit,count):
    page1=page
    if int(page) == -1:
       page=0
    if (page) and (limit) is not None:
        total_data = Paginator(data, limit)
        try:
            page_number = total_data.page(page)
        except PageNotAnInteger:
            page_number = total_data.page(page)
        except EmptyPage:
            page_number = total_data.page(page) not in range(
                total_data.num_pages)
        data = page_number.object_list
    result = {"count":count,"page_limit":int(limit),"page_number":int(page),
    "category_layout_data": data}

    return result

def get_response_structure(data,page,limit,count):
    page1=page
    if int(page) == -1:
       page=0
    if (page) and (limit) is not None:
        total_data = Paginator(data, limit)
        try:
            page_number = total_data.page(page)
        except PageNotAnInteger:
            page_number = total_data.page(page)
        except EmptyPage:
            page_number = total_data.page(page) not in range(
                total_data.num_pages)
        data = page_number.object_list
    result = {"count":count,"page_limit":int(limit),"page_number":int(page),
    "product_type_layout_data": data}

    return result

def get_response_structurelay(store_id, data,page,limit,count):
    page1=page
    if int(page) == -1:
       page=0
    if (page) and (limit) is not None:
        total_data = Paginator(data, limit)
        try:
            page_number = total_data.page(page)
        except PageNotAnInteger:
            page_number = total_data.page(page)
        except EmptyPage:
            page_number = total_data.page(page) not in range(
                total_data.num_pages)
        data = page_number.object_list
    serialzier= LayoutSerializer(instance=data, many=True)

    result = {"count":count,"page_limit":int(limit),"page_number":int(page),
    "data":{
        "store_id": store_id,
        "layout_data": serialzier.data}
        }

    return result