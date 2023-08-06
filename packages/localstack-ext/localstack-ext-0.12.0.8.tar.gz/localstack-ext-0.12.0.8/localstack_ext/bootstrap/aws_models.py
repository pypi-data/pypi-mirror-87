from localstack.utils.aws import aws_models
saQDW=super
saQDR=None
saQDn=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  saQDW(LambdaLayer,self).__init__(arn)
  self.cwd=saQDR
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.saQDn.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,saQDn,env=saQDR):
  saQDW(RDSDatabase,self).__init__(saQDn,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,saQDn,env=saQDR):
  saQDW(RDSCluster,self).__init__(saQDn,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,saQDn,env=saQDR):
  saQDW(AppSyncAPI,self).__init__(saQDn,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,saQDn,env=saQDR):
  saQDW(AmplifyApp,self).__init__(saQDn,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,saQDn,env=saQDR):
  saQDW(ElastiCacheCluster,self).__init__(saQDn,env=env)
class TransferServer(BaseComponent):
 def __init__(self,saQDn,env=saQDR):
  saQDW(TransferServer,self).__init__(saQDn,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,saQDn,env=saQDR):
  saQDW(CloudFrontDistribution,self).__init__(saQDn,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,saQDn,env=saQDR):
  saQDW(CodeCommitRepository,self).__init__(saQDn,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
