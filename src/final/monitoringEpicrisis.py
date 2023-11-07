import os
import sys
import time
import configparser
import shlex
import subprocess

from solver import solver

def startBaseline(baselineDir):
    cmd = f'docker compose -f {baselineDir}/docker-compose.yml up -d --force-recreate'
    cmds = shlex.split(cmd)
    subprocess.run(cmds, start_new_session=True)
    time.sleep(1)
    cmd = 'docker exec -it baseline sh -c "python baseline.py check"'
    cmds = shlex.split(cmd)
    subprocess.run(cmds, start_new_session=True)
    time.sleep(1)
    ###test
    # cmd = 'docker exec -it baseline sh -c "python baseline.py start --contest=finder --stage=qualifying --type=estimated-training --count=10 --timeout=10"'
    ### final
    # cmd = 'docker exec -it baseline sh -c "python baseline.py start --contest=finder --stage=final --type=challenge"' 
    # cmds = shlex.split(cmd)
    # subprocess.run(cmds, start_new_session=True)

if __name__ == '__main__':
    args = sys.argv[1:]
    baselineDir = args[0]
    
    config = configparser.ConfigParser()
    pathXml = config.read(baselineDir + '/tmp/currentepicrisispath.cfg')
    
    startBaseline(baselineDir)
    
    try:
        while True:
            config.read(baselineDir + '/tmp/currentepicrisispath.cfg')
            tmp = config['DEFAULT']['currentepicrisispath']
            if (tmp != pathXml):
                pathXml = tmp
                nameXml = pathXml[4:]
                taskId = nameXml.split("/")[-1].split("_")[-1].split(".")[0]
                try:
                    solver().solve(baselineDir + nameXml, taskId)
                except:
                    print(f'Error in solver. xmlPath={baselineDir + nameXml}, taskId={taskId}')
            time.sleep(1)
    except KeyboardInterrupt:
        pass