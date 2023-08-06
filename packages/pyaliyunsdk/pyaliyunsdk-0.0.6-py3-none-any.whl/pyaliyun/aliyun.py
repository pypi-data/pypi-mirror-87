from typing import Dict, List
from aliyunsdkcore.client import AcsClient

import json
import time
import datetime
import logging
from typing import Dict

from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest, DescribeInstanceAttributeRequest, DescribeDisksRequest, \
    DescribeInstanceTypesRequest, AllocatePublicIpAddressRequest, StartInstanceRequest, DescribeVpcsRequest, AddTagsRequest, JoinSecurityGroupRequest, \
    StopInstanceRequest, ModifyInstanceSpecRequest, ModifyPrepayInstanceSpecRequest

from aliyunsdkrds.request.v20140815 import DescribeDBInstancesRequest, DescribeDBInstanceAttributeRequest, DescribeResourceUsageRequest, \
    DescribeBackupsRequest, CreateBackupRequest, DescribeBackupTasksRequest, CreateDBInstanceRequest, ModifySecurityIpsRequest

from aliyunsdkslb.request.v20140515 import DescribeLoadBalancersRequest, DescribeLoadBalancerAttributeRequest, CreateLoadBalancerHTTPListenerRequest, \
    CreateLoadBalancerTCPListenerRequest, AddBackendServersRequest, StartLoadBalancerListenerRequest, RemoveBackendServersRequest, \
    DeleteLoadBalancerRequest

from aliyunsdkcore.acs_exception.exceptions import ClientException

logger = logging.getLogger(__name__)


class Base:
    pagesize = 100
    totalstring = ""

    def __init__(self, ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION_ID):
        self.client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION_ID)
        self.ins_list = []

    def do_action(self, request):
        status = False

        for i in range(1, 4):
            try:
                # request.set_accept_format('json')
                response = self.client.do_action_with_exception(request)
                response = json.loads(str(response, encoding='utf-8'))
                logger.debug(response)
                status = True
                return response
            except ClientException as e:
                print('超時 請求重試 等待10秒 {}'.format(e))
                logger.error('超時 請求重試 等待10秒 {}'.format(e))
                time.sleep(10)
            except Exception as e:
                print(f"未知錯誤 請求重試 {e}")

        if not status:
            logger.error('多次請求錯誤')
            raise Exception('多次請求錯誤')

    def get_totel_page(self, request):
        request.set_PageSize(1)
        data = self.do_action(request)
        pagenum = data[self.totalstring] // self.pagesize
        if data[self.totalstring] % self.pagesize != 0:
            pagenum += 1
        return pagenum


class ECS(Base):
    totalstring = 'TotalCount'

    def _getInsList(self):
        request = DescribeInstancesRequest.DescribeInstancesRequest()
        for pagenum in range(1, self.get_totel_page(request) + 1):
            request.set_PageNumber(pagenum)
            request.set_PageSize(self.pagesize)
            ret = self.do_action(request)
            for ins in ret['Instances']['Instance']:
                yield ins

    def getInsList(self, detail=None):

        if not detail:
            self.ins_list = list(self._getInsList())
            return self.ins_list
        else:
            self.ins_list = [self.getDetail(ins['InstanceId']) for ins in self._getInsList()]

        return self.ins_list

    def getDetail(self, id):
        request = DescribeInstanceAttributeRequest.DescribeInstanceAttributeRequest()
        request.set_InstanceId(id)
        status = False

        # 重試次數
        for loop in range(3):

            ret = self.do_action(request)
            logger.debug(ret)
            if not ret['VpcAttributes']['PrivateIpAddress']['IpAddress']:
                logging.error('獲取不到私有IP detail %s' % ret)
                time.sleep(5)
                continue

            size = self.getDiskSize(ret['InstanceId'])
            ret.update({"Disk": size})
            status = True
            break

        if not status:
            raise Exception('%s 獲取不到私有IP' % id)
        else:
            return ret

    def getDiskSize(self, id):
        request = DescribeDisksRequest.DescribeDisksRequest()
        request.set_InstanceId(id)
        ret = self.do_action(request)
        disk_size = ret['Disks']['Disk'][0]['Size']
        return disk_size

    def getTypeAll(self):
        request = DescribeInstanceTypesRequest.DescribeInstanceTypesRequest()
        ret = self.do_action(request)
        return ret['InstanceTypes']['InstanceType']

    def setPublicIP(self, id):
        """取得公網iP

        :param id:
        :return:
        """
        request = AllocatePublicIpAddressRequest.AllocatePublicIpAddressRequest()
        request.set_InstanceId(id)
        ret = self.do_action(request)

        return ret

    def startInstance(self, id):
        '''啟動實例

        :param id:
        :return:
        '''
        request = StartInstanceRequest.StartInstanceRequest()
        request.set_InstanceId(id)
        ret = self.do_action(request)
        return ret

    def getDisk(self, id):
        request = DescribeDisksRequest.DescribeDisksRequest()
        request.set_InstanceId(id)
        ret = self.do_action(request)
        return ret

    def getVpcList(self):
        request = DescribeVpcsRequest.DescribeVpcsRequest()
        request.set_PageSize(10)
        response = self.do_action(request)
        return response

    def addTagsRequest(self, id, k, y):
        request = AddTagsRequest.AddTagsRequest()
        request.set_ResourceId(id)
        request.set_ResourceType('instance')
        request.set_Tags([{'Key': k, 'Value': y}])
        response = self.do_action(request)
        return response

    def addSecurityGroup(self, id, securitygroupid):
        request = JoinSecurityGroupRequest.JoinSecurityGroupRequest()
        request.set_InstanceId(id)
        request.set_SecurityGroupId(securitygroupid)
        response = self.do_action(request)
        return response

    def updateModifyInstance(self, id, instancetype):
        """调用ModifyInstanceSpec调整一台按量付费ECS实例的实例规格和公网带宽大小。

        :param id:
        :param instancetype:
        :return:
        """
        request = ModifyInstanceSpecRequest.ModifyInstanceSpecRequest()
        request.set_InstanceId(id)
        request.set_InstanceType(instancetype)
        response = self.do_action(request)
        return response

    def updateModifyPrepayInstance(self, id, instancetype):
        """调用ModifyPrepayInstanceSpec升级或者降低一台包年包月ECS实例的实例规格，新实例规格将会覆盖实例的整个生命周期。

        :param id:
        :param instancetype:
        :return:
        """
        request = ModifyPrepayInstanceSpecRequest.ModifyPrepayInstanceSpecRequest()
        request.set_InstanceId(id)
        request.set_InstanceType(instancetype)
        response = self.do_action(request)
        return response

    def stopInstance(self, id):
        request = StopInstanceRequest.StopInstanceRequest()
        request.set_InstanceId(id)
        response = self.do_action(request)
        return response

    def get_mapping_site_ip(self):
        data = {}
        for i in self.ins_list:
            data[i['InstanceName']] = {
                'PrivateIpAddress': i['VpcAttributes']['PrivateIpAddress']['IpAddress'],
                'PublicIpAddress': i['PublicIpAddress']['IpAddress']
            }
        return data


class RDS(Base):
    totalstring = 'TotalRecordCount'

    def _getInsList(self):
        request = DescribeDBInstancesRequest.DescribeDBInstancesRequest()
        for pagenum in range(1, self.get_totel_page(request) + 1):
            request.set_PageNumber(pagenum)
            request.set_PageSize(self.pagesize)
            ret = self.do_action(request)
            for ins in ret['Items']['DBInstance']:
                # self.ins_list.append(i)
                yield ins
        # if not self.ins_list:
        #     logging.error('rds_list {} 為空 {}'.format(self.client, self.rds_list))
        # return self.ins_list

    def getInsList(self, detail=None):

        if not detail:
            self.ins_list = list(self._getInsList())
            return self.ins_list
        else:
            self.ins_list = [self.getDetail(ins['DBInstanceId']) for ins in self._getInsList()]

        return self.ins_list

    def getDetail(self, id):
        request = DescribeDBInstanceAttributeRequest.DescribeDBInstanceAttributeRequest()
        request.set_DBInstanceId(id)
        ret = self.do_action(request)

        data = ret['Items']['DBInstanceAttribute'][0]
        use_data = self.getUsage(id)

        # logging.debug("use_data %s %s %s" % (id, data['DBInstanceDescription'], use_data))

        if use_data:
            pass
        else:
            logging.error("use_data %s %s %s" % (id, data['DBInstanceDescription'], use_data))
            raise Exception('use_data 空 %s ' % use_data)

        data.update(use_data)

        return data

    def getUsage(self, id):
        request = DescribeResourceUsageRequest.DescribeResourceUsageRequest()
        request.set_DBInstanceId(id)
        ret = self.do_action(request)
        return ret

    def getDBInstanceID(self, name: str) -> str:
        '''

        :param name:
        :return:
        '''
        ids = [i['DBInstanceId'] for i in self.ins_list if i['DBInstanceDescription'] == name]
        print(ids)
        if ids:
            return ids[0]
        else:
            print('找不到名稱或當前名稱錯誤')
            raise ValueError("輸入錯誤,找不到名稱或當前名稱錯誤")

    def getBackupList(self, name: str = None, id: str = None):
        '''返回備份列表

        :param name:
        :param id:
        :return:
        '''
        if name:
            id = self.getDBInstanceID(name)

        request = DescribeBackupsRequest.DescribeBackupsRequest()
        request.set_DBInstanceId(id)
        ret = self.do_action(request)
        backup_list = []
        for lst in ret['Items']['Backup']:
            lst['Datetime'] = datetime.datetime.strptime(lst['BackupEndTime'], '%Y-%m-%dT%H:%M:%S%z')
            backup_list.append(lst)

        return backup_list

    def getBackupLastet(self, name=None, id=None):
        '''返回最新一筆備份資料

        :param name:
        :param id:
        :return:
        '''
        backup_list = self.getBackupList(name=name, id=id)
        d = max([i['Datetime'] for i in backup_list])
        _data = [i for i in backup_list if i['Datetime'] == d][0]
        data = {
            'Name': name,
            'DBInstanceId': _data['DBInstanceId'],
            'BackupIntranetDownloadURL': _data['BackupIntranetDownloadURL'],
            'BackupDownloadURL': _data['BackupDownloadURL'],
            'BackupEndTime': datetime.datetime.fromtimestamp(_data['Datetime'].timestamp()).strftime("%Y/%m/%d %H:%M:%S"),
            'BackupSize': f"{int(_data['BackupSize'] / 1024 / 1024 // 1024)}G",
            'FileName': _data['BackupIntranetDownloadURL'].split('/')[-1].split('?Expires')[0]

        }
        return data

    def createBackup(self, name=None, id=None) -> dict:
        '''創建備份任務

        :param name:
        :param id:
        :return:
        '''
        if name:
            id = self.getDBInstanceID(name)

        request = CreateBackupRequest.CreateBackupRequest()
        request.set_DBInstanceId(id)
        ret = self.do_action(request)
        return ret

    def getBackupTasks(self, id, jobid) -> Dict:
        '''返回備份任務狀態

        :param id:
        :param jobid:
        :return:
        '''
        request = DescribeBackupTasksRequest.DescribeBackupTasksRequest()
        request.set_DBInstanceId(id)
        request.set_BackupJobId(jobid)
        ret = self.do_action(request)

        return ret['Items']['BackupJob'][0] if ret['Items']['BackupJob'] else {}

    def createInstance(self, name, type, version, storage, paytype, dbclass, security_ip_list='127.0.0.1', vpcid=None):
        '''創建實例

        :param name: 實例名稱
        :param type: mysql
        :param version: 5.7
        :param storage: 100
        :param paytype: Postpaid, Prepaid
        :param dbclass: rds.mysql.s3.large, mysql.n4.large.1
        :param security_ip_list: "127.0.0.1,"
        :param vpcid:
        :return:
        '''

        request = CreateDBInstanceRequest.CreateDBInstanceRequest()
        request.set_Engine(type)
        request.set_EngineVersion(version)
        request.set_DBInstanceClass(dbclass)  # rds.mysql.s3.large , mysql.n4.large.1
        request.set_DBInstanceStorage(storage)
        request.set_DBInstanceNetType("Intranet")
        request.set_DBInstanceDescription(name)  # 描述
        request.set_SecurityIPList(security_ip_list)
        if vpcid:
            request.set_VPCId(vpcid)  # VPCID

        request.set_PayType(paytype)  # Postpaid, Prepaid
        # request.set_ZoneId("cn-hongkong-b")
        request.set_InstanceNetworkType("VPC")
        # request.set_Period("Month") # ??
        # request.set_UsedTime("2") # ??
        self.do_action(request)

    def updateModifySecurityIps(self, id, iplist):
        request = ModifySecurityIpsRequest.ModifySecurityIpsRequest()
        request.set_DBInstanceId(id)
        request.set_SecurityIps(iplist)
        ret = self.do_action(request)
        return ret


class SLB(Base):
    totalstring = 'TotalCount'

    def _getInsList(self):
        request = DescribeLoadBalancersRequest.DescribeLoadBalancersRequest()
        for pagenum in range(1, self.get_totel_page(request) + 1):
            request.set_PageNumber(pagenum)
            request.set_PageSize(self.pagesize)
            ret = self.do_action(request)
            logger.debug(ret)
            for ins in ret['LoadBalancers']['LoadBalancer']:
                yield ins

    def getInsList(self, detail=None):

        if not detail:
            self.ins_list = list(self._getInsList())
            return self.ins_list
        else:
            self.ins_list = [self.getDetail(ins['LoadBalancerId']) for ins in self._getInsList()]

        return self.ins_list

    def getDetail(self, id):
        request = DescribeLoadBalancerAttributeRequest.DescribeLoadBalancerAttributeRequest()
        request.set_LoadBalancerId(id)
        ret = self.do_action(request)
        return ret

    def addBackendServer(self, id, ecs_instance_id):
        request = AddBackendServersRequest.AddBackendServersRequest()
        request.set_LoadBalancerId(id)
        data = [{"Type": "ecs", "ServerId": i, "Weight": 100} for i in ecs_instance_id]
        request.set_BackendServers(json.dumps(data))
        ret = self.do_action(request)
        return ret

    def removeBackendServer(self, id, BackendServers):
        '''

        :param id:
        :param BackendServers:  json'[{"Type":"ecs","ServerId":"i-t4n1epdcvalegf7doz0f","Weight":100}]'
        :return:
        '''
        request = RemoveBackendServersRequest.RemoveBackendServersRequest()
        request.set_LoadBalancerId(id)
        request.set_BackendServers(BackendServers)
        ret = self.do_action(request)
        return ret

    def createListener(self, id, port, type):
        if type == 'tcp':
            self.createTCPListener(id, port)
        else:
            self.createHttpListener(id, port)

    def createHttpListener(self, id, port):
        logger.debug('createHttpListener')
        request = CreateLoadBalancerHTTPListenerRequest.CreateLoadBalancerHTTPListenerRequest()
        request.set_LoadBalancerId(id)
        request.set_ListenerPort(port)
        request.set_StickySession('off')
        request.set_HealthCheck('on')
        request.set_HealthCheckURI('/')
        request.set_HealthCheckTimeout(5)
        request.set_HealthCheckInterval(2)
        request.set_HealthyThreshold(3)
        request.set_UnhealthyThreshold(3)
        request.set_BackendServerPort(port)
        ret = self.do_action(request)
        return ret

    def createTCPListener(self, id, port):
        logger.debug('createTCPListener')
        request = CreateLoadBalancerTCPListenerRequest.CreateLoadBalancerTCPListenerRequest()
        request.set_LoadBalancerId(id)
        request.set_ListenerPort(port)
        request.set_BackendServerPort(port)
        request.set_Bandwidth(-1)
        ret = self.do_action(request)
        return ret

    def startListener(self, id, port, type):
        request = StartLoadBalancerListenerRequest.StartLoadBalancerListenerRequest()
        request.set_LoadBalancerId(id)
        request.set_ListenerPort(port)
        request.set_protocol_type(type)
        ret = self.do_action(request)
        return ret

    def deleteLoadBalancerRequest(self, id):
        request = DeleteLoadBalancerRequest.DeleteLoadBalancerRequest()
        request.set_LoadBalancerId(id)
        ret = self.do_action(request)
        return ret


class Aliyun:

    def __init__(self, ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION_ID):
        self.ecs = ECS(ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION_ID)
        self.rds = RDS(ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION_ID)
        self.slb = SLB(ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION_ID)
