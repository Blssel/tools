# 脚本使用说明
上传数据集前需要事先提供数据集的元数据，同时脚本运行过程中也会生成若干中间元数据，本脚本规定数据集元数据一律使用meta.json名称，可以事先填写好放在当前目录(默认)，或其它任意目录(只要运行脚本的时候指定一下即可)。然后运行以下命令:
```shell
python upload.py base_path/to/data --working_path ./meta_and_out --mode update
```
其中
- `base_path/to/data`指要上传的数据所在目录，必选(只需提供根目录即可)，目前只提供video以及image类型数据的搜寻，video可搜寻'mp4', 'avi', 'rmvb', 'mkv', 'webm'格式的文件，image可搜寻'jpeg', 'jpg', 'png', 'bmp'几种格式，如有新格式，可手动添加进脚本。
- `--working_path`为可选参数，比如此处指定为`./meta_and_out`，代表当前路径下的一个名为meta_and_out的文件夹，meta.json被存放在里面，其它生成的中间数据也被存放在里面。如果不使用--working_path参数，则默认meta.json以及其它中间生成数据都存放在当前目录下。
- `--mode`的取值应该从'create'和'update'当中选取，默认为'update'。

