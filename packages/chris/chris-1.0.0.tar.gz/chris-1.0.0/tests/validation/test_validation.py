from chris.validation.projects.project_validator import validate as validate_projects
from chris.validation.posts.post_validator import validate as validate_posts


class TestValidation:

    def test_validation(self):
        validate_posts()
        validate_projects()
