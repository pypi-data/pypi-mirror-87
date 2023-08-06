from localstack.utils.aws import aws_models
nalwK=super
nalwJ=None
nalwc=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  nalwK(LambdaLayer,self).__init__(arn)
  self.cwd=nalwJ
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.nalwc.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,nalwc,env=nalwJ):
  nalwK(RDSDatabase,self).__init__(nalwc,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,nalwc,env=nalwJ):
  nalwK(RDSCluster,self).__init__(nalwc,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,nalwc,env=nalwJ):
  nalwK(AppSyncAPI,self).__init__(nalwc,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,nalwc,env=nalwJ):
  nalwK(AmplifyApp,self).__init__(nalwc,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,nalwc,env=nalwJ):
  nalwK(ElastiCacheCluster,self).__init__(nalwc,env=env)
class TransferServer(BaseComponent):
 def __init__(self,nalwc,env=nalwJ):
  nalwK(TransferServer,self).__init__(nalwc,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,nalwc,env=nalwJ):
  nalwK(CloudFrontDistribution,self).__init__(nalwc,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,nalwc,env=nalwJ):
  nalwK(CodeCommitRepository,self).__init__(nalwc,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
