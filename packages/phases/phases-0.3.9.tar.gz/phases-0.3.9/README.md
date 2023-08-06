# pyPhase Project-builder

This Generator will create a ready-to-go pyPhase-Project, based on a config-Yaml.

## Setup

`pip install phases`

## create `project.yaml`

### minimal
```YAML
name: myProject
namespace: myGroup
phases:
    - name: Phase1
      description: my first phase
      exports: [myData]
    - name: Phase2
      description: my second phase
```

run with `python myProject`

### complete
```YAML
name: "sleepClassificationCNN"
namespace: tud.ibmt
exporter:
    - ObjectExporter
    - KerasExporter
publisher:
    - DotSience
phases:
    prepareData:
        - name: DataWrapper
          description: get EDF Data
          exports:
            - trainingRaw
            - validationRaw
            - evaluationRaw
        - name: EDF4SleepStages
          description: Prepare EDF Data for sleep stage recognition
          exports:
            - trainingTransformed
            - validationTransformed
    train:
        - name: SleepPhaseDetectionModel
          description: Create Model for sleep stage recognition
          exports:
            - model
    evaluate:
        - name: SleepPhaseDetectionModel
          description: Create Model for sleep stage recognition
```

### Generate

`phases create`


### Development

The generator will create stubs for each phase, publisher, storage, exporter and generator that
does not exists in the pyPhase-Package. The stubs are in the project folder and implement empty
method that are required.

To implement your project, you only need to fill those methods. For the minimal example you need
to fill the `main`-methods of Phase1 (`myProject/phases/Phase1.py`) and Phase2.

### Execute

If you want to run the whole Project run: `python [ProjectName]` for the minimal example: `python myProject`

To run a single stage: `python [ProjectName] [StageName]` for the minimal example: `python myProject stage2`

## additional files

- `doc/` placeholder for automated documentation
- `.editorconfig` some settings for supporting IDE about File encoding and formats (see https://editorconfig.org/)
- `.gitignore` some folders and files that should be ignored by git (see https://git-scm.com/docs/gitignore)

- `requirements.txt` the python requirements (just pyPhases in an empty project)
- `setup.py` a python setup-file with some data (https://docs.python.org/3/installing/index.html#installing-index)
- `README.md` an Readme file that is used for git and python packages
- `Dockerfile` a simple dockerfile that can be used to run the project in a container (The `FROM` image should properly changed)
- `docker-compose.yml` this is a helper to create and run the container. simply run `docker-compose up` or `docker compose run --rm [projectname] [stagename]`
- `.gitlab-ci.yml` a Configuration for the Gitlab-CI Pipeline, that will be automaticly run if there is a push to gitlab
