from localstack.utils.aws import aws_models
SBYjD=super
SBYjQ=None
SBYjJ=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  SBYjD(LambdaLayer,self).__init__(arn)
  self.cwd=SBYjQ
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.SBYjJ.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,SBYjJ,env=SBYjQ):
  SBYjD(RDSDatabase,self).__init__(SBYjJ,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,SBYjJ,env=SBYjQ):
  SBYjD(RDSCluster,self).__init__(SBYjJ,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,SBYjJ,env=SBYjQ):
  SBYjD(AppSyncAPI,self).__init__(SBYjJ,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,SBYjJ,env=SBYjQ):
  SBYjD(AmplifyApp,self).__init__(SBYjJ,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,SBYjJ,env=SBYjQ):
  SBYjD(ElastiCacheCluster,self).__init__(SBYjJ,env=env)
class TransferServer(BaseComponent):
 def __init__(self,SBYjJ,env=SBYjQ):
  SBYjD(TransferServer,self).__init__(SBYjJ,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,SBYjJ,env=SBYjQ):
  SBYjD(CloudFrontDistribution,self).__init__(SBYjJ,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,SBYjJ,env=SBYjQ):
  SBYjD(CodeCommitRepository,self).__init__(SBYjJ,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
