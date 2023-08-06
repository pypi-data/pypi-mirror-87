import os
oAYKW=False
oAYKz=Exception
oAYKT=True
import logging
import traceback
import localstack
from localstack.constants import LOCALSTACK_ROOT_FOLDER
from localstack.utils.common import(mkdir,run,new_tmp_file,rm_rf,chmod_r,download,unzip,get_arch,in_docker,is_alpine,now)
from localstack_ext.constants import ARTIFACTS_REPO
LOG=logging.getLogger(__name__)
RULE_ENGINE_INSTALL_URL='https://github.com/whummer/serverless-iot-offline'
H2_DOWNLOAD_URL='http://www.h2database.com/h2-2019-10-14.zip'
REDIS_URL_PATTERN='https://github.com/whummer/miniredis/raw/master/build/miniredis.<arch>.bin'
SSL_CERT_URL='%s/raw/master/local-certs/server.key'%ARTIFACTS_REPO
MINIREDIS_BINARY=os.path.join(LOCALSTACK_ROOT_FOLDER,'localstack','infra','redis','miniredis.<arch>.bin')
INFRA_DIR=os.path.join(os.path.dirname(localstack.__file__),'infra')
LOCALSTACK_DIR=os.path.dirname(localstack.__file__)
def install_libs():
 install_iot_rule_engine()
 install_postgres()
 install_redis()
 install_mqtt()
def install_iot_rule_engine():
 target_dir=LOCALSTACK_DIR
 main_file=os.path.join(target_dir,'node_modules','serverless-iot-offline','query.js')
 if not os.path.exists(main_file):
  LOG.info('Installing IoT rule engine. This may take a while.')
  run('cd %s; npm install %s'%(target_dir,RULE_ENGINE_INSTALL_URL))
 return main_file
def install_postgres():
 if not in_docker():
  return
 try:
  run('which postgres',print_error=oAYKW)
 except oAYKz:
  install_alpine_package('postgresql','RDS')
 try:
  run('which pg_config',print_error=oAYKW)
 except oAYKz:
  install_alpine_package('postgresql-dev','RDS')
def install_redis():
 try:
  run('which redis-server',print_error=oAYKW)
 except oAYKz:
  install_alpine_package('redis','ElastiCache')
 return 'redis-server'
def install_mqtt():
 try:
  run('which mosquitto',print_error=oAYKW)
 except oAYKz:
  install_alpine_package('mosquitto','IoT')
 return 'mosquitto'
def install_alpine_package(package,api_name):
 if not is_alpine():
  return
 LOG.info('Downloading dependencies for %s API. This may take a while.'%api_name)
 run('apk add %s'%package)
def setup_ssl_cert():
 from localstack.services import generic_proxy
 target_file=generic_proxy.get_cert_pem_file_path()
 cache_duration_secs=6*60*60
 if os.path.exists(target_file):
  mod_time=os.path.getmtime(target_file)
  if mod_time>(now()-cache_duration_secs):
   return
 download_github_artifact(SSL_CERT_URL,target_file)
def download_github_artifact(url,target_file):
 def do_download(url,print_error=oAYKW):
  try:
   download(url,target_file)
   return oAYKT
  except oAYKz as e:
   if print_error:
    LOG.info('Unable to download local test SSL certificate from %s to %s: %s %s'%(url,target_file,e,traceback.format_exc()))
 result=do_download(url)
 if not result:
  url=url.replace('https://github.com','https://cdn.jsdelivr.net/gh')
  url=url.replace('/raw/master/','/')
  do_download(url,oAYKT)
def install_h2():
 target_dir=os.path.join(INFRA_DIR,'h2')
 if not os.path.exists(target_dir):
  mkdir(target_dir)
  zip_file=new_tmp_file()
  LOG.info('Downloading dependencies for RDS server. This may take a while.')
  download(H2_DOWNLOAD_URL,zip_file)
  unzip(zip_file,target_dir)
  rm_rf(zip_file)
def install_miniredis():
 arch=get_arch()
 bin_path=MINIREDIS_BINARY.replace('<arch>',arch)
 if not os.path.exists(bin_path):
  redis_folder=os.path.dirname(bin_path)
  mkdir(redis_folder)
  url=REDIS_URL_PATTERN.replace('<arch>',arch)
  LOG.debug('Downloading binary from %s'%url)
  download(url,bin_path)
  chmod_r(bin_path,0o755)
 return bin_path
# Created by pyminifier (https://github.com/liftoff/pyminifier)
