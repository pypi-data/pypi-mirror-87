from localstack.utils.aws import aws_models
hYNiS=super
hYNik=None
hYNiu=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  hYNiS(LambdaLayer,self).__init__(arn)
  self.cwd=hYNik
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.hYNiu.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,hYNiu,env=hYNik):
  hYNiS(RDSDatabase,self).__init__(hYNiu,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,hYNiu,env=hYNik):
  hYNiS(RDSCluster,self).__init__(hYNiu,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,hYNiu,env=hYNik):
  hYNiS(AppSyncAPI,self).__init__(hYNiu,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,hYNiu,env=hYNik):
  hYNiS(AmplifyApp,self).__init__(hYNiu,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,hYNiu,env=hYNik):
  hYNiS(ElastiCacheCluster,self).__init__(hYNiu,env=env)
class TransferServer(BaseComponent):
 def __init__(self,hYNiu,env=hYNik):
  hYNiS(TransferServer,self).__init__(hYNiu,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,hYNiu,env=hYNik):
  hYNiS(CloudFrontDistribution,self).__init__(hYNiu,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,hYNiu,env=hYNik):
  hYNiS(CodeCommitRepository,self).__init__(hYNiu,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
