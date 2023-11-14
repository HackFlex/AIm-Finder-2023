import os
import sys
import time
import configparser
import shlex
import subprocess

from solver import solver, LoRALayer

def startBaseline(baselineDir):
    cmd = f'docker compose -f {baselineDir}/docker-compose.yml up -d --force-recreate'
    cmds = shlex.split(cmd)
    subprocess.run(cmds, start_new_session=True)
    time.sleep(1)
    cmd = 'docker exec -it baseline sh -c "python baseline.py check"'
    cmds = shlex.split(cmd)
    subprocess.run(cmds, start_new_session=True)
    time.sleep(1)
    #test
    cmd = 'docker exec -it baseline sh -c "python baseline.py start --contest=finder --stage=final --type=estimated-training --count=90 --timeout=15"'
    ## final
    # cmd = 'docker exec -it baseline sh -c "python baseline.py start --contest=finder --stage=final --type=challenge"' 
    cmds = shlex.split(cmd)
    subprocess.run(cmds, start_new_session=True)
    time.sleep(2)
    pass

def getEmptyXmlInfo(name, succes):
    xml = {'name': name, 'succes': succes}
    return xml

def XmlSuccesProcesed(processedXml, pathXml):
    for xml in processedXml:
        if (xml['name'] == pathXml and xml['succes'] == True):
            return True
    return False

if __name__ == '__main__':
    args = sys.argv[1:]
    baselineDir = args[0]
    
    config = configparser.ConfigParser()
    config.read(baselineDir + '/tmp/currentepicrisispath.cfg')
    pathXml = config['DEFAULT']['currentepicrisispath']
    sessionStarted = False
    startBaseline(baselineDir)
    processedXml = []
    try:
        while True:
            config.read(baselineDir + '/tmp/currentepicrisispath.cfg')
            tmpPathXml = config['DEFAULT']['currentepicrisispath']    
            if (sessionStarted == False):
                if (tmpPathXml != pathXml):
                    sessionStarted = True
            elif (XmlSuccesProcesed(processedXml, tmpPathXml) == False):
                time.sleep(2)
                pathXml = tmpPathXml
                nameXml = pathXml[4:]
                taskId = nameXml.split("/")[-1].split("_")[-1].split(".")[0]
                try:
                    solver().solve(baselineDir + nameXml, taskId)
                    processedXml.append(getEmptyXmlInfo(pathXml, True))
                except Exception as e:
                    processedXml.append(getEmptyXmlInfo(pathXml, False))
                    print(f'Error in solver. xmlPath={baselineDir + nameXml}, taskId={taskId}')
                    print(str(e))
                    print()
            time.sleep(2)
    except KeyboardInterrupt:
        pass