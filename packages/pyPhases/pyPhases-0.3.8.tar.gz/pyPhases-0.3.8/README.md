# pyPhases

A small framework for python projects that are mainly progress based.

The main princible of the framework are `Phases`.

# Architecure

![arch](assets/achitektur.svg)

## Project

A Project is the composition of phases and the backend.

## Phase
A Phase has a `main` Method and can export data.

## Stage

A stage is a group of Phases and only have a name. A Stage can be run seperatly with `project.run("stagename")`

## Decorators

# Compontents

## Storage and Exporters

### Storage

You can add diffrent storage-engines to your project, with `project.addStorage(Engine())`. A storage you be inherited from `pyPhases.storage.Storage` and implement the methods `read(path: str)` and `write(path: str, data: bytes)`.
The order is important and the Storages should be ordered from fast to slow.

By Default there is a memory storage, that will save the data in the project, but is not persitent. The default persistent data layer is the filesystem(`storage.FileStorage`).

### Exporter

An Exporter can be registered to transform an Instance or primitive type into a `byte` string (`export(obj : MyObject): bytes`) and vice versa (`importData(bytes): MyObject`).

There is a default `ObjectExporter`, that is based on [pyarror](https://pypi.org/project/pyarrow/) and is compatible with diffrent fromats like pandas Dataframes and numpy arrays. If the Defaultexporter is used, the `numpy` and `pyarrow` package need to be installed.

### register Data
When a phase wants to register data (`self.project.registerData("myDataId", myData)` within the phase), the data is passed to an exporter. If an exporter is found the data will be passed to alle the storages. They will save the data somewhere (persitent or not).

example:

![seq](assets/seq-save-data.svg)

### reading the data
A phase can request data with `self.project.getData("myDataId", MyDataType)`. The Data will be passed sequential to the storage layer and will pass the data from the first storage that is able to get it. If no storage can provide the data, the project will search for a phase that exports this data-id and run that specific phase.

example:

![get-data](assets/seq-get-data.svg)


### example

This is a example data layer with 3 storages: memory, file, database (`not default`)
![data-layer](assets/data-layer.svg)


# development

## build

`python setup.py sdist bdist_wheel`

## publish

`twine upload dist/*`

