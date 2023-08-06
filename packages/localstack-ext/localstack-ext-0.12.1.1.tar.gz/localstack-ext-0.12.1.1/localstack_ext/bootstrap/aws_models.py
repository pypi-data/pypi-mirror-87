from localstack.utils.aws import aws_models
QGMiV=super
QGMid=None
QGMiv=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  QGMiV(LambdaLayer,self).__init__(arn)
  self.cwd=QGMid
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.QGMiv.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,QGMiv,env=QGMid):
  QGMiV(RDSDatabase,self).__init__(QGMiv,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,QGMiv,env=QGMid):
  QGMiV(RDSCluster,self).__init__(QGMiv,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,QGMiv,env=QGMid):
  QGMiV(AppSyncAPI,self).__init__(QGMiv,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,QGMiv,env=QGMid):
  QGMiV(AmplifyApp,self).__init__(QGMiv,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,QGMiv,env=QGMid):
  QGMiV(ElastiCacheCluster,self).__init__(QGMiv,env=env)
class TransferServer(BaseComponent):
 def __init__(self,QGMiv,env=QGMid):
  QGMiV(TransferServer,self).__init__(QGMiv,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,QGMiv,env=QGMid):
  QGMiV(CloudFrontDistribution,self).__init__(QGMiv,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,QGMiv,env=QGMid):
  QGMiV(CodeCommitRepository,self).__init__(QGMiv,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
