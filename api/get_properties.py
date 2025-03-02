from CoolProp.CoolProp import PropsSI
from urllib.parse import urlparse, parse_qs
import json

def main(request):
    try:
        # 解析查询参数
        parsed_url = urlparse(request.url)
        query_params = parse_qs(parsed_url.query)
        
        temp = query_params.get('temp', [''])[0]
        pressure = query_params.get('pressure', [''])[0]

        # 验证参数
        if not temp or not pressure:
            raise ValueError('Missing temperature or pressure parameter')
        
        temp = float(temp)
        pressure = float(pressure)

        # 计算物性参数
        properties = {
            'density': PropsSI('D', 'T', temp, 'P', pressure, 'Hydrogen'),
            'specific_heat': PropsSI('C', 'T', temp, 'P', pressure, 'Hydrogen'),
            'enthalpy': PropsSI('H', 'T', temp, 'P', pressure, 'Hydrogen'),
            'entropy': PropsSI('S', 'T', temp, 'P', pressure, 'Hydrogen')
        }

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({k: v for k, v in properties.items()})
        }

    except Exception as e:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        }