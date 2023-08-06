from   onebrain.utils.requeststool import  RequestsTool
import onebrain.utils.FileUpload as uoLoad
class DataSet():
    def __init__(self, yaml=None):
        self.api_url ='/api/1/datasets'
        if yaml:
            metadata = yaml['metadata']
            self.name = metadata['name']
            if 'version' in metadata:
                self.version = metadata['version']
            if 'labels' in metadata:
                self.labels = metadata['labels']
            if 'description' in metadata:
                self.description = metadata['description']
            if 'filepath' in metadata:
                self.filepath = metadata['filepath']
            if 'visibility' in metadata:
                self.visibility =  metadata['visibility']

    def find(self, name,visibility):
        r = RequestsTool()
        url=self.api_url+"/byname/"+name+"/"+str(visibility)
        re = r.get(url)
        if  'status'in re and re['status'] == 200:
            return re['result']['id']
        else:
            print(re)

    def create(self):
        r = RequestsTool()
        data = {
            "name": self.name,
            "version": self.version,
            "labels": self.labels,
            "visibility": self.visibility,
            "description": self.description
        }
        re = r.post(self.api_url, data)
        print(re)
        if  'status'in re and re['status'] == 200:
            id = re['result']['id']
            self.append(id,self.filepath)

    def delete(self):
        id = self.find(self.name, self.visibility)
        if id:
            r = RequestsTool()
            url = self.api_url+"/"+id
            re = r.delete(url)
            if 'status' in re and re['status'] == 200:
               print("删除成功")
        else:
            print("没有找到数据集")
    def update(self):
        id = self.find(self.name, self.visibility)
        print(id)
        if id == None:
            print("没有找到数据集")
            return
        r = RequestsTool()
        data = {
            "id": id,
            "name": self.name,
            "version": self.version,
            "visibility": self.visibility,
            "labels": self.labels,
            "description": self.description
        }
        print(data)
        re = r.put(self.api_url, data)
        print(re)
        if 'status' in re and re['status'] == 200:
            self.append(id, self.filepath)


    def append(self, id, path):
        print(id)
        print(path)
        uoLoad.uploadPathFiles(id,"dataset",id, path)
