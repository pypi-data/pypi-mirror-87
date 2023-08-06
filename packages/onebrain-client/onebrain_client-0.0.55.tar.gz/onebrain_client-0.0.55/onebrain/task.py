from   onebrain.utils.requeststool import  RequestsTool
import onebrain.utils.FileUpload as uoLoad
class Task():
    def __init__(self, yaml=None):
        self.api_url ='/api/1/task'
        self.name = None
        self.project_name = None
        self.image_name = None
        self.image_visibility = None
        self.image_version = None
        self.dataset_name = None
        self.dataset_visibility = None
        self.filepath = None
        self.master_product_name = None
        self.master_command = None
        self.slave_product_name = None
        self.slave_command = None
        self.slave_num = None
        if yaml:
            metadata = yaml['metadata']
            self.name = metadata['name']
            if 'project_name' in metadata:
                self.project_name = metadata['project_name']
            if 'image_name' in metadata:
                self.image_name = metadata['image_name']
            if 'image_visibility' in metadata:
                self.image_visibility = metadata['image_visibility']
            if 'image_version' in metadata:
                self.image_version = metadata['image_version']
            if 'master_product_name' in metadata:
                self.master_product_name = metadata['master_product_name']
            if 'master_command' in metadata:
                self.master_command = metadata['master_command']
            if 'slave_product_name' in metadata:
                self.slave_product_name = metadata['slave_product_name']
            if 'slave_num' in metadata:
                self.slave_num = metadata['slave_num']
            if 'slave_command' in metadata:
                self.slave_command = metadata['slave_command']
            if 'dataset_name' in metadata:
                self.dataset_name = metadata['dataset_name']
            if 'dataset_visibility' in metadata:
                self.dataset_visibility = metadata['dataset_visibility']    
            if 'filepath' in metadata:
                self.filepath = metadata['filepath']
    

    def _initData(self):
        data = {
            "name": self.name,
            "projectName": self.project_name,
            "imageName": self.image_name,
            "imageVisibility": self.image_visibility,
            "imageVersion": self.image_version,
            "datasetName": self.dataset_name,
            "datasetVisibility": self.dataset_visibility,
            "filepath": self.filepath,
            "masterProductName": self.master_product_name,
            "masterCommand": self.master_command,
            "slaveProductName": self.slave_product_name,
            "slaveCommand": self.slave_command,
            "salvePodNum": self.slave_num
        }
        return data

    def find(self, name, porject_name):
        r = RequestsTool()
        url=self.api_url+"/find/"+porject_name+"/"+name
        re = r.get(url)
        if  'status' in re and re['status'] == 200:
            return re['result']['id']
        else:
            print(re)
    
    def create(self):
        print("begin create")
        r = RequestsTool()
        data = self._initData()
        re = r.post(self.api_url+"/cli", data)
        if  'status'in re and re['status'] == 200:
            id = re['result']['id']
            self.append(id,self.filepath)
            if self._doDone(id):
                print("创建任务成功")
        else:
            print(re)

    def delete(self):
        id = self.find(self.name, self.project_name)
        if id:
            r = RequestsTool()
            url = self.api_url+"/"+id
            re = r.delete(url)
            if 'status' in re and re['status'] == 200:
               print("删除成功")
            else:
               print(re)
        else:
            print("任务没有找到")
    def update(self):
        id = self.find(self.name, self.project_name)
        print(id)
        if id == None:
            print("任务没有找到")
            return
        r = RequestsTool()
        data = self._initData()
        re = r.put(self.api_url+"/cli", data)
        if 'status' in re and re['status'] == 200:
            self.append(id, self.filepath)
            if self._doDone(id):
                print("创建任务成功")
        else:
            print(re)

    def start(self, debug = False):
        id = self.find(self.name, self.project_name)
        if id == None:
            print("任务没有找到")
            return
        r = RequestsTool()
        url = self.api_url+"/start/"+id
        if debug:
            url = self.api_url+"/debug/"+id
        print(url)
        re = r.put(url)
        if 'status' in re and re['status'] == 200:
            print(re['result']['version']+"启动成功")
        else:
            print(re)    
               

    def log(self,version,pod,current,size):
        id = self.find(self.name, self.project_name)
        if id == None:
            print("任务没有找到")
            return
        r = RequestsTool()
        data = {
            "pod": pod,
            "version": version,
            "current": current,
            "size": size
        }
        url = self.api_url+"/log/"+id
        re = r.get(url,params=data)
        if 'status' in re and re['status'] == 200:
            for log in re['result']:
                print(log)
        else:
            print(re)
    def describe(self):
        id = self.find(self.name, self.project_name)
        if id == None:
            print("任务没有找到")
            return
        r = RequestsTool()
        url = self.api_url+"/task_version/pageList/"+id
        re = r.get(url)
        if 'status' in re and re['status'] == 200:
            taskVersionList = re['result']['result']
            for taskVersion in taskVersionList:
                print(taskVersion['version']+"-------"+taskVersion['status'])
        else:
            print(re)

    def stop(self, version):
        id = self.find(self.name, self.project_name)
        if id == None:
            print("任务没有找到")
            return
        r = RequestsTool()
        url = self.api_url + "/stop/" + id+"/"+version
        re = r.put(url)
        if 'status' in re and re['status'] == 200:
            print("停止成功")
        else:
            print(re)
        
    def _doDone(self,id):
        r = RequestsTool()
        url = self.api_url+"/doDone/"+id
        re = r.put(url)
        if 'status' in re and re['status'] == 200:
           return True
        else:
           print(re)
           return False

    def append(self, id, path):
        uoLoad.uploadPathFiles(id,"task",id, path, False)
        