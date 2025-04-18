## 登录接口 
```
POST /api/v1/auth/SignIn

Header:
access_type: android

入参：
{
    "account": "medo_gh",
    "password": "medo123456"
}

返回数据：
{
    "code": 0,
    "msg": null,
    "data": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMDEwODgiLCJjb21wYW55SUQiOiI1ODYiLCJleHAiOjE3NDUxMTU1MzMsImlhdCI6MTc0MjQzNzEzMywic3ViamVjdFR5cGUiOiIwIiwic3ViamVjdE5hbWUiOiLlrqvotLoifQ._ImnNDkrlbeBhQZnUl9BytVG5VD9MyV65rknV_UEOXM"
}
```

## 认证说明
系统支持两种格式的认证头:
1. `Authorization: Bearer <token>` (标准OAuth2格式)
2. `Authorization: <token>` (简化格式)

两种格式都可以正常工作，但建议使用标准的OAuth2格式。

## 通过token获取用户信息
``` 
GET /api/v1/auth/GetUserByToken

Header:
Authorization: Bearer <token>  
或
Authorization: <token>

返回数据：
{
    "code": 0,
    "msg": null,
    "data": {
        "subjectID": 636,
        "subjectName": "宫贺",
        "companyID": 138,
        "companyName": "上海米度测控科技有限公司"
    }
}
```

## 获取MR702-遥测终端机传感器配置列表
```
POST  /api/v1/config/QueryMR702SensorConfigList

Header:
Authorization: Bearer <token>
或
Authorization: <token>

入参：
{
    "port": "485-1",
    "sensorName": "MD-VWP数字渗压计" 
}

返回数据：
{
    "code": 0,
    "msg": null,
    "data": {
        "sensorList": [
            {
                "id": 1,
                "port": "485-1",
                "sensorID": 1,
                "sensorName": "MD-VWP数字渗压计",
                "modelToken": "214",
                "modelName": "水位",
                "modelFieldList": [
                        {
                            "fieldName": "水深",
                            "engUnit": "m",
                            "hydrologicalIdentification": "3B",
                            "collectionInstructions": "03000A0002",
                            "ratio": "0.001",
                            "dataFormat": "浮点型ABCD",
                            "triggerValue": "0",
                            "upperLimit": "10000",
                            "lowerLimit": "0",
                            "correctValue": "0",
                            "ngateval": "3"
                        },
                        {
                            "fieldName": "温度",
                            "engUnit": "℃",
                            "hydrologicalIdentification": "3B",
                            "collectionInstructions": "03000C0002",
                            "ratio": "1",
                            "dataFormat": "浮点型ABCD",
                            "triggerValue": "0",
                            "upperLimit": "10000",
                            "lowerLimit": "-10000",
                            "correctValue": "0",
                            "ngateval": "3"
                        }
                    ],
                "createUserID": 636,
                "createTime": "2025-04-02 17:02:06",
                "updateUserID": 636,
                "updateTime": "2025-04-12 17:02:06",
           }
}
```
1. **入参字段说明**：
| 字段 | 说明 |备注 |
| - | - |- |
| port | 串口号 | 485-1 或 485-2 |
| sensorName | 传感器名称 | 可以为空，为空时查询所有传感器 |

2. **返回数据字段说明**：
| 字段 | 说明 |备注 |
| - | - |- |
| id | 传感器配置ID | 数据库表主键 |
| port | 串口号 |  |
| sensorID | 传感器ID | 相同串口下传感器ID唯一 |
| sensorName | 传感器名称 |  |
| modelToken | 物模型Token |  |
| modelName | 物模型名称 |  |
| modelFieldList | 物模型字段列表 |  |
| createUserID | 创建者ID |  |
| createTime | 创建时间 |  |
| updateUserID | 更新者ID |  |
| updateTime | 更新时间 |  |
| fieldName | 采集项名称 |  |
| engUnit | 采集项单位 |  |
| hydrologicalIdentification | 水文标识 |  |
| collectionInstructions | 采集指令 |  |
| ratio | 倍率 |  |
| dataFormat | 数据类型 |  |
| triggerValue | 触发值 |  |
| upperLimit | 上限值 |  |
| lowerLimit | 下限值 |  |
| correctValue | 修正值 |  |
| ngateval | 阈值次数 |  |


## 添加MR702-遥测终端机传感器配置项
```
POST /api/v1/config/AddMR702SensorConfigItem

Header:
Authorization: SignIn 接口返回的 token 
Content-Type: application/json

请求体:
{
    "port": "485-1",
    "sensorID": 1,
    "sensorName": "水位传感器",
    "modelToken": "10066",
    "modelName": "水位",
    "modelFieldList": [
        {
            "fieldName": "水深",
            "engUnit": "m",
            "hydrologicalIdentification": "3B",
            "collectionInstructions": "03000A0002",
            "ratio": "0.001",
            "dataFormat": "浮点型ABCD",
            "triggerValue": "0",
            "upperLimit": "10000",
            "lowerLimit": "0",
            "correctValue": "0",
            "ngateval": "3"
        }
    ]
}

响应体:
{
    "code": 200,
    "message": "success",
    "data": {
        "id": 1
    }
}
```

 **注意**：
   - id 为新增的传感器配置项ID，自增
   - 传感器ID 在同一串口下需要唯一


## 编辑MR702-遥测终端机传感器配置项
```
POST /api/v1/config/EditMR702SensorConfigItem

Header:
Authorization: SignIn 接口返回的 token 
Content-Type: application/json

请求体:
{
    "id": 1,
    "port": "485-1",
    "sensorID": 1,
    "sensorName": "水位传感器",
    "modelToken": "10066",
    "modelName": "水位",
    "modelFieldList": [
        {
            "fieldName": "水深",
            "engUnit": "m",
            "hydrologicalIdentification": "3B",
            "collectionInstructions": "03000A0002",
            "ratio": "0.001",
            "dataFormat": "浮点型ABCD",
            "triggerValue": "0",
            "upperLimit": "10000",
            "lowerLimit": "0",
            "correctValue": "0",
            "ngateval": "3"
        }
    ]
}

响应体:
{
    "code": 200,
    "message": "success",
    "data": null
}
```

## 批量删除MR702-遥测终端机传感器配置项
```
POST /api/v1/config/BatchDeleteMR702SensorConfigItem

Header:
Authorization: SignIn 接口返回的 token 
Content-Type: application/json

请求体:
{
    "ids": [1,2,3]
}

响应体:
{
    "code": 200,
    "message": "success",
    "data": null
}
```

 **注意**：
   - ids 为需要删除的传感器配置项ID列表
