from itsicli.use_cases.files import UseCaseConfig
from itsicli.use_cases.validate.result import Level, result
from itsicli.use_cases.workspace import root_path


class ValidateConfig(object):

    in_progress_text = 'Checking {}'.format(UseCaseConfig.file_name)

    def run(self, *args, **kwargs):
        config = UseCaseConfig(root_path())

        results = []

        if not config.exists():
            results.append(
                result(
                    Level.ERROR, "Missing '{}' file.".format(config.path)
                )
            )
            return results

        title = config.title
        if not title:
            results.append(
                result(
                    Level.ERROR, "Add a 'title' setting in '{}'.".format(config.path)
                )
            )

        version = config.version
        if not version:
            results.append(
                result(
                    Level.ERROR, "Add a valid 'version' setting in '{}'.".format(config.path)
                )
            )
        else:
            try:
                int(version)
            except ValueError:
                results.append(
                    result(
                        Level.ERROR, "Invalid single integer value for 'version' in '{}'.".format(config.path)
                    )
                )

        description = config.description
        if not description:
            results.append(
                result(
                    Level.WARNING, "Add a valid 'description' setting in '{}'.".format(config.path)
                )
            )

        return results
