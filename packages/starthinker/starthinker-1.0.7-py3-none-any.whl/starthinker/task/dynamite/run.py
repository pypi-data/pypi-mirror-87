from starthinker.util.project import project
from starthinker.util.dynamite import dynamite_write


@project.from_parameters
def dynamite():
  if project.verbose:
    print('DYNAMITE')
  dynamite_write(project.task['room'], project.task['key'],
                 project.task['token'], project.task['message'])


if __name__ == '__main__':
  dynamite()
