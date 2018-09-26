#coding:utf-8
import os
import os.path as osp
import argparse
import json
import glob

img_extensions = ['jpeg', 'jpg', 'png', 'bmp']
vid_extensions = ['mp4', 'avi', 'rmvb', 'mkv', 'webm']

def _construct_data_info(working_path, data_for_upload):
  data_info_json = []
  for i in range(len(data_for_upload)):
    data_info_json.append({"abspath": data_for_upload[i], "metadata": {"customFields": {}}})
  with open(osp.join(working_path, 'data_info.json'), 'w') as f:
    json.dump(data_info_json, f)

def _get_data(path_to_data, type_of_data):
  extensions = vid_extensions if type_of_data == 'VIDEO' else img_extensions
  data_for_upload = []
  for cur_location, dir_names, file_names in os.walk(path_to_data):
    if not file_names: contiue
    for file_name in file_names:
      if file_name.split('.')[-1] in extensions:
        data_for_upload.append(osp.join(cur_location, file_name))
  return data_for_upload

def _cls(working_path):
  extra_file = []
  extra_file = extra_file + \
               glob.glob(osp.join(working_path, 'data_info*')) + \
               glob.glob(osp.join(working_path, 'upload.sh')) + \
               glob.glob(osp.join(working_path, 'upload_failed_*'))
  for item in extra_file:
    os.system('rm '+ item)

def _parse_args():
  parser = argparse.ArgumentParser(description='path to data')
  parser.add_argument('path_to_data',help='path to data for uploading')
  #parser.add_argument('dataset_meta',help='a json file')
  parser.add_argument('--working_path',dest='working_path',help='optional config file',default='./',type=str)
  parser.add_argument('--mode',dest='mode',choices=['create','update'],help='create of update',default='create')
  args=parser.parse_args()
  return args

if __name__ == '__main__':
  args = _parse_args()

  """获取已经准备好的meta数据,并创建数据集"""
  working_path = args.working_path
  _cls(working_path)
  mode = args.mode
  path_to_meta = osp.join(working_path, 'meta.json' if mode == 'create' else 'meta_update.json') # 依据mode而不同
  if not osp.exists(path_to_meta):
    raise ValueError(path_to_meta + 'not found !')
  print '##################'
  print path_to_meta
  print '##################'
  with open(path_to_meta, 'r') as f:
    meta = json.load(f)
  dataset_name = meta['name']
  if mode == 'create':
    dataset_create_cmd = 'damine dataset create    \
                         --metadata-json ' + path_to_meta
    os.system(dataset_create_cmd)
  else:
    dataset_update_cmd = 'damine dataset update ' +    \
                         '--dataset-name ' + dataset_name + ' ' \
                         '--metadata-json ' + path_to_meta
    os.system(dataset_update_cmd)

  """读取所有需要上传的数据，制作data-info.json文件(程序会自动从meta json中得知要传的是video还是image)"""
  type_of_data = meta['dataType'] # 'VIDEO' or 'IMAGE'
  if not (type_of_data=='VIDEO' or type_of_data=='IMAGE'):
    raise ValueError('dataType must be one of "VIDEO" or "IMAGE" !')
  path_to_data = args.path_to_data
  data_for_upload = _get_data(path_to_data, type_of_data) # ['path_to_data1', 'path_to_data2', ...]
  _construct_data_info(working_path, data_for_upload)
  path_to_data_info = osp.join(working_path, 'data_info.json')
  if not osp.exists(path_to_data_info):
    raise ValueError('data_info.json not exist')
  """生成upload.sh脚本"""
  batch_upload_cmd = 'damine script init-upload ' + \
                     '--dataset-name ' + dataset_name + ' ' + \
                     '--data-info-json ' + path_to_data_info + ' ' + \
                     '--output-dir ' + working_path + ' ' + \
                     '--processes 4 ' + \
                     '--retry 2 '
  os.system(batch_upload_cmd)
  """上传数据"""
  #path_to_upload_script = osp.join(working_path, 'upload.sh')
  #upload_cmd = 'chmod +x ' + path_to_upload_script+ ' && ' + path_to_upload_script
  os.chdir(working_path)
  upload_cmd = 'chmod +x upload.sh && ./upload.sh'
  os.system(upload_cmd)
  
