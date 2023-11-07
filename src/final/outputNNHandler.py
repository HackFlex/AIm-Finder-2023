import shlex
import subprocess

def run_send(pathJson, taskId):

    # Здесь нужно вызвать наш скрипт: 
    #   MedFlex(current_epicrisis_path, data["taskId"])
    # subprocess.call(['sh', './test.sh'])
    # cmd=f'python baseline.py send --path="/app/test_result.json" --taskid="{data["taskId"]}"'
    # logger.info(cmd)
    # subprocess.call(cmd)

    # process = subprocess.run(["/app/send.sh", pathJsonArg, taskIdArg])
    # logger.info(process, pathJsonArg, taskIdArg)
    # process.detach()


    # cmd = f'/app/send.sh {pathJson} {taskId}'
    # cmds = shlex.split(cmd)
    # # print(cmd, cmds)
    # process = subprocess.run(cmds, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, start_new_session=True)
    # # process.detach()
    
    # with open('output.txt', 'w') as f: 
    process= subprocess.Popen(["python", "-u", "/app/baseline.py", "send", f'--path={pathJson}', f'--taskid="{taskId}"'], start_new_session=True)
    process.wait()
    # logger.info(p)
    # logger.info(subprocess.run(["/app/send.sh", pathJsonArg, taskIdArg], shell=True, check=True))
    # logger.info(subprocess.run(["/app/send.sh", pathJsonArg, taskIdArg], check=True))
    # logger.info(subprocess.run(["/app/send.sh", pathJsonArg, taskIdArg], shell=True, check=True, capture_output=True))
    # logger.info(subprocess.run(["/app/send.sh", pathJsonArg, taskIdArg], check=True, capture_output=True))

    # logger.info(os.system(f'python baseline.py --path=/app/test_result.json --taskid={data["taskId"]}'))
    # subprocess.run(["python", "baseline.py", "send", pathJsonArg, taskIdArg])
    # Логика нашей проги должна быть следующая:
    #       Чтение файла "current_epicrisis_path"
    #       генерация json <path_to_solution_json>
    #       вызов скрипта `python baseline.py send --path=<path_to_solution_json> --taskid=<ID_задачи>`

# if __name__ == '__main__':
#     MedFlexSolve("/app/test_result.json", "10011")