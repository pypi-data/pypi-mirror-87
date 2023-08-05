from localstack.utils.aws import aws_models
GphLP=super
GphLc=None
GphLu=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  GphLP(LambdaLayer,self).__init__(arn)
  self.cwd=GphLc
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.GphLu.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,GphLu,env=GphLc):
  GphLP(RDSDatabase,self).__init__(GphLu,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,GphLu,env=GphLc):
  GphLP(RDSCluster,self).__init__(GphLu,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,GphLu,env=GphLc):
  GphLP(AppSyncAPI,self).__init__(GphLu,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,GphLu,env=GphLc):
  GphLP(AmplifyApp,self).__init__(GphLu,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,GphLu,env=GphLc):
  GphLP(ElastiCacheCluster,self).__init__(GphLu,env=env)
class TransferServer(BaseComponent):
 def __init__(self,GphLu,env=GphLc):
  GphLP(TransferServer,self).__init__(GphLu,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,GphLu,env=GphLc):
  GphLP(CloudFrontDistribution,self).__init__(GphLu,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,GphLu,env=GphLc):
  GphLP(CodeCommitRepository,self).__init__(GphLu,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
