from localstack.utils.aws import aws_models
zYHUV=super
zYHUR=None
zYHUm=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  zYHUV(LambdaLayer,self).__init__(arn)
  self.cwd=zYHUR
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.zYHUm.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,zYHUm,env=zYHUR):
  zYHUV(RDSDatabase,self).__init__(zYHUm,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,zYHUm,env=zYHUR):
  zYHUV(RDSCluster,self).__init__(zYHUm,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,zYHUm,env=zYHUR):
  zYHUV(AppSyncAPI,self).__init__(zYHUm,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,zYHUm,env=zYHUR):
  zYHUV(AmplifyApp,self).__init__(zYHUm,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,zYHUm,env=zYHUR):
  zYHUV(ElastiCacheCluster,self).__init__(zYHUm,env=env)
class TransferServer(BaseComponent):
 def __init__(self,zYHUm,env=zYHUR):
  zYHUV(TransferServer,self).__init__(zYHUm,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,zYHUm,env=zYHUR):
  zYHUV(CloudFrontDistribution,self).__init__(zYHUm,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,zYHUm,env=zYHUR):
  zYHUV(CodeCommitRepository,self).__init__(zYHUm,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
