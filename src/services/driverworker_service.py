import psutil

from src.proto import driverworker_pb2
from src.proto import driverworker_pb2_grpc
from src.utils import serialization


class DriverWorkerService(driverworker_pb2_grpc.DriverWorkerServiceServicer):
    def Execute(self, request, context):
        print("Worker: Execute RPC Called")

        depickled_func = serialization.deserialize(request.function)
        depickled_args = serialization.deserialize(request.args)

        print(f"Worker: Received task ({depickled_func.__name__}) with args ({depickled_args})")
        
        # TODO: scheduler code
        # if localObjectStore.hasAllObjects(request.object_ids, depickled_args):
        #     # excute as normal and send back new mapping to master
        #     pass
        # else:
        #     storedObj, missingObj = localObjectStore.getFromLocalObjStore(request.object_ids)
        #     serverAddr = master_has_all_objects(request.object_ids, depickled_args)
        #     if serverAddr != None:
        #         send_request_to_worker(request, depickled_args)
        #         pass   
        #     else:
        #         # excute as normal but update local object store, return new mapping to master
        #         pass
                
        
        # unpack arguments array
        result = depickled_func(*depickled_args)
        
        # return result to client
        print("Worker: Returning result:", result)
        return driverworker_pb2.TaskReply(task_id=request.task_id, result=serialization.serialize(result))
    
    # worker send grpc to master to check if master has all objects, return 
    # def MasterHasObjectsMapping():
    #     pass
    
    # send grpc to worker to get resource load  
    def GetLoad(self, request, context):
        cpu_load = psutil.cpu_percent()
        memory_info = psutil.virtual_memory()
        memory_used = memory_info.used

        return driverworker_pb2.LoadReply(cpu_load=serialization.serialize(cpu_load), memory_used=serialization.serialize(memory_used))
    
    # Helper functions
    # convert a request to an internal Task representation
    # def task_from_request(self, request):
    #         # Convert a request to an internal Task representation
    #         depickled_func = cloudpickle.loads(request.function)
    #         depickled_args = cloudpickle.loads(request.args)
    #         return Task(
    #             task_id=request.id,
    #             # resources=request.resources,
    #             function=depickled_func,
    #             args=depickled_args,
    #             state=TaskState.READY,
    #         )

    # def SubmitTask(self, task1):
    #     scheduling_queue.queue_tasks([task1], TaskState.PLACEABLE)
    #     print(scheduling_queue.has_task("task1"))  # This should print True
        
    #     scheduling_queue.move_tasks(["task1"], TaskState.PLACEABLE, TaskState.RUNNING)