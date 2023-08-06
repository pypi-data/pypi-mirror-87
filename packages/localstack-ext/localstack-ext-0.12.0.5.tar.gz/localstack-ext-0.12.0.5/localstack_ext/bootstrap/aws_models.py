from localstack.utils.aws import aws_models
TMBGg=super
TMBGi=None
TMBGo=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  TMBGg(LambdaLayer,self).__init__(arn)
  self.cwd=TMBGi
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.TMBGo.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,TMBGo,env=TMBGi):
  TMBGg(RDSDatabase,self).__init__(TMBGo,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,TMBGo,env=TMBGi):
  TMBGg(RDSCluster,self).__init__(TMBGo,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,TMBGo,env=TMBGi):
  TMBGg(AppSyncAPI,self).__init__(TMBGo,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,TMBGo,env=TMBGi):
  TMBGg(AmplifyApp,self).__init__(TMBGo,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,TMBGo,env=TMBGi):
  TMBGg(ElastiCacheCluster,self).__init__(TMBGo,env=env)
class TransferServer(BaseComponent):
 def __init__(self,TMBGo,env=TMBGi):
  TMBGg(TransferServer,self).__init__(TMBGo,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,TMBGo,env=TMBGi):
  TMBGg(CloudFrontDistribution,self).__init__(TMBGo,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,TMBGo,env=TMBGi):
  TMBGg(CodeCommitRepository,self).__init__(TMBGo,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
