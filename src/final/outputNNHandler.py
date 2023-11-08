import shlex
import subprocess

class outNNHandler:
    def __init(self):
        pass

    def _getSymptomJson(self, xPath, start, end, name) -> dict:
        return {
            'xPath': xPath,
            'start': start,
            'end': end,
            'name': name,
            'decorCode': 'symptom',
            'code': ''
        }

    def sendJson(self, pathJson, taskId):
        cmd = f'docker exec -it baseline sh -c "python baseline.py send --path={pathJson} --taskid={taskId}" > ./log.txt'
        cmds = shlex.split(cmd)
        process = subprocess.run(cmds, start_new_session=True)

    def generateJsonSection(self, srcSection, outSection):
        arrSymptoms = []
        for symptom in outSection['symptoms']:
            symptomJson = self._getSymptomJson(
                srcSection['xPath'],
                int(symptom[0]),
                int(symptom[1]),
                outSection['text'][int(symptom[0]):int(symptom[1])])
            arrSymptoms.append(symptomJson)
        return arrSymptoms