from copy import deepcopy
from dataclasses import dataclass
from typing import Dict, List

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import colorful as cf

cf.use_256_ansi_colors()


@dataclass
class ProgrammingExerciseModel:
    exercise_uuid: str
    instructor_uuid: str
    name: str
    language: str
    description_md: str
    main_py: str
    run_py: str
    tests: Dict
    solutions: List[str]
    download_files: List[Dict]
    requirements: str

    EXECUTE_ENDPOINT_URL = 'https://ine-execute.rmotr.com/execute'
    EXERCISE_ENDPOINT_URL = 'https://exercise.rmotr.com/api/v1/exercises'
    # EXERCISE_ENDPOINT_URL = 'http://localhost:8000/api/v1/exercises'
    # EXERCISE_ENDPOINT_URL = 'https://exercise.development.rmotr.com/api/v1/exercises'
    FILE_ENDPOINT_URL = 'https://file.rmotr.com/api/v1/files'
    # FILE_ENDPOINT_URL = 'http://localhost:8001/api/v1/files'
    # FILE_ENDPOINT_URL = 'https://file.development.rmotr.com/api/v1/files'

    def run(self):
        files = {'main.py': self.run_py}

        data = {
            "command": "python main.py",
            "files": files,
            "flavor": "ds-3.8",
            "language": "python",
            "produces": []
        }
        if self.download_files:
            data['download_files'] = self.download_files
        if self.requirements:
            data['pre_command'] = "pip install -q -r requirements.txt"
            data['files']['requirements.txt'] = self.requirements

        response = requests.post(self.EXECUTE_ENDPOINT_URL, json=data)
        if response.status_code != 200:
            print(response.json())
            return

        data = response.json()
        if data['successful']:
            print(cf.bold_green("Success!"))
            print(data['stdout'])
            return

        print(cf.bold_red("Error!\n\n"))
        print(cf.yellow(data['stderr']))
        print(data['stdout'])

    def test(self):
        files = deepcopy(self.tests)
        files['main.py'] = "".join(self.solutions)
        for _, value in self.tests.items():
            files['main.py'] += f"\n\n{value}"

        data = {
            "command": "py.test --json=report.json -q --tb=short main.py",
            "files": files,
            "flavor": "ds-3.8",
            "language": "python",
            "produces": ['report.json'],
        }
        if self.download_files:
            data['download_files'] = self.download_files
        if self.requirements:
            data['pre_command'] = "pip install -q -r requirements.txt"
            data['files']['requirements.txt'] = self.requirements

        response = requests.post(self.EXECUTE_ENDPOINT_URL, json=data)
        if response.status_code != 200:
            print(response.content)
            return

        data = response.json()
        if data['successful']:
            print(cf.bold_green("Success!"))
            print(data['stdout'])
            return

        print(cf.bold_red("Error!\n\n"))
        print(cf.yellow(data['stderr']))
        print(data['stdout'])

    def create(self, auth_token):
        if not all((self.instructor_uuid, self.exercise_uuid, self.name)):
            raise RuntimeError("You need to provide a 'manifest.json' for creating an exercise.")

        detail_url = self.EXERCISE_ENDPOINT_URL + f"/{self.exercise_uuid}"
        response = requests.get(
            detail_url,
            headers={
                'Authorization': f"Bearer {auth_token}"
            }
        )
        if response.status_code == requests.codes.ok:
            raise RuntimeError("Can't create an exercise if already exists.")

        data = {
            'id': self.exercise_uuid,
            'name': self.name,
            'description': self.description_md,
            'starter_code': self.main_py,
            'language': self.language,
            'instructor_id': self.instructor_uuid,
        }
        response = requests.post(
            self.EXERCISE_ENDPOINT_URL,
            headers={
                'Authorization': f"Bearer {auth_token}"
            },
            json=data
        )
        response.raise_for_status()
        data = response.json()
        print(cf.bold_green(f"Exercise created with id: {self.exercise_uuid}"))

        url = self.EXERCISE_ENDPOINT_URL + f"/{self.exercise_uuid}/tests"
        for key, value in self.tests.items():
            data = {
                'exercise': self.exercise_uuid,
                'name': key,
                'code': value
            }
            response = requests.post(
                url,
                headers={
                    'Authorization': f"Bearer {auth_token}"
                },
                json=data
            )
            response.raise_for_status()
            data = response.json()
            test_id = data.get('id')
            if not test_id:
                print(cf.bold_red(f"ERROR! Test could not be created."))
            else:
                print(cf.bold_green(f"Test created with id: {test_id}."))

        url = self.EXERCISE_ENDPOINT_URL + f"/{self.exercise_uuid}/solutions"
        solution_number = 1
        for solution in self.solutions:
            data = {
                'exercise': self.exercise_uuid,
                'name': f"Solution {solution_number}",
                'code': solution
            }
            solution_number += 1
            response = requests.post(
                url,
                headers={
                    'Authorization': f"Bearer {auth_token}"
                },
                json=data
            )
            response.raise_for_status()
            data = response.json()
            solution_id = data.get('id')
            if not solution_id:
                print(cf.bold_red(f"ERROR! Solution could not be created."))
            else:
                print(cf.bold_green(f"Solution created with id: {solution_id}."))

        url = self.FILE_ENDPOINT_URL + f"/upload"
        file_uuid_list = [] 
        for key, value in self.download_files.items():
            file = requests.get(value)
            data = MultipartEncoder(
                fields={
                    'name': key,
                    'type': key.split('.')[-1].lower(),
                    'file': (key, file.content),
                }
            )
            response = requests.post(
                url,
                headers={
                    'Authorization': f"Bearer {auth_token}",
                    'Content-Type': data.content_type,
                },
                data=data.to_string(),
            )
            if response.status_code == "400":
                print(response.json())
            else:
                response.raise_for_status()

            file_id = response.json().get('id')
            if not file_id:
                print(cf.bold_red(f"ERROR! File {key} could not be created."))
            else:
                print(cf.bold_green(f"File {key} created with id: {file_id}."))
                file_uuid_list.append(file_id)

        url = self.EXERCISE_ENDPOINT_URL + f"/{self.exercise_uuid}"
        response = requests.patch(
            url,
            headers={
                'Authorization': f"Bearer {auth_token}",
            },
            json={'files': file_uuid_list},
        )
        response.raise_for_status()
        print(cf.bold_green(f"Successfuly associated to exercise the file ids: {file_uuid_list}."))

    def submit(self):
        raise NotImplementedError()
