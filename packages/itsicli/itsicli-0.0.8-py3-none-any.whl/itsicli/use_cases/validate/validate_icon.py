from itsicli.use_cases.workspace import root_path
from itsicli.use_cases.validate.result import Level, result


class ValidateIcon(object):

    in_progress_text = 'Checking for icon'

    def run(self, *args, **kwargs):
        path = root_path()
        icon_path = path.joinpath('icon.png')

        if not icon_path.exists():
            results = [
                result(Level.ERROR, "Add a 200x200px icon file at '{}'.".format(icon_path))
            ]
        else:
            results = []

        return results
