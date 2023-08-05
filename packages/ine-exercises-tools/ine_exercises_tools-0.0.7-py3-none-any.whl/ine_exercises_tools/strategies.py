import json
import requests

from .models import ProgrammingExerciseModel


class BaseStrategy:
    def is_valid(self, *args, **kwargs):
        return False

    def build_exercise(self, *args, **kwargs):
        raise NotImplementedError()


class GistStrategy(BaseStrategy):
    GITHUB_BASE_URL = "https://api.github.com/"

    @classmethod
    def endpoint(cls, *args):
        path = "/".join([arg.lstrip('/') for arg in args])
        return cls.GITHUB_BASE_URL + path

    @staticmethod
    def _read_gist_file(file_data):
        if not file_data['truncated']:
            return file_data['content']
        return requests.get(file_data['raw_url']).text

    def _get_file_content(self, data, file_name, required=False):
        if file_name not in data['files']:
            if required:
                raise ValueError(f"Invalid Gist: {file_name} not found")
            return ""
        return self._read_gist_file(data['files'][file_name])

    def _parse_tests(self, data):
        tests = {}
        for key, value in data['files'].items():
            if key.startswith('test_'):
                tests[key] = self._read_gist_file(value)

        if not tests:
            raise ValueError("Invalid Gist: tests not found")

        return tests

    def _parse_solutions(self, data):
        solutions = []
        for key, value in data['files'].items():
            if key.startswith('solution_'):
                solutions.append(self._read_gist_file(value))

        if not solutions:
            raise ValueError("Invalid Gist: solutions not found")

        return solutions

    def _parse_files(self, data):
        files = self._get_file_content(data, 'files.json', required=False)

        if files:
            return json.loads(files)

        return {}

    def _parse_manifest(self, data):
        file_content = self._get_file_content(data, 'manifest.json', required=False)
        manifest = json.loads(file_content) if file_content else {}

        if manifest and not manifest.get('exercise_uuid'):
            raise RuntimeError("manifest.json: No value provided for 'exercise_uuid'.")
        elif manifest and not manifest.get('instructor_uuid'):
            raise RuntimeError("manifest.json: No value provided for 'instructor_uuid'.")
        elif manifest and not manifest.get('name'):
            raise RuntimeError("manifest.json: No value provided for 'name'.")

        return manifest

    ##################################################
    #             Public Interface                   #
    ##################################################
    @classmethod
    def is_valid(self, *args, **kwargs):
        return bool(kwargs.get('gist_id'))

    def build_exercise(self, *args, **kwargs):
        gist_id = kwargs['gist_id']
        resp = requests.get(self.endpoint('gists', gist_id))
        resp.raise_for_status()

        data = resp.json()
        manifest = self._parse_manifest(data)
        return ProgrammingExerciseModel(
            exercise_uuid=manifest.get('exercise_uuid', '').strip(),
            instructor_uuid=manifest.get('instructor_uuid', '').strip(),
            name=manifest.get('name', ''),
            language=manifest.get('language', 'python'),
            description_md=self._get_file_content(data, 'README.md'),
            main_py=self._get_file_content(data, 'main.py'),
            run_py=self._get_file_content(data, 'run.py'),
            solutions=self._parse_solutions(data),
            tests=self._parse_tests(data),
            download_files=self._parse_files(data),
            requirements=self._get_file_content(data, 'requirements.txt', required=False),
        )

