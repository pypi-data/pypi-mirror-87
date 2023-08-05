from localstack.utils.aws import aws_models
sxcfB=super
sxcfC=None
sxcfX=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  sxcfB(LambdaLayer,self).__init__(arn)
  self.cwd=sxcfC
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.sxcfX.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,sxcfX,env=sxcfC):
  sxcfB(RDSDatabase,self).__init__(sxcfX,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,sxcfX,env=sxcfC):
  sxcfB(RDSCluster,self).__init__(sxcfX,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,sxcfX,env=sxcfC):
  sxcfB(AppSyncAPI,self).__init__(sxcfX,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,sxcfX,env=sxcfC):
  sxcfB(AmplifyApp,self).__init__(sxcfX,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,sxcfX,env=sxcfC):
  sxcfB(ElastiCacheCluster,self).__init__(sxcfX,env=env)
class TransferServer(BaseComponent):
 def __init__(self,sxcfX,env=sxcfC):
  sxcfB(TransferServer,self).__init__(sxcfX,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,sxcfX,env=sxcfC):
  sxcfB(CloudFrontDistribution,self).__init__(sxcfX,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,sxcfX,env=sxcfC):
  sxcfB(CodeCommitRepository,self).__init__(sxcfX,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
