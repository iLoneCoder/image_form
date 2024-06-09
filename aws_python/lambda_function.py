import json
import boto3
from boto3.dynamodb.types import TypeSerializer
from urllib.request import urlopen, Request
from requests_toolbelt.multipart import decoder
import base64
from datetime import datetime
import uuid
from decimal import Decimal


API_TOKEN = "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"

headers = {"Authorization": f"Bearer {API_TOKEN}"}
API_URL_FACEBOOK = "https://api-inference.huggingface.co/models/facebook/detr-resnet-50"
API_URL_MICROSOFT = "https://api-inference.huggingface.co/models/microsoft/table-transformer-detection"
DYNAMODB_TABLE = 'image_dynamo'

s3_client = boto3.client('s3')

available_modes = ["facebook", "microsoft"]

def query_image_facebook(f):
  http_request = Request(API_URL_FACEBOOK, data=f, headers=headers)
  with urlopen(http_request) as response:
    result = response.read().decode()
    print(result)
  return result


def query_name_microsoft(f):
  http_request = Request(API_URL_MICROSOFT, data=f, headers=headers)
  with urlopen(http_request) as response:
    result = response.read().decode()
    print(result)
    return result


def save_to_dynamodb(data, model_name):
  dynamodb = boto3.client('dynamodb')
  timestamp = datetime.utcnow().replace(microsecond=0).isoformat()
  serializer = TypeSerializer()
  dynamo_serialized_data = []
  for item in json.loads(data, parse_float=Decimal):
    dynamo_serialized_item = {'M':{}}
    for key, value in item.items():
      if isinstance(value, (float, Decimal)):
        dynamo_serialized_item['M'][key] = {'N': str(value)}
      elif isinstance(value, dict):
        dynamo_serialized_item['M'][key] = {
          'M': {k: serializer.serialize(v)
                for k, v in value.items()}
        }
      else:
        dynamo_serialized_item['M'][key] = {'S': str(value)}
    dynamo_serialized_data.append(dynamo_serialized_item)

  data_ready_to_be_saved = {
    'id': {
      'S': str(uuid.uuid1())
    },
    'createdAt': {
      'S': timestamp
    },
    'updatedAt': {
      'S': timestamp
    },
    'huggingJson': {
      'L': dynamo_serialized_data
    },
    'huggingFaceStringData': {
      'S': data
    },
    'modelName': {
      'S': model_name
    }
  }
  print(json.dumps(data_ready_to_be_saved))
  dynamodb.put_item(TableName=DYNAMODB_TABLE, Item=data_ready_to_be_saved)


def lambda_handler(event, context):
    print("event: ", event)
    print("event headers: ", event['headers'])

    content_type_header = event['headers']["content-type"] if "content-type" in event['headers'] else event['headers']["Content-Type"]
    print(content_type_header)
    body = base64.b64decode(event["body"])

    multipart_data = decoder.MultipartDecoder(body, content_type_header)

    for part in multipart_data.parts:
        if part.headers[b'Content-Disposition']:
            content_disposition = part.headers[b'Content-Disposition'].decode('utf-8')
            print("content_disposition: ",content_disposition)
            if 'name="file"' in content_disposition:
              filename = content_disposition.split('filename=')[1].replace('"', '')
              file_content = part.content
            if 'name="name"' in content_disposition:
              model_name = part.text
              
    print("filename: ", filename)
    print("model_name: ", model_name)

    if not model_name.lower() in available_modes:
      return {
        'statusCode': 404,
        'headers': {
            'Access-Control-Allow-Origin': "*",
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps({'message': f'{model_name} not available'})
      }

    s3_client.put_object(Bucket='bucket1-6200', Key=filename, Body=file_content)

    # Send file to Huggingface API
    if model_name.lower() == 'facebook':
      result = query_image_facebook(file_content)
    elif model_name.lower() == 'microsoft':
      result = query_name_microsoft(file_content)

    print("result", result)

    # save data to DynamoDB
    save_to_dynamodb(result, model_name)
   
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': "*",
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps({'message':'File uploaded successfully'})
    }
